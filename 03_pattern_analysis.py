"""
Pattern analysis script for DPF maintenance prediction
Identifies specific sensor patterns that indicate impending maintenance needs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

def load_processed_data():
    """Load the processed DPF datasets"""
    print("Loading processed DPF datasets...")
    
    dpf_maintenance = pd.read_csv('data/dpf_maintenance_records.csv')
    dpf_vehicle_stats = pd.read_csv('data/dpf_vehicle_stats.csv')
    dpf_diagnostic = pd.read_csv('data/dpf_diagnostic_data.csv')
    
    # Convert time columns and handle timezone
    dpf_maintenance['Date of Issue'] = pd.to_datetime(dpf_maintenance['Date of Issue']).dt.tz_localize(None)
    dpf_vehicle_stats['time'] = pd.to_datetime(dpf_vehicle_stats['time']).dt.tz_localize(None)
    dpf_diagnostic['Time'] = pd.to_datetime(dpf_diagnostic['Time'], errors='coerce').dt.tz_localize(None)
    
    return dpf_maintenance, dpf_vehicle_stats, dpf_diagnostic

def identify_critical_patterns(dpf_maintenance, dpf_vehicle_stats):
    """Identify critical sensor patterns before maintenance events"""
    print("\n=== CRITICAL PATTERN IDENTIFICATION ===")
    
    # Key sensors for DPF analysis
    key_sensors = [
        'engineLoadPercent', 'engineRpm', 'ecuSpeedMph', 
        'engineOilPressureKPa', 'engineCoolantTemperatureMilliC',
        'ambientAirTemperatureMilliC', 'fuelPercents', 'defLevelMilliPercent'
    ]
    
    # Create feature matrix for each maintenance event
    features_list = []
    labels_list = []
    
    for idx, maintenance_event in dpf_maintenance.iterrows():
        vin = maintenance_event['VIN Number']
        maintenance_date = maintenance_event['Date of Issue']
        job_type = maintenance_event['lines_jobDescriptions']
        
        if pd.isna(maintenance_date) or pd.isna(vin):
            continue
            
        # Get vehicle data
        vehicle_data = dpf_vehicle_stats[dpf_vehicle_stats['vin'] == vin].copy()
        if len(vehicle_data) == 0:
            continue
        
        # Look at different time windows before maintenance
        windows = [7, 14, 30]  # days
        
        for window in windows:
            start_date = maintenance_date - timedelta(days=window)
            window_data = vehicle_data[
                (vehicle_data['time'] >= start_date) & 
                (vehicle_data['time'] < maintenance_date)
            ]
            
            if len(window_data) < 5:  # Need minimum data points
                continue
            
            # Calculate features for this window
            features = {}
            features['vin'] = vin
            features['window_days'] = window
            features['data_points'] = len(window_data)
            
            # Statistical features for each sensor
            for sensor in key_sensors:
                if sensor in window_data.columns:
                    sensor_data = window_data[sensor].dropna()
                    if len(sensor_data) > 0:
                        features[f'{sensor}_mean'] = sensor_data.mean()
                        features[f'{sensor}_std'] = sensor_data.std()
                        features[f'{sensor}_min'] = sensor_data.min()
                        features[f'{sensor}_max'] = sensor_data.max()
                        features[f'{sensor}_trend'] = calculate_trend(sensor_data)
                        features[f'{sensor}_volatility'] = sensor_data.std() / sensor_data.mean() if sensor_data.mean() != 0 else 0
                    else:
                        features[f'{sensor}_mean'] = np.nan
                        features[f'{sensor}_std'] = np.nan
                        features[f'{sensor}_min'] = np.nan
                        features[f'{sensor}_max'] = np.nan
                        features[f'{sensor}_trend'] = np.nan
                        features[f'{sensor}_volatility'] = np.nan
            
            features_list.append(features)
            labels_list.append(job_type)
    
    # Convert to DataFrame
    features_df = pd.DataFrame(features_list)
    features_df['job_type'] = labels_list
    
    print(f"Created {len(features_df)} feature vectors")
    print(f"Job type distribution:")
    print(features_df['job_type'].value_counts())
    
    return features_df

def calculate_trend(series):
    """Calculate trend (slope) of a time series"""
    if len(series) < 2:
        return 0
    x = np.arange(len(series))
    y = series.values
    try:
        slope = np.polyfit(x, y, 1)[0]
        return slope
    except:
        return 0

def analyze_sensor_criticality(features_df):
    """Analyze which sensors are most critical for predicting maintenance"""
    print("\n=== SENSOR CRITICALITY ANALYSIS ===")
    
    # Separate features by job type
    job_types = features_df['job_type'].unique()
    
    # Calculate baseline statistics for each job type
    baseline_stats = {}
    for job_type in job_types:
        job_data = features_df[features_df['job_type'] == job_type]
        baseline_stats[job_type] = {}
        
        # Get numeric columns only
        numeric_cols = job_data.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col not in ['window_days', 'data_points']]
        
        for col in numeric_cols:
            values = job_data[col].dropna()
            if len(values) > 0:
                baseline_stats[job_type][col] = {
                    'mean': values.mean(),
                    'std': values.std(),
                    'count': len(values)
                }
    
    # Find sensors with significant differences between job types
    critical_sensors = {}
    sensor_names = set()
    for job_type in baseline_stats:
        for sensor in baseline_stats[job_type]:
            sensor_names.add(sensor.split('_')[0])
    
    for sensor in sensor_names:
        if sensor in ['vin', 'window', 'data']:
            continue
            
        sensor_patterns = {}
        for job_type in job_types:
            sensor_mean_col = f'{sensor}_mean'
            if sensor_mean_col in baseline_stats.get(job_type, {}):
                sensor_patterns[job_type] = baseline_stats[job_type][sensor_mean_col]['mean']
        
        if len(sensor_patterns) > 1:
            # Calculate coefficient of variation across job types
            values = list(sensor_patterns.values())
            if len(values) > 1 and np.std(values) > 0:
                cv = np.std(values) / np.mean(values)
                critical_sensors[sensor] = {
                    'cv': cv,
                    'patterns': sensor_patterns
                }
    
    # Sort by coefficient of variation
    sorted_sensors = sorted(critical_sensors.items(), key=lambda x: x[1]['cv'], reverse=True)
    
    print(f"Top 10 most discriminative sensors:")
    for i, (sensor, data) in enumerate(sorted_sensors[:10]):
        print(f"{i+1}. {sensor}: CV={data['cv']:.3f}")
        for job_type, value in data['patterns'].items():
            print(f"   {job_type}: {value:.2f}")
        print()
    
    return sorted_sensors

def build_predictive_model(features_df):
    """Build predictive model for maintenance type"""
    print("\n=== PREDICTIVE MODEL BUILDING ===")
    
    # Prepare data for modeling
    numeric_features = features_df.select_dtypes(include=[np.number]).columns
    numeric_features = [col for col in numeric_features if col not in ['window_days', 'data_points']]
    
    # Fill missing values with median
    X = features_df[numeric_features].fillna(features_df[numeric_features].median())
    y = features_df['job_type']
    
    # Only use cases with sufficient data
    valid_indices = X.notna().sum(axis=1) > len(numeric_features) * 0.5
    X = X[valid_indices]
    y = y[valid_indices]
    
    if len(X) < 10:
        print("Insufficient data for modeling")
        return None
    
    print(f"Training data: {len(X)} samples, {len(numeric_features)} features")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf_model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = rf_model.predict(X_test_scaled)
    
    # Results
    print(f"\nModel Performance:")
    print(f"Training accuracy: {rf_model.score(X_train_scaled, y_train):.3f}")
    print(f"Testing accuracy: {rf_model.score(X_test_scaled, y_test):.3f}")
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': numeric_features,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    return rf_model, scaler, feature_importance

def analyze_dpf_specific_patterns(dpf_diagnostic, dpf_maintenance):
    """Analyze DPF-specific diagnostic patterns"""
    print("\n=== DPF-SPECIFIC PATTERN ANALYSIS ===")
    
    # Focus on exhaust gas pressure readings
    exhaust_pressure = dpf_diagnostic[
        (dpf_diagnostic['Diagnostic'] == 'Exhaust Gas Pressure') & 
        (dpf_diagnostic['Value'].notna())
    ].copy()
    
    if len(exhaust_pressure) == 0:
        print("No exhaust gas pressure data available")
        return
    
    print(f"Exhaust gas pressure readings: {len(exhaust_pressure)}")
    
    # Convert Asset Name to vehicle number for merging
    exhaust_pressure['Vehicle_Number'] = exhaust_pressure['Asset Name'].astype(str)
    
    # Merge with maintenance data
    merged_data = []
    for idx, maintenance_event in dpf_maintenance.iterrows():
        vehicle_num = str(maintenance_event['Vehicle_Number'])
        maintenance_date = maintenance_event['Date of Issue']
        job_type = maintenance_event['lines_jobDescriptions']
        
        if pd.isna(maintenance_date):
            continue
        
        # Get pressure readings for this vehicle
        vehicle_pressure = exhaust_pressure[exhaust_pressure['Vehicle_Number'] == vehicle_num].copy()
        
        if len(vehicle_pressure) == 0:
            continue
        
        # Look at readings before maintenance
        start_date = maintenance_date - timedelta(days=30)
        pre_maintenance_pressure = vehicle_pressure[
            (vehicle_pressure['Time'] >= start_date) & 
            (vehicle_pressure['Time'] < maintenance_date)
        ]
        
        if len(pre_maintenance_pressure) > 0:
            pressure_values = pre_maintenance_pressure['Value'].astype(float)
            merged_data.append({
                'vehicle_number': vehicle_num,
                'job_type': job_type,
                'maintenance_date': maintenance_date,
                'pressure_mean': pressure_values.mean(),
                'pressure_std': pressure_values.std(),
                'pressure_min': pressure_values.min(),
                'pressure_max': pressure_values.max(),
                'pressure_readings': len(pressure_values)
            })
    
    if len(merged_data) == 0:
        print("No matching pressure data found")
        return
    
    pressure_df = pd.DataFrame(merged_data)
    
    print(f"\nExhaust pressure patterns before maintenance:")
    print(pressure_df.groupby('job_type').agg({
        'pressure_mean': ['mean', 'std'],
        'pressure_std': ['mean', 'std'],
        'pressure_min': ['mean', 'std'],
        'pressure_max': ['mean', 'std']
    }).round(2))
    
    # Identify anomalous pressure patterns
    overall_pressure_mean = pressure_df['pressure_mean'].mean()
    overall_pressure_std = pressure_df['pressure_mean'].std()
    
    pressure_df['pressure_anomaly'] = (
        (pressure_df['pressure_mean'] < overall_pressure_mean - 2 * overall_pressure_std) |
        (pressure_df['pressure_mean'] > overall_pressure_mean + 2 * overall_pressure_std)
    )
    
    print(f"\nAnomalous pressure patterns:")
    anomalies = pressure_df[pressure_df['pressure_anomaly']]
    if len(anomalies) > 0:
        print(f"Vehicles with anomalous exhaust pressure: {len(anomalies)}")
        print(anomalies[['vehicle_number', 'job_type', 'pressure_mean', 'pressure_std']])
    else:
        print("No anomalous pressure patterns detected")
    
    return pressure_df

def main():
    """Main pattern analysis pipeline"""
    print("=== DPF PATTERN ANALYSIS ===")
    
    # Load data
    dpf_maintenance, dpf_vehicle_stats, dpf_diagnostic = load_processed_data()
    
    # Identify critical patterns
    features_df = identify_critical_patterns(dpf_maintenance, dpf_vehicle_stats)
    
    # Analyze sensor criticality
    critical_sensors = analyze_sensor_criticality(features_df)
    
    # Build predictive model
    model_results = build_predictive_model(features_df)
    
    # Analyze DPF-specific patterns
    pressure_patterns = analyze_dpf_specific_patterns(dpf_diagnostic, dpf_maintenance)
    
    print("\n=== PATTERN ANALYSIS COMPLETE ===")
    print("Key insights:")
    print(f"- {len(features_df)} feature vectors created from sensor data")
    print(f"- {len(critical_sensors)} sensors analyzed for criticality")
    print("- Machine learning model built for maintenance type prediction")
    print("- DPF-specific exhaust pressure patterns analyzed")
    
    # Summary recommendations
    print("\n=== RECOMMENDATIONS ===")
    print("1. Monitor exhaust gas pressure trends - negative values may indicate DPF issues")
    print("2. Track engine load patterns - consistent high load may stress DPF")
    print("3. Watch DEF level trends - low levels can cause DPF problems")
    print("4. Monitor engine coolant temperature - overheating can damage DPF")
    print("5. Set up alerts for vehicles showing anomalous sensor patterns")

if __name__ == "__main__":
    main()