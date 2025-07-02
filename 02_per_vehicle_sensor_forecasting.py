#!/usr/bin/env python3
"""
Script 1: Per-Vehicle Univariate Sensor Forecasting for DPF RUL Analysis
========================================================================

This script forecasts individual sensor degradation patterns PER VEHICLE
using Nixtla's StatsForecast library for classical time-series methods.

Key Objectives:
- Model degradation trends for critical DPF sensors by individual vehicle
- Predict future sensor values to identify vehicles needing maintenance
- Find vehicles with concerning degradation patterns  
- Provide vehicle-specific maintenance recommendations

Approach:
- Load DPF maintenance records to identify vehicles with known issues
- Extract per-vehicle sensor time series with sufficient data
- Forecast each vehicle's sensor trends individually
- Flag vehicles with predicted degradation beyond safe thresholds

Author: RUL Analysis Pipeline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings

# Nixtla StatsForecast imports
try:
    from statsforecast import StatsForecast
    from statsforecast.models import (
        AutoARIMA, AutoETS, HistoricAverage,
        Naive, RandomWalkWithDrift, SeasonalNaive,
        SimpleExponentialSmoothing
    )
    NIXTLA_AVAILABLE = True
    print("✅ StatsForecast successfully imported")
except ImportError as e:
    print(f"⚠️ Nixtla StatsForecast import failed: {e}")
    print("Run: uv add statsforecast")
    NIXTLA_AVAILABLE = False

warnings.filterwarnings('ignore')

# Set up plotting
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (15, 8)


def load_dpf_datasets():
    """Load and prepare the DPF datasets following the pattern from explainable RUL analysis."""
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
        
        # Convert time columns
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


def identify_vehicles_for_forecasting(maintenance_df, sensor_df, min_days_data=60):
    """
    Identify vehicles with sufficient sensor data for meaningful forecasting.
    Focus on vehicles with known DPF maintenance history.
    """
    print(f"\n🔍 Identifying vehicles suitable for forecasting...")
    
    # Get vehicles with DPF maintenance history
    dpf_vehicles = maintenance_df['VIN Number'].unique()
    print(f"   🚗 Vehicles with DPF maintenance history: {len(dpf_vehicles)}")
    
    # Check sensor data availability for each vehicle
    vehicle_data_quality = {}
    
    for vin in dpf_vehicles:
        vehicle_sensors = sensor_df[sensor_df['vin'] == vin]
        
        if len(vehicle_sensors) == 0:
            continue
            
        # Calculate data quality metrics
        date_range = (vehicle_sensors['time'].max() - vehicle_sensors['time'].min()).days
        unique_days = vehicle_sensors['time'].dt.date.nunique()
        
        # Check for key DPF sensors
        key_sensors = ['defLevelMilliPercent', 'engineLoadPercent', 'engineCoolantTemperatureMilliC', 
                      'engineRpm', 'ecuSpeedMph']
        
        sensor_coverage = {}
        for sensor in key_sensors:
            if sensor in vehicle_sensors.columns:
                non_null_count = vehicle_sensors[sensor].notna().sum()
                sensor_coverage[sensor] = non_null_count
            else:
                sensor_coverage[sensor] = 0
        
        # Only include vehicles with meaningful data
        if unique_days >= min_days_data and sum(sensor_coverage.values()) > 100:
            vehicle_data_quality[vin] = {
                'days_span': date_range,
                'unique_days': unique_days,
                'total_records': len(vehicle_sensors),
                'sensor_coverage': sensor_coverage,
                'data_density': len(vehicle_sensors) / max(1, unique_days)
            }
    
    # Sort by data quality (prioritize vehicles with more comprehensive data)
    sorted_vehicles = sorted(vehicle_data_quality.items(), 
                           key=lambda x: (x[1]['unique_days'], x[1]['total_records']), 
                           reverse=True)
    
    print(f"\n📈 Top vehicles for forecasting (by data quality):")
    for i, (vin, stats) in enumerate(sorted_vehicles[:10]):
        print(f"   {i+1}. VIN {vin}:")
        print(f"      📅 {stats['unique_days']} days of data ({stats['days_span']} day span)")
        print(f"      📊 {stats['total_records']:,} sensor readings")
        print(f"      🎯 Density: {stats['data_density']:.1f} readings/day")
        
        # Show sensor coverage
        covered_sensors = [s for s, count in stats['sensor_coverage'].items() if count > 10]
        print(f"      🔧 Key sensors: {', '.join(covered_sensors)}")
        print()
    
    return [vin for vin, _ in sorted_vehicles[:15]]  # Return top 15 vehicles


def prepare_vehicle_time_series(sensor_df, vin, sensor_name, min_data_points=30):
    """
    Prepare time series data for a specific vehicle and sensor.
    """
    print(f"\n🔧 Preparing {sensor_name} time series for vehicle {vin}...")
    
    # Filter data for this vehicle and sensor
    vehicle_data = sensor_df[
        (sensor_df['vin'] == vin) & 
        (sensor_df[sensor_name].notna())
    ].copy()
    
    if len(vehicle_data) < min_data_points:
        print(f"   ❌ Insufficient data: {len(vehicle_data)} points (need {min_data_points})")
        return None
    
    # Aggregate by day to create regular time series
    daily_data = vehicle_data.groupby(vehicle_data['time'].dt.date).agg({
        sensor_name: ['mean', 'median', 'std', 'count']
    }).reset_index()
    
    # Flatten column names
    daily_data.columns = ['date', 'mean', 'median', 'std', 'count']
    daily_data['date'] = pd.to_datetime(daily_data['date'])
    daily_data = daily_data.sort_values('date')
    
    # Remove days with very few readings (< 3 per day suggests incomplete data)
    daily_data = daily_data[daily_data['count'] >= 3]
    
    if len(daily_data) < min_data_points:
        print(f"   ❌ Insufficient daily data after filtering: {len(daily_data)} days")
        return None
    
    # Create StatsForecast compatible format
    ts_df = pd.DataFrame({
        'unique_id': f'{vin}_{sensor_name}',
        'ds': daily_data['date'],
        'y': daily_data['mean']  # Use daily mean
    })
    
    # Remove outliers (beyond 3 IQR)
    q1 = ts_df['y'].quantile(0.25)
    q3 = ts_df['y'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 3 * iqr
    upper_bound = q3 + 3 * iqr
    
    outliers_before = len(ts_df)
    ts_df = ts_df[(ts_df['y'] >= lower_bound) & (ts_df['y'] <= upper_bound)]
    outliers_removed = outliers_before - len(ts_df)
    
    if outliers_removed > 0:
        print(f"   🗑️ Removed {outliers_removed} outlier days")
    
    print(f"   ✅ Created time series: {len(ts_df)} days")
    print(f"   📊 Value range: {ts_df['y'].min():.2f} to {ts_df['y'].max():.2f}")
    print(f"   📈 Recent trend: {ts_df['y'].tail(7).mean():.2f} (last 7 days avg)")
    
    return ts_df


def perform_vehicle_sensor_forecasting(ts_df, forecast_horizon=30):
    """
    Perform forecasting for a single vehicle-sensor combination.
    """
    if not NIXTLA_AVAILABLE:
        print("❌ StatsForecast not available. Cannot perform forecasting.")
        return None
    
    unique_id = ts_df['unique_id'].iloc[0]
    print(f"   🔮 Forecasting {unique_id} for {forecast_horizon} days...")
    
    # Use simpler models that work well with shorter series
    models = [
        Naive(),                           # Simple baseline
        HistoricAverage(),                # Historical average  
        RandomWalkWithDrift(),            # Random walk with trend
        SimpleExponentialSmoothing(alpha=0.3),  # Exponential smoothing
        AutoETS(season_length=7),         # Auto exponential smoothing (weekly pattern)
    ]
    
    # Add AutoARIMA only if we have enough data
    if len(ts_df) >= 50:
        models.append(AutoARIMA(season_length=7))
    
    try:
        # Initialize StatsForecast
        sf = StatsForecast(
            models=models,
            freq='D',  # Daily frequency
            n_jobs=1   # Single job for individual vehicle
        )
        
        # Generate forecasts
        forecasts = sf.forecast(df=ts_df, h=forecast_horizon)
        
        print(f"   ✅ Forecasting successful!")
        print(f"   📈 Models used: {len(models)}")
        
        return forecasts
        
    except Exception as e:
        print(f"   ❌ Forecasting failed: {e}")
        return None


def analyze_vehicle_forecasts(historical_data, forecasts, sensor_name, vin, maintenance_df):
    """
    Analyze forecasts for a vehicle to identify maintenance needs.
    """
    if forecasts is None or len(forecasts) == 0:
        return None
    
    unique_id = f'{vin}_{sensor_name}'
    print(f"\n📊 Analyzing forecasts for {unique_id}...")
    
    # Get the best performing model (use AutoETS if available, otherwise RandomWalkWithDrift)
    model_priority = ['AutoARIMA', 'AutoETS', 'RandomWalkWithDrift', 'SimpleExponentialSmoothing', 'HistoricAverage', 'Naive']
    best_model = None
    
    for model in model_priority:
        if model in forecasts.columns:
            best_model = model
            break
    
    if best_model is None:
        print("   ❌ No suitable forecast model found")
        return None
    
    # Analyze the forecast
    current_value = historical_data['y'].iloc[-1]
    forecast_values = forecasts[best_model]
    
    # Calculate trend
    first_forecast = forecast_values.iloc[0]
    last_forecast = forecast_values.iloc[-1]
    trend_direction = "increasing" if last_forecast > first_forecast else "decreasing"
    trend_magnitude = abs(last_forecast - first_forecast)
    
    # Define sensor-specific thresholds for concern
    thresholds = {
        'defLevelMilliPercent': {'critical_low': 50000, 'warning_low': 70000},
        'engineLoadPercent': {'critical_high': 85, 'warning_high': 75},
        'engineCoolantTemperatureMilliC': {'critical_high': 100000, 'warning_high': 95000},
        'engineRpm': {'critical_high': 2200, 'warning_high': 2000},
        'ecuSpeedMph': {'normal_range': (10, 80)}
    }
    
    # Assess risk level
    risk_level = "NORMAL"
    risk_reason = ""
    days_to_threshold = None
    
    if sensor_name in thresholds:
        thresh = thresholds[sensor_name]
        
        # Check if forecast crosses critical thresholds
        if 'critical_low' in thresh:
            critical_days = forecast_values[forecast_values <= thresh['critical_low']]
            if len(critical_days) > 0:
                days_to_threshold = critical_days.index[0] + 1  # +1 because index starts at 0
                risk_level = "CRITICAL"
                risk_reason = f"DEF level predicted to drop below {thresh['critical_low']:,} in {days_to_threshold} days"
                
        elif 'critical_high' in thresh:
            critical_days = forecast_values[forecast_values >= thresh['critical_high']]
            if len(critical_days) > 0:
                days_to_threshold = critical_days.index[0] + 1
                risk_level = "CRITICAL" 
                risk_reason = f"{sensor_name} predicted to exceed {thresh['critical_high']:,} in {days_to_threshold} days"
        
        # Check warning levels if not critical
        if risk_level == "NORMAL":
            if 'warning_low' in thresh:
                warning_days = forecast_values[forecast_values <= thresh['warning_low']]
                if len(warning_days) > 0:
                    days_to_threshold = warning_days.index[0] + 1
                    risk_level = "WARNING"
                    risk_reason = f"DEF level trending toward low threshold ({thresh['warning_low']:,})"
                    
            elif 'warning_high' in thresh:
                warning_days = forecast_values[forecast_values >= thresh['warning_high']]
                if len(warning_days) > 0:
                    days_to_threshold = warning_days.index[0] + 1
                    risk_level = "WARNING"
                    risk_reason = f"{sensor_name} trending toward high threshold ({thresh['warning_high']:,})"
    
    # Get last maintenance date for this vehicle
    vehicle_maintenance = maintenance_df[maintenance_df['VIN Number'] == vin]
    last_maintenance = None
    if len(vehicle_maintenance) > 0:
        last_maintenance = vehicle_maintenance['Date of Issue'].max()
        days_since_maintenance = (pd.Timestamp.now() - last_maintenance).days
    else:
        days_since_maintenance = None
    
    # Create analysis summary
    analysis = {
        'vin': vin,
        'sensor': sensor_name,
        'current_value': current_value,
        'forecast_30d': last_forecast,
        'trend_direction': trend_direction,
        'trend_magnitude': trend_magnitude,
        'risk_level': risk_level,
        'risk_reason': risk_reason,
        'days_to_threshold': days_to_threshold,
        'best_model': best_model,
        'last_maintenance': last_maintenance,
        'days_since_maintenance': days_since_maintenance,
        'forecast_data': forecasts
    }
    
    # Print summary
    print(f"   📈 Current {sensor_name}: {current_value:.2f}")
    print(f"   🔮 30-day forecast: {last_forecast:.2f}")
    print(f"   📊 Trend: {trend_direction} by {trend_magnitude:.2f}")
    print(f"   🚨 Risk Level: {risk_level}")
    if risk_reason:
        print(f"   ⚠️ {risk_reason}")
    if days_since_maintenance:
        print(f"   🔧 Days since last maintenance: {days_since_maintenance}")
    
    return analysis


def create_vehicle_forecast_visualization(analyses, top_n=6):
    """
    Create visualizations for the most concerning vehicle forecasts.
    """
    if not analyses:
        print("❌ No analyses to visualize")
        return
    
    # Sort by risk level and days to threshold
    risk_priority = {'CRITICAL': 3, 'WARNING': 2, 'NORMAL': 1}
    sorted_analyses = sorted(analyses, 
                           key=lambda x: (risk_priority.get(x['risk_level'], 0), 
                                        -(x['days_to_threshold'] or 999)), 
                           reverse=True)
    
    # Create visualization for top concerning vehicles
    top_analyses = sorted_analyses[:top_n]
    
    if len(top_analyses) == 0:
        print("📊 All vehicles show normal sensor patterns - no concerning trends detected")
        return
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Vehicle-Specific Sensor Forecasting: Maintenance Risk Assessment', fontsize=16)
    
    for i, analysis in enumerate(top_analyses):
        if i >= 6:  # Only plot first 6
            break
            
        row = i // 3
        col = i % 3
        ax = axes[row, col]
        
        # Get historical and forecast data
        vin = analysis['vin']
        sensor = analysis['sensor']
        forecasts = analysis['forecast_data']
        
        # Plot historical trend (last 30 days of historical data)
        # Note: We'd need to pass historical data to make this work fully
        # For now, show the forecast
        
        forecast_dates = pd.date_range(start=pd.Timestamp.now(), periods=30, freq='D')
        best_model = analysis['best_model']
        
        if best_model in forecasts.columns:
            ax.plot(forecast_dates, forecasts[best_model], 
                   label=f'Forecast ({best_model})', 
                   color='red', linewidth=2, linestyle='--')
        
        # Add current value point
        ax.scatter([forecast_dates[0]], [analysis['current_value']], 
                  color='blue', s=100, label='Current Value', zorder=5)
        
        # Color code based on risk level
        if analysis['risk_level'] == 'CRITICAL':
            ax.set_facecolor('#ffe6e6')  # Light red background
            title_color = 'red'
        elif analysis['risk_level'] == 'WARNING':
            ax.set_facecolor('#fff7e6')  # Light orange background  
            title_color = 'orange'
        else:
            title_color = 'green'
        
        ax.set_title(f"VIN {vin} - {sensor}\nRisk: {analysis['risk_level']}", 
                    color=title_color, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel(f'{sensor}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Add risk information as text
        if analysis['days_to_threshold']:
            ax.text(0.02, 0.98, f"Threshold in {analysis['days_to_threshold']} days", 
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.show()


def main():
    """Main per-vehicle forecasting pipeline."""
    print("🚀 PER-VEHICLE SENSOR FORECASTING FOR DPF RUL")
    print("="*60)
    
    # Load datasets
    maintenance_df, sensor_df, diagnostic_df = load_dpf_datasets()
    
    # Identify vehicles suitable for forecasting
    target_vehicles = identify_vehicles_for_forecasting(maintenance_df, sensor_df)
    
    if not target_vehicles:
        print("❌ No vehicles found with sufficient data for forecasting")
        return
    
    print(f"\n🎯 Selected {len(target_vehicles)} vehicles for forecasting")
    
    # Key sensors to forecast (prioritized by importance for DPF health)
    key_sensors = ['defLevelMilliPercent', 'engineLoadPercent', 'engineCoolantTemperatureMilliC']
    
    # Perform forecasting for each vehicle-sensor combination
    all_analyses = []
    
    for sensor_name in key_sensors:
        print(f"\n{'='*60}")
        print(f"📊 FORECASTING: {sensor_name}")
        print(f"{'='*60}")
        
        for i, vin in enumerate(target_vehicles[:8]):  # Limit to first 8 vehicles for demo
            print(f"\n--- Vehicle {i+1}/{min(8, len(target_vehicles))}: {vin} ---")
            
            # Prepare time series data
            ts_df = prepare_vehicle_time_series(sensor_df, vin, sensor_name)
            
            if ts_df is None:
                print(f"   ⏭️ Skipping {vin} - insufficient {sensor_name} data")
                continue
            
            # Perform forecasting
            forecasts = perform_vehicle_sensor_forecasting(ts_df, forecast_horizon=30)
            
            # Analyze results
            analysis = analyze_vehicle_forecasts(ts_df, forecasts, sensor_name, vin, maintenance_df)
            
            if analysis:
                all_analyses.append(analysis)
    
    # Summarize findings
    print(f"\n🎉 FORECASTING ANALYSIS COMPLETE!")
    print(f"{'='*60}")
    
    if all_analyses:
        # Count risk levels
        risk_counts = {}
        for analysis in all_analyses:
            risk = analysis['risk_level']
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        print(f"📊 Risk Assessment Summary:")
        for risk, count in sorted(risk_counts.items(), key=lambda x: {'CRITICAL': 3, 'WARNING': 2, 'NORMAL': 1}[x[0]], reverse=True):
            emoji = {'CRITICAL': '🚨', 'WARNING': '⚠️', 'NORMAL': '✅'}[risk]
            print(f"   {emoji} {risk}: {count} vehicle-sensor combinations")
        
        # Show top concerns
        critical_analyses = [a for a in all_analyses if a['risk_level'] == 'CRITICAL']
        warning_analyses = [a for a in all_analyses if a['risk_level'] == 'WARNING']
        
        if critical_analyses:
            print(f"\n🚨 CRITICAL ALERTS:")
            for analysis in critical_analyses:
                print(f"   Vehicle {analysis['vin']} - {analysis['sensor']}")
                print(f"   {analysis['risk_reason']}")
                print()
        
        if warning_analyses:
            print(f"\n⚠️ WARNING ALERTS:")
            for analysis in warning_analyses[:3]:  # Show top 3
                print(f"   Vehicle {analysis['vin']} - {analysis['sensor']}")
                print(f"   {analysis['risk_reason']}")
                print()
        
        # Create visualizations
        create_vehicle_forecast_visualization(all_analyses)
        
    else:
        print("❌ No successful forecasts generated")
    
    print(f"\n📋 Next Steps:")
    print(f"   1. Schedule maintenance for CRITICAL vehicles immediately")
    print(f"   2. Monitor WARNING vehicles closely")  
    print(f"   3. Use insights for predictive maintenance planning")
    print(f"   4. Move to multivariate analysis (Script 2)")


if __name__ == "__main__":
    main()