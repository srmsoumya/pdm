✅ Statsmodels VAR successfully imported
✅ StatsForecast successfully imported
🚀 COMPREHENSIVE FLEET MULTIVARIATE FORECASTING FOR DPF RUL
======================================================================
📊 Loading DPF datasets for multivariate analysis...
✅ Maintenance records: 82 events
✅ Sensor readings: 12,700,964 data points

🎯 Identifying ALL vehicles suitable for multivariate analysis...
   🚗 Total vehicles with DPF maintenance history: 34

📊 Found 34 vehicles suitable for multivariate analysis:
   📈 Data quality range: 177 - 791 days
   🔧 Maintenance urgency: 23 - 756 days since last service

🚨 Top 10 Most Urgent Vehicles (by maintenance recency):
    1. 1XKWD40X6FJ436975 - 756 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 511 days data
    2. 5KJJAED19GPHF6382 - 751 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 484 days data
    3. 1M2TE2GC7LM004209 - 744 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 529 days data
    4. 2FZACGBS28AZ75394 - 728 days since maintenance 🔴 OVERDUE
       📊 4 sensors, 177 days data
    5. 1M2AV04C9JM019131 - 711 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 524 days data
    6. 1M2AX07C9FM022480 - 616 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 564 days data
    7. 1M2AV04C3HM015506 - 547 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 522 days data
    8. 1M2AV04C5HM015507 - 539 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 360 days data
    9. 1XK1D40X8LJ409220 - 512 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 662 days data
   10. 1M2AV04C2EM011457 - 508 days since maintenance 🔴 OVERDUE
       📊 5 sensors, 344 days data

🎯 Analyzing ALL 34 viable vehicles for comprehensive fleet assessment

======================================================================
📊 ANALYZING VEHICLE 1/34: 1XKWD40X6FJ436975
======================================================================

🔧 Preparing multivariate time series for vehicle 1XKWD40X6FJ436975...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 28 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 311 days, 3 sensors
   📅 Date range: 2023-04-18 00:00:00 to 2024-09-27 00:00:00
   📊 defLevelMilliPercent: μ=64609.20, σ=15206.45
   📊 engineLoadPercent: μ=43.16, σ=9.12
   📊 engineCoolantTemperatureMilliC: μ=83119.53, σ=4438.60

📈 Analyzing sensor correlations for vehicle 1XKWD40X6FJ436975...
🔍 Cross-Sensor Correlations:
   🔗 engineLoadPercent & engineCoolantTemperatureMilliC: strongly positively correlated (+0.712)

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1XKWD40X6FJ436975...
   📊 Checking stationarity...
   🔄 defLevelMilliPercent non-stationary (p=0.061), applying differencing
   ✅ engineLoadPercent stationary (p=0.001)
   ✅ engineCoolantTemperatureMilliC stationary (p=0.013)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1XKWD40X6FJ436975...
   🔧 Days since last maintenance: 756
   📈 defLevelMilliPercent:
      Current: 47266.67 → 30-day: 43095.23
      Change: -4171.44 (-8.8%)
      Volatility: 0.086
   📈 engineLoadPercent:
      Current: 24.89 → 30-day: 42.74
      Change: +17.84 (+71.7%)
      Volatility: 0.052
   📈 engineCoolantTemperatureMilliC:
      Current: 70727.27 → 30-day: 82843.34
      Change: +12116.07 (+17.1%)
      Volatility: 0.019

   🚨 System Risk Level: HIGH
   ⚠️ Risk Factors:
      • DEF system showing significant decline
      • Engine load increasing or becoming unstable
      • Engine temperature rising concern
   ✅ Risk Assessment: HIGH (3 factors)

======================================================================
📊 ANALYZING VEHICLE 2/34: 5KJJAED19GPHF6382
======================================================================

🔧 Preparing multivariate time series for vehicle 5KJJAED19GPHF6382...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 228 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2024-10-09 00:00:00
   📊 defLevelMilliPercent: μ=68154.87, σ=17860.59
   📊 engineLoadPercent: μ=43.89, σ=12.27
   📊 engineCoolantTemperatureMilliC: μ=77880.82, σ=23774.05

📈 Analyzing sensor correlations for vehicle 5KJJAED19GPHF6382...
🔍 Cross-Sensor Correlations:
   🔗 engineLoadPercent & engineCoolantTemperatureMilliC: moderately positively correlated (+0.636)

🕒 Analyzing lead-lag relationships...
   ⏰ engineCoolantTemperatureMilliC leads engineLoadPercent by 1 days (r=+0.438)
   ⏰ engineCoolantTemperatureMilliC leads engineLoadPercent by 1 days (r=+0.438)

🤖 Building VAR model for vehicle 5KJJAED19GPHF6382...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   ✅ engineCoolantTemperatureMilliC stationary (p=0.034)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 2
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 5KJJAED19GPHF6382...
   🔧 Days since last maintenance: 751
   📈 defLevelMilliPercent:
      Current: 89044.00 → 30-day: 68102.90
      Change: -20941.10 (-23.5%)
      Volatility: 0.016
   📈 engineLoadPercent:
      Current: 51.86 → 30-day: 43.72
      Change: -8.13 (-15.7%)
      Volatility: 0.016
   📈 engineCoolantTemperatureMilliC:
      Current: 89401.46 → 30-day: 77714.70
      Change: -11686.76 (-13.1%)
      Volatility: 0.025

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • DEF system showing significant decline
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 3/34: 1M2TE2GC7LM004209
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2TE2GC7LM004209...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 12 outliers from engineLoadPercent
   🗑️ Removed 56 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 456 days, 3 sensors
   📅 Date range: 2023-04-01 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=78308.10, σ=13776.96
   📊 engineLoadPercent: μ=41.90, σ=3.28
   📊 engineCoolantTemperatureMilliC: μ=88316.98, σ=2535.53

