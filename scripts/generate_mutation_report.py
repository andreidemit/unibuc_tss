#!/usr/bin/env python3
"""Generate an HTML report from mutmut result metadata."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "mutants" / "src" / "shipping_calculator.py.meta"
OUTPUT_PATH = ROOT / "reports" / "mutation.html"

STATUS_BY_EXIT_CODE = {
    0: "survived",
    1: "killed",
    3: "killed",
    5: "no tests",
    33: "no tests",
    34: "skipped",
    35: "suspicious",
    36: "timeout",
}


def status_for(exit_code: int) -> str:
    return STATUS_BY_EXIT_CODE.get(exit_code, f"unknown ({exit_code})")


def mutant_sort_key(name: str) -> tuple[str, int]:
    prefix, _, suffix = name.rpartition("_")
    if suffix.isdigit():
        return prefix, int(suffix)
    return name, 0


def render_report() -> str:
    if not META_PATH.exists():
        rows = ""
        summary = "No mutmut metadata found"
        detail = "Run mutmut first: mutmut run --max-children 1"
    else:
        data = json.loads(META_PATH.read_text(encoding="utf-8"))
        results = data["exit_code_by_key"]
        statuses = {name: status_for(code) for name, code in results.items()}
        counts = Counter(statuses.values())
        total = len(statuses)
        killed = counts["killed"]
        survived = counts["survived"]
        score = 0 if total == 0 else round(killed / total * 100, 2)
        summary = f"{killed}/{total} mutants killed"
        detail = f"Mutation score: {score}% | Survived: {survived}"
        rows = "\n".join(
            "<tr>"
            f"<td>{index}</td>"
            f"<td><code>{html.escape(name)}</code></td>"
            f"<td class=\"status {html.escape(status)}\">{html.escape(status)}</td>"
            "</tr>"
            for index, (name, status) in enumerate(
                sorted(statuses.items(), key=lambda item: mutant_sort_key(item[0])),
                start=1,
            )
        )

    return f"""<!doctype html>
<html lang="ro">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Raport mutmut</title>
  <style>
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: #172033; line-height: 1.5; }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 40px 24px; }}
    a {{ color: #1f6feb; font-weight: 700; text-decoration: none; }}
    h1 {{ margin: 0 0 12px; }}
    .metric {{ display: inline-block; padding: 8px 12px; border-radius: 8px; background: #e7f7ef; color: #18794e; font-weight: 700; }}
    .detail {{ color: #5d6678; }}
    table {{ width: 100%; border-collapse: collapse; margin: 18px 0; }}
    th, td {{ border: 1px solid #d7dce5; padding: 10px 12px; text-align: left; vertical-align: top; }}
    th {{ background: #f7f8fb; }}
    code {{ font-family: Menlo, Consolas, monospace; font-size: 14px; }}
    .status {{ font-weight: 700; }}
    .killed {{ color: #18794e; }}
    .survived {{ color: #b42318; }}
    .timeout, .suspicious, .unknown {{ color: #a15c00; }}
  </style>
</head>
<body>
  <main>
    <a href="index.html">Inapoi la index</a>
    <h1>Raport mutation testing</h1>
    <p><span class="metric">{html.escape(summary)}</span></p>
    <p class="detail">{html.escape(detail)}</p>

    <h2>Comenzi</h2>
    <pre><code>mutmut run --max-children 1
python scripts/generate_mutation_report.py</code></pre>

    <h2>Rezultate pe mutant</h2>
    <table>
      <tr><th>#</th><th>Mutant</th><th>Status</th></tr>
      {rows}
    </table>
  </main>
</body>
</html>
"""


def main() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_report(), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
