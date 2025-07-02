🚀 Explainable DPF RUL Analysis
==================================================
📊 Loading DPF datasets...
🔄 Loading vehicle stats from multiple years...
✅ Maintenance records: 82 events
✅ Sensor readings (combined 2023-2025): 12,700,964 data points
   └─ 2023-2024 data: 8,234,692 points
   └─ 2024-2025 data: 4,466,272 points
✅ Diagnostic readings: 168,810 measurements

📅 Data Time Ranges:
   Maintenance: 2023-05-31 00:00:00 to 2025-06-04 00:00:00
   Sensors: 2023-04-01 00:00:00 to 2025-06-07 23:58:00
   Diagnostics: 2024-06-20 16:40:32 to 2024-07-31 23:59:59

🔗 Data Integration:
   VINs in both maintenance & sensor data: 34
🔄 Creating backtrack RUL labels with lookback periods: [7, 15, 30, 45, 60]
   Processed 20/82 maintenance events
   Processed 40/82 maintenance events
   Processed 60/82 maintenance events
   Processed 80/82 maintenance events

✅ Backtrack RUL Generation Results:
   Total maintenance events: 82
   Total RUL labels created: 346
   Average labels per event: 4.2
🔄 Processing 346 RUL examples...
   Processed 50/346 examples (50 successful)
   Processed 100/346 examples (98 successful)
   Processed 150/346 examples (143 successful)
   Processed 200/346 examples (193 successful)
   Processed 250/346 examples (243 successful)
   Processed 300/346 examples (290 successful)

✅ Successfully created RUL dataset with 336 examples
📊 Success rate: 336/346 (97.1%)
🎯 RUL range: 7-60 days
🔍 Analyzing Explainable Features...

📈 Top 10 Features Most Predictive of RUL:
   1. barometricPressurePa - 🔄 Recent vs historical behavior change (%)
      Correlation: -0.140 (stronger = more predictive)

   2. fuelPercents - ⚠️ Time spent above normal thresholds (%)
      Correlation: +0.128 (stronger = more predictive)

   3. defLevelMilliPercent - 📈 Trend direction (positive=increasing, negative=decreasing)
      Correlation: -0.124 (stronger = more predictive)

   4. fuelPercents - 📊 Stability (higher=more erratic readings)
      Correlation: -0.106 (stronger = more predictive)

   5. intakeManifoldTemperatureMilliC - 🔄 Recent vs historical behavior change (%)
      Correlation: +0.102 (stronger = more predictive)

   6. barometricPressurePa - 📊 Stability (higher=more erratic readings)
      Correlation: -0.083 (stronger = more predictive)

   7. fuelPercents - ⬇️ Time spent below normal thresholds (%)
      Correlation: -0.081 (stronger = more predictive)

   8. engineRpm - 🔄 Recent vs historical behavior change (%)
      Correlation: -0.079 (stronger = more predictive)

   9. engineRpm - ⬇️ Time spent below normal thresholds (%)
      Correlation: -0.077 (stronger = more predictive)

   10. defLevelMilliPercent - 🔄 Recent vs historical behavior change (%)
      Correlation: -0.075 (stronger = more predictive)

💡 Enhanced Interpretation Guide:
   📊 RUL Categories: CRITICAL(≤7d) → HIGH(≤15d) → MEDIUM(≤30d) → LOW(≤45d) → NORMAL(≤60d)
   📈 Positive correlation: Higher feature = Longer RUL (protective factor)
   📉 Negative correlation: Higher feature = Shorter RUL (risk factor)
   🎯 Strong correlation (>0.5): Highly predictive for maintenance planning
   📦 Quartile Analysis: Q1(lowest 25%) vs Q4(highest 25%) shows feature impact

🔍 RUL Category Insights:
   CRITICAL: 71.0 examples, avg 7.0 days (±0.0)
   HIGH: 68.0 examples, avg 15.0 days (±0.0)
   LOW: 66.0 examples, avg 45.0 days (±0.0)
   MEDIUM: 67.0 examples, avg 30.0 days (±0.0)
   NORMAL: 64.0 examples, avg 60.0 days (±0.0)

🎯 RUL CATEGORY PATTERN ANALYSIS
==================================================

🚨 CRITICAL Risk Pattern (71 examples):
   📊 engineLoadPercent trend_slope: 1245.2% higher than average
      ➡️ engineLoadPercent readings increasing faster (degradation accelerating)
   📊 barometricPressurePa pattern_change_pct: 1199.5% lower than average
   📊 fuelPercents trend_slope: 859.0% higher than average
      ➡️ fuelPercents readings increasing faster (degradation accelerating)

🚨 HIGH Risk Pattern (68 examples):
   📊 barometricPressurePa pattern_change_pct: 959.5% lower than average
   📊 engineLoadPercent trend_slope: 454.9% lower than average
      ➡️ engineLoadPercent readings more stable (slower degradation)
   📊 engineLoadPercent pattern_change_pct: 263.0% higher than average

🚨 MEDIUM Risk Pattern (67 examples):
   📊 barometricPressurePa pattern_change_pct: 461.8% higher than average
   📊 engineLoadPercent trend_slope: 427.8% lower than average
      ➡️ engineLoadPercent readings more stable (slower degradation)
   📊 engineRpm pattern_change_pct: 394.6% lower than average

🚨 LOW Risk Pattern (66 examples):
   📊 barometricPressurePa pattern_change_pct: 493.7% higher than average
   📊 engineLoadPercent trend_slope: 329.0% lower than average
      ➡️ engineLoadPercent readings more stable (slower degradation)
   📊 barometricPressurePa trend_slope: 227.6% higher than average
      ➡️ barometricPressurePa readings increasing faster (degradation accelerating)

🚨 NORMAL Risk Pattern (64 examples):
   📊 barometricPressurePa pattern_change_pct: 1344.8% higher than average
   📊 ambientAirTemperatureMilliC trend_slope: 265.9% lower than average
      ➡️ ambientAirTemperatureMilliC readings more stable (slower degradation)
   📊 intakeManifoldTemperatureMilliC pattern_change_pct: 247.6% higher than average
📊 Building model with 336 examples and 58 features

🎯 Selected Top 5 Explainable Features:
   1. barometricPressurePa_pattern_change_pct: 0.139 correlation
   2. fuelPercents_pct_time_high: 0.123 correlation
   3. defLevelMilliPercent_trend_slope: 0.123 correlation
   4. fuelPercents_volatility: 0.118 correlation
   5. intakeManifoldTemperatureMilliC_pattern_change_pct: 0.088 correlation

📈 Model Performance:
   Training MAE: 15.7 days
   Testing MAE: 17.4 days
   Training R²: 0.086
   Testing R²: 0.008

🔍 Feature Importance (How Each Factor Affects RUL):
   barometricPressurePa_pattern_change_pct: ↘️ Decreases RUL by 3.2 days per unit
   fuelPercents_pct_time_high: ↗️ Increases RUL by 3.0 days per unit
   defLevelMilliPercent_trend_slope: ↘️ Decreases RUL by 1.0 days per unit
   fuelPercents_volatility: ↘️ Decreases RUL by 2.9 days per unit
   intakeManifoldTemperatureMilliC_pattern_change_pct: ↗️ Increases RUL by 0.9 days per unit
📊 EXPLAINABLE RUL MODEL SUMMARY
==================================================
✅ Model Type: Linear Regression (Explainable)
📈 Features Used: 5
🎯 Target: Days until next DPF maintenance

🔧 Key Monitoring Features:
   1. barometricPressurePa - Pattern Change Pct
   2. fuelPercents - Pct Time High
   3. defLevelMilliPercent - Trend Slope
   4. fuelPercents - Volatility
   5. intakeManifoldTemperatureMilliC - Pattern Change Pct

🚨 Alert Thresholds:
   🚨 URGENT: ≤30 days predicted RUL
   ⚠️ WARNING: 31-60 days predicted RUL
   ⚡ CAUTION: 61-90 days predicted RUL
   ✅ NORMAL: >90 days predicted RUL

💾 To save this model for production use:
   import joblib
   joblib.dump(model, 'dpf_rul_model.pkl')
   joblib.dump(scaler, 'dpf_rul_scaler.pkl')

🎉 Explainable RUL Analysis Complete!
   Ready for deployment in fleet management system
