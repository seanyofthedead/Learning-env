#!/usr/bin/env python3
"""Reproduce all output spec calculations without contacting any website."""
import json
import subprocess
import sys
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent
ROOT = OUTPUT.parents[1]
MODEL = ROOT / 'wedding/budget/wedding_budget_model.py'

def main():
    records = []
    for path in sorted((OUTPUT / 'specs').rglob('*.json')):
        result = subprocess.run([sys.executable, str(MODEL), '--venue', str(path), '--guests', '185'], check=True, text=True, capture_output=True)
        priced = json.loads(result.stdout)
        catering = sum(v for k, v in priced['lines'].items() if k.startswith('outside catering'))
        records.append({'spec': str(path.relative_to(ROOT)), 'result': priced,
                        'max_caterer_all_in_pp_at_modeled_fees': round((32139 - priced['all_in'] + catering) / 185, 2) if catering else None})
    destination = OUTPUT / 'research/model_results.json'
    destination.write_text(json.dumps({'guests': 185, 'strict_target': 32139, 'warning': 'Scenarios and incomplete subtotals, not quotes. Read venue_shortlist and evidence before interpreting a result. Reserve spending is forbidden. Approved allocations and strict policy gates apply; budget verdict and overall fit are separate.', 'venues': records}, indent=2) + '\n')
    print(f'{len(records)} specs passed model CLI and embedded tests; results: {destination}')

if __name__ == '__main__':
    main()
