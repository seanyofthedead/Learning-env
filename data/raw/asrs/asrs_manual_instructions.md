# NASA ASRS Manual Export Instructions

The DBOL (Database Online) tool is an ASP.NET WebForms wizard at
**https://akama.arc.nasa.gov/ASRSDBOnline/QueryWizard_Filter.aspx** whose export endpoint is only reachable after
walking a multi-step form with hidden `__VIEWSTATE` tokens. Scripted
scraping is fragile without a headless browser — the pragmatic path
is to drive the UI yourself and drop the exports into this directory.

## Procedure

1. Open DBOL: <https://asrs.arc.nasa.gov/search/database.html>
2. Click **Begin Query**.
3. For each row in the plan below, configure these filters:
   - **Incident Date**: start and end of the quarter
   - **Anomaly**: select the anomaly from the list
   - **Airports** (multi-select): ATL, ORD, LAX, DFW, DEN, JFK, SFO, CLT, PHX, LAS, MIA, SEA, EWR, MSP, DTW, BOS, FLL, IAH, SAN, SLC
4. Run the query. On the results page, click **Export → CSV**.
5. Save the CSV into `data/raw/asrs/chunks/` using the filename in
   the table — this lets the combine step pick it up on re-run.
6. Re-run `python -m scripts.acquire_asrs`. It will concatenate all
   chunks into `asrs_combined.csv` and report summary stats.

## Chunk plan

224 chunks = 8 anomalies × 28 quarters

