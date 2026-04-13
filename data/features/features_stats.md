# Phase 2C stats — structured + text features

_Generated at 2026-04-13T20:39:56+00:00_

**Structured features:** 1,702,668 rows × 27 cols
**Text features:** 1,702,668 rows × 19 cols

## Text-quality feature summary

| Feature | Mean | Median | Min | Max | Null% |
|---|---:|---:|---:|---:|---:|
| word_count | 50.869 | 45.000 | 0.000 | 836.000 | 0.0% |
| sentence_count | 2.135 | 1.000 | 1.000 | 67.000 | 0.0% |
| mean_sentence_length | 32.747 | 26.500 | 0.000 | 468.000 | 0.0% |
| type_token_ratio | 0.643 | 0.647 | 0.000 | 1.000 | 0.0% |
| char_count | 336.076 | 306.000 | 0.000 | 4467.000 | 0.0% |
| mean_word_length | 6.907 | 6.778 | 0.000 | 62.182 | 0.0% |
| causal_density_per100 | 0.143 | 0.000 | 0.000 | 20.000 | 0.0% |
| hedge_density_per100 | 0.164 | 0.000 | 0.000 | 27.273 | 0.0% |
| numeric_density_per100 | 0.797 | 0.000 | 0.000 | 50.000 | 0.0% |
| temporal_density_per100 | 0.052 | 0.000 | 0.000 | 20.000 | 0.0% |
| first_person_density_per100 | 0.405 | 0.000 | 0.000 | 33.333 | 0.0% |
| third_person_density_per100 | 2.739 | 1.515 | 0.000 | 32.143 | 0.0% |
| first_third_ratio | 0.833 | 1.000 | 0.011 | 77.000 | 0.0% |
| passive_per_sentence | 0.076 | 0.000 | 0.000 | 16.000 | 0.0% |
| flesch_kincaid_grade | 17.061 | 15.822 | -2.230 | 238.470 | 0.0% |
| gunning_fog | 19.983 | 18.429 | 1.200 | 185.383 | 0.0% |
| dale_chall | 11.983 | 11.823 | 0.198 | 31.490 | 0.0% |
| ari | 23.099 | 22.857 | -4.358 | 480.004 | 0.0% |

## Structured feature columns

- `year` (mean=2023.28, min=2018, max=2026)
- `month` (mean=6.46, min=1, max=12)
- `quarter` (mean=2.49, min=1, max=4)
- `day_of_week` (mean=2.56, min=0, max=6)
- `src_msha` (mean=0.03, min=0, max=1)
- `src_nrc` (mean=0.00, min=0, max=1)
- `src_osha_ita` (mean=0.93, min=0, max=1)
- `src_osha_sir` (mean=0.04, min=0, max=1)
- `prior_report_count` (mean=83.23, min=0, max=6410)
- `days_since_first_seen` (mean=261.75, min=0, max=3012)
- `entity_total_reports` (mean=167.47, min=1, max=6411)
- `narrative_word_count` (mean=50.39, min=0.0, max=794.0)
- `log_narrative_word_count` (mean=3.82, min=0.0, max=6.678342114654332)
- `has_severity` (mean=1.00, min=1, max=1)
- `has_address` (mean=0.97, min=0, max=1)
- `has_location` (mean=1.00, min=1, max=1)
- `fam_other` (mean=0.21, min=0, max=1)
- `fam_overexertion` (mean=0.21, min=0, max=1)
- `fam_struck_by` (mean=0.21, min=0, max=1)
- `fam_fall` (mean=0.20, min=0, max=1)
- `fam_exposure` (mean=0.11, min=0, max=1)
- `fam_caught_in` (mean=0.03, min=0, max=1)
- `fam_transport` (mean=0.02, min=0, max=1)
- `fam_fire_explosion` (mean=0.00, min=0, max=1)
- `fam_cut_pierce` (mean=0.00, min=0, max=1)
- `fam_electrical` (mean=0.00, min=0, max=1)
