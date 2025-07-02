#!/usr/bin/env python3
"""
Script 1: Univariate Sensor Forecasting for DPF RUL Analysis
============================================================

This script focuses on forecasting individual sensor degradation patterns
using Nixtla's StatsForecast library for classical time-series methods.

Key Objectives:
- Model degradation trends for critical DPF sensors
- Predict future sensor values to identify deterioration
- Establish baseline forecasting performance
- Identify sensors with predictable degradation patterns

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
        HoltWinters, SimpleExponentialSmoothing
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


def load_dpf_sensor_data():
    """Load and prepare DPF sensor data for time-series analysis."""
    print("📊 Loading DPF sensor data for time-series analysis...")
    
    try:
        # Load both vehicle stats files
        sensor_df_2024 = pd.read_csv('data/dpf_vehicle_stats.csv')
        sensor_df_2023 = pd.read_csv('data/vehicle_stats_23-24.csv')
        
        # Combine datasets
        sensor_df = pd.concat([sensor_df_2023, sensor_df_2024], ignore_index=True)
        
        # Remove duplicates
        initial_rows = len(sensor_df)
        sensor_df = sensor_df.drop_duplicates(subset=['time', 'vin'], keep='first')
        duplicates_removed = initial_rows - len(sensor_df)
        
        print(f"✅ Combined sensor data: {len(sensor_df):,} records")
        if duplicates_removed > 0:
            print(f"   🗑️ Removed {duplicates_removed:,} duplicates")
        
        # Convert time column
        sensor_df['time'] = pd.to_datetime(sensor_df['time']).dt.tz_localize(None)
        
        # Sort by time
        sensor_df = sensor_df.sort_values('time').reset_index(drop=True)
        
        print(f"📅 Time range: {sensor_df['time'].min()} to {sensor_df['time'].max()}")
        print(f"🚗 Unique vehicles: {sensor_df['vin'].nunique():,}")
        
        return sensor_df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None


def identify_critical_dpf_sensors(sensor_df, min_data_points=1000):
    """Identify sensors most critical for DPF health with sufficient data."""
    print(f"\n🔍 Identifying critical DPF sensors...")
    
    # DPF-critical sensors (prioritized by importance)
    critical_sensors = [
        'defLevelMilliPercent',          # DEF fluid level - critical for DPF regen
        'engineLoadPercent',             # Engine load - affects DPF loading
        'engineCoolantTemperatureMilliC', # Temperature - affects DPF efficiency  
        'engineRpm',                     # RPM - affects DPF burn-off
        'ecuSpeedMph',                   # Speed - highway vs city affects DPF
        'fuelPercents',                  # Fuel level - affects operations
        'ambientAirTemperatureMilliC',   # Ambient temp - affects DPF performance
        'engineOilPressureKPa',          # Oil pressure - system health
        'intakeManifoldTemperatureMilliC', # Intake temp - combustion efficiency
        'barometricPressurePa'           # Atmospheric pressure - affects combustion
    ]
    
    # Check data availability for each sensor
    sensor_quality = {}
    
    for sensor in critical_sensors:
        if sensor not in sensor_df.columns:
            continue
            
        # Calculate data quality metrics
        total_records = len(sensor_df)
        non_null_records = sensor_df[sensor].notna().sum()
        data_coverage = (non_null_records / total_records) * 100
        
        # Check if values are not all identical (meaningful variation)
        unique_values = sensor_df[sensor].nunique()
        has_variation = unique_values > 10
        
        if non_null_records >= min_data_points and has_variation:
            sensor_quality[sensor] = {
                'records': non_null_records,
                'coverage': data_coverage,
                'unique_values': unique_values,
                'mean': sensor_df[sensor].mean(),
                'std': sensor_df[sensor].std(),
                'cv': sensor_df[sensor].std() / sensor_df[sensor].mean() if sensor_df[sensor].mean() != 0 else 0
            }
    
    # Sort by data coverage and variation
    sorted_sensors = sorted(sensor_quality.items(), 
                           key=lambda x: (x[1]['coverage'], x[1]['unique_values']), 
                           reverse=True)
    
    print(f"\n📈 Top DPF-Critical Sensors (Data Quality):")
    for i, (sensor, stats) in enumerate(sorted_sensors[:5]):
        print(f"   {i+1}. {sensor}")
        print(f"      📊 {stats['records']:,} records ({stats['coverage']:.1f}% coverage)")
        print(f"      🔄 {stats['unique_values']:,} unique values")
        print(f"      📉 CV: {stats['cv']:.3f} (variation)")
        print()
    
    return [sensor for sensor, _ in sorted_sensors[:3]]  # Return top 3


def prepare_time_series_data(sensor_df, sensor_name, aggregation='daily'):
    """Prepare sensor data for time-series forecasting."""
    print(f"\n🔧 Preparing {sensor_name} for time-series analysis...")
    
    # Filter non-null values
    sensor_data = sensor_df[['time', 'vin', sensor_name]].dropna()
    
    if len(sensor_data) == 0:
        print(f"❌ No data available for {sensor_name}")
        return None
    
    print(f"   📊 {len(sensor_data):,} non-null records")
    
    # Aggregate data by time period
    if aggregation == 'daily':
        # Daily aggregation across all vehicles
        daily_data = sensor_data.groupby(sensor_data['time'].dt.date)[sensor_name].agg([
            'mean', 'median', 'std', 'count'
        ]).reset_index()
        
        daily_data['time'] = pd.to_datetime(daily_data['time'])
        daily_data = daily_data.sort_values('time')
        
        # Create time-series dataframe for StatsForecast
        ts_df = pd.DataFrame({
            'unique_id': f'fleet_avg_{sensor_name}',
            'ds': daily_data['time'],
            'y': daily_data['mean']
        })
        
        print(f"   📅 Daily aggregation: {len(ts_df)} days")
        
    elif aggregation == 'per_vehicle':
        # Per-vehicle time series (select vehicles with most data)
        vehicle_counts = sensor_data['vin'].value_counts()
        top_vehicles = vehicle_counts.head(5).index
        
        ts_list = []
        for vin in top_vehicles:
            vehicle_data = sensor_data[sensor_data['vin'] == vin].copy()
            vehicle_data = vehicle_data.groupby(vehicle_data['time'].dt.date)[sensor_name].mean().reset_index()
            vehicle_data['time'] = pd.to_datetime(vehicle_data['time'])
            
            if len(vehicle_data) >= 30:  # Minimum 30 days of data
                vehicle_ts = pd.DataFrame({
                    'unique_id': f'{vin}_{sensor_name}',
                    'ds': vehicle_data['time'],
                    'y': vehicle_data[sensor_name]
                })
                ts_list.append(vehicle_ts)
        
        if ts_list:
            ts_df = pd.concat(ts_list, ignore_index=True)
            print(f"   🚗 Per-vehicle series: {len(ts_list)} vehicles, {len(ts_df)} total points")
        else:
            print(f"   ❌ No vehicles with sufficient data")
            return None
    
    # Remove any infinite or extreme outliers
    ts_df = ts_df.replace([np.inf, -np.inf], np.nan).dropna()
    
    # Remove extreme outliers (beyond 3 standard deviations)
    q1 = ts_df['y'].quantile(0.25)
    q3 = ts_df['y'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 3 * iqr
    upper_bound = q3 + 3 * iqr
    
    outliers_removed = len(ts_df) - len(ts_df[(ts_df['y'] >= lower_bound) & (ts_df['y'] <= upper_bound)])
    ts_df = ts_df[(ts_df['y'] >= lower_bound) & (ts_df['y'] <= upper_bound)]
    
    if outliers_removed > 0:
        print(f"   🗑️ Removed {outliers_removed} extreme outliers")
    
    print(f"   ✅ Final dataset: {len(ts_df)} observations")
    print(f"   📊 Value range: {ts_df['y'].min():.2f} to {ts_df['y'].max():.2f}")
    
    return ts_df


def perform_univariate_forecasting(ts_df, forecast_horizon=30):
    """Perform univariate forecasting using StatsForecast models."""
    
    if not NIXTLA_AVAILABLE:
        print("❌ StatsForecast not available. Cannot perform forecasting.")
        return None, None
    
    print(f"\n🔮 Performing univariate forecasting...")
    print(f"   📅 Forecast horizon: {forecast_horizon} days")
    
    # Define forecasting models (from simple to complex)
    models = [
        Naive(),                           # Simple baseline
        HistoricAverage(),                # Historical average
        RandomWalkWithDrift(),            # Random walk with trend
        SimpleExponentialSmoothing(alpha=0.3),  # Simple exponential smoothing with alpha
        AutoETS(season_length=7),         # Auto Exponential smoothing (weekly seasonality)
        AutoARIMA(season_length=7)        # Auto ARIMA (weekly seasonality)
    ]
    
    # Initialize StatsForecast
    sf = StatsForecast(
        models=models,
        freq='D',  # Daily frequency
        n_jobs=-1  # Use all CPU cores
    )
    
    try:
        # Generate forecasts
        print("   🔄 Training models and generating forecasts...")
        forecasts = sf.forecast(df=ts_df, h=forecast_horizon)
        
        # Skip prediction intervals for now - focus on main forecasting
        print("   📊 Skipping prediction intervals for simplicity...")
        prediction_intervals = None
        
        print(f"   ✅ Forecasting complete!")
        print(f"   📈 Models: {len(models)}")
        print(f"   🎯 Unique series: {ts_df['unique_id'].nunique()}")
        
        return forecasts, prediction_intervals
        
    except Exception as e:
        print(f"   ❌ Forecasting failed: {e}")
        return None, None


def analyze_forecasting_results(ts_df, forecasts, prediction_intervals, sensor_name):
    """Analyze and visualize forecasting results."""
    
    if forecasts is None:
        return
    
    print(f"\n📊 Analyzing forecasting results for {sensor_name}...")
    
    # Get unique series
    unique_series = ts_df['unique_id'].unique()
    
    # Create comprehensive visualization
    fig, axes = plt.subplots(2, 2, figsize=(20, 12))
    fig.suptitle(f'Univariate Forecasting Analysis: {sensor_name}', fontsize=16)
    
    for i, series_id in enumerate(unique_series[:4]):  # Plot first 4 series
        row = i // 2
        col = i % 2
        ax = axes[row, col]
        
        # Historical data
        historical = ts_df[ts_df['unique_id'] == series_id].copy()
        forecast_data = forecasts[forecasts['unique_id'] == series_id].copy()
        
        if len(historical) == 0 or len(forecast_data) == 0:
            continue
        
        # Plot historical data
        ax.plot(historical['ds'], historical['y'], 
                label='Historical', color='blue', linewidth=2)
        
        # Plot forecasts for each model
        model_colors = ['red', 'green', 'orange', 'purple', 'brown', 'pink']
        model_names = ['Naive', 'HistoricAverage', 'RandomWalkWithDrift', 
                      'SimpleExponentialSmoothing', 'AutoETS', 'AutoARIMA']
        
        for j, model in enumerate(model_names):
            if model in forecast_data.columns:
                ax.plot(forecast_data['ds'], forecast_data[model], 
                       label=f'{model} Forecast', color=model_colors[j], 
                       linestyle='--', alpha=0.8)
        
        # Add prediction intervals if available
        if prediction_intervals is not None:
            pi_data = prediction_intervals[prediction_intervals['unique_id'] == series_id]
            if len(pi_data) > 0 and 'AutoARIMA-lo-95' in pi_data.columns:
                ax.fill_between(pi_data['ds'], 
                               pi_data['AutoARIMA-lo-95'], 
                               pi_data['AutoARIMA-hi-95'],
                               alpha=0.2, color='purple', label='95% Prediction Interval')
        
        ax.set_title(f'{series_id}')
        ax.set_xlabel('Date')
        ax.set_ylabel(f'{sensor_name} Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Print forecasting insights
    print(f"\n💡 Forecasting Insights for {sensor_name}:")
    
    # Calculate forecast trends
    for series_id in unique_series[:3]:  # Analyze first 3 series
        forecast_data = forecasts[forecasts['unique_id'] == series_id]
        historical_data = ts_df[ts_df['unique_id'] == series_id]
        
        if len(forecast_data) == 0 or len(historical_data) == 0:
            continue
        
        # Compare last historical value with forecast trend
        last_historical = historical_data['y'].iloc[-1]
        
        if 'AutoARIMA' in forecast_data.columns:
            first_forecast = forecast_data['AutoARIMA'].iloc[0]
            last_forecast = forecast_data['AutoARIMA'].iloc[-1]
            
            trend_direction = "increasing" if last_forecast > first_forecast else "decreasing"
            trend_magnitude = abs(last_forecast - first_forecast)
            
            print(f"\n   🔍 {series_id}:")
            print(f"      📊 Current value: {last_historical:.2f}")
            print(f"      📈 30-day forecast: {last_forecast:.2f}")
            print(f"      📉 Trend: {trend_direction} by {trend_magnitude:.2f}")
            
            # RUL implications
            if trend_direction == "decreasing" and sensor_name == 'defLevelMilliPercent':
                print(f"      ⚠️ DEF level declining - monitor for refill needs")
            elif trend_direction == "increasing" and sensor_name == 'engineCoolantTemperatureMilliC':
                print(f"      🔥 Temperature rising - potential overheating risk")
            elif trend_direction == "increasing" and sensor_name == 'engineLoadPercent':
                print(f"      ⚡ Engine load increasing - higher DPF stress expected")


def main():
    """Main univariate forecasting pipeline."""
    print("🚀 UNIVARIATE SENSOR FORECASTING FOR DPF RUL")
    print("="*60)
    
    # Load sensor data
    sensor_df = load_dpf_sensor_data()
    if sensor_df is None:
        return
    
    # Identify critical sensors
    critical_sensors = identify_critical_dpf_sensors(sensor_df)
    
    if not critical_sensors:
        print("❌ No suitable sensors found for forecasting")
        return
    
    print(f"\n🎯 Selected sensors for forecasting: {critical_sensors}")
    
    # Perform forecasting for each critical sensor
    for sensor_name in critical_sensors[:2]:  # Start with top 2 sensors
        print(f"\n{'='*60}")
        print(f"📊 FORECASTING: {sensor_name}")
        print(f"{'='*60}")
        
        # Prepare time-series data
        ts_df = prepare_time_series_data(sensor_df, sensor_name, aggregation='daily')
        
        if ts_df is None:
            print(f"⏭️ Skipping {sensor_name} - insufficient data")
            continue
        
        # Perform forecasting
        forecasts, prediction_intervals = perform_univariate_forecasting(ts_df, forecast_horizon=30)
        
        # Analyze results
        analyze_forecasting_results(ts_df, forecasts, prediction_intervals, sensor_name)
    
    print(f"\n🎉 Univariate forecasting analysis complete!")
    print(f"📋 Next steps:")
    print(f"   1. Review sensor degradation trends")
    print(f"   2. Identify sensors with predictable patterns")
    print(f"   3. Move to multivariate forecasting (Script 2)")


if __name__ == "__main__":
    main()