#!/usr/bin/env python3
"""
Explainable DPF Remaining Useful Life (RUL) Analysis

This script demonstrates how to predict when a vehicle's DPF (Diesel Particulate Filter) 
will need maintenance using explainable time-series analysis.

Key Features:
- Builds interpretable time-series features that fleet managers can understand
- Creates explainable RUL models using simple, actionable metrics
- Identifies early warning signals for proactive maintenance
- Provides clear, actionable warnings based on explainable features

Author: Generated from Jupyter notebook analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')

# Set up plotting
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)


def load_dpf_datasets():
    """Load and prepare the DPF datasets."""
    print("📊 Loading DPF datasets...")
    
    try:
        maintenance_df = pd.read_csv('data/dpf_maintenance_records.csv')
        
        # Load and combine both vehicle stats files for expanded dataset (2023-2025)
        print("🔄 Loading vehicle stats from multiple years...")
        sensor_df_2024 = pd.read_csv('data/dpf_vehicle_stats.csv')
        sensor_df_2023 = pd.read_csv('data/vehicle_stats_23-24.csv')
        
        # Combine the datasets and remove duplicates
        sensor_df = pd.concat([sensor_df_2023, sensor_df_2024], ignore_index=True)
        
        # Remove duplicates based on time and vin to avoid double-counting
        initial_rows = len(sensor_df)
        sensor_df = sensor_df.drop_duplicates(subset=['time', 'vin'], keep='first')
        duplicates_removed = initial_rows - len(sensor_df)
        
        if duplicates_removed > 0:
            print(f"   🗑️ Removed {duplicates_removed:,} duplicate records")
        
        diagnostic_df = pd.read_csv('data/dpf_diagnostic_data.csv')
        
        print(f"✅ Maintenance records: {len(maintenance_df):,} events")
        print(f"✅ Sensor readings (combined 2023-2025): {len(sensor_df):,} data points")
        print(f"   └─ 2023-2024 data: {len(sensor_df_2023):,} points")
        print(f"   └─ 2024-2025 data: {len(sensor_df_2024):,} points")
        print(f"✅ Diagnostic readings: {len(diagnostic_df):,} measurements")
        
        # Convert time columns and inspect data quality
        maintenance_df['Date of Issue'] = pd.to_datetime(maintenance_df['Date of Issue'])
        sensor_df['time'] = pd.to_datetime(sensor_df['time']).dt.tz_localize(None)
        diagnostic_df['Time'] = pd.to_datetime(diagnostic_df['Time'], errors='coerce').dt.tz_localize(None)
        
        print("\n📅 Data Time Ranges:")
        print(f"   Maintenance: {maintenance_df['Date of Issue'].min()} to {maintenance_df['Date of Issue'].max()}")
        print(f"   Sensors: {sensor_df['time'].min()} to {sensor_df['time'].max()}")
        print(f"   Diagnostics: {diagnostic_df['Time'].min()} to {diagnostic_df['Time'].max()}")
        
        # Check data overlap
        maintenance_vins = set(maintenance_df['VIN Number'].unique())
        sensor_vins = set(sensor_df['vin'].unique())
        overlap_vins = maintenance_vins.intersection(sensor_vins)
        
        print(f"\n🔗 Data Integration:")
        print(f"   VINs in both maintenance & sensor data: {len(overlap_vins)}")
        
        return maintenance_df, sensor_df, diagnostic_df
        
    except FileNotFoundError:
        print("❌ Processed data not found. Please ensure DPF datasets are available")
        raise


def create_backtrack_rul_labels(maintenance_df, lookback_days=[7, 15, 30, 45, 60]):
    """
    Create RUL labels by backtracking from each maintenance event.
    This generates much more training data than consecutive event pairs.
    
    For each maintenance event, we create multiple RUL examples:
    - 7 days before: RUL = 7 days (CRITICAL)
    - 15 days before: RUL = 15 days (HIGH)
    - 30 days before: RUL = 30 days (MEDIUM)
    - 45 days before: RUL = 45 days (LOW)
    - 60 days before: RUL = 60 days (NORMAL)
    """
    rul_data = []
    
    print(f"🔄 Creating backtrack RUL labels with lookback periods: {lookback_days}")
    
    total_events = len(maintenance_df)
    successful_labels = 0
    
    for idx, event in maintenance_df.iterrows():
        vehicle_num = event['Vehicle_Number']
        maintenance_date = event['Date of Issue']
        
        # Get all maintenance events for this vehicle to check for interference
        vehicle_maintenance = maintenance_df[
            maintenance_df['Vehicle_Number'] == vehicle_num
        ].sort_values('Date of Issue')
        
        for days_back in lookback_days:
            prediction_date = maintenance_date - timedelta(days=days_back)
            
            # Check if there are any maintenance events between prediction_date and maintenance_date
            interfering_events = vehicle_maintenance[
                (vehicle_maintenance['Date of Issue'] > prediction_date) &
                (vehicle_maintenance['Date of Issue'] < maintenance_date)
            ]
            
            # Only create RUL label if there's a clean window (no interfering maintenance)
            if len(interfering_events) == 0:
                # Assign RUL category labels
                if days_back <= 7:
                    rul_category = 'CRITICAL'
                elif days_back <= 15:
                    rul_category = 'HIGH'
                elif days_back <= 30:
                    rul_category = 'MEDIUM'
                elif days_back <= 45:
                    rul_category = 'LOW'
                else:
                    rul_category = 'NORMAL'
                
                rul_entry = {
                    'vehicle_number': vehicle_num,
                    'vin': event['VIN Number'],
                    'prediction_date': prediction_date,
                    'maintenance_date': maintenance_date,
                    'rul_days': days_back,
                    'rul_category': rul_category,
                    'maintenance_type': event['lines_jobDescriptions'],
                    'maintenance_cost': event.get('Total_Cost', 0),
                    'downtime_days': event.get('Downtime Days', 0)
                }
                
                rul_data.append(rul_entry)
                successful_labels += 1
        
        if (idx + 1) % 20 == 0:
            print(f"   Processed {idx + 1}/{total_events} maintenance events")
    
    rul_df = pd.DataFrame(rul_data)
    
    print(f"\n✅ Backtrack RUL Generation Results:")
    print(f"   Total maintenance events: {total_events}")
    print(f"   Total RUL labels created: {len(rul_df)}")
    print(f"   Average labels per event: {len(rul_df)/total_events:.1f}")
    
    return rul_df


def calculate_explainable_features(sensor_data, window_days=30):
    """
    Calculate explainable time-series features for RUL prediction.
    These features are designed to be interpretable by fleet managers.
    """
    features = {}
    
    # Expanded sensors for comprehensive DPF health monitoring
    key_sensors = [
        # Engine Performance Metrics
        'engineLoadPercent', 'engineRpm', 'ecuSpeedMph',
        'engineOilPressureKPa', 'engineCoolantTemperatureMilliC',
        
        # Fuel & Emissions System
        'defLevelMilliPercent', 'fuelPercents',
        
        # Environmental & Operational
        'ambientAirTemperatureMilliC', 'intakeManifoldTemperatureMilliC',
        'barometricPressurePa', 'obdEngineSeconds',
        
        # Distance & Usage Patterns
        'gpsDistanceMeters',
        
        # Additional diagnostic parameters that may be available
        'exhaustTemperature', 'dpfPressureDifferential', 'sootLevel',
        'regenCycles', 'turbochargerPressure', 'airFlowMass'
    ]
    
    for sensor in key_sensors:
        if sensor not in sensor_data.columns:
            continue
            
        values = sensor_data[sensor].dropna()
        if len(values) < 3:  # Need minimum data points
            continue
            
        # 1. TREND ANALYSIS FEATURES (Easy to explain)
        
        # Linear trend slope (positive = increasing, negative = decreasing)
        x = np.arange(len(values))
        if len(values) > 1:
            try:
                slope = np.polyfit(x, values, 1)[0]
                features[f'{sensor}_trend_slope'] = slope
            except:
                features[f'{sensor}_trend_slope'] = 0.0
        
        # Trend strength (R-squared of linear fit)
        if len(values) > 2:
            try:
                correlation = np.corrcoef(x, values)[0, 1] ** 2
                if np.isfinite(correlation):
                    features[f'{sensor}_trend_strength'] = correlation
            except:
                pass
        
        # Volatility (coefficient of variation)
        if values.mean() != 0 and values.std() > 0:
            cv = values.std() / abs(values.mean())
            features[f'{sensor}_volatility'] = cv
        
        # 2. THRESHOLD-BASED FEATURES (Actionable alerts)
        
        # Define sensor-specific thresholds (based on operational knowledge)
        thresholds = {
            # Engine Performance
            'engineLoadPercent': {'high': 80, 'low': 10},
            'engineRpm': {'high': 2000, 'low': 500},
            'ecuSpeedMph': {'high': 70, 'low': 5},
            
            # Fluid Systems
            'defLevelMilliPercent': {'high': 95000, 'low': 50000},
            'fuelPercents': {'high': 95, 'low': 25},
            'engineOilPressureKPa': {'high': 500, 'low': 200},
            
            # Temperature Systems
            'engineCoolantTemperatureMilliC': {'high': 95000, 'low': 70000},
            'ambientAirTemperatureMilliC': {'high': 40000, 'low': -10000},
            'intakeManifoldTemperatureMilliC': {'high': 60000, 'low': 15000},
            
            # Pressure & Environmental
            'barometricPressurePa': {'high': 102000, 'low': 98000},
            
            # Usage Patterns
            'obdEngineSeconds': {'high': 36000, 'low': 3600}  # 10 hours to 1 hour daily
        }
        
        if sensor in thresholds:
            high_thresh = thresholds[sensor]['high']
            low_thresh = thresholds[sensor]['low']
            
            # Percentage of time above/below thresholds
            pct_high = (values > high_thresh).mean() * 100
            pct_low = (values < low_thresh).mean() * 100
            
            features[f'{sensor}_pct_time_high'] = pct_high
            features[f'{sensor}_pct_time_low'] = pct_low
        
        # 3. OPERATIONAL PATTERN FEATURES
        
        # Recent vs historical comparison (last 25% vs first 75%)
        split_point = max(1, int(len(values) * 0.75))
        if split_point > 0 and split_point < len(values):
            historical_mean = values[:split_point].mean()
            recent_mean = values[split_point:].mean()
            
            if historical_mean != 0 and np.isfinite(historical_mean) and np.isfinite(recent_mean):
                pattern_change = (recent_mean - historical_mean) / abs(historical_mean) * 100
                features[f'{sensor}_pattern_change_pct'] = pattern_change
    
    # Add basic features if no sensor-specific features were found
    if not features:
        # Add basic data availability features
        features['data_availability'] = len(sensor_data) / max(1, window_days)
        features['sensor_count'] = sum(1 for sensor in key_sensors if sensor in sensor_data.columns and sensor_data[sensor].notna().any())
    
    return features


def build_rul_dataset(rul_df, sensor_df, window_days=30):
    """
    Build RUL dataset with explainable features.
    For each RUL example, extract features from sensor data before the maintenance event.
    """
    rul_features = []
    
    print(f"🔄 Processing {len(rul_df)} RUL examples...")
    
    successful_extractions = 0
    
    for idx, row in rul_df.iterrows():
        try:
            vin = row['vin']
            prediction_date = row['prediction_date']
            rul_days = row['rul_days']
            
            # Extract sensor data from BEFORE the prediction date to avoid data leakage
            feature_end_date = prediction_date
            feature_start_date = prediction_date - timedelta(days=window_days)
            
            vehicle_sensors = sensor_df[
                (sensor_df['vin'] == vin) &
                (sensor_df['time'] >= feature_start_date) &
                (sensor_df['time'] < feature_end_date)
            ].copy()
            
            if len(vehicle_sensors) < 5:  # Need minimum data
                continue
            
            # Calculate explainable features
            features = calculate_explainable_features(vehicle_sensors, window_days)
            
            # Add metadata
            features['vehicle_number'] = row['vehicle_number']
            features['vin'] = vin
            features['prediction_date'] = prediction_date
            features['maintenance_date'] = row['maintenance_date']
            features['rul_days'] = rul_days
            features['rul_category'] = row['rul_category']
            features['maintenance_type'] = row['maintenance_type']
            features['data_points'] = len(vehicle_sensors)
            features['window_days'] = window_days
            
            rul_features.append(features)
            successful_extractions += 1
            
            if (idx + 1) % 50 == 0:
                print(f"   Processed {idx + 1}/{len(rul_df)} examples ({successful_extractions} successful)")
                
        except Exception as e:
            continue
    
    if successful_extractions == 0:
        print("❌ No successful feature extractions. Check sensor data availability.")
        return pd.DataFrame()
    
    result_df = pd.DataFrame(rul_features)
    print(f"\n✅ Successfully created RUL dataset with {len(result_df)} examples")
    print(f"📊 Success rate: {len(result_df)}/{len(rul_df)} ({len(result_df)/len(rul_df):.1%})")
    print(f"🎯 RUL range: {result_df['rul_days'].min()}-{result_df['rul_days'].max()} days")
    
    return result_df


def build_explainable_rul_model(rul_feature_df, max_features=5):
    """
    Build an explainable RUL prediction model using only the most important features.
    """
    # Select feature columns
    feature_cols = [col for col in rul_feature_df.columns if col.endswith((
        '_trend_slope', '_volatility', '_pct_time_high', '_pct_time_low', '_pattern_change_pct'
    ))]
    
    if len(feature_cols) == 0:
        print("❌ No explainable features found!")
        return None, None, None
    
    # Prepare data
    X = rul_feature_df[feature_cols].fillna(0)  # Fill missing with 0 (no change)
    y = rul_feature_df['rul_days']
    
    # Remove outliers (RUL > 365 days is likely data quality issue)
    mask = y <= 365
    X = X[mask]
    y = y[mask]
    
    if len(X) < 10:
        print("❌ Insufficient data for modeling!")
        return None, None, None
    
    print(f"📊 Building model with {len(X)} examples and {len(feature_cols)} features")
    
    # Select top features based on correlation
    correlations = X.corrwith(y).abs().sort_values(ascending=False)
    top_features = correlations.head(max_features).index.tolist()
    
    print(f"\n🎯 Selected Top {len(top_features)} Explainable Features:")
    for i, feature in enumerate(top_features):
        corr = correlations[feature]
        print(f"   {i+1}. {feature}: {corr:.3f} correlation")
    
    # Train model with selected features
    X_selected = X[top_features]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_selected, y, test_size=0.3, random_state=42
    )
    
    # Scale features for interpretability
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    print(f"\n📈 Model Performance:")
    print(f"   Training MAE: {train_mae:.1f} days")
    print(f"   Testing MAE: {test_mae:.1f} days")
    print(f"   Training R²: {train_r2:.3f}")
    print(f"   Testing R²: {test_r2:.3f}")
    
    # Show feature importance (coefficients)
    print(f"\n🔍 Feature Importance (How Each Factor Affects RUL):")
    for feature, coef in zip(top_features, model.coef_):
        direction = "↗️ Increases" if coef > 0 else "↘️ Decreases"
        print(f"   {feature}: {direction} RUL by {abs(coef):.1f} days per unit")
    
    return model, scaler, top_features


def analyze_explainable_features(rul_feature_df):
    """Analyze and visualize the most explainable features."""
    feature_cols = [col for col in rul_feature_df.columns if col.endswith((
        '_trend_slope', '_volatility', '_pct_time_high', '_pct_time_low', '_pattern_change_pct'
    ))]

    if len(feature_cols) > 0:
        print("🔍 Analyzing Explainable Features...")
        
        # Correlation with RUL
        correlations = rul_feature_df[feature_cols + ['rul_days']].corr()['rul_days'].drop('rul_days')
        correlations = correlations.sort_values(key=abs, ascending=False)
        
        print(f"\n📈 Top 10 Features Most Predictive of RUL:")
        for i, (feature, corr) in enumerate(correlations.head(10).items()):
            sensor = feature.split('_')[0]
            metric = '_'.join(feature.split('_')[1:])
            
            # Explain what this feature means
            if 'trend_slope' in metric:
                explanation = "📈 Trend direction (positive=increasing, negative=decreasing)"
            elif 'volatility' in metric:
                explanation = "📊 Stability (higher=more erratic readings)"
            elif 'pct_time_high' in metric:
                explanation = "⚠️ Time spent above normal thresholds (%)"
            elif 'pct_time_low' in metric:
                explanation = "⬇️ Time spent below normal thresholds (%)"
            elif 'pattern_change' in metric:
                explanation = "🔄 Recent vs historical behavior change (%)"
            else:
                explanation = "📊 Operational metric"
                
            print(f"   {i+1}. {sensor} - {explanation}")
            print(f"      Correlation: {corr:+.3f} (stronger = more predictive)")
            print()

        # Create comprehensive visualization suite
        if len(correlations) > 0:
            # 1. RUL Distribution by Category
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Enhanced RUL Analysis: Distribution, Patterns & Insights', fontsize=16)
            
            # Plot 1: RUL Distribution by Category
            ax1 = axes[0, 0]
            rul_categories = rul_feature_df['rul_category'].value_counts().sort_index()
            colors = ['#ff4444', '#ff8800', '#ffcc00', '#88dd00', '#00dd88']
            bars = ax1.bar(rul_categories.index, rul_categories.values, color=colors)
            ax1.set_title('RUL Distribution by Risk Category')
            ax1.set_ylabel('Number of Examples')
            ax1.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{int(height)}', ha='center', va='bottom')
            
            # Plot 2: RUL Days Histogram
            ax2 = axes[0, 1]
            ax2.hist(rul_feature_df['rul_days'], bins=20, alpha=0.7, color='steelblue', edgecolor='black')
            ax2.axvline(rul_feature_df['rul_days'].mean(), color='red', linestyle='--', 
                       label=f'Mean: {rul_feature_df["rul_days"].mean():.1f} days')
            ax2.set_title('RUL Days Distribution')
            ax2.set_xlabel('Days Until Maintenance')
            ax2.set_ylabel('Frequency')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Plot 3: Feature Correlation Heatmap (Top 10)
            ax3 = axes[0, 2]
            top_10_features = correlations.head(10).index
            if len(top_10_features) > 1:
                corr_matrix = rul_feature_df[list(top_10_features) + ['rul_days']].corr()
                im = ax3.imshow(corr_matrix.values, cmap='RdBu_r', vmin=-1, vmax=1)
                ax3.set_xticks(range(len(corr_matrix.columns)))
                ax3.set_yticks(range(len(corr_matrix.columns)))
                ax3.set_xticklabels([col.split('_')[0][:8] for col in corr_matrix.columns], rotation=45)
                ax3.set_yticklabels([col.split('_')[0][:8] for col in corr_matrix.columns])
                ax3.set_title('Feature Correlation Heatmap')
                plt.colorbar(im, ax=ax3, shrink=0.8)
            
            # Plot 4-6: Top 3 Feature Relationships with Binned Analysis
            top_3_features = correlations.head(3).index
            
            for i, feature in enumerate(top_3_features):
                ax = axes[1, i]
                
                # Create binned analysis instead of scatter
                feature_data = rul_feature_df[feature].dropna()
                rul_data = rul_feature_df.loc[feature_data.index, 'rul_days']
                
                # Bin the feature values into quartiles
                try:
                    feature_data_binned = pd.qcut(feature_data, q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
                    
                    # Box plot by quartiles
                    rul_by_quartile = [rul_data[feature_data_binned == q] for q in ['Q1', 'Q2', 'Q3', 'Q4']]
                    box_plot = ax.boxplot(rul_by_quartile, labels=['Q1\n(Low)', 'Q2', 'Q3', 'Q4\n(High)'], 
                                         patch_artist=True)
                    
                    # Color the boxes
                    colors_box = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
                    for patch, color in zip(box_plot['boxes'], colors_box):
                        patch.set_facecolor(color)
                    
                    ax.set_title(f'{feature.split("_")[0]} - {"_".join(feature.split("_")[1:])}')
                    ax.set_ylabel('RUL (Days)')
                    ax.set_xlabel('Feature Quartile')
                    ax.grid(True, alpha=0.3)
                    
                    # Add correlation as text
                    ax.text(0.02, 0.98, f'Correlation: {correlations[feature]:+.3f}', 
                           transform=ax.transAxes, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                    
                except Exception:
                    # Fallback to scatter plot if binning fails
                    ax.scatter(feature_data, rul_data, alpha=0.6)
                    ax.set_xlabel(feature.replace('_', ' ').title())
                    ax.set_ylabel('RUL (Days)')
                    ax.set_title(f'Correlation: {correlations[feature]:+.3f}')
                    ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
            print("💡 Enhanced Interpretation Guide:")
            print("   📊 RUL Categories: CRITICAL(≤7d) → HIGH(≤15d) → MEDIUM(≤30d) → LOW(≤45d) → NORMAL(≤60d)")
            print("   📈 Positive correlation: Higher feature = Longer RUL (protective factor)")
            print("   📉 Negative correlation: Higher feature = Shorter RUL (risk factor)")
            print("   🎯 Strong correlation (>0.5): Highly predictive for maintenance planning")
            print("   📦 Quartile Analysis: Q1(lowest 25%) vs Q4(highest 25%) shows feature impact")
            
            # Add RUL category insights
            print(f"\n🔍 RUL Category Insights:")
            category_stats = rul_feature_df.groupby('rul_category')['rul_days'].agg(['count', 'mean', 'std']).round(1)
            for category, stats in category_stats.iterrows():
                print(f"   {category}: {stats['count']} examples, avg {stats['mean']} days (±{stats['std']})")


def analyze_rul_patterns_by_category(rul_feature_df):
    """Analyze patterns specific to each RUL category for actionable insights."""
    print("\n🎯 RUL CATEGORY PATTERN ANALYSIS")
    print("="*50)
    
    feature_cols = [col for col in rul_feature_df.columns if col.endswith((
        '_trend_slope', '_volatility', '_pct_time_high', '_pct_time_low', '_pattern_change_pct'
    ))]
    
    if len(feature_cols) == 0:
        print("❌ No features available for category analysis")
        return
    
    categories = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NORMAL']
    
    for category in categories:
        category_data = rul_feature_df[rul_feature_df['rul_category'] == category]
        
        if len(category_data) == 0:
            continue
            
        print(f"\n🚨 {category} Risk Pattern ({len(category_data)} examples):")
        
        # Find distinguishing features for this category
        category_means = category_data[feature_cols].mean()
        overall_means = rul_feature_df[feature_cols].mean()
        differences = ((category_means - overall_means) / overall_means * 100).fillna(0)
        
        # Show top 3 distinguishing features
        top_differences = differences.abs().nlargest(3)
        
        for feature in top_differences.index:
            diff_pct = differences[feature]
            sensor = feature.split('_')[0]
            metric = '_'.join(feature.split('_')[1:])
            
            if abs(diff_pct) > 10:  # Only show significant differences
                direction = "higher" if diff_pct > 0 else "lower"
                print(f"   📊 {sensor} {metric}: {abs(diff_pct):.1f}% {direction} than average")
                
                # Provide actionable interpretation
                if 'trend_slope' in metric:
                    if diff_pct > 0:
                        print(f"      ➡️ {sensor} readings increasing faster (degradation accelerating)")
                    else:
                        print(f"      ➡️ {sensor} readings more stable (slower degradation)")
                elif 'volatility' in metric:
                    if diff_pct > 0:
                        print(f"      ➡️ {sensor} more erratic (system stress indicators)")
                    else:
                        print(f"      ➡️ {sensor} more stable (consistent operation)")
                elif 'pct_time_high' in metric:
                    if diff_pct > 0:
                        print(f"      ➡️ {sensor} spends more time in danger zone")
                    else:
                        print(f"      ➡️ {sensor} operates within safe thresholds")


def print_model_summary(model, scaler, selected_features):
    """Print final model summary."""
    print("📊 EXPLAINABLE RUL MODEL SUMMARY")
    print("="*50)

    if model is not None:
        print(f"✅ Model Type: Linear Regression (Explainable)")
        print(f"📈 Features Used: {len(selected_features)}")
        print(f"🎯 Target: Days until next DPF maintenance")
        
        print(f"\n🔧 Key Monitoring Features:")
        for i, feature in enumerate(selected_features, 1):
            sensor = feature.split('_')[0]
            metric = '_'.join(feature.split('_')[1:])
            print(f"   {i}. {sensor} - {metric.replace('_', ' ').title()}")
        
        print(f"\n🚨 Alert Thresholds:")
        print(f"   🚨 URGENT: ≤30 days predicted RUL")
        print(f"   ⚠️ WARNING: 31-60 days predicted RUL")
        print(f"   ⚡ CAUTION: 61-90 days predicted RUL")
        print(f"   ✅ NORMAL: >90 days predicted RUL")
        
    else:
        print("❌ Model training incomplete - need more data")

    print(f"\n💾 To save this model for production use:")
    print(f"   import joblib")
    print(f"   joblib.dump(model, 'dpf_rul_model.pkl')")
    print(f"   joblib.dump(scaler, 'dpf_rul_scaler.pkl')")

    print(f"\n🎉 Explainable RUL Analysis Complete!")
    print(f"   Ready for deployment in fleet management system")


def main():
    """Main analysis pipeline."""
    print("🚀 Explainable DPF RUL Analysis")
    print("="*50)
    
    # Load data
    maintenance_df, sensor_df, diagnostic_df = load_dpf_datasets()
    
    # Create RUL labels using backtrack approach
    rul_df = create_backtrack_rul_labels(maintenance_df)
    
    if len(rul_df) == 0:
        print("❌ No RUL labels created. Cannot proceed with analysis.")
        return
    
    # Build RUL dataset with features
    rul_feature_df = build_rul_dataset(rul_df, sensor_df, window_days=30)
    
    if len(rul_feature_df) == 0:
        print("❌ No feature data extracted. Cannot proceed with modeling.")
        return
    
    # Analyze explainable features
    analyze_explainable_features(rul_feature_df)
    
    # Analyze RUL patterns by category for actionable insights
    analyze_rul_patterns_by_category(rul_feature_df)
    
    # Build explainable model
    model, scaler, selected_features = build_explainable_rul_model(rul_feature_df)
    
    # Print final summary
    print_model_summary(model, scaler, selected_features)


if __name__ == "__main__":
    main()