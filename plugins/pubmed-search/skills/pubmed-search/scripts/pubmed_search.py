#!/usr/bin/env python3
"""Fetch a page of PubMed results with everything needed to cite and appraise them.

Ports the network layer of the Lantern iOS app (ios/Lantern/Services/PubMedService.swift,
PubMedArticleParser.swift, PMCFullTextParser.swift) so the skill's trust weights are
judged from exactly the same inputs the app judges from:

  esearch  -> matching PMIDs for this page, plus PubMed's own query translation
  esummary -> citation fields (journal, volume, issue, pages, DOI, authors, pubtypes)
  efetch   -> the abstract, structured labels preserved (one batched call for the page)
  efetch   -> open-access PMC full text, but only for the records the app enriches:
              an abstract under 900 characters, or a review, where the synthesis
              lives in the body rather than the abstract

Stdlib only, so it runs anywhere with python3 and needs no install step.
Writes one JSON object to stdout. Progress and warnings go to stderr, so piping
stdout into a file or a parser stays clean.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

# NCBI is a trusted TLS endpoint, but stdlib ElementTree still expands internal
# entities, so a hostile or corrupted response could blow up memory. Use
# defusedxml when it happens to be installed and fall back otherwise, which keeps
# the script dependency-free while taking the hardening when it is available.
try:
    from defusedxml.ElementTree import fromstring as xml_fromstring
except ImportError:  # pragma: no cover - depends on the host environment
    xml_fromstring = ET.fromstring

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = "lantern-skill"

# Publication-type labels that say nothing about study strength. Dropped so the
# tags left on a result carry signal. Mirrors NOISE_PUBTYPES in PubMedService.swift.
NOISE_PUBTYPES = {
    "Journal Article",
    "Comparative Study",
    "English Abstract",
    "Research Support, Non-U.S. Gov't",
    "Research Support, N.I.H., Extramural",
    "Research Support, U.S. Gov't, Non-P.H.S.",
}

# Below this an abstract reads thin (a brief highlight, an editorial), so the app
# reaches for open-access full text before appraising. Same threshold here.
ENRICH_BELOW_CHARS = 900
FULLTEXT_MAX_CHARS = 6000
FULLTEXT_MIN_CHARS = 400

# NCBI allows unauthenticated clients ~3 requests/second. An API key raises that
# to 10/sec. Same margin the app's NCBIThrottle keeps.
THROTTLE_ANON = 0.35
THROTTLE_KEYED = 0.11
BACKOFFS = (0.4, 0.9)

_last_request = 0.0


class PubMedError(RuntimeError):
    pass


def _api_key() -> str | None:
    key = os.environ.get("NCBI_API_KEY", "").strip()
    return key or None


def _throttle() -> None:
    """Space requests out so a burst never draws 429s."""
    global _last_request
    interval = THROTTLE_KEYED if _api_key() else THROTTLE_ANON
    wait = _last_request + interval - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last_request = time.monotonic()


def _get(endpoint: str, params: dict[str, str], accept: str) -> bytes:
    """One E-utilities GET, throttled, retrying only what a retry can fix.

    A 429 or a 5xx is transient and worth a short backoff. A 400 (malformed
    query) or a 404 will say the same thing the second time, so it is raised at
    once rather than burning the retry budget.
    """
    params = {k: v for k, v in params.items() if v not in (None, "")}
    params.setdefault("tool", TOOL)
    key = _api_key()
    if key:
        params.setdefault("api_key", key)
    if os.environ.get("NCBI_EMAIL"):
        params.setdefault("email", os.environ["NCBI_EMAIL"])

    url = f"{BASE}/{endpoint}?{urllib.parse.urlencode(params)}"
    last = "no response"

    for attempt in range(len(BACKOFFS) + 1):
        _throttle()
        try:
            req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": TOOL})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429,) and not 500 <= e.code < 600:
                raise PubMedError(f"PubMed returned HTTP {e.code} for {endpoint}") from e
            last = f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = str(getattr(e, "reason", e))
        if attempt < len(BACKOFFS):
            time.sleep(BACKOFFS[attempt])

    raise PubMedError(f"Could not reach PubMed ({endpoint}): {last}")


def _collapse(raw: str | None) -> str:
    """Runs of whitespace to single spaces, then trim. Analog of the app's collapse()."""
    return re.sub(r"\s+", " ", raw or "").strip()


def _first_year(*candidates: str | None) -> str:
    for c in candidates:
        if c:
            m = re.search(r"\d{4}", c)
            if m:
                return m.group(0)
    return ""


# ---------------------------------------------------------------- esearch


def esearch(term: str, retmax: int, retstart: int, sort: str,
            mindate: str | None, maxdate: str | None, datetype: str) -> dict:
    params = {
        "db": "pubmed",
        "term": term,
        "retstart": str(retstart),
        "retmax": str(retmax),
        "sort": "date" if sort == "date" else "relevance",
        "retmode": "json",
    }
    if mindate or maxdate:
        # PubMed needs both ends of the range. An open-ended "no earlier than
        # 2025" becomes 2025 -> 3000, which is how its own date filter renders it.
        params["mindate"] = mindate or "1800"
        params["maxdate"] = maxdate or "3000"
        params["datetype"] = datetype

    payload = json.loads(_get("esearch.fcgi", params, "application/json"))
    result = payload.get("esearchresult", {})

    if result.get("ERROR"):
        raise PubMedError(f"PubMed rejected the query: {result['ERROR']}")

    warnings = []
    for key in ("warninglist", "errorlist"):
        block = result.get(key) or {}
        for label, items in block.items():
            if items:
                warnings.append(f"{label}: {', '.join(items)}")

    return {
        "ids": result.get("idlist", []),
        "total": int(result.get("count", 0) or 0),
        "translation": result.get("querytranslation", ""),
        # PubMed silently remaps unrecognized terms. Surfacing the per-term
        # mapping is the only way to catch a wrong-disease expansion such as
        # B-ALL -> "burkitt lymphoma"[MeSH Terms].
        "translationSet": [
            {"from": t.get("from", ""), "to": t.get("to", "")}
            for t in (result.get("translationset") or [])
        ],
        "warnings": warnings,
    }


# ---------------------------------------------------------------- esummary


