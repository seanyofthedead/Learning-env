# Normalized corpus statistics

_Generated at 2026-04-13T20:26:28+00:00_

**Total normalized rows:** 1,702,668
**Output:** `data/processed/normalized.parquet`

## Per-source breakdown

| Source | Rows | Date range | Narrative (mean/median words) |
|---|---:|---|---|
| osha_sir | 73,398 | 2018-01-01 → 2025-08-31 | 35.2 / 32.0 |
| osha_ita | 1,579,555 | 2022-02-26 → 2025-08-15 | 51.5 / 45.0 |
| msha | 49,666 | 2018-01-01 → 2026-04-07 | 36.4 / 35.0 |
| nrc | 49 | 2023-10-01 → 2025-11-26 | 240.7 / 179.0 |
| ntsb | 0 | — | — |
| asrs | 0 | — | — |

## Null rates (per-column, excluding `source` and `meta`)

### osha_sir

| Column | Null rate |
|---|---:|
| report_id | 0.0% |
| event_date | 0.0% |
| entity_raw_key | 0.0% |
| entity_name | 0.0% |
| entity_address | 0.0% |
| location | 0.0% |
| event_type | 0.0% |
| severity | 0.0% |
| narrative | 0.0% |
| synopsis | 100.0% |

### osha_ita

| Column | Null rate |
|---|---:|
| report_id | 0.0% |
| event_date | 0.0% |
| entity_raw_key | 0.0% |
| entity_name | 0.0% |
| entity_address | 0.0% |
| location | 0.0% |
| event_type | 0.0% |
| severity | 0.0% |
| narrative | 0.0% |
| synopsis | 0.1% |

### msha

| Column | Null rate |
|---|---:|
| report_id | 0.0% |
| event_date | 0.0% |
| entity_raw_key | 0.0% |
| entity_name | 0.0% |
| entity_address | 100.0% |
| location | 0.0% |
| event_type | 0.0% |
| severity | 0.0% |
| narrative | 0.0% |
| synopsis | 100.0% |

### nrc

| Column | Null rate |
|---|---:|
| report_id | 0.0% |
| event_date | 0.0% |
| entity_raw_key | 0.0% |
| entity_name | 0.0% |
| entity_address | 0.0% |
| location | 0.0% |
| event_type | 0.0% |
| severity | 0.0% |
| narrative | 0.0% |
| synopsis | 100.0% |

### ntsb

| Column | Null rate |
|---|---:|

### asrs

| Column | Null rate |
|---|---:|

