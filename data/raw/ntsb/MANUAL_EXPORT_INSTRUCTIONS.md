# NTSB CAROL Manual Export Instructions

The CAROL public API at `https://data.ntsb.gov/carol-main-public/api/Query/Main` requires an undocumented `QueryRule`
schema. Scripted queries receive HTTP 400 with
`{"Error":"QueryGroups does not contain valid QueryRules"}`. Rather
than block Phase 1, this file was generated automatically so the
acquisition pipeline can complete; you can fill in NTSB data manually.

## Manual export procedure

1. Open the CAROL basic search UI in a browser:
   **https://data.ntsb.gov/carol-main-public/basic-search**
2. Event Type: **Aviation**
3. Event Date: **2018-01-01** through **2025-12-31**
4. Run the search.
5. Click the "Export" button (CSV or JSON).
6. Save the exported file into this directory
   (`data/raw/ntsb/`) with any filename — for example
   `carol_aviation_2018_2025.csv`.
7. Re-run `python -m scripts.acquire_ntsb` and the script will pick up
   any CSV/JSON file in this directory, compute summary stats, and
   update the manifest.

## Capturing a working API body (for full automation)

If you want the acquirer to paginate automatically:

1. Open the CAROL UI above.
2. Open browser DevTools → Network tab.
3. Run any search.
4. Find the POST request to `/carol-main-public/api/Query/Main`.
5. Copy the JSON request body from the "Request" panel.
6. Paste it into `scripts/acquire_ntsb.py` as the value of
   `CAROL_QUERY_BODY` at the top of the file.
7. Re-run the acquirer.

The pagination loop is already written — it just needs a known-good
base query body.
