# Acquisition Log

_Generated at 2026-04-13T18:49:34+00:00_

**Sources attempted:** 4  
**Combined row count (summary):** 1,733,050

## Summary

| Source | Status | Rows | Date range | Narrative (words) | Duration |
|---|---|---:|---|---|---:|
| osha_sir | ok | 103,750 | 2015-01-01 → 2025-08-31 | n=103750, mean=34.5, median=31.0, p25=23.0, p75=42.0 | 3.7s |
| msha | ok | 49,668 | 2018-01-01 → 2026-04-07 | n=49667, mean=36.4, median=35.0, p25=23.0, p75=49.0 | 12.8s |
| osha_ita | ok | 1,579,583 | 2022-02-26 → 2025-08-15 | n=1579583, mean=46.5, median=40.0, p25=28.0, p75=58.0 | 112.4s |
| nrc | partial | 49 | 2023-10-01 → 2025-11-26 | n=49, mean=240.7, median=179.0, p25=150.0, p75=292.0 | 0.6s |

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

### osha_ita — `ok`

**Notes:** case_detail_zips=2, total_zips=9; row_count reflects case_detail only (summary has no narratives)

**Columns (49):** `id`, `establishment_id`, `establishment_name`, `ein`, `company_name`, `street_address`, `city`, `state`, `zip_code`, `naics_code`, `naics_year`, `industry_description`, `establishment_type`, `size`, `annual_average_employees` …(+34 more)

**Files:**
- `/home/user/Learning-env/data/raw/osha_ita/ITA_300A_Summary_Data_2024_through_12-31-2025.zip`
- `/home/user/Learning-env/data/raw/osha_ita/ITA_Case_Detail_Data_2024_through_12-31-2025.zip`
- `/home/user/Learning-env/data/raw/osha_ita/ITA_300A_Summary_Data_2023_through_12-31-2024.zip`
- `/home/user/Learning-env/data/raw/osha_ita/ITA_Case_Detail_Data_2023_through_12-31-2023OIICS.zip`
- `/home/user/Learning-env/data/raw/osha_ita/ITA-data-cy2022.zip`
- `/home/user/Learning-env/data/raw/osha_ita/ITA-data-cy2021.zip`
- `/home/user/Learning-env/data/raw/osha_ita/ITA-Data-CY-2020.zip`
- `/home/user/Learning-env/data/raw/osha_ita/ITA_Data_CY_2019.zip`
- `/home/user/Learning-env/data/raw/osha_ita/ITA_Data_CY_2018.zip`

### nrc — `partial`

**Notes:** Only last-month snapshot; historical 2018-2024 coverage requires scraping daily HTML pages at /reading-rm/doc-collections/event-status/event/{YEAR}/YYYYMMDDen and is deferred as a future enhancement.

**Columns (71):** `Event Desc`, `En No`, `Site Name`, `Licensee Name`, `Region No`, `City Name`, `State Cd`, `County Name`, `License No`, `Agreement State Ind`, `Docket No`, `Unit Ind1`, `Unit Ind2`, `Unit Ind3`, `Reactor Type` …(+56 more)

**Files:**
- `/home/user/Learning-env/data/raw/nrc/event-notification-rpt-lastmonth.txt`