| # | Anomaly | Quarter | Save as |
|---:|---|---|---|
| 1 | Deviation-Altitude | 2018Q1 | `asrs_Deviation_Altitude_2018Q1.csv` |
| 2 | Deviation-Altitude | 2018Q2 | `asrs_Deviation_Altitude_2018Q2.csv` |
| 3 | Deviation-Altitude | 2018Q3 | `asrs_Deviation_Altitude_2018Q3.csv` |
| 4 | Deviation-Altitude | 2018Q4 | `asrs_Deviation_Altitude_2018Q4.csv` |
| 5 | Deviation-Altitude | 2019Q1 | `asrs_Deviation_Altitude_2019Q1.csv` |
| 6 | Deviation-Altitude | 2019Q2 | `asrs_Deviation_Altitude_2019Q2.csv` |
| 7 | Deviation-Altitude | 2019Q3 | `asrs_Deviation_Altitude_2019Q3.csv` |
| 8 | Deviation-Altitude | 2019Q4 | `asrs_Deviation_Altitude_2019Q4.csv` |
| 9 | Deviation-Altitude | 2020Q1 | `asrs_Deviation_Altitude_2020Q1.csv` |
| 10 | Deviation-Altitude | 2020Q2 | `asrs_Deviation_Altitude_2020Q2.csv` |
| 11 | Deviation-Altitude | 2020Q3 | `asrs_Deviation_Altitude_2020Q3.csv` |
| 12 | Deviation-Altitude | 2020Q4 | `asrs_Deviation_Altitude_2020Q4.csv` |
| 13 | Deviation-Altitude | 2021Q1 | `asrs_Deviation_Altitude_2021Q1.csv` |
| 14 | Deviation-Altitude | 2021Q2 | `asrs_Deviation_Altitude_2021Q2.csv` |
| 15 | Deviation-Altitude | 2021Q3 | `asrs_Deviation_Altitude_2021Q3.csv` |
| 16 | Deviation-Altitude | 2021Q4 | `asrs_Deviation_Altitude_2021Q4.csv` |
| 17 | Deviation-Altitude | 2022Q1 | `asrs_Deviation_Altitude_2022Q1.csv` |
| 18 | Deviation-Altitude | 2022Q2 | `asrs_Deviation_Altitude_2022Q2.csv` |
| 19 | Deviation-Altitude | 2022Q3 | `asrs_Deviation_Altitude_2022Q3.csv` |
| 20 | Deviation-Altitude | 2022Q4 | `asrs_Deviation_Altitude_2022Q4.csv` |
| 21 | Deviation-Altitude | 2023Q1 | `asrs_Deviation_Altitude_2023Q1.csv` |
| 22 | Deviation-Altitude | 2023Q2 | `asrs_Deviation_Altitude_2023Q2.csv` |
| 23 | Deviation-Altitude | 2023Q3 | `asrs_Deviation_Altitude_2023Q3.csv` |
| 24 | Deviation-Altitude | 2023Q4 | `asrs_Deviation_Altitude_2023Q4.csv` |
| 25 | Deviation-Altitude | 2024Q1 | `asrs_Deviation_Altitude_2024Q1.csv` |
| 26 | Deviation-Altitude | 2024Q2 | `asrs_Deviation_Altitude_2024Q2.csv` |
| 27 | Deviation-Altitude | 2024Q3 | `asrs_Deviation_Altitude_2024Q3.csv` |
| 28 | Deviation-Altitude | 2024Q4 | `asrs_Deviation_Altitude_2024Q4.csv` |
| 29 | Deviation-Procedural | 2018Q1 | `asrs_Deviation_Procedural_2018Q1.csv` |
| 30 | Deviation-Procedural | 2018Q2 | `asrs_Deviation_Procedural_2018Q2.csv` |
| 31 | Deviation-Procedural | 2018Q3 | `asrs_Deviation_Procedural_2018Q3.csv` |
| 32 | Deviation-Procedural | 2018Q4 | `asrs_Deviation_Procedural_2018Q4.csv` |
| 33 | Deviation-Procedural | 2019Q1 | `asrs_Deviation_Procedural_2019Q1.csv` |
| 34 | Deviation-Procedural | 2019Q2 | `asrs_Deviation_Procedural_2019Q2.csv` |
| 35 | Deviation-Procedural | 2019Q3 | `asrs_Deviation_Procedural_2019Q3.csv` |
| 36 | Deviation-Procedural | 2019Q4 | `asrs_Deviation_Procedural_2019Q4.csv` |
| 37 | Deviation-Procedural | 2020Q1 | `asrs_Deviation_Procedural_2020Q1.csv` |
| 38 | Deviation-Procedural | 2020Q2 | `asrs_Deviation_Procedural_2020Q2.csv` |
| 39 | Deviation-Procedural | 2020Q3 | `asrs_Deviation_Procedural_2020Q3.csv` |
| 40 | Deviation-Procedural | 2020Q4 | `asrs_Deviation_Procedural_2020Q4.csv` |
| 41 | Deviation-Procedural | 2021Q1 | `asrs_Deviation_Procedural_2021Q1.csv` |
| 42 | Deviation-Procedural | 2021Q2 | `asrs_Deviation_Procedural_2021Q2.csv` |
| 43 | Deviation-Procedural | 2021Q3 | `asrs_Deviation_Procedural_2021Q3.csv` |
| 44 | Deviation-Procedural | 2021Q4 | `asrs_Deviation_Procedural_2021Q4.csv` |
| 45 | Deviation-Procedural | 2022Q1 | `asrs_Deviation_Procedural_2022Q1.csv` |
| 46 | Deviation-Procedural | 2022Q2 | `asrs_Deviation_Procedural_2022Q2.csv` |
| 47 | Deviation-Procedural | 2022Q3 | `asrs_Deviation_Procedural_2022Q3.csv` |
| 48 | Deviation-Procedural | 2022Q4 | `asrs_Deviation_Procedural_2022Q4.csv` |
| 49 | Deviation-Procedural | 2023Q1 | `asrs_Deviation_Procedural_2023Q1.csv` |
| 50 | Deviation-Procedural | 2023Q2 | `asrs_Deviation_Procedural_2023Q2.csv` |
| 51 | Deviation-Procedural | 2023Q3 | `asrs_Deviation_Procedural_2023Q3.csv` |
| 52 | Deviation-Procedural | 2023Q4 | `asrs_Deviation_Procedural_2023Q4.csv` |
| 53 | Deviation-Procedural | 2024Q1 | `asrs_Deviation_Procedural_2024Q1.csv` |
| 54 | Deviation-Procedural | 2024Q2 | `asrs_Deviation_Procedural_2024Q2.csv` |
| 55 | Deviation-Procedural | 2024Q3 | `asrs_Deviation_Procedural_2024Q3.csv` |
| 56 | Deviation-Procedural | 2024Q4 | `asrs_Deviation_Procedural_2024Q4.csv` |
| 57 | Conflict | 2018Q1 | `asrs_Conflict_2018Q1.csv` |
| 58 | Conflict | 2018Q2 | `asrs_Conflict_2018Q2.csv` |
| 59 | Conflict | 2018Q3 | `asrs_Conflict_2018Q3.csv` |
| 60 | Conflict | 2018Q4 | `asrs_Conflict_2018Q4.csv` |
| 61 | Conflict | 2019Q1 | `asrs_Conflict_2019Q1.csv` |
| 62 | Conflict | 2019Q2 | `asrs_Conflict_2019Q2.csv` |
| 63 | Conflict | 2019Q3 | `asrs_Conflict_2019Q3.csv` |
| 64 | Conflict | 2019Q4 | `asrs_Conflict_2019Q4.csv` |
| 65 | Conflict | 2020Q1 | `asrs_Conflict_2020Q1.csv` |
| 66 | Conflict | 2020Q2 | `asrs_Conflict_2020Q2.csv` |
| 67 | Conflict | 2020Q3 | `asrs_Conflict_2020Q3.csv` |
| 68 | Conflict | 2020Q4 | `asrs_Conflict_2020Q4.csv` |
| 69 | Conflict | 2021Q1 | `asrs_Conflict_2021Q1.csv` |
| 70 | Conflict | 2021Q2 | `asrs_Conflict_2021Q2.csv` |
| 71 | Conflict | 2021Q3 | `asrs_Conflict_2021Q3.csv` |
| 72 | Conflict | 2021Q4 | `asrs_Conflict_2021Q4.csv` |
| 73 | Conflict | 2022Q1 | `asrs_Conflict_2022Q1.csv` |
| 74 | Conflict | 2022Q2 | `asrs_Conflict_2022Q2.csv` |
| 75 | Conflict | 2022Q3 | `asrs_Conflict_2022Q3.csv` |
| 76 | Conflict | 2022Q4 | `asrs_Conflict_2022Q4.csv` |
| 77 | Conflict | 2023Q1 | `asrs_Conflict_2023Q1.csv` |
| 78 | Conflict | 2023Q2 | `asrs_Conflict_2023Q2.csv` |
| 79 | Conflict | 2023Q3 | `asrs_Conflict_2023Q3.csv` |
| 80 | Conflict | 2023Q4 | `asrs_Conflict_2023Q4.csv` |
| 81 | Conflict | 2024Q1 | `asrs_Conflict_2024Q1.csv` |
| 82 | Conflict | 2024Q2 | `asrs_Conflict_2024Q2.csv` |
| 83 | Conflict | 2024Q3 | `asrs_Conflict_2024Q3.csv` |
| 84 | Conflict | 2024Q4 | `asrs_Conflict_2024Q4.csv` |
| 85 | ATC Issue | 2018Q1 | `asrs_ATC_Issue_2018Q1.csv` |
| 86 | ATC Issue | 2018Q2 | `asrs_ATC_Issue_2018Q2.csv` |
| 87 | ATC Issue | 2018Q3 | `asrs_ATC_Issue_2018Q3.csv` |
| 88 | ATC Issue | 2018Q4 | `asrs_ATC_Issue_2018Q4.csv` |
| 89 | ATC Issue | 2019Q1 | `asrs_ATC_Issue_2019Q1.csv` |
| 90 | ATC Issue | 2019Q2 | `asrs_ATC_Issue_2019Q2.csv` |
| 91 | ATC Issue | 2019Q3 | `asrs_ATC_Issue_2019Q3.csv` |
| 92 | ATC Issue | 2019Q4 | `asrs_ATC_Issue_2019Q4.csv` |
| 93 | ATC Issue | 2020Q1 | `asrs_ATC_Issue_2020Q1.csv` |
| 94 | ATC Issue | 2020Q2 | `asrs_ATC_Issue_2020Q2.csv` |
| 95 | ATC Issue | 2020Q3 | `asrs_ATC_Issue_2020Q3.csv` |
| 96 | ATC Issue | 2020Q4 | `asrs_ATC_Issue_2020Q4.csv` |
| 97 | ATC Issue | 2021Q1 | `asrs_ATC_Issue_2021Q1.csv` |
| 98 | ATC Issue | 2021Q2 | `asrs_ATC_Issue_2021Q2.csv` |
| 99 | ATC Issue | 2021Q3 | `asrs_ATC_Issue_2021Q3.csv` |
| 100 | ATC Issue | 2021Q4 | `asrs_ATC_Issue_2021Q4.csv` |
| 101 | ATC Issue | 2022Q1 | `asrs_ATC_Issue_2022Q1.csv` |
| 102 | ATC Issue | 2022Q2 | `asrs_ATC_Issue_2022Q2.csv` |
| 103 | ATC Issue | 2022Q3 | `asrs_ATC_Issue_2022Q3.csv` |
| 104 | ATC Issue | 2022Q4 | `asrs_ATC_Issue_2022Q4.csv` |
| 105 | ATC Issue | 2023Q1 | `asrs_ATC_Issue_2023Q1.csv` |
| 106 | ATC Issue | 2023Q2 | `asrs_ATC_Issue_2023Q2.csv` |
| 107 | ATC Issue | 2023Q3 | `asrs_ATC_Issue_2023Q3.csv` |
| 108 | ATC Issue | 2023Q4 | `asrs_ATC_Issue_2023Q4.csv` |
| 109 | ATC Issue | 2024Q1 | `asrs_ATC_Issue_2024Q1.csv` |
| 110 | ATC Issue | 2024Q2 | `asrs_ATC_Issue_2024Q2.csv` |
| 111 | ATC Issue | 2024Q3 | `asrs_ATC_Issue_2024Q3.csv` |
| 112 | ATC Issue | 2024Q4 | `asrs_ATC_Issue_2024Q4.csv` |
| 113 | Aircraft Equipment Problem | 2018Q1 | `asrs_Aircraft_Equipment_Problem_2018Q1.csv` |
| 114 | Aircraft Equipment Problem | 2018Q2 | `asrs_Aircraft_Equipment_Problem_2018Q2.csv` |
| 115 | Aircraft Equipment Problem | 2018Q3 | `asrs_Aircraft_Equipment_Problem_2018Q3.csv` |
| 116 | Aircraft Equipment Problem | 2018Q4 | `asrs_Aircraft_Equipment_Problem_2018Q4.csv` |
| 117 | Aircraft Equipment Problem | 2019Q1 | `asrs_Aircraft_Equipment_Problem_2019Q1.csv` |
| 118 | Aircraft Equipment Problem | 2019Q2 | `asrs_Aircraft_Equipment_Problem_2019Q2.csv` |
| 119 | Aircraft Equipment Problem | 2019Q3 | `asrs_Aircraft_Equipment_Problem_2019Q3.csv` |
| 120 | Aircraft Equipment Problem | 2019Q4 | `asrs_Aircraft_Equipment_Problem_2019Q4.csv` |
| 121 | Aircraft Equipment Problem | 2020Q1 | `asrs_Aircraft_Equipment_Problem_2020Q1.csv` |
| 122 | Aircraft Equipment Problem | 2020Q2 | `asrs_Aircraft_Equipment_Problem_2020Q2.csv` |
| 123 | Aircraft Equipment Problem | 2020Q3 | `asrs_Aircraft_Equipment_Problem_2020Q3.csv` |
| 124 | Aircraft Equipment Problem | 2020Q4 | `asrs_Aircraft_Equipment_Problem_2020Q4.csv` |
| 125 | Aircraft Equipment Problem | 2021Q1 | `asrs_Aircraft_Equipment_Problem_2021Q1.csv` |
| 126 | Aircraft Equipment Problem | 2021Q2 | `asrs_Aircraft_Equipment_Problem_2021Q2.csv` |
| 127 | Aircraft Equipment Problem | 2021Q3 | `asrs_Aircraft_Equipment_Problem_2021Q3.csv` |
| 128 | Aircraft Equipment Problem | 2021Q4 | `asrs_Aircraft_Equipment_Problem_2021Q4.csv` |
| 129 | Aircraft Equipment Problem | 2022Q1 | `asrs_Aircraft_Equipment_Problem_2022Q1.csv` |
| 130 | Aircraft Equipment Problem | 2022Q2 | `asrs_Aircraft_Equipment_Problem_2022Q2.csv` |
| 131 | Aircraft Equipment Problem | 2022Q3 | `asrs_Aircraft_Equipment_Problem_2022Q3.csv` |
| 132 | Aircraft Equipment Problem | 2022Q4 | `asrs_Aircraft_Equipment_Problem_2022Q4.csv` |
| 133 | Aircraft Equipment Problem | 2023Q1 | `asrs_Aircraft_Equipment_Problem_2023Q1.csv` |
| 134 | Aircraft Equipment Problem | 2023Q2 | `asrs_Aircraft_Equipment_Problem_2023Q2.csv` |
| 135 | Aircraft Equipment Problem | 2023Q3 | `asrs_Aircraft_Equipment_Problem_2023Q3.csv` |
| 136 | Aircraft Equipment Problem | 2023Q4 | `asrs_Aircraft_Equipment_Problem_2023Q4.csv` |
| 137 | Aircraft Equipment Problem | 2024Q1 | `asrs_Aircraft_Equipment_Problem_2024Q1.csv` |
| 138 | Aircraft Equipment Problem | 2024Q2 | `asrs_Aircraft_Equipment_Problem_2024Q2.csv` |
| 139 | Aircraft Equipment Problem | 2024Q3 | `asrs_Aircraft_Equipment_Problem_2024Q3.csv` |
| 140 | Aircraft Equipment Problem | 2024Q4 | `asrs_Aircraft_Equipment_Problem_2024Q4.csv` |
| 141 | Airspace Violation | 2018Q1 | `asrs_Airspace_Violation_2018Q1.csv` |
| 142 | Airspace Violation | 2018Q2 | `asrs_Airspace_Violation_2018Q2.csv` |
| 143 | Airspace Violation | 2018Q3 | `asrs_Airspace_Violation_2018Q3.csv` |
| 144 | Airspace Violation | 2018Q4 | `asrs_Airspace_Violation_2018Q4.csv` |
| 145 | Airspace Violation | 2019Q1 | `asrs_Airspace_Violation_2019Q1.csv` |
| 146 | Airspace Violation | 2019Q2 | `asrs_Airspace_Violation_2019Q2.csv` |
| 147 | Airspace Violation | 2019Q3 | `asrs_Airspace_Violation_2019Q3.csv` |
| 148 | Airspace Violation | 2019Q4 | `asrs_Airspace_Violation_2019Q4.csv` |
| 149 | Airspace Violation | 2020Q1 | `asrs_Airspace_Violation_2020Q1.csv` |
| 150 | Airspace Violation | 2020Q2 | `asrs_Airspace_Violation_2020Q2.csv` |
| 151 | Airspace Violation | 2020Q3 | `asrs_Airspace_Violation_2020Q3.csv` |
| 152 | Airspace Violation | 2020Q4 | `asrs_Airspace_Violation_2020Q4.csv` |
| 153 | Airspace Violation | 2021Q1 | `asrs_Airspace_Violation_2021Q1.csv` |
| 154 | Airspace Violation | 2021Q2 | `asrs_Airspace_Violation_2021Q2.csv` |
| 155 | Airspace Violation | 2021Q3 | `asrs_Airspace_Violation_2021Q3.csv` |
| 156 | Airspace Violation | 2021Q4 | `asrs_Airspace_Violation_2021Q4.csv` |
| 157 | Airspace Violation | 2022Q1 | `asrs_Airspace_Violation_2022Q1.csv` |
| 158 | Airspace Violation | 2022Q2 | `asrs_Airspace_Violation_2022Q2.csv` |
| 159 | Airspace Violation | 2022Q3 | `asrs_Airspace_Violation_2022Q3.csv` |
| 160 | Airspace Violation | 2022Q4 | `asrs_Airspace_Violation_2022Q4.csv` |
| 161 | Airspace Violation | 2023Q1 | `asrs_Airspace_Violation_2023Q1.csv` |
| 162 | Airspace Violation | 2023Q2 | `asrs_Airspace_Violation_2023Q2.csv` |
| 163 | Airspace Violation | 2023Q3 | `asrs_Airspace_Violation_2023Q3.csv` |
| 164 | Airspace Violation | 2023Q4 | `asrs_Airspace_Violation_2023Q4.csv` |
| 165 | Airspace Violation | 2024Q1 | `asrs_Airspace_Violation_2024Q1.csv` |
| 166 | Airspace Violation | 2024Q2 | `asrs_Airspace_Violation_2024Q2.csv` |
| 167 | Airspace Violation | 2024Q3 | `asrs_Airspace_Violation_2024Q3.csv` |
| 168 | Airspace Violation | 2024Q4 | `asrs_Airspace_Violation_2024Q4.csv` |
| 169 | Runway Incursion | 2018Q1 | `asrs_Runway_Incursion_2018Q1.csv` |
| 170 | Runway Incursion | 2018Q2 | `asrs_Runway_Incursion_2018Q2.csv` |
| 171 | Runway Incursion | 2018Q3 | `asrs_Runway_Incursion_2018Q3.csv` |
| 172 | Runway Incursion | 2018Q4 | `asrs_Runway_Incursion_2018Q4.csv` |
| 173 | Runway Incursion | 2019Q1 | `asrs_Runway_Incursion_2019Q1.csv` |
| 174 | Runway Incursion | 2019Q2 | `asrs_Runway_Incursion_2019Q2.csv` |
| 175 | Runway Incursion | 2019Q3 | `asrs_Runway_Incursion_2019Q3.csv` |
| 176 | Runway Incursion | 2019Q4 | `asrs_Runway_Incursion_2019Q4.csv` |
| 177 | Runway Incursion | 2020Q1 | `asrs_Runway_Incursion_2020Q1.csv` |
| 178 | Runway Incursion | 2020Q2 | `asrs_Runway_Incursion_2020Q2.csv` |
| 179 | Runway Incursion | 2020Q3 | `asrs_Runway_Incursion_2020Q3.csv` |
| 180 | Runway Incursion | 2020Q4 | `asrs_Runway_Incursion_2020Q4.csv` |
| 181 | Runway Incursion | 2021Q1 | `asrs_Runway_Incursion_2021Q1.csv` |
| 182 | Runway Incursion | 2021Q2 | `asrs_Runway_Incursion_2021Q2.csv` |
| 183 | Runway Incursion | 2021Q3 | `asrs_Runway_Incursion_2021Q3.csv` |
| 184 | Runway Incursion | 2021Q4 | `asrs_Runway_Incursion_2021Q4.csv` |
| 185 | Runway Incursion | 2022Q1 | `asrs_Runway_Incursion_2022Q1.csv` |
| 186 | Runway Incursion | 2022Q2 | `asrs_Runway_Incursion_2022Q2.csv` |
| 187 | Runway Incursion | 2022Q3 | `asrs_Runway_Incursion_2022Q3.csv` |
| 188 | Runway Incursion | 2022Q4 | `asrs_Runway_Incursion_2022Q4.csv` |
| 189 | Runway Incursion | 2023Q1 | `asrs_Runway_Incursion_2023Q1.csv` |
| 190 | Runway Incursion | 2023Q2 | `asrs_Runway_Incursion_2023Q2.csv` |
| 191 | Runway Incursion | 2023Q3 | `asrs_Runway_Incursion_2023Q3.csv` |
| 192 | Runway Incursion | 2023Q4 | `asrs_Runway_Incursion_2023Q4.csv` |
| 193 | Runway Incursion | 2024Q1 | `asrs_Runway_Incursion_2024Q1.csv` |
| 194 | Runway Incursion | 2024Q2 | `asrs_Runway_Incursion_2024Q2.csv` |
| 195 | Runway Incursion | 2024Q3 | `asrs_Runway_Incursion_2024Q3.csv` |
| 196 | Runway Incursion | 2024Q4 | `asrs_Runway_Incursion_2024Q4.csv` |
| 197 | Ground Incursion | 2018Q1 | `asrs_Ground_Incursion_2018Q1.csv` |
| 198 | Ground Incursion | 2018Q2 | `asrs_Ground_Incursion_2018Q2.csv` |
| 199 | Ground Incursion | 2018Q3 | `asrs_Ground_Incursion_2018Q3.csv` |
| 200 | Ground Incursion | 2018Q4 | `asrs_Ground_Incursion_2018Q4.csv` |
| 201 | Ground Incursion | 2019Q1 | `asrs_Ground_Incursion_2019Q1.csv` |
| 202 | Ground Incursion | 2019Q2 | `asrs_Ground_Incursion_2019Q2.csv` |
| 203 | Ground Incursion | 2019Q3 | `asrs_Ground_Incursion_2019Q3.csv` |
| 204 | Ground Incursion | 2019Q4 | `asrs_Ground_Incursion_2019Q4.csv` |
| 205 | Ground Incursion | 2020Q1 | `asrs_Ground_Incursion_2020Q1.csv` |
| 206 | Ground Incursion | 2020Q2 | `asrs_Ground_Incursion_2020Q2.csv` |
| 207 | Ground Incursion | 2020Q3 | `asrs_Ground_Incursion_2020Q3.csv` |
| 208 | Ground Incursion | 2020Q4 | `asrs_Ground_Incursion_2020Q4.csv` |
| 209 | Ground Incursion | 2021Q1 | `asrs_Ground_Incursion_2021Q1.csv` |
| 210 | Ground Incursion | 2021Q2 | `asrs_Ground_Incursion_2021Q2.csv` |
| 211 | Ground Incursion | 2021Q3 | `asrs_Ground_Incursion_2021Q3.csv` |
| 212 | Ground Incursion | 2021Q4 | `asrs_Ground_Incursion_2021Q4.csv` |
| 213 | Ground Incursion | 2022Q1 | `asrs_Ground_Incursion_2022Q1.csv` |
| 214 | Ground Incursion | 2022Q2 | `asrs_Ground_Incursion_2022Q2.csv` |
| 215 | Ground Incursion | 2022Q3 | `asrs_Ground_Incursion_2022Q3.csv` |
| 216 | Ground Incursion | 2022Q4 | `asrs_Ground_Incursion_2022Q4.csv` |
| 217 | Ground Incursion | 2023Q1 | `asrs_Ground_Incursion_2023Q1.csv` |
| 218 | Ground Incursion | 2023Q2 | `asrs_Ground_Incursion_2023Q2.csv` |
| 219 | Ground Incursion | 2023Q3 | `asrs_Ground_Incursion_2023Q3.csv` |
| 220 | Ground Incursion | 2023Q4 | `asrs_Ground_Incursion_2023Q4.csv` |
| 221 | Ground Incursion | 2024Q1 | `asrs_Ground_Incursion_2024Q1.csv` |
| 222 | Ground Incursion | 2024Q2 | `asrs_Ground_Incursion_2024Q2.csv` |
| 223 | Ground Incursion | 2024Q3 | `asrs_Ground_Incursion_2024Q3.csv` |
| 224 | Ground Incursion | 2024Q4 | `asrs_Ground_Incursion_2024Q4.csv` |

## If a quarter returns exactly 10,000 rows

DBOL caps results at 10,000 per query. If any quarterly chunk hits
the cap, split it into months (e.g. 2022M01…2022M03 for 2022Q1) and
rename the files accordingly — the combine step concatenates all
CSVs in the chunks directory regardless of filename.

## Status

This file was generated by `scripts/acquire_asrs.py`. It is kept in
git so anyone rebuilding the corpus has a concrete playbook.