def esummary(ids: list[str]) -> dict[str, dict]:
    """Citation details per PMID. esummary keys `result` by uid, so this is parsed
    as a plain dict rather than a fixed schema."""
    payload = json.loads(_get(
        "esummary.fcgi",
        {"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
        "application/json",
    ))
    result = payload.get("result", {})
    out: dict[str, dict] = {}

    for uid in result.get("uids", ids):
        r = result.get(uid)
        if not isinstance(r, dict):
            continue

        names = [a.get("name", "") for a in (r.get("authors") or []) if a.get("name")]
        article_ids = {a.get("idtype"): a.get("value") for a in (r.get("articleids") or [])}

        # Bracketed titles mark a translated foreign-language article. Strip the
        # brackets the way the app does so the title reads normally.
        title = (r.get("title") or "").strip()
        if title.startswith("["):
            title = title[1:]
        title = re.sub(r"\]\.?$", "", title).strip()

        all_types = r.get("pubtype") or []
        doi = article_ids.get("doi") or ""
        if not doi:
            m = re.search(r"10\.\S+", r.get("elocationid") or "")
            doi = m.group(0) if m else ""

        pmc = (article_ids.get("pmc") or "").replace("PMC", "").strip()

        out[uid] = {
            "pmid": uid,
            "title": title or "Untitled study",
            "journal": r.get("source") or "",
            "journalFull": r.get("fulljournalname") or r.get("source") or "",
            "pubdate": r.get("pubdate") or "",
            "epubdate": r.get("epubdate") or "",
            "year": _first_year(r.get("pubdate"), r.get("sortpubdate")),
            "volume": r.get("volume") or "",
            "issue": r.get("issue") or "",
            "pages": r.get("pages") or "",
            "doi": doi,
            "leadAuthor": r.get("sortfirstauthor") or (names[0] if names else ""),
            "lastAuthor": r.get("lastauthor") or (names[-1] if names else ""),
            "authorCount": len(names),
            "authors": "" if not names else (names[0] if len(names) == 1 else f"{names[0]} et al."),
            "publicationTypes": [t for t in all_types if t not in NOISE_PUBTYPES],
            "allPublicationTypes": all_types,
            "pmcid": pmc or None,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
        }
    return out


# ---------------------------------------------------------------- efetch (abstracts)


def efetch_abstracts(ids: list[str]) -> dict[str, dict]:
    """Abstracts for the whole page in one call.

    esummary has no abstract, and the weight rubric turns on design and sample
    size, which only the abstract carries. Batching keeps that to a single
    request instead of one per article. Structured section labels (BACKGROUND,
    METHODS...) are kept, since they are part of how a design is read.
    """
    raw = _get(
        "efetch.fcgi",
        {"db": "pubmed", "id": ",".join(ids), "rettype": "abstract", "retmode": "xml"},
        "application/xml",
    )
    root = xml_fromstring(raw)
    out: dict[str, dict] = {}

    for article in root.iter("PubmedArticle"):
        pmid_el = article.find(".//MedlineCitation/PMID")
        pmid = _collapse(pmid_el.text if pmid_el is not None else None)
        if not pmid:
            continue

        parts = []
        for node in article.iter("AbstractText"):
            body = _collapse("".join(node.itertext()))
            if not body:
                continue
            label = (node.get("Label") or "").strip()
            parts.append(f"{label.upper()}: {body}" if label else body)

        pmc = None
        for aid in article.iter("ArticleId"):
            if aid.get("IdType") == "pmc" and aid.text:
                pmc = aid.text.replace("PMC", "").strip() or None

        pub_types = [
            _collapse("".join(t.itertext()))
            for t in article.iter("PublicationType")
        ]

        out[pmid] = {
            "abstract": "\n\n".join(parts).strip(),
            "pmcid": pmc,
            "publicationTypesXml": [t for t in pub_types if t],
        }
    return out


# ---------------------------------------------------------------- efetch (PMC body)


def fetch_fulltext(pmcid: str) -> str | None:
    """Best-effort open-access body text. Never raises: a record outside the
    open-access subset, or any network hiccup, just falls back to the abstract."""
    try:
        raw = _get(
            "efetch.fcgi",
            {"db": "pmc", "id": pmcid, "retmode": "xml"},
            "application/xml",
        )
        root = xml_fromstring(raw)
    except (PubMedError, ET.ParseError):
        return None

    skip = {"ref-list", "table-wrap", "fig", "supplementary-material", "table", "disp-formula"}
    blocks: list[str] = []

    for body in root.iter("body"):
        for node in body.iter():
            if node.tag not in ("p", "title"):
                continue
            if _has_skipped_ancestor(body, node, skip):
                continue
            text = _collapse("".join(node.itertext()))
            if len(text) >= 3:
                blocks.append(text)

    text = "\n\n".join(blocks).strip()
    if len(text) < FULLTEXT_MIN_CHARS:
        return None

    if len(text) > FULLTEXT_MAX_CHARS:
        # Keep head and tail: a paper's intro and conclusion carry the most
        # appraisal signal, and the methods detail in between matters less to a
        # strength judgment than the design statement and the stated limits.
        head = text[: FULLTEXT_MAX_CHARS * 3 // 5].strip()
        tail = text[-(FULLTEXT_MAX_CHARS * 2 // 5):].strip()
        text = f"{head}\n\n[...middle of the article omitted...]\n\n{tail}"
    return text


def _has_skipped_ancestor(root: ET.Element, target: ET.Element, skip: set[str]) -> bool:
    """ElementTree has no parent pointers, so walk down from body once and mark
    everything under a skipped container."""
    for parent in root.iter():
        if parent.tag in skip:
            for descendant in parent.iter():
                if descendant is target:
                    return True
    return False


# ---------------------------------------------------------------- assembly


def citation(a: dict) -> str:
    """A compact reference line: Journal. Year;Volume(Issue):Pages."""
    bits = f"{a['journal']}. {a['year'] or a['pubdate']}"
    if a["volume"]:
        bits += f";{a['volume']}"
        if a["issue"]:
            bits += f"({a['issue']})"
        if a["pages"]:
            bits += f":{a['pages']}"
    elif a["pages"]:
        bits += f":{a['pages']}"
    return bits.rstrip(".") + "."


def run(args: argparse.Namespace) -> dict:
    search = esearch(
        term=args.term,
        retmax=args.retmax,
        retstart=args.retstart,
        sort=args.sort,
        mindate=args.mindate,
        maxdate=args.maxdate,
        datetype=args.datetype,
    )
    ids = search["ids"]
    print(f"[esearch] {search['total']} matches, fetching {len(ids)}", file=sys.stderr)

    asked = {
        "term": args.term,
        "sort": args.sort,
        "retmax": args.retmax,
        "retstart": args.retstart,
        "mindate": args.mindate,
        "maxdate": args.maxdate,
        "datetype": args.datetype,
    }

    if not ids:
        return {
            "query": asked,
            "queryTranslation": search["translation"],
            "translationSet": search["translationSet"],
            "warnings": search["warnings"],
            "total": search["total"],
            "returned": 0,
            "articles": [],
        }

    summaries = esummary(ids)
    print(f"[esummary] {len(summaries)} records", file=sys.stderr)

    abstracts = efetch_abstracts(ids)
    print(f"[efetch] {len(abstracts)} abstracts", file=sys.stderr)

    articles = []
    for rank, pmid in enumerate(ids, start=1):
        a = summaries.get(pmid)
        if not a:
            print(f"[warn] no summary for PMID {pmid}, skipping", file=sys.stderr)
            continue

        fetched = abstracts.get(pmid, {})
        abstract = fetched.get("abstract", "")
        a["pmcid"] = a.get("pmcid") or fetched.get("pmcid")
        if not a["publicationTypes"] and fetched.get("publicationTypesXml"):
            a["publicationTypes"] = [
                t for t in fetched["publicationTypesXml"] if t not in NOISE_PUBTYPES
            ]

        # Same enrichment rule as the app: a thin abstract, or a review whose
        # synthesis and conclusions live in the body rather than the abstract.
        is_review = any("review" in t.lower() for t in a["publicationTypes"])
        enriched = False
        if args.enrich and a["pmcid"] and (len(abstract) < ENRICH_BELOW_CHARS or is_review):
            body = fetch_fulltext(a["pmcid"])
            if body:
                abstract = f"{abstract}\n\nFrom the full article:\n{body}".strip()
                enriched = True
                print(f"[pmc] enriched {pmid} from PMC{a['pmcid']}", file=sys.stderr)

        a.update({
            "rank": rank,
            "citation": citation(a),
            "abstract": abstract,
            "abstractMissing": not fetched.get("abstract"),
            "abstractChars": len(abstract),
            "fullTextAdded": enriched,
        })
        articles.append(a)

    return {
        "query": asked,
        "queryTranslation": search["translation"],
        "translationSet": search["translationSet"],
        "warnings": search["warnings"],
        "total": search["total"],
        "returned": len(articles),
        "articles": articles,
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description="PubMed search returning citation fields plus abstracts for appraisal.")
    p.add_argument("--term", required=True,
                   help="PubMed query, field tags and boolean operators included.")
    p.add_argument("--retmax", type=int, default=10, help="Results to return (default 10).")
    p.add_argument("--retstart", type=int, default=0, help="Offset, for paging past page one.")
    p.add_argument("--sort", choices=["relevance", "date"], default="relevance")
    p.add_argument("--mindate", help="Earliest date, e.g. 2025 or 2025/03/01.")
    p.add_argument("--maxdate", help="Latest date. Defaults to 3000 when only mindate is given.")
    p.add_argument("--datetype", default="pdat", choices=["pdat", "edat", "mhda"],
                   help="pdat = publication date, edat = Entrez date, mhda = MeSH date.")
    p.add_argument("--no-enrich", dest="enrich", action="store_false",
                   help="Skip PMC full-text enrichment for thin abstracts and reviews.")
    p.add_argument("--out", help="Write JSON here instead of stdout.")
    args = p.parse_args()

    try:
        payload = run(args)
    except PubMedError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"[out] wrote {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