📈 Analyzing sensor correlations for vehicle 1M2TE2GC7LM004209...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2TE2GC7LM004209...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.002)
   ✅ engineLoadPercent stationary (p=0.009)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.115), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 8
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2TE2GC7LM004209...
   🔧 Days since last maintenance: 744
   📈 defLevelMilliPercent:
      Current: 63974.11 → 30-day: 77971.33
      Change: +13997.22 (+21.9%)
      Volatility: 0.035
   📈 engineLoadPercent:
      Current: 52.09 → 30-day: 42.69
      Change: -9.40 (-18.1%)
      Volatility: 0.020
   📈 engineCoolantTemperatureMilliC:
      Current: 92627.45 → 30-day: 90593.83
      Change: -2033.62 (-2.2%)
      Volatility: 0.002

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 4/34: 2FZACGBS28AZ75394
======================================================================

🔧 Preparing multivariate time series for vehicle 2FZACGBS28AZ75394...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   ❌ Insufficient clean data: 0 days (need 60)
   ⏭️ Skipping 2FZACGBS28AZ75394 - insufficient multivariate data

======================================================================
📊 ANALYZING VEHICLE 5/34: 1M2AV04C9JM019131
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AV04C9JM019131...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 12 outliers from defLevelMilliPercent
   🗑️ Removed 7 outliers from engineLoadPercent
   🗑️ Removed 68 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 422 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=86248.99, σ=6831.26
   📊 engineLoadPercent: μ=38.30, σ=3.90
   📊 engineCoolantTemperatureMilliC: μ=85664.30, σ=4756.21

📈 Analyzing sensor correlations for vehicle 1M2AV04C9JM019131...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AV04C9JM019131...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.001)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.149), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 8
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AV04C9JM019131...
   🔧 Days since last maintenance: 711
   📈 defLevelMilliPercent:
      Current: 92147.95 → 30-day: 86445.49
      Change: -5702.46 (-6.2%)
      Volatility: 0.005
   📈 engineLoadPercent:
      Current: 33.15 → 30-day: 37.91
      Change: +4.76 (+14.4%)
      Volatility: 0.011
   📈 engineCoolantTemperatureMilliC:
      Current: 88912.55 → 30-day: 88955.57
      Change: +43.02 (+0.0%)
      Volatility: 0.003

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 6/34: 1M2AX07C9FM022480
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AX07C9FM022480...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 2 outliers from engineLoadPercent
   🗑️ Removed 65 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 415 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=81217.90, σ=14117.74
   📊 engineLoadPercent: μ=29.79, σ=5.83
   📊 engineCoolantTemperatureMilliC: μ=80010.33, σ=3830.66

📈 Analyzing sensor correlations for vehicle 1M2AX07C9FM022480...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AX07C9FM022480...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   ✅ engineCoolantTemperatureMilliC stationary (p=0.032)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 4
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AX07C9FM022480...
   🔧 Days since last maintenance: 616
   📈 defLevelMilliPercent:
      Current: 75390.63 → 30-day: 80902.82
      Change: +5512.18 (+7.3%)
      Volatility: 0.021
   📈 engineLoadPercent:
      Current: 23.36 → 30-day: 29.42
      Change: +6.06 (+26.0%)
      Volatility: 0.052
   📈 engineCoolantTemperatureMilliC:
      Current: 85766.67 → 30-day: 80003.69
      Change: -5762.98 (-6.7%)
      Volatility: 0.008

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine load increasing or becoming unstable
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 7/34: 1M2AV04C3HM015506
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AV04C3HM015506...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 25 outliers from defLevelMilliPercent
   🗑️ Removed 78 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 406 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=83713.67, σ=8689.81
   📊 engineLoadPercent: μ=43.64, σ=4.53
   📊 engineCoolantTemperatureMilliC: μ=87743.37, σ=3077.83

📈 Analyzing sensor correlations for vehicle 1M2AV04C3HM015506...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AV04C3HM015506...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   🔄 engineLoadPercent non-stationary (p=0.180), applying differencing
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.201), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 7
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AV04C3HM015506...
   🔧 Days since last maintenance: 547
   📈 defLevelMilliPercent:
      Current: 81522.58 → 30-day: 83669.24
      Change: +2146.66 (+2.6%)
      Volatility: 0.003
   📈 engineLoadPercent:
      Current: 44.85 → 30-day: 45.13
      Change: +0.27 (+0.6%)
      Volatility: 0.004
   📈 engineCoolantTemperatureMilliC:
      Current: 92076.61 → 30-day: 90919.96
      Change: -1156.65 (-1.3%)
      Volatility: 0.002

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 8/34: 1M2AV04C5HM015507
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AV04C5HM015507...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 1 outliers from defLevelMilliPercent
   🗑️ Removed 5 outliers from engineLoadPercent
   🗑️ Removed 48 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 271 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=83165.76, σ=14170.28
   📊 engineLoadPercent: μ=43.45, σ=4.77
   📊 engineCoolantTemperatureMilliC: μ=84464.15, σ=7504.50

📈 Analyzing sensor correlations for vehicle 1M2AV04C5HM015507...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AV04C5HM015507...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.003)
   ✅ engineLoadPercent stationary (p=0.000)
   ✅ engineCoolantTemperatureMilliC stationary (p=0.000)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AV04C5HM015507...
   🔧 Days since last maintenance: 539
   📈 defLevelMilliPercent:
      Current: 83400.00 → 30-day: 83138.31
      Change: -261.69 (-0.3%)
      Volatility: 0.014
   📈 engineLoadPercent:
      Current: 42.67 → 30-day: 43.40
      Change: +0.73 (+1.7%)
      Volatility: 0.016
   📈 engineCoolantTemperatureMilliC:
      Current: 72142.86 → 30-day: 84290.58
      Change: +12147.73 (+16.8%)
      Volatility: 0.015

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 9/34: 1XK1D40X8LJ409220
======================================================================

🔧 Preparing multivariate time series for vehicle 1XK1D40X8LJ409220...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 4 outliers from defLevelMilliPercent
   🗑️ Removed 50 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 481 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=81778.37, σ=14275.99
   📊 engineLoadPercent: μ=47.11, σ=6.70
   📊 engineCoolantTemperatureMilliC: μ=83813.98, σ=2349.38

📈 Analyzing sensor correlations for vehicle 1XK1D40X8LJ409220...
🔍 Cross-Sensor Correlations:
   🔗 engineLoadPercent & engineCoolantTemperatureMilliC: moderately positively correlated (+0.402)

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1XK1D40X8LJ409220...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.001)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.240), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 6
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1XK1D40X8LJ409220...
   🔧 Days since last maintenance: 512
   📈 defLevelMilliPercent:
      Current: 89101.84 → 30-day: 81790.97
      Change: -7310.87 (-8.2%)
      Volatility: 0.017
   📈 engineLoadPercent:
      Current: 29.98 → 30-day: 46.94
      Change: +16.95 (+56.5%)
      Volatility: 0.026
   📈 engineCoolantTemperatureMilliC:
      Current: 87096.05 → 30-day: 89413.56
      Change: +2317.52 (+2.7%)
      Volatility: 0.004

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine load increasing or becoming unstable
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 10/34: 1M2AV04C2EM011457
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AV04C2EM011457...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 2 outliers from engineLoadPercent
   ✅ Created multivariate series: 314 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=76623.88, σ=18997.29
   📊 engineLoadPercent: μ=43.79, σ=6.55
   📊 engineCoolantTemperatureMilliC: μ=65269.95, σ=25349.96

📈 Analyzing sensor correlations for vehicle 1M2AV04C2EM011457...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AV04C2EM011457...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.014)
   ✅ engineLoadPercent stationary (p=0.000)
   ✅ engineCoolantTemperatureMilliC stationary (p=0.000)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AV04C2EM011457...
   🔧 Days since last maintenance: 508
   📈 defLevelMilliPercent:
      Current: 98421.79 → 30-day: 77894.07
      Change: -20527.72 (-20.9%)
      Volatility: 0.042
   📈 engineLoadPercent:
      Current: 42.55 → 30-day: 43.96
      Change: +1.41 (+3.3%)
      Volatility: 0.008
   📈 engineCoolantTemperatureMilliC:
      Current: 89996.12 → 30-day: 65162.07
      Change: -24834.05 (-27.6%)
      Volatility: 0.066

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • DEF system showing significant decline
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 11/34: 1M2GR4GC7NM025968
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2GR4GC7NM025968...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 22 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 547 days, 3 sensors
   📅 Date range: 2023-04-06 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=73277.92, σ=17631.16
   📊 engineLoadPercent: μ=36.83, σ=6.23
   📊 engineCoolantTemperatureMilliC: μ=82748.86, σ=3038.39

📈 Analyzing sensor correlations for vehicle 1M2GR4GC7NM025968...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2GR4GC7NM025968...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.010)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.296), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 8
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2GR4GC7NM025968...
   🔧 Days since last maintenance: 491
   📈 defLevelMilliPercent:
      Current: 35865.00 → 30-day: 71655.74
      Change: +35790.74 (+99.8%)
      Volatility: 0.045
   📈 engineLoadPercent:
      Current: 31.07 → 30-day: 35.81
      Change: +4.74 (+15.3%)
      Volatility: 0.023
   📈 engineCoolantTemperatureMilliC:
      Current: 84246.75 → 30-day: 84293.28
      Change: +46.53 (+0.1%)
      Volatility: 0.002

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • DEF system showing significant decline
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 12/34: 1M2AX07C9CM010731
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AX07C9CM010731...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 4 outliers from engineLoadPercent
   🗑️ Removed 27 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 259 days, 3 sensors
   📅 Date range: 2023-11-15 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=78991.46, σ=14558.70
   📊 engineLoadPercent: μ=31.13, σ=4.87
   📊 engineCoolantTemperatureMilliC: μ=76400.21, σ=4149.13

📈 Analyzing sensor correlations for vehicle 1M2AX07C9CM010731...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AX07C9CM010731...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   ✅ engineCoolantTemperatureMilliC stationary (p=0.000)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 2
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AX07C9CM010731...
   🔧 Days since last maintenance: 471
   📈 defLevelMilliPercent:
      Current: 85490.67 → 30-day: 79115.65
      Change: -6375.02 (-7.5%)
      Volatility: 0.009
   📈 engineLoadPercent:
      Current: 33.73 → 30-day: 31.19
      Change: -2.54 (-7.5%)
      Volatility: 0.006
   📈 engineCoolantTemperatureMilliC:
      Current: 82045.25 → 30-day: 76394.99
      Change: -5650.26 (-6.9%)
      Volatility: 0.006

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 13/34: 1M2AV04C0JM018353
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AV04C0JM018353...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 8 outliers from engineLoadPercent
   🗑️ Removed 36 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 411 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-05 00:00:00
   📊 defLevelMilliPercent: μ=74805.04, σ=16725.58
   📊 engineLoadPercent: μ=36.62, σ=4.64
   📊 engineCoolantTemperatureMilliC: μ=82416.09, σ=7661.88

📈 Analyzing sensor correlations for vehicle 1M2AV04C0JM018353...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AV04C0JM018353...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   ✅ engineCoolantTemperatureMilliC stationary (p=0.003)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 6
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AV04C0JM018353...
   🔧 Days since last maintenance: 466
   📈 defLevelMilliPercent:
      Current: 74746.67 → 30-day: 74641.06
      Change: -105.60 (-0.1%)
      Volatility: 0.011
   📈 engineLoadPercent:
      Current: 43.02 → 30-day: 36.63
      Change: -6.39 (-14.9%)
      Volatility: 0.011
   📈 engineCoolantTemperatureMilliC:
      Current: 88602.51 → 30-day: 82478.08
      Change: -6124.43 (-6.9%)
      Volatility: 0.010

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 14/34: 1M2AX07C9BM009609
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AX07C9BM009609...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 2 outliers from engineLoadPercent
   🗑️ Removed 13 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 168 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2024-04-19 00:00:00
   📊 defLevelMilliPercent: μ=78857.11, σ=13912.54
   📊 engineLoadPercent: μ=31.97, σ=4.41
   📊 engineCoolantTemperatureMilliC: μ=77469.74, σ=8530.15

📈 Analyzing sensor correlations for vehicle 1M2AX07C9BM009609...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AX07C9BM009609...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.484), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 2
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AX07C9BM009609...
   🔧 Days since last maintenance: 444
   📈 defLevelMilliPercent:
      Current: 68400.00 → 30-day: 78151.01
      Change: +9751.01 (+14.3%)
      Volatility: 0.038
   📈 engineLoadPercent:
      Current: 41.67 → 30-day: 32.12
      Change: -9.55 (-22.9%)
      Volatility: 0.035
   📈 engineCoolantTemperatureMilliC:
      Current: 53281.47 → 30-day: 44675.61
      Change: -8605.86 (-16.2%)
      Volatility: 0.032

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 15/34: 1M2GR4GC3KM008161
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2GR4GC3KM008161...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 20 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 547 days, 3 sensors
   📅 Date range: 2023-04-04 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=72651.18, σ=18214.27
   📊 engineLoadPercent: μ=32.60, σ=8.51
   📊 engineCoolantTemperatureMilliC: μ=83351.18, σ=2868.73

📈 Analyzing sensor correlations for vehicle 1M2GR4GC3KM008161...
🔍 Cross-Sensor Correlations:
   🔗 engineLoadPercent & engineCoolantTemperatureMilliC: moderately positively correlated (+0.493)

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2GR4GC3KM008161...
   📊 Checking stationarity...
   🔄 defLevelMilliPercent non-stationary (p=0.067), applying differencing
   🔄 engineLoadPercent non-stationary (p=0.078), applying differencing
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.479), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 9
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2GR4GC3KM008161...
   🔧 Days since last maintenance: 364
   📈 defLevelMilliPercent:
      Current: 95061.87 → 30-day: 83022.17
      Change: -12039.70 (-12.7%)
      Volatility: 0.018
   📈 engineLoadPercent:
      Current: 35.44 → 30-day: 38.29
      Change: +2.85 (+8.1%)
      Volatility: 0.009
   📈 engineCoolantTemperatureMilliC:
      Current: 87973.80 → 30-day: 87334.35
      Change: -639.45 (-0.7%)
      Volatility: 0.002

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 16/34: 1XK1D40X1LJ409222
======================================================================

🔧 Preparing multivariate time series for vehicle 1XK1D40X1LJ409222...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 49 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 406 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=73602.83, σ=19410.42
   📊 engineLoadPercent: μ=42.44, σ=7.02
   📊 engineCoolantTemperatureMilliC: μ=81253.31, σ=3724.68

📈 Analyzing sensor correlations for vehicle 1XK1D40X1LJ409222...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1XK1D40X1LJ409222...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.017)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.206), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1XK1D40X1LJ409222...
   🔧 Days since last maintenance: 324
   📈 defLevelMilliPercent:
      Current: 87291.80 → 30-day: 75253.98
      Change: -12037.82 (-13.8%)
      Volatility: 0.095
   📈 engineLoadPercent:
      Current: 22.62 → 30-day: 41.88
      Change: +19.27 (+85.2%)
      Volatility: 0.094
   📈 engineCoolantTemperatureMilliC:
      Current: 79166.67 → 30-day: 80454.30
      Change: +1287.63 (+1.6%)
      Volatility: 0.007

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine load increasing or becoming unstable
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 17/34: 5KJJBWD17SLVV1910
======================================================================

🔧 Preparing multivariate time series for vehicle 5KJJBWD17SLVV1910...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 38 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 388 days, 3 sensors
   📅 Date range: 2023-04-01 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=67798.28, σ=17295.23
   📊 engineLoadPercent: μ=37.35, σ=12.15
   📊 engineCoolantTemperatureMilliC: μ=80419.79, σ=12010.68

📈 Analyzing sensor correlations for vehicle 5KJJBWD17SLVV1910...
🔍 Cross-Sensor Correlations:
   🔗 engineLoadPercent & engineCoolantTemperatureMilliC: moderately positively correlated (+0.623)

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 5KJJBWD17SLVV1910...
   📊 Checking stationarity...
   🔄 defLevelMilliPercent non-stationary (p=0.176), applying differencing
   ✅ engineLoadPercent stationary (p=0.038)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.056), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 9
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 5KJJBWD17SLVV1910...
   🔧 Days since last maintenance: 301
   📈 defLevelMilliPercent:
      Current: 68903.03 → 30-day: 73640.50
      Change: +4737.47 (+6.9%)
      Volatility: 0.026
   📈 engineLoadPercent:
      Current: 25.65 → 30-day: 34.99
      Change: +9.34 (+36.4%)
      Volatility: 0.054
   📈 engineCoolantTemperatureMilliC:
      Current: 87352.46 → 30-day: 93522.28
      Change: +6169.82 (+7.1%)
      Volatility: 0.021

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine load increasing or becoming unstable
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 18/34: 1M2AX07C7JM038332
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AX07C7JM038332...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 27 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 511 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=75058.85, σ=17712.23
   📊 engineLoadPercent: μ=29.03, σ=5.86
   📊 engineCoolantTemperatureMilliC: μ=79486.01, σ=5747.77

📈 Analyzing sensor correlations for vehicle 1M2AX07C7JM038332...
🔍 Cross-Sensor Correlations:
   🔗 engineLoadPercent & engineCoolantTemperatureMilliC: moderately positively correlated (+0.426)

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AX07C7JM038332...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.010)
   🔄 engineLoadPercent non-stationary (p=0.352), applying differencing
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.125), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 9
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AX07C7JM038332...
   🔧 Days since last maintenance: 245
   📈 defLevelMilliPercent:
      Current: 76848.13 → 30-day: 75056.72
      Change: -1791.40 (-2.3%)
      Volatility: 0.033
   📈 engineLoadPercent:
      Current: 24.94 → 30-day: 28.42
      Change: +3.48 (+14.0%)
      Volatility: 0.019
   📈 engineCoolantTemperatureMilliC:
      Current: 80483.70 → 30-day: 76175.44
      Change: -4308.26 (-5.4%)
      Volatility: 0.005

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 19/34: 1M2GR4GC3MM019664
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2GR4GC3MM019664...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 12 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 582 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-07 00:00:00
   📊 defLevelMilliPercent: μ=75096.19, σ=17902.48
   📊 engineLoadPercent: μ=27.47, σ=4.56
   📊 engineCoolantTemperatureMilliC: μ=81961.07, σ=2878.15

📈 Analyzing sensor correlations for vehicle 1M2GR4GC3MM019664...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2GR4GC3MM019664...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.010)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.178), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2GR4GC3MM019664...
   🔧 Days since last maintenance: 235
   📈 defLevelMilliPercent:
      Current: 93833.77 → 30-day: 75307.15
      Change: -18526.61 (-19.7%)
      Volatility: 0.067
   📈 engineLoadPercent:
      Current: 40.54 → 30-day: 27.61
      Change: -12.93 (-31.9%)
      Volatility: 0.037
   📈 engineCoolantTemperatureMilliC:
      Current: 88943.09 → 30-day: 84109.07
      Change: -4834.02 (-5.4%)
      Volatility: 0.002

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • DEF system showing significant decline
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 20/34: 1M2GR4GC1LM008158
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2GR4GC1LM008158...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 31 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 536 days, 3 sensors
   📅 Date range: 2023-04-01 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=72193.72, σ=17996.36
   📊 engineLoadPercent: μ=29.69, σ=5.62
   📊 engineCoolantTemperatureMilliC: μ=82371.98, σ=2891.05

📈 Analyzing sensor correlations for vehicle 1M2GR4GC1LM008158...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2GR4GC1LM008158...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   🔄 engineLoadPercent non-stationary (p=0.108), applying differencing
   ✅ engineCoolantTemperatureMilliC stationary (p=0.023)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 8
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2GR4GC1LM008158...
   🔧 Days since last maintenance: 225
   📈 defLevelMilliPercent:
      Current: 62617.59 → 30-day: 71604.21
      Change: +8986.61 (+14.4%)
      Volatility: 0.028
   📈 engineLoadPercent:
      Current: 25.13 → 30-day: 26.82
      Change: +1.69 (+6.7%)
      Volatility: 0.021
   📈 engineCoolantTemperatureMilliC:
      Current: 83751.02 → 30-day: 83133.29
      Change: -617.73 (-0.7%)
      Volatility: 0.004

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 21/34: 1M2GR4GC1KM008160
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2GR4GC1KM008160...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 21 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 545 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-07 00:00:00
   📊 defLevelMilliPercent: μ=76934.13, σ=16003.35
   📊 engineLoadPercent: μ=29.63, σ=6.77
   📊 engineCoolantTemperatureMilliC: μ=82678.76, σ=2988.06

📈 Analyzing sensor correlations for vehicle 1M2GR4GC1KM008160...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2GR4GC1KM008160...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.380), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2GR4GC1KM008160...
   🔧 Days since last maintenance: 192
   📈 defLevelMilliPercent:
      Current: 60033.23 → 30-day: 76855.07
      Change: +16821.84 (+28.0%)
      Volatility: 0.015
   📈 engineLoadPercent:
      Current: 25.27 → 30-day: 29.60
      Change: +4.34 (+17.2%)
      Volatility: 0.017
   📈 engineCoolantTemperatureMilliC:
      Current: 85085.60 → 30-day: 85158.44
      Change: +72.84 (+0.1%)
      Volatility: 0.003

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 22/34: 1M2TE2GC9KM002685
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2TE2GC9KM002685...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 4 outliers from defLevelMilliPercent
   🗑️ Removed 5 outliers from engineLoadPercent
   🗑️ Removed 38 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 466 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=85345.36, σ=12551.68
   📊 engineLoadPercent: μ=33.34, σ=3.06
   📊 engineCoolantTemperatureMilliC: μ=87231.17, σ=3277.60

📈 Analyzing sensor correlations for vehicle 1M2TE2GC9KM002685...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2TE2GC9KM002685...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.254), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 8
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2TE2GC9KM002685...
   🔧 Days since last maintenance: 126
   📈 defLevelMilliPercent:
      Current: 89889.94 → 30-day: 85265.57
      Change: -4624.37 (-5.1%)
      Volatility: 0.013
   📈 engineLoadPercent:
      Current: 33.15 → 30-day: 33.38
      Change: +0.23 (+0.7%)
      Volatility: 0.019
   📈 engineCoolantTemperatureMilliC:
      Current: 91075.86 → 30-day: 91443.77
      Change: +367.91 (+0.4%)
      Volatility: 0.004

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 23/34: 1M2AX07C0FM022481
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AX07C0FM022481...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 43 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 497 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-05 00:00:00
   📊 defLevelMilliPercent: μ=78082.35, σ=15874.47
   📊 engineLoadPercent: μ=32.66, σ=4.90
   📊 engineCoolantTemperatureMilliC: μ=81441.14, σ=3383.14

📈 Analyzing sensor correlations for vehicle 1M2AX07C0FM022481...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AX07C0FM022481...
   📊 Checking stationarity...
   🔄 defLevelMilliPercent non-stationary (p=0.135), applying differencing
   🔄 engineLoadPercent non-stationary (p=0.599), applying differencing
   ✅ engineCoolantTemperatureMilliC stationary (p=0.008)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 8
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AX07C0FM022481...
   🔧 Days since last maintenance: 115
   📈 defLevelMilliPercent:
      Current: 85913.92 → 30-day: 84334.00
      Change: -1579.92 (-1.8%)
      Volatility: 0.018
   📈 engineLoadPercent:
      Current: 25.54 → 30-day: 25.93
      Change: +0.39 (+1.5%)
      Volatility: 0.008
   📈 engineCoolantTemperatureMilliC:
      Current: 81521.24 → 30-day: 81708.45
      Change: +187.22 (+0.2%)
      Volatility: 0.002

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 24/34: 1M2TE2GC7KM002684
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2TE2GC7KM002684...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 3 outliers from defLevelMilliPercent
   🗑️ Removed 16 outliers from engineLoadPercent
   🗑️ Removed 39 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 442 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=81426.74, σ=6600.55
   📊 engineLoadPercent: μ=41.08, σ=3.25
   📊 engineCoolantTemperatureMilliC: μ=85338.82, σ=3768.71

📈 Analyzing sensor correlations for vehicle 1M2TE2GC7KM002684...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2TE2GC7KM002684...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.001)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.099), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2TE2GC7KM002684...
   🔧 Days since last maintenance: 115
   📈 defLevelMilliPercent:
      Current: 79380.97 → 30-day: 81276.92
      Change: +1895.95 (+2.4%)
      Volatility: 0.009
   📈 engineLoadPercent:
      Current: 39.82 → 30-day: 41.18
      Change: +1.36 (+3.4%)
      Volatility: 0.008
   📈 engineCoolantTemperatureMilliC:
      Current: 90363.92 → 30-day: 88327.09
      Change: -2036.84 (-2.3%)
      Volatility: 0.001

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 25/34: 1M2TE2GC3NM006624
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2TE2GC3NM006624...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 1 outliers from engineLoadPercent
   🗑️ Removed 27 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 517 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=83944.70, σ=9967.08
   📊 engineLoadPercent: μ=35.06, σ=4.65
   📊 engineCoolantTemperatureMilliC: μ=85552.00, σ=2978.46

📈 Analyzing sensor correlations for vehicle 1M2TE2GC3NM006624...
🔍 Cross-Sensor Correlations:
   🔗 defLevelMilliPercent & engineLoadPercent: moderately negatively correlated (-0.571)

🕒 Analyzing lead-lag relationships...
   ⏰ engineLoadPercent leads defLevelMilliPercent by 5 days (r=-0.409)
   ⏰ engineLoadPercent leads defLevelMilliPercent by 5 days (r=-0.409)

🤖 Building VAR model for vehicle 1M2TE2GC3NM006624...
   📊 Checking stationarity...
   🔄 defLevelMilliPercent non-stationary (p=0.367), applying differencing
   🔄 engineLoadPercent non-stationary (p=0.709), applying differencing
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.445), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 9
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2TE2GC3NM006624...
   🔧 Days since last maintenance: 87
   📈 defLevelMilliPercent:
      Current: 79495.53 → 30-day: 79653.39
      Change: +157.86 (+0.2%)
      Volatility: 0.012
   📈 engineLoadPercent:
      Current: 37.52 → 30-day: 39.31
      Change: +1.80 (+4.8%)
      Volatility: 0.034
   📈 engineCoolantTemperatureMilliC:
      Current: 88652.36 → 30-day: 86298.30
      Change: -2354.06 (-2.7%)
      Volatility: 0.005

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 26/34: 1XK1D40X1NJ495537
======================================================================

🔧 Preparing multivariate time series for vehicle 1XK1D40X1NJ495537...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 26 outliers from engineLoadPercent
   🗑️ Removed 13 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 506 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-05-16 00:00:00
   📊 defLevelMilliPercent: μ=63987.72, σ=17965.25
   📊 engineLoadPercent: μ=49.35, σ=5.34
   📊 engineCoolantTemperatureMilliC: μ=84756.03, σ=3795.29

📈 Analyzing sensor correlations for vehicle 1XK1D40X1NJ495537...
🔍 Cross-Sensor Correlations:
   🔗 engineLoadPercent & engineCoolantTemperatureMilliC: moderately positively correlated (+0.325)

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1XK1D40X1NJ495537...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.007)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.151), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 7
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1XK1D40X1NJ495537...
   🔧 Days since last maintenance: 79
   📈 defLevelMilliPercent:
      Current: 84770.18 → 30-day: 64042.10
      Change: -20728.07 (-24.5%)
      Volatility: 0.048
   📈 engineLoadPercent:
      Current: 44.01 → 30-day: 49.23
      Change: +5.22 (+11.8%)
      Volatility: 0.013
   📈 engineCoolantTemperatureMilliC:
      Current: 84478.95 → 30-day: 82425.38
      Change: -2053.57 (-2.4%)
      Volatility: 0.007

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • DEF system showing significant decline
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 27/34: 1M2AV04C0JM019132
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AV04C0JM019132...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 30 outliers from defLevelMilliPercent
   🗑️ Removed 8 outliers from engineLoadPercent
   🗑️ Removed 49 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 472 days, 3 sensors
   📅 Date range: 2023-04-21 00:00:00 to 2025-06-05 00:00:00
   📊 defLevelMilliPercent: μ=90447.30, σ=5542.22
   📊 engineLoadPercent: μ=35.23, σ=3.51
   📊 engineCoolantTemperatureMilliC: μ=86177.09, σ=3113.41

📈 Analyzing sensor correlations for vehicle 1M2AV04C0JM019132...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AV04C0JM019132...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.318), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AV04C0JM019132...
   🔧 Days since last maintenance: 73
   📈 defLevelMilliPercent:
      Current: 87280.90 → 30-day: 90447.30
      Change: +3166.40 (+3.6%)
      Volatility: 0.002
   📈 engineLoadPercent:
      Current: 34.57 → 30-day: 35.24
      Change: +0.67 (+1.9%)
      Volatility: 0.007
   📈 engineCoolantTemperatureMilliC:
      Current: 89367.49 → 30-day: 89480.45
      Change: +112.96 (+0.1%)
      Volatility: 0.001

   🚨 System Risk Level: LOW
   ✅ Risk Assessment: LOW (0 factors)

======================================================================
📊 ANALYZING VEHICLE 28/34: 1M2GR4GC1MM019663
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2GR4GC1MM019663...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 1 outliers from engineLoadPercent
   🗑️ Removed 21 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 545 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=76594.97, σ=18266.20
   📊 engineLoadPercent: μ=27.21, σ=4.44
   📊 engineCoolantTemperatureMilliC: μ=82931.45, σ=2658.71

📈 Analyzing sensor correlations for vehicle 1M2GR4GC1MM019663...
🔍 Cross-Sensor Correlations:
   🔗 engineLoadPercent & engineCoolantTemperatureMilliC: moderately positively correlated (+0.378)

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2GR4GC1MM019663...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.001)
   🔄 engineLoadPercent non-stationary (p=0.185), applying differencing
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.323), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 9
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2GR4GC1MM019663...
   🔧 Days since last maintenance: 63
   📈 defLevelMilliPercent:
      Current: 59208.78 → 30-day: 76452.97
      Change: +17244.19 (+29.1%)
      Volatility: 0.031
   📈 engineLoadPercent:
      Current: 29.57 → 30-day: 26.91
      Change: -2.66 (-9.0%)
      Volatility: 0.018
   📈 engineCoolantTemperatureMilliC:
      Current: 86230.43 → 30-day: 84465.73
      Change: -1764.71 (-2.0%)
      Volatility: 0.002

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • DEF system showing significant decline
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 29/34: 1M2TE2GC5LM004211
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2TE2GC5LM004211...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 6 outliers from defLevelMilliPercent
   🗑️ Removed 43 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 544 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=85835.24, σ=6264.54
   📊 engineLoadPercent: μ=42.20, σ=4.08
   📊 engineCoolantTemperatureMilliC: μ=87541.20, σ=3395.66

📈 Analyzing sensor correlations for vehicle 1M2TE2GC5LM004211...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2TE2GC5LM004211...
   📊 Checking stationarity...
   🔄 defLevelMilliPercent non-stationary (p=0.067), applying differencing
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.492), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 10
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2TE2GC5LM004211...
   🔧 Days since last maintenance: 59
   📈 defLevelMilliPercent:
      Current: 77521.88 → 30-day: 81961.40
      Change: +4439.52 (+5.7%)
      Volatility: 0.008
   📈 engineLoadPercent:
      Current: 41.60 → 30-day: 42.19
      Change: +0.59 (+1.4%)
      Volatility: 0.009
   📈 engineCoolantTemperatureMilliC:
      Current: 91513.81 → 30-day: 91728.65
      Change: +214.84 (+0.2%)
      Volatility: 0.002

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 30/34: 1M2TE2GC0PM009077
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2TE2GC0PM009077...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 9 outliers from defLevelMilliPercent
   🗑️ Removed 2 outliers from engineLoadPercent
   🗑️ Removed 14 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 501 days, 3 sensors
   📅 Date range: 2023-05-16 00:00:00 to 2025-06-05 00:00:00
   📊 defLevelMilliPercent: μ=82125.74, σ=4928.80
   📊 engineLoadPercent: μ=39.79, σ=3.98
   📊 engineCoolantTemperatureMilliC: μ=85817.18, σ=3374.97

📈 Analyzing sensor correlations for vehicle 1M2TE2GC0PM009077...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2TE2GC0PM009077...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   🔄 engineLoadPercent non-stationary (p=0.099), applying differencing
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.563), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 10
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2TE2GC0PM009077...
   🔧 Days since last maintenance: 37
   📈 defLevelMilliPercent:
      Current: 79459.66 → 30-day: 81861.78
      Change: +2402.12 (+3.0%)
      Volatility: 0.011
   📈 engineLoadPercent:
      Current: 43.34 → 30-day: 41.58
      Change: -1.75 (-4.0%)
      Volatility: 0.008
   📈 engineCoolantTemperatureMilliC:
      Current: 90214.55 → 30-day: 89288.37
      Change: -926.18 (-1.0%)
      Volatility: 0.006

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 31/34: 1M2TE2GC7LM004212
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2TE2GC7LM004212...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 11 outliers from defLevelMilliPercent
   🗑️ Removed 37 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 431 days, 3 sensors
   📅 Date range: 2023-04-11 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=84870.61, σ=4898.45
   📊 engineLoadPercent: μ=38.70, σ=3.40
   📊 engineCoolantTemperatureMilliC: μ=87981.28, σ=3158.90

📈 Analyzing sensor correlations for vehicle 1M2TE2GC7LM004212...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2TE2GC7LM004212...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.023)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.326), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2TE2GC7LM004212...
   🔧 Days since last maintenance: 35
   📈 defLevelMilliPercent:
      Current: 81911.84 → 30-day: 84890.99
      Change: +2979.15 (+3.6%)
      Volatility: 0.004
   📈 engineLoadPercent:
      Current: 38.80 → 30-day: 38.70
      Change: -0.10 (-0.3%)
      Volatility: 0.011
   📈 engineCoolantTemperatureMilliC:
      Current: 92403.91 → 30-day: 91831.13
      Change: -572.78 (-0.6%)
      Volatility: 0.002

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 32/34: 5KJJBWD10RLVC7924
======================================================================

🔧 Preparing multivariate time series for vehicle 5KJJBWD10RLVC7924...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 32 outliers from engineLoadPercent
   🗑️ Removed 15 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 391 days, 3 sensors
   📅 Date range: 2023-09-14 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=68191.32, σ=17821.61
   📊 engineLoadPercent: μ=46.78, σ=5.43
   📊 engineCoolantTemperatureMilliC: μ=89769.00, σ=4051.85

📈 Analyzing sensor correlations for vehicle 5KJJBWD10RLVC7924...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 5KJJBWD10RLVC7924...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.000)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.387), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 6
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 5KJJBWD10RLVC7924...
   🔧 Days since last maintenance: 29
   📈 defLevelMilliPercent:
      Current: 68790.20 → 30-day: 68095.37
      Change: -694.82 (-1.0%)
      Volatility: 0.031
   📈 engineLoadPercent:
      Current: 31.93 → 30-day: 46.75
      Change: +14.82 (+46.4%)
      Volatility: 0.020
   📈 engineCoolantTemperatureMilliC:
      Current: 90163.27 → 30-day: 97168.56
      Change: +7005.29 (+7.8%)
      Volatility: 0.005

   🚨 System Risk Level: HIGH
   ⚠️ Risk Factors:
      • Engine load increasing or becoming unstable
      • Engine temperature rising concern
   ✅ Risk Assessment: HIGH (2 factors)

======================================================================
📊 ANALYZING VEHICLE 33/34: 1M2TE2GCXNM006622
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2TE2GCXNM006622...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 15 outliers from defLevelMilliPercent
   🗑️ Removed 11 outliers from engineLoadPercent
   🗑️ Removed 26 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 505 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-06 00:00:00
   📊 defLevelMilliPercent: μ=90308.34, σ=4011.51
   📊 engineLoadPercent: μ=37.24, σ=3.02
   📊 engineCoolantTemperatureMilliC: μ=87246.35, σ=3318.42

📈 Analyzing sensor correlations for vehicle 1M2TE2GCXNM006622...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2TE2GCXNM006622...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.004)
   ✅ engineLoadPercent stationary (p=0.001)
   🔄 engineCoolantTemperatureMilliC non-stationary (p=0.599), applying differencing
   🔧 Fitting VAR model...
   📈 Optimal lag order: 6
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2TE2GCXNM006622...
   🔧 Days since last maintenance: 29
   📈 defLevelMilliPercent:
      Current: 88604.18 → 30-day: 90359.26
      Change: +1755.08 (+2.0%)
      Volatility: 0.003
   📈 engineLoadPercent:
      Current: 33.84 → 30-day: 37.20
      Change: +3.36 (+9.9%)
      Volatility: 0.013
   📈 engineCoolantTemperatureMilliC:
      Current: 90321.64 → 30-day: 89930.03
      Change: -391.60 (-0.4%)
      Volatility: 0.004

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

======================================================================
📊 ANALYZING VEHICLE 34/34: 1M2AV04C9JM018352
======================================================================

🔧 Preparing multivariate time series for vehicle 1M2AV04C9JM018352...
   🎯 Sensors: defLevelMilliPercent, engineLoadPercent, engineCoolantTemperatureMilliC
   🗑️ Removed 7 outliers from defLevelMilliPercent
   🗑️ Removed 2 outliers from engineLoadPercent
   🗑️ Removed 51 outliers from engineCoolantTemperatureMilliC
   ✅ Created multivariate series: 451 days, 3 sensors
   📅 Date range: 2023-04-03 00:00:00 to 2025-06-07 00:00:00
   📊 defLevelMilliPercent: μ=86774.58, σ=10937.17
   📊 engineLoadPercent: μ=39.47, σ=3.72
   📊 engineCoolantTemperatureMilliC: μ=85887.33, σ=3854.63

📈 Analyzing sensor correlations for vehicle 1M2AV04C9JM018352...
🔍 Cross-Sensor Correlations:

🕒 Analyzing lead-lag relationships...

🤖 Building VAR model for vehicle 1M2AV04C9JM018352...
   📊 Checking stationarity...
   ✅ defLevelMilliPercent stationary (p=0.000)
   ✅ engineLoadPercent stationary (p=0.006)
   ✅ engineCoolantTemperatureMilliC stationary (p=0.002)
   🔧 Fitting VAR model...
   📈 Optimal lag order: 5
   🔮 Generating 30-day forecasts...
   ✅ VAR model successfully fitted and forecast generated

📊 Analyzing multivariate forecasts for vehicle 1M2AV04C9JM018352...
   🔧 Days since last maintenance: 23
   📈 defLevelMilliPercent:
      Current: 88764.67 → 30-day: 86842.67
      Change: -1922.01 (-2.2%)
      Volatility: 0.009
   📈 engineLoadPercent:
      Current: 47.54 → 30-day: 39.61
      Change: -7.93 (-16.7%)
      Volatility: 0.009
   📈 engineCoolantTemperatureMilliC:
      Current: 90262.57 → 30-day: 86065.66
      Change: -4196.91 (-4.6%)
      Volatility: 0.008

   🚨 System Risk Level: MODERATE
   ⚠️ Risk Factors:
      • Engine temperature rising concern
   ✅ Risk Assessment: MODERATE (1 factors)

🎉 COMPREHENSIVE FLEET MULTIVARIATE ANALYSIS COMPLETE!
======================================================================
📊 Analysis Results: 33/34 vehicles successfully analyzed

🏭 FLEET-WIDE RISK ASSESSMENT SUMMARY
=================================================================
📊 Fleet Risk Distribution (33 vehicles analyzed):
   🚨 HIGH Risk: 2 vehicles (6.1%)
   ⚠️ MODERATE Risk: 20 vehicles (60.6%)
   ✅ LOW Risk: 11 vehicles (33.3%)

🔧 Maintenance Status:
   🔴 Overdue (>365 days): 13 vehicles
   🟡 Due Soon (180-365 days): 7 vehicles
   🟢 Recent (<180 days): 13 vehicles

🚨 TOP 10 HIGHEST RISK VEHICLES - IMMEDIATE ACTION REQUIRED:
Rank VIN               Risk     Days Since Maint Primary Concerns
---- ----------------- -------- --------------- --------------------------------------------------
1    1XKWD40X6FJ436975 🚨 HIGH   756             DEF system showing significant decline
2    5KJJBWD10RLVC7924 🚨 HIGH   29              Engine load increasing or becoming unstable
3    5KJJAED19GPHF6382 ⚠️ MODERATE 751             DEF system showing significant decline
4    1M2TE2GC7LM004209 ⚠️ MODERATE 744             Engine temperature rising concern
5    1M2AX07C9FM022480 ⚠️ MODERATE 616             Engine load increasing or becoming unstable
6    1M2AV04C3HM015506 ⚠️ MODERATE 547             Engine temperature rising concern
7    1M2AV04C5HM015507 ⚠️ MODERATE 539             Engine temperature rising concern
8    1XK1D40X8LJ409220 ⚠️ MODERATE 512             Engine load increasing or becoming unstable
9    1M2AV04C2EM011457 ⚠️ MODERATE 508             DEF system showing significant decline
10   1M2GR4GC7NM025968 ⚠️ MODERATE 491             DEF system showing significant decline

📈 Fleet-Wide Degradation Patterns:
   Most Common Issues Across Fleet:
   • Engine temperature rising concern: 12 vehicles (36.4%)
   • DEF system showing significant decline: 7 vehicles (21.2%)
   • Engine load increasing or becoming unstable: 6 vehicles (18.2%)

💰 Business Impact Assessment:
   🚨 Potential breakdown costs: $38,000
   🔧 Preventive maintenance costs: $26,400
   💵 Potential savings with action: $11,600
   📊 ROI of predictive maintenance: 44%

💡 Key Insights from Fleet-Wide Multivariate Analysis:
   🔗 Sensor interactions reveal system-level degradation patterns across fleet
   📈 VAR models capture cross-sensor relationships missed by univariate analysis
   🎯 System-level risk assessment provides holistic fleet health view
   🏭 Fleet-wide patterns identify common maintenance issues and priorities

📋 Immediate Action Items:
   🚨 URGENT: Schedule immediate maintenance for 2 HIGH risk vehicles
   ⚠️ PRIORITY: Implement enhanced monitoring for 20 MODERATE risk vehicles
   📈 STRATEGIC: Use fleet patterns to optimize maintenance scheduling
   💰 FINANCIAL: Implement predictive maintenance to achieve estimated ROI

📋 Next Analysis Steps:
   1. Threshold-based RUL predictions using forecasted trends (Script 3)
   2. Hierarchical forecasting by vehicle type/model (Script 4)
   3. Advanced RUL with survival analysis concepts (Script 5)
