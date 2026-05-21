#!/usr/bin/env bash
set -euo pipefail

mutmut run --max-children 1
mutmut results || true
python3 scripts/generate_mutation_report.py
