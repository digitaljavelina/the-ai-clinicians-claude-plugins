"""
Test harness. Generate synthetic notes, redact them, and score how much planted
PHI survived. Recall is the metric that matters: a survivor is a leak.

    uv run evaluate.py                      # baseline vs clinical, 15 notes
    uv run evaluate.py --engine baseline    # one engine only
    uv run evaluate.py -n 30                 # more notes
    uv run evaluate.py --sample             # print one redacted note to eyeball

The leaked values printed here are synthetic, so they are safe to display.
"""
import argparse
from collections import Counter, defaultdict

import notes as N
import engine as E


def survives(value, redacted):
    """A planted value counts as leaked if it still appears verbatim.

    Simple and readable. It does not catch partial leaks (half a phone number),
    so treat it as a floor on the leak rate, not a ceiling. See the tutorial's
    limits section.
    """
    return value in redacted


def score(engine_name, dataset):
    analyzer = E.build_analyzer(engine_name)
    total, leaked = Counter(), Counter()
    examples = defaultdict(list)
    for text, planted in dataset:
        redacted, _ = E.redact(text, analyzer)
        for cat, val in planted:
            total[cat] += 1
            if survives(val, redacted):
                leaked[cat] += 1
                if len(examples[cat]) < 3:
                    examples[cat].append(val)
    return total, leaked, examples


def report(name, total, leaked, examples):
    print(f"\n=== {name} ===")
    print(f"{'category':18} {'planted':>7} {'caught':>7} {'leaked':>7} {'recall':>8}")
    print("-" * 52)
    gt = gc = 0
    for cat in sorted(total):
        t = total[cat]
        lk = leaked[cat]
        c = t - lk
        gt += t
        gc += c
        print(f"{cat:18} {t:7} {c:7} {lk:7} {c / t:8.1%}")
    print("-" * 52)
    print(f"{'OVERALL':18} {gt:7} {gc:7} {gt - gc:7} {gc / gt:8.1%}   <- recall is the safety number")
    for cat, ex in examples.items():
        if ex:
            print(f"  leaked {cat}: {', '.join(ex)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", choices=["baseline", "clinical", "both"], default="both")
    ap.add_argument("-n", type=int, default=15, help="number of synthetic notes")
    ap.add_argument("--sample", action="store_true", help="print one redacted note and stop")
    args = ap.parse_args()

    data = N.generate(args.n)

    if args.sample:
        eng = args.engine if args.engine != "both" else "clinical"
        analyzer = E.build_analyzer(eng)
        redacted, counts = E.redact(data[0][0], analyzer)
        print(f"--- one note redacted by the {eng} engine (synthetic, safe to view) ---\n")
        print(redacted)
        print("counts:", dict(counts))
        return

    engines = ["baseline", "clinical"] if args.engine == "both" else [args.engine]
    for eng in engines:
        t, lk, ex = score(eng, data)
        report(eng, t, lk, ex)


if __name__ == "__main__":
    main()
