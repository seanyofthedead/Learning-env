# Acquisition Log

_Generated at 2026-04-13T18:36:28+00:00_

**Sources attempted:** 2  
**Combined row count (summary):** 153,418

## Summary

| Source | Status | Rows | Date range | Narrative (words) | Duration |
|---|---|---:|---|---|---:|
| osha_sir | ok | 103,750 | 2015-01-01 → 2025-08-31 | n=103750, mean=34.5, median=31.0, p25=23.0, p75=42.0 | 4.4s |
| msha | ok | 49,668 | 2018-01-01 → 2026-04-07 | n=49667, mean=36.4, median=35.0, p25=23.0, p75=49.0 | 12.0s |

## Details

### osha_sir — `ok`

**Notes:** downloaded from https://www.osha.gov/sites/default/files/January2015toAugust2025.zip

**Columns (28):** `ID`, `UPA`, `EventDate`, `Employer`, `Address1`, `Address2`, `City`, `State`, `Zip`, `Latitude`, `Longitude`, `Primary NAICS`, `Hospitalized`, `Amputation`, `Loss of Eye` …(+13 more)

**Files:**
- `/home/user/Learning-env/data/raw/osha_sir/January2015toAugust2025.zip`

### msha — `ok`

**Notes:** row_count is 2018+ only (total archive rows=272291)

**Columns (57):** `MINE_ID`, `CONTROLLER_ID`, `CONTROLLER_NAME`, `OPERATOR_ID`, `OPERATOR_NAME`, `CONTRACTOR_ID`, `DOCUMENT_NO`, `SUBUNIT_CD`, `SUBUNIT`, `ACCIDENT_DT`, `CAL_YR`, `CAL_QTR`, `FISCAL_YR`, `FISCAL_QTR`, `ACCIDENT_TIME` …(+42 more)

**Files:**
- `/home/user/Learning-env/data/raw/msha/Accidents.zip`

