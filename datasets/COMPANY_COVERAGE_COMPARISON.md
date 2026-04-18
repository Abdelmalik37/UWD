# Wearable Company Coverage Comparison

This file compares companies currently represented in this repository versus companies not yet covered.

Assumption used for this comparison:
- All listed companies can provide health-related data (including heart rate) through their devices, exports, APIs, or SDKs.

## Covered Companies

| Company | Coverage Status | Heart Rate Coverage | Evidence in Repository |
|---|---|---|---|
| Garmin | Covered | Yes | `garmin_heart_rate_real.tcx`, `garmin_biking_activity_real.tcx` |
| Apple | Covered | Yes (via Apple Health export records) | `apple_health_export_real.xml`, Apple CSV files |
| Fitbit | Covered | Yes | `fitbit_heart_glucose_real_examples.json` + Fitbit activity/sleep CSV files |
| Samsung | Covered | Yes | `samsung_heart_rate_sdk_example.json`, `samsung_heart_rate_sdk_example.csv` |
| Huawei | Covered | Yes | `huawei_health_detail_data_template.json` |
| Xiaomi | Covered | Yes | `xiaomi_hlth_center_fitness_data_template.csv` |
| Amazfit / Zepp | Covered | Yes | `amazfit_zepp_activity_run_1698569116_detail_real.json`, `amazfit_zepp_activity_run_1698569116_summary_real.json` |
| Oura | Covered | Yes | `oura_heartrate_real.json`, `oura_2022-03-15T09-41-37_real.json` |
| Polar | Covered | Yes | `polar_flow_heart_rate_sample.csv`, `polar_flow_heart_rate_sample.json` |

## Non-Covered Companies (Yet)

| Company | Coverage Status | Heart Rate Assumed | Suggested Data Source Direction |
|---|---|---|---|
| WHOOP | Not covered yet | Yes | Official API/export references or public sample exports |
| Suunto | Not covered yet | Yes | Suunto app export/API examples or SDK docs |
| COROS | Not covered yet | Yes | COROS export examples or public API references |
| Withings | Not covered yet | Yes | Health Mate/API sample payloads |
| Google Pixel Watch (Google Fit ecosystem) | Not covered yet | Yes | Google Health Connect / Google Fit export or API sample payloads |
| OnePlus Watch ecosystem | Not covered yet | Yes | OHealth export/API examples |
| OPPO Watch ecosystem | Not covered yet | Yes | HeyTap/OHealth export examples |
| Vivo Watch ecosystem | Not covered yet | Yes | Vivo Health export/API examples |
| Mobvoi TicWatch | Not covered yet | Yes | Mobvoi Health/TicHealth export examples |

## Coverage Summary

- Covered companies: 9
- Not-yet-covered companies listed here: 9
- Current repository strength: broad heart-rate coverage across major wearable ecosystems.
- Main gap: fewer datasets from brands outside the current Apple/Fitbit/Garmin/Samsung/Huawei/Xiaomi/Amazfit/Oura/Polar set.

## Recommended Next Additions (Priority)

1. WHOOP
2. Suunto
3. COROS
4. Withings
5. Google Pixel Watch ecosystem

These five would improve market diversity while keeping the same health-metric focus (heart rate first, then sleep/activity/workouts).
