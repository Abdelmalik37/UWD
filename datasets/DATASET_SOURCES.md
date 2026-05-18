Dataset provenance notes:
- garmin_heart_rate_real.tcx: copied from tcxreader test fixture at https://github.com/alenrajsp/tcxreader (real TCX activity with heart-rate trackpoints).
- garmin_biking_activity_real.tcx: copied from tcxreader test fixture at https://github.com/alenrajsp/tcxreader (real biking TCX with GPS, timing, distance, speed, and cadence-style extensions where available).
- apple_health_export_real.xml: copied from apple-health-parser test fixture at https://github.com/alxdrcirilo/apple-health-parser (real Apple Health export format).
- apple_activity_summary_real.csv: copied from https://github.com/tdda/applehealthdata testdata.
- apple_step_count_real.csv: copied from https://github.com/tdda/applehealthdata testdata.
- apple_distance_walking_running_real.csv: copied from https://github.com/tdda/applehealthdata testdata.
- apple_workout_real.csv: copied from https://github.com/tdda/applehealthdata testdata.
- fitbit_heart_glucose_real_examples.json: official Fitbit Web API example payloads from docs (heart rate + blood glucose).
- fitbit_daily_activity_real.csv: copied from https://github.com/colinh80/fitbit_data_analysis fitabase_data.
- fitbit_sleep_real.csv: copied from https://github.com/colinh80/fitbit_data_analysis fitabase_data.
- fitbit_hourly_calories_real.csv: copied from https://github.com/colinh80/fitbit_data_analysis fitabase_data.
- fitbit_hourly_intensity_real.csv: copied from https://github.com/colinh80/fitbit_data_analysis fitabase_data.
- fitbit_weight_log_real.csv: copied from https://github.com/colinh80/fitbit_data_analysis fitabase_data.
- samsung_health_export_sample.csv: public Samsung Health export sample from https://github.com/bfaure/sHealthParser.
- samsung_heart_rate_sdk_example.json: official Samsung Health Android Data API example for HeartRate.BINNING_DATA from https://developer.samsung.com/health/android/data/api-reference/com/samsung/android/sdk/healthdata/HealthConstants.HeartRate.html.
- samsung_heart_rate_sdk_example.csv: CSV conversion of the same official Samsung heart-rate example values.

Coverage status:
- Heart rate: Garmin TCX, Fitbit JSON, Apple XML, Samsung (official SDK heart-rate example).
- Activity and workouts: Garmin TCX, Apple workout/activity CSV, Fitbit daily activity and hourly intensity CSV.
- Steps and distance: Apple step/distance CSV, Fitbit daily activity CSV, Samsung step-count CSV.
- Sleep: Fitbit sleep CSV.
- Calories and energy: Apple activity summary CSV, Fitbit daily/hourly calories CSV, Samsung step-count calorie field.
- Weight/body: Fitbit weight log CSV.
- Glucose: Fitbit JSON example payload.
- Blood pressure: still not found in publicly retrievable Garmin/Fitbit/Samsung sample files during this run; needs a user export or authenticated API pull.
