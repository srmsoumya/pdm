#!/usr/bin/env python3
"""
Script 2: Multivariate Sensor Forecasting for DPF RUL Analysis
==============================================================

This script models interactions between multiple sensors per vehicle to
improve RUL predictions beyond univariate approaches.

Key Objectives:
- Model cross-correlations between DPF-critical sensors
- Use Vector Autoregression (VAR) for multivariate time series
- Identify sensor interaction patterns that predict maintenance needs
- Provide system-level health assessment per vehicle

Approach:
- Start with vehicles identified as having concerning patterns from Script 1
- Model sensor relationships: DEF vs Engine Load vs Temperature
- Forecast all sensors simultaneously considering interactions
- Detect complex degradation patterns invisible to univariate models

Author: RUL Analysis Pipeline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings

# Multivariate forecasting libraries
try:
    from statsmodels.tsa.vector_ar.var_model import VAR
    from statsmodels.tsa.stattools import adfuller
    from statsmodels.stats.diagnostic import acorr_ljungbox
    STATSMODELS_AVAILABLE = True
    print("✅ Statsmodels VAR successfully imported")
except ImportError as e:
    print(f"⚠️ Statsmodels import failed: {e}")
    print("Run: uv add statsmodels")
    STATSMODELS_AVAILABLE = False

# Nixtla for hierarchical forecasting
try:
    from statsforecast import StatsForecast
    from statsforecast.models import AutoARIMA, AutoETS
    NIXTLA_AVAILABLE = True
    print("✅ StatsForecast successfully imported")
except ImportError as e:
    print(f"⚠️ StatsForecast import failed: {e}")
    NIXTLA_AVAILABLE = False

warnings.filterwarnings('ignore')

# Set up plotting
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (16, 10)


def load_dpf_datasets():
    """Load and prepare the DPF datasets for multivariate analysis."""
    print("📊 Loading DPF datasets for multivariate analysis...")
    
    try:
        maintenance_df = pd.read_csv('data/dpf_maintenance_records.csv')
        
        # Load and combine both vehicle stats files
        sensor_df_2024 = pd.read_csv('data/dpf_vehicle_stats.csv')
        sensor_df_2023 = pd.read_csv('data/vehicle_stats_23-24.csv')
        
        # Combine datasets and remove duplicates
        sensor_df = pd.concat([sensor_df_2023, sensor_df_2024], ignore_index=True)
        initial_rows = len(sensor_df)
        sensor_df = sensor_df.drop_duplicates(subset=['time', 'vin'], keep='first')
        duplicates_removed = initial_rows - len(sensor_df)
        
        if duplicates_removed > 0:
            print(f"   🗑️ Removed {duplicates_removed:,} duplicate records")
        
        print(f"✅ Maintenance records: {len(maintenance_df):,} events")
        print(f"✅ Sensor readings: {len(sensor_df):,} data points")
        
        # Convert time columns
        maintenance_df['Date of Issue'] = pd.to_datetime(maintenance_df['Date of Issue'])
        sensor_df['time'] = pd.to_datetime(sensor_df['time']).dt.tz_localize(None)
        
        return maintenance_df, sensor_df
        
    except FileNotFoundError:
        print("❌ Processed data not found. Please ensure DPF datasets are available")
        raise


def identify_all_viable_vehicles(maintenance_df, sensor_df, min_days_data=60):
    """
    Identify ALL vehicles with sufficient data for multivariate analysis.
    This provides comprehensive fleet-wide risk assessment.
    """
    print("\n🎯 Identifying ALL vehicles suitable for multivariate analysis...")
    
    # Get all vehicles with maintenance history (DPF-related issues)
    dpf_vehicles = maintenance_df['VIN Number'].unique()
    print(f"   🚗 Total vehicles with DPF maintenance history: {len(dpf_vehicles)}")
    
    # Multivariate sensors required for analysis
    multivariate_sensors = [
        'defLevelMilliPercent',
        'engineLoadPercent', 
        'engineCoolantTemperatureMilliC',
        'engineRpm',
        'ecuSpeedMph'
    ]
    
    vehicle_candidates = []
    
    for vin in dpf_vehicles:
        vehicle_data = sensor_df[sensor_df['vin'] == vin]
        
        if len(vehicle_data) == 0:
            continue
            
        # Calculate data quality metrics
        date_range = (vehicle_data['time'].max() - vehicle_data['time'].min()).days
        unique_days = vehicle_data['time'].dt.date.nunique()
        
        # Check sensor coverage
        sensor_coverage = {}
        for sensor in multivariate_sensors:
            if sensor in vehicle_data.columns:
                non_null_count = vehicle_data[sensor].notna().sum()
                sensor_coverage[sensor] = non_null_count
            else:
                sensor_coverage[sensor] = 0
        
        # Count sensors with meaningful data
        good_sensors = [s for s, count in sensor_coverage.items() if count > 100]
        total_sensor_data = sum(sensor_coverage.values())
        
        # Quality criteria: minimum days, minimum sensors, minimum total data points
        if (unique_days >= min_days_data and 
            len(good_sensors) >= 3 and 
            total_sensor_data > 1000):
            
            # Calculate maintenance recency
            vehicle_maintenance = maintenance_df[maintenance_df['VIN Number'] == vin]
            if len(vehicle_maintenance) > 0:
                last_maintenance = vehicle_maintenance['Date of Issue'].max()
                days_since_maintenance = (pd.Timestamp.now() - last_maintenance).days
            else:
                days_since_maintenance = 999  # No maintenance history
            
            vehicle_candidates.append({
                'vin': vin,
                'unique_days': unique_days,
                'date_range': date_range,
                'good_sensors': good_sensors,
                'total_sensor_data': total_sensor_data,
                'days_since_maintenance': days_since_maintenance,
                'data_density': total_sensor_data / max(1, unique_days)
            })
    
    # Sort by data quality and maintenance urgency
    # Prioritize: long time since maintenance, high data quality
    vehicle_candidates.sort(
        key=lambda x: (x['days_since_maintenance'], -x['data_density'], -x['unique_days']),
        reverse=True
    )
    
    print(f"\n📊 Found {len(vehicle_candidates)} vehicles suitable for multivariate analysis:")
    print(f"   📈 Data quality range: {min([v['unique_days'] for v in vehicle_candidates])} - {max([v['unique_days'] for v in vehicle_candidates])} days")
    print(f"   🔧 Maintenance urgency: {min([v['days_since_maintenance'] for v in vehicle_candidates])} - {max([v['days_since_maintenance'] for v in vehicle_candidates])} days since last service")
    
    # Show top candidates by urgency
    print(f"\n🚨 Top 10 Most Urgent Vehicles (by maintenance recency):")
    for i, vehicle in enumerate(vehicle_candidates[:10]):
        urgency = "🔴 OVERDUE" if vehicle['days_since_maintenance'] > 365 else "🟡 DUE SOON" if vehicle['days_since_maintenance'] > 180 else "🟢 RECENT"
        print(f"   {i+1:2d}. {vehicle['vin']} - {vehicle['days_since_maintenance']:3d} days since maintenance {urgency}")
        print(f"       📊 {len(vehicle['good_sensors'])} sensors, {vehicle['unique_days']} days data")
    
    return [v['vin'] for v in vehicle_candidates]


def prepare_multivariate_time_series(sensor_df, vin, sensors, min_days=60):
    """
    Prepare multivariate time series data for a specific vehicle.
    Returns a DataFrame with all sensors aligned by date.
    """
    print(f"\n🔧 Preparing multivariate time series for vehicle {vin}...")
    print(f"   🎯 Sensors: {', '.join(sensors)}")
    
    # Filter data for this vehicle
    vehicle_data = sensor_df[sensor_df['vin'] == vin].copy()
    
    if len(vehicle_data) == 0:
        print(f"   ❌ No data found for vehicle {vin}")
        return None
    
    # Create daily aggregations for each sensor
    daily_data = vehicle_data.groupby(vehicle_data['time'].dt.date).agg({
        sensor: ['mean', 'count'] for sensor in sensors if sensor in vehicle_data.columns
    }).reset_index()
    
    # Flatten column names
    flattened_cols = ['date']
    for sensor in sensors:
        if sensor in vehicle_data.columns:
            flattened_cols.extend([f'{sensor}_mean', f'{sensor}_count'])
    
    # Handle missing sensors
    available_sensors = [s for s in sensors if s in vehicle_data.columns]
    if len(available_sensors) < 2:
        print(f"   ❌ Insufficient sensors available: {available_sensors}")
        return None
    
    # Reconstruct DataFrame with proper column names
    daily_data.columns = ['date'] + [f'{sensor}_{stat}' for sensor in available_sensors for stat in ['mean', 'count']]
    daily_data['date'] = pd.to_datetime(daily_data['date'])
    daily_data = daily_data.sort_values('date')
    
    # Filter out days with insufficient readings (require at least 3 readings per sensor per day)
    sensor_means = []
    for sensor in available_sensors:
        mean_col = f'{sensor}_mean'
        count_col = f'{sensor}_count'
        
        if mean_col in daily_data.columns and count_col in daily_data.columns:
            # Only keep days with sufficient readings
            valid_mask = daily_data[count_col] >= 3
            daily_data.loc[~valid_mask, mean_col] = np.nan
            sensor_means.append(mean_col)
    
    # Create clean multivariate DataFrame
    result_df = daily_data[['date'] + sensor_means].copy()
    result_df.columns = ['date'] + available_sensors
    
    # Remove rows where all sensors are null
    result_df = result_df.dropna(how='all', subset=available_sensors)
    
    # Forward fill small gaps (up to 3 days)
    for sensor in available_sensors:
        result_df[sensor] = result_df[sensor].fillna(method='ffill', limit=3)
    
    # Remove remaining rows with any nulls for clean multivariate analysis
    result_df = result_df.dropna()
    
    if len(result_df) < min_days:
        print(f"   ❌ Insufficient clean data: {len(result_df)} days (need {min_days})")
        return None
    
    # Remove outliers using IQR method for each sensor
    for sensor in available_sensors:
        q1 = result_df[sensor].quantile(0.25)
        q3 = result_df[sensor].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 3 * iqr
        upper_bound = q3 + 3 * iqr
        
        outlier_mask = (result_df[sensor] < lower_bound) | (result_df[sensor] > upper_bound)
        outliers_removed = outlier_mask.sum()
        
        if outliers_removed > 0:
            result_df = result_df[~outlier_mask]
            print(f"   🗑️ Removed {outliers_removed} outliers from {sensor}")
    
    print(f"   ✅ Created multivariate series: {len(result_df)} days, {len(available_sensors)} sensors")
    print(f"   📅 Date range: {result_df['date'].min()} to {result_df['date'].max()}")
    
    # Display summary statistics
    for sensor in available_sensors:
        mean_val = result_df[sensor].mean()
        std_val = result_df[sensor].std()
        print(f"   📊 {sensor}: μ={mean_val:.2f}, σ={std_val:.2f}")
    
    return result_df


def analyze_sensor_correlations(multivariate_df, vin):
    """
    Analyze cross-correlations between sensors to understand relationships.
    """
    print(f"\n📈 Analyzing sensor correlations for vehicle {vin}...")
    
    sensors = [col for col in multivariate_df.columns if col != 'date']
    
    if len(sensors) < 2:
        print("   ❌ Need at least 2 sensors for correlation analysis")
        return None
    
    # Calculate correlation matrix
    sensor_data = multivariate_df[sensors]
    correlation_matrix = sensor_data.corr()
    
    print(f"🔍 Cross-Sensor Correlations:")
    for i, sensor1 in enumerate(sensors):
        for j, sensor2 in enumerate(sensors):
            if i < j:  # Only show upper triangle
                corr = correlation_matrix.loc[sensor1, sensor2]
                if abs(corr) > 0.3:  # Only show meaningful correlations
                    direction = "positively" if corr > 0 else "negatively"
                    strength = "strongly" if abs(corr) > 0.7 else "moderately"
                    print(f"   🔗 {sensor1} & {sensor2}: {strength} {direction} correlated ({corr:+.3f})")
    
    # Identify lagged correlations (lead-lag relationships)
    print(f"\n🕒 Analyzing lead-lag relationships...")
    lag_results = {}
    
    for sensor1 in sensors:
        for sensor2 in sensors:
            if sensor1 != sensor2:
                max_corr = 0
                best_lag = 0
                
                # Check lags from -5 to +5 days
                for lag in range(-5, 6):
                    if lag == 0:
                        continue
                        
                    if lag > 0:
                        # sensor1 leads sensor2
                        s1_data = sensor_data[sensor1][:-lag]
                        s2_data = sensor_data[sensor2][lag:]
                    else:
                        # sensor2 leads sensor1  
                        s1_data = sensor_data[sensor1][-lag:]
                        s2_data = sensor_data[sensor2][:lag]
                    
                    if len(s1_data) > 10 and len(s2_data) > 10:
                        corr = np.corrcoef(s1_data, s2_data)[0, 1]
                        if not np.isnan(corr) and abs(corr) > abs(max_corr):
                            max_corr = corr
                            best_lag = lag
                
                if abs(max_corr) > 0.4:  # Only significant lag correlations
                    if best_lag > 0:
                        print(f"   ⏰ {sensor1} leads {sensor2} by {best_lag} days (r={max_corr:+.3f})")
                    else:
                        print(f"   ⏰ {sensor2} leads {sensor1} by {abs(best_lag)} days (r={max_corr:+.3f})")
                    
                    lag_results[f"{sensor1}_{sensor2}"] = {'lag': best_lag, 'correlation': max_corr}
    
    return correlation_matrix, lag_results


def build_var_model(multivariate_df, vin, forecast_horizon=30):
    """
    Build Vector Autoregression (VAR) model for multivariate forecasting.
    """
    if not STATSMODELS_AVAILABLE:
        print("❌ Statsmodels not available. Cannot build VAR model.")
        return None, None
    
    print(f"\n🤖 Building VAR model for vehicle {vin}...")
    
    sensors = [col for col in multivariate_df.columns if col != 'date']
    
    if len(sensors) < 2:
        print("   ❌ Need at least 2 sensors for VAR modeling")
        return None, None
    
    # Prepare data for VAR (remove date column)
    var_data = multivariate_df[sensors].copy()
    
    # Check stationarity and difference if needed
    print("   📊 Checking stationarity...")
    differenced_data = var_data.copy()
    differencing_applied = {}
    
    for sensor in sensors:
        # Augmented Dickey-Fuller test
        try:
            adf_result = adfuller(var_data[sensor].dropna())
            p_value = adf_result[1]
            
            if p_value > 0.05:  # Non-stationary
                print(f"   🔄 {sensor} non-stationary (p={p_value:.3f}), applying differencing")
                differenced_data[sensor] = var_data[sensor].diff()
                differencing_applied[sensor] = True
            else:
                print(f"   ✅ {sensor} stationary (p={p_value:.3f})")
                differencing_applied[sensor] = False
                
        except Exception as e:
            print(f"   ⚠️ Could not test stationarity for {sensor}: {e}")
            differencing_applied[sensor] = False
    
    # Remove NaN values created by differencing
    differenced_data = differenced_data.dropna()
    
    if len(differenced_data) < 30:
        print(f"   ❌ Insufficient data after preprocessing: {len(differenced_data)} observations")
        return None, None
    
    try:
        # Fit VAR model
        print("   🔧 Fitting VAR model...")
        var_model = VAR(differenced_data)
        
        # Select optimal lag order
        lag_order_results = var_model.select_order(maxlags=min(10, len(differenced_data)//4))
        optimal_lag = lag_order_results.aic
        
        print(f"   📈 Optimal lag order: {optimal_lag}")
        
        # Fit model with optimal lag
        var_fitted = var_model.fit(optimal_lag)
        
        # Generate forecasts
        print(f"   🔮 Generating {forecast_horizon}-day forecasts...")
        forecast_input = differenced_data.values[-optimal_lag:]
        forecast = var_fitted.forecast(forecast_input, steps=forecast_horizon)
        
        # Convert forecasts back to DataFrame
        forecast_dates = pd.date_range(
            start=multivariate_df['date'].max() + timedelta(days=1),
            periods=forecast_horizon,
            freq='D'
        )
        
        forecast_df = pd.DataFrame(forecast, columns=sensors, index=forecast_dates)
        
        # If differencing was applied, integrate forecasts back
        for sensor in sensors:
            if differencing_applied[sensor]:
                # Add back the last actual value and cumsum
                last_actual = var_data[sensor].iloc[-1]
                forecast_df[sensor] = last_actual + forecast_df[sensor].cumsum()
        
        print(f"   ✅ VAR model successfully fitted and forecast generated")
        
        return var_fitted, forecast_df
        
    except Exception as e:
        print(f"   ❌ VAR modeling failed: {e}")
        return None, None


def analyze_multivariate_forecasts(historical_df, forecast_df, vin, maintenance_df):
    """
    Analyze multivariate forecasts to identify system-level degradation patterns.
    """
    print(f"\n📊 Analyzing multivariate forecasts for vehicle {vin}...")
    
    if forecast_df is None or len(forecast_df) == 0:
        print("   ❌ No forecast data available")
        return None
    
    sensors = forecast_df.columns.tolist()
    analysis_results = {}
    
    # Get last maintenance date
    vehicle_maintenance = maintenance_df[maintenance_df['VIN Number'] == vin]
    last_maintenance = None
    days_since_maintenance = None
    
    if len(vehicle_maintenance) > 0:
        last_maintenance = vehicle_maintenance['Date of Issue'].max()
        days_since_maintenance = (pd.Timestamp.now() - last_maintenance).days
    
    print(f"   🔧 Days since last maintenance: {days_since_maintenance}")
    
    # Analyze each sensor's forecast
    for sensor in sensors:
        current_value = historical_df[sensor].iloc[-1]
        forecast_values = forecast_df[sensor]
        
        # Calculate trend metrics
        first_forecast = forecast_values.iloc[0]
        last_forecast = forecast_values.iloc[-1]
        total_change = last_forecast - current_value
        percent_change = (total_change / current_value) * 100 if current_value != 0 else 0
        
        # Assess volatility in forecast
        forecast_volatility = forecast_values.std() / forecast_values.mean() if forecast_values.mean() != 0 else 0
        
        # Trend direction and strength
        trend_direction = "increasing" if total_change > 0 else "decreasing"
        trend_strength = abs(percent_change)
        
        analysis_results[sensor] = {
            'current_value': current_value,
            'forecast_30d': last_forecast,
            'total_change': total_change,
            'percent_change': percent_change,
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'forecast_volatility': forecast_volatility
        }
        
        print(f"   📈 {sensor}:")
        print(f"      Current: {current_value:.2f} → 30-day: {last_forecast:.2f}")
        print(f"      Change: {total_change:+.2f} ({percent_change:+.1f}%)")
        print(f"      Volatility: {forecast_volatility:.3f}")
    
    # System-level risk assessment
    risk_factors = []
    
    # Check for concerning patterns
    if 'defLevelMilliPercent' in analysis_results:
        def_change = analysis_results['defLevelMilliPercent']['percent_change']
        def_current = analysis_results['defLevelMilliPercent']['current_value']
        
        if def_change < -15 or def_current < 60000:
            risk_factors.append("DEF system showing significant decline")
    
    if 'engineLoadPercent' in analysis_results:
        load_change = analysis_results['engineLoadPercent']['percent_change']
        load_volatility = analysis_results['engineLoadPercent']['forecast_volatility']
        
        if load_change > 20 or load_volatility > 0.3:
            risk_factors.append("Engine load increasing or becoming unstable")
    
    if 'engineCoolantTemperatureMilliC' in analysis_results:
        temp_change = analysis_results['engineCoolantTemperatureMilliC']['percent_change']
        temp_current = analysis_results['engineCoolantTemperatureMilliC']['current_value']
        
        if temp_change > 10 or temp_current > 90000:
            risk_factors.append("Engine temperature rising concern")
    
    # Overall system risk level
    if len(risk_factors) >= 2:
        system_risk = "HIGH"
    elif len(risk_factors) == 1:
        system_risk = "MODERATE"
    else:
        system_risk = "LOW"
    
    print(f"\n   🚨 System Risk Level: {system_risk}")
    if risk_factors:
        print(f"   ⚠️ Risk Factors:")
        for factor in risk_factors:
            print(f"      • {factor}")
    
    return {
        'vin': vin,
        'system_risk': system_risk,
        'risk_factors': risk_factors,
        'sensor_analyses': analysis_results,
        'days_since_maintenance': days_since_maintenance,
        'last_maintenance': last_maintenance
    }


def create_multivariate_visualization(historical_df, forecast_df, correlation_matrix, vin, system_analysis):
    """
    Create comprehensive visualization of multivariate analysis.
    """
    if forecast_df is None:
        print("❌ No forecast data to visualize")
        return
    
    sensors = list(forecast_df.columns)
    n_sensors = len(sensors)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 15))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    fig.suptitle(f'Multivariate Analysis: Vehicle {vin} - System Risk: {system_analysis["system_risk"]}', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1-3: Individual sensor forecasts
    for i, sensor in enumerate(sensors[:3]):
        ax = fig.add_subplot(gs[0, i])
        
        # Historical data (last 60 days)
        hist_recent = historical_df.tail(60)
        ax.plot(hist_recent['date'], hist_recent[sensor], 
                label='Historical', color='blue', linewidth=2)
        
        # Forecast data
        forecast_dates = forecast_df.index
        ax.plot(forecast_dates, forecast_df[sensor], 
                label='Forecast', color='red', linewidth=2, linestyle='--')
        
        # Current value marker
        current_val = historical_df[sensor].iloc[-1]
        current_date = historical_df['date'].iloc[-1]
        ax.scatter([current_date], [current_val], color='green', s=100, 
                  label='Current', zorder=5)
        
        ax.set_title(f'{sensor}')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    # Plot 4: Correlation heatmap
    ax_corr = fig.add_subplot(gs[1, 0])
    if correlation_matrix is not None and len(correlation_matrix) > 1:
        sns.heatmap(correlation_matrix, annot=True, cmap='RdBu_r', center=0,
                    square=True, fmt='.2f', ax=ax_corr)
        ax_corr.set_title('Sensor Correlations')
    
    # Plot 5: Risk assessment summary
    ax_risk = fig.add_subplot(gs[1, 1])
    risk_colors = {'LOW': 'green', 'MODERATE': 'orange', 'HIGH': 'red'}
    risk_color = risk_colors.get(system_analysis['system_risk'], 'gray')
    
    ax_risk.text(0.5, 0.7, f"System Risk Level", ha='center', va='center',
                fontsize=14, fontweight='bold', transform=ax_risk.transAxes)
    ax_risk.text(0.5, 0.5, system_analysis['system_risk'], ha='center', va='center',
                fontsize=20, fontweight='bold', color=risk_color, 
                transform=ax_risk.transAxes)
    
    if system_analysis['risk_factors']:
        risk_text = '\n'.join([f"• {factor}" for factor in system_analysis['risk_factors'][:3]])
        ax_risk.text(0.5, 0.2, risk_text, ha='center', va='center',
                    fontsize=10, transform=ax_risk.transAxes)
    
    ax_risk.set_xlim(0, 1)
    ax_risk.set_ylim(0, 1)
    ax_risk.axis('off')
    
    # Plot 6: Maintenance timeline
    ax_maint = fig.add_subplot(gs[1, 2])
    if system_analysis['days_since_maintenance']:
        days = system_analysis['days_since_maintenance']
        ax_maint.text(0.5, 0.7, f"Days Since\nLast Maintenance", ha='center', va='center',
                     fontsize=12, fontweight='bold', transform=ax_maint.transAxes)
        ax_maint.text(0.5, 0.4, f"{days}", ha='center', va='center',
                     fontsize=24, fontweight='bold', transform=ax_maint.transAxes)
        
        # Color code based on days
        if days > 365:
            color = 'red'
            status = 'Overdue'
        elif days > 180:
            color = 'orange'
            status = 'Due Soon'
        else:
            color = 'green'
            status = 'Recent'
        
        ax_maint.text(0.5, 0.2, status, ha='center', va='center',
                     fontsize=12, color=color, fontweight='bold',
                     transform=ax_maint.transAxes)
    
    ax_maint.set_xlim(0, 1)
    ax_maint.set_ylim(0, 1)
    ax_maint.axis('off')
    
    # Plot 7-9: Sensor trend analysis
    for i, sensor in enumerate(sensors[:3]):
        if i < 3:
            ax = fig.add_subplot(gs[2, i])
            
            sensor_analysis = system_analysis['sensor_analyses'].get(sensor, {})
            
            # Create trend visualization
            values = [sensor_analysis.get('current_value', 0), 
                     sensor_analysis.get('forecast_30d', 0)]
            labels = ['Current', '30-Day\nForecast']
            
            bars = ax.bar(labels, values, color=['blue', 'red'], alpha=0.7)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            # Add trend arrow
            change = sensor_analysis.get('percent_change', 0)
            if abs(change) > 5:  # Significant change
                arrow_props = dict(arrowstyle='->', lw=2, 
                                 color='red' if change < 0 else 'green')
                ax.annotate(f'{change:+.1f}%', xy=(1, values[1]), xytext=(0.5, max(values)*1.1),
                           arrowprops=arrow_props, ha='center', fontweight='bold')
            
            ax.set_title(f'{sensor} Trend')
            ax.set_ylabel('Value')
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{vin}_multivariate_trends.png", dpi=300, bbox_inches='tight')
    plt.close()


def create_fleet_risk_summary(all_analyses):
    """Create comprehensive fleet-wide risk summary and prioritization."""
    if not all_analyses:
        return
    
    print(f"\n🏭 FLEET-WIDE RISK ASSESSMENT SUMMARY")
    print(f"="*65)
    
    # Sort by risk level and urgency
    risk_priority = {'HIGH': 3, 'MODERATE': 2, 'LOW': 1}
    sorted_analyses = sorted(all_analyses, 
                           key=lambda x: (risk_priority.get(x['system_risk'], 0), 
                                        x['days_since_maintenance']), 
                           reverse=True)
    
    # Risk level counts
    risk_counts = {}
    maintenance_overdue = 0
    total_vehicles = len(all_analyses)
    
    for analysis in all_analyses:
        risk = analysis['system_risk']
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        if analysis['days_since_maintenance'] and analysis['days_since_maintenance'] > 365:
            maintenance_overdue += 1
    
    print(f"📊 Fleet Risk Distribution ({total_vehicles} vehicles analyzed):")
    for risk in ['HIGH', 'MODERATE', 'LOW']:
        count = risk_counts.get(risk, 0)
        percentage = (count / total_vehicles) * 100 if total_vehicles > 0 else 0
        emoji = {'HIGH': '🚨', 'MODERATE': '⚠️', 'LOW': '✅'}[risk]
        if count > 0:
            print(f"   {emoji} {risk} Risk: {count} vehicles ({percentage:.1f}%)")
    
    print(f"\n🔧 Maintenance Status:")
    print(f"   🔴 Overdue (>365 days): {maintenance_overdue} vehicles")
    print(f"   🟡 Due Soon (180-365 days): {len([a for a in all_analyses if a['days_since_maintenance'] and 180 < a['days_since_maintenance'] <= 365])} vehicles")
    print(f"   🟢 Recent (<180 days): {len([a for a in all_analyses if a['days_since_maintenance'] and a['days_since_maintenance'] <= 180])} vehicles")
    
    # Top 10 highest risk vehicles
    print(f"\n🚨 TOP 10 HIGHEST RISK VEHICLES - IMMEDIATE ACTION REQUIRED:")
    print(f"{'Rank':<4} {'VIN':<17} {'Risk':<8} {'Days Since Maint':<15} {'Primary Concerns'}")
    print(f"{'-'*4} {'-'*17} {'-'*8} {'-'*15} {'-'*50}")
    
    for i, analysis in enumerate(sorted_analyses[:10]):
        risk_emoji = {'HIGH': '🚨', 'MODERATE': '⚠️', 'LOW': '✅'}[analysis['system_risk']]
        primary_concern = analysis['risk_factors'][0] if analysis['risk_factors'] else 'System monitoring'
        maint_days = analysis['days_since_maintenance'] if analysis['days_since_maintenance'] else 'Unknown'
        
        print(f"{i+1:<4} {analysis['vin']:<17} {risk_emoji} {analysis['system_risk']:<6} {maint_days:<15} {primary_concern}")
    
    # Fleet-wide patterns
    print(f"\n📈 Fleet-Wide Degradation Patterns:")
    
    # Count common risk factors
    all_risk_factors = []
    for analysis in all_analyses:
        all_risk_factors.extend(analysis['risk_factors'])
    
    from collections import Counter
    risk_factor_counts = Counter(all_risk_factors)
    
    print(f"   Most Common Issues Across Fleet:")
    for factor, count in risk_factor_counts.most_common(5):
        percentage = (count / total_vehicles) * 100
        print(f"   • {factor}: {count} vehicles ({percentage:.1f}%)")
    
    # Business impact estimation
    high_risk_count = risk_counts.get('HIGH', 0)
    moderate_risk_count = risk_counts.get('MODERATE', 0)
    
    estimated_cost_per_breakdown = 5000  # Average DPF replacement cost
    estimated_preventive_cost = 1200    # Average preventive maintenance cost
    
    potential_breakdown_cost = (high_risk_count * 0.8 + moderate_risk_count * 0.3) * estimated_cost_per_breakdown
    preventive_maintenance_cost = (high_risk_count + moderate_risk_count) * estimated_preventive_cost
    potential_savings = potential_breakdown_cost - preventive_maintenance_cost
    
    print(f"\n💰 Business Impact Assessment:")
    print(f"   🚨 Potential breakdown costs: ${potential_breakdown_cost:,.0f}")
    print(f"   🔧 Preventive maintenance costs: ${preventive_maintenance_cost:,.0f}")
    print(f"   💵 Potential savings with action: ${potential_savings:,.0f}")
    print(f"   📊 ROI of predictive maintenance: {(potential_savings/preventive_maintenance_cost)*100:.0f}%")


def main():
    """Main comprehensive multivariate forecasting pipeline."""
    print("🚀 COMPREHENSIVE FLEET MULTIVARIATE FORECASTING FOR DPF RUL")
    print("="*70)
    
    # Load datasets
    maintenance_df, sensor_df = load_dpf_datasets()
    
    # Identify ALL viable vehicles for multivariate analysis
    all_vehicles = identify_all_viable_vehicles(maintenance_df, sensor_df)
    
    if not all_vehicles:
        print("❌ No vehicles identified for multivariate analysis")
        return
    
    print(f"\n🎯 Analyzing ALL {len(all_vehicles)} viable vehicles for comprehensive fleet assessment")
    
    # Key sensors for multivariate modeling
    multivariate_sensors = [
        'defLevelMilliPercent',
        'engineLoadPercent',
        'engineCoolantTemperatureMilliC'
    ]
    
    # Perform multivariate analysis for ALL vehicles
    all_analyses = []
    successful_analyses = 0
    
    for i, vin in enumerate(all_vehicles):
        print(f"\n{'='*70}")
        print(f"📊 ANALYZING VEHICLE {i+1}/{len(all_vehicles)}: {vin}")
        print(f"{'='*70}")
        
        try:
            # Prepare multivariate time series
            multivariate_df = prepare_multivariate_time_series(
                sensor_df, vin, multivariate_sensors
            )
            
            if multivariate_df is None:
                print(f"   ⏭️ Skipping {vin} - insufficient multivariate data")
                continue
            
            # Analyze sensor correlations (brief output for fleet analysis)
            correlation_matrix, lag_results = analyze_sensor_correlations(multivariate_df, vin)
            
            # Build VAR model and generate forecasts
            var_model, forecast_df = build_var_model(multivariate_df, vin)
            
            # Analyze forecasts for system-level insights
            system_analysis = analyze_multivariate_forecasts(
                multivariate_df, forecast_df, vin, maintenance_df
            )
            
            if system_analysis:
                all_analyses.append(system_analysis)
                successful_analyses += 1
                
                # Only create detailed visualizations for HIGH risk vehicles
                if system_analysis['system_risk'] == 'HIGH':
                    create_multivariate_visualization(
                        multivariate_df, forecast_df, correlation_matrix, vin, system_analysis
                    )
                    
                print(f"   ✅ Risk Assessment: {system_analysis['system_risk']} ({len(system_analysis['risk_factors'])} factors)")
            
        except Exception as e:
            print(f"   ❌ Analysis failed for {vin}: {e}")
            continue
    
    print(f"\n🎉 COMPREHENSIVE FLEET MULTIVARIATE ANALYSIS COMPLETE!")
    print(f"="*70)
    print(f"📊 Analysis Results: {successful_analyses}/{len(all_vehicles)} vehicles successfully analyzed")
    
    if all_analyses:
        # Create comprehensive fleet-wide risk summary
        create_fleet_risk_summary(all_analyses)
        
        print(f"\n💡 Key Insights from Fleet-Wide Multivariate Analysis:")
        print(f"   🔗 Sensor interactions reveal system-level degradation patterns across fleet")
        print(f"   📈 VAR models capture cross-sensor relationships missed by univariate analysis")
        print(f"   🎯 System-level risk assessment provides holistic fleet health view")
        print(f"   🏭 Fleet-wide patterns identify common maintenance issues and priorities")
        
    else:
        print("❌ No successful multivariate analyses completed")
    
    print(f"\n📋 Immediate Action Items:")
    if all_analyses:
        high_risk_count = len([a for a in all_analyses if a['system_risk'] == 'HIGH'])
        moderate_risk_count = len([a for a in all_analyses if a['system_risk'] == 'MODERATE'])
        
        if high_risk_count > 0:
            print(f"   🚨 URGENT: Schedule immediate maintenance for {high_risk_count} HIGH risk vehicles")
        if moderate_risk_count > 0:
            print(f"   ⚠️ PRIORITY: Implement enhanced monitoring for {moderate_risk_count} MODERATE risk vehicles")
        
        print(f"   📈 STRATEGIC: Use fleet patterns to optimize maintenance scheduling")
        print(f"   💰 FINANCIAL: Implement predictive maintenance to achieve estimated ROI")
    
    print(f"\n📋 Next Analysis Steps:")
    print(f"   1. Threshold-based RUL predictions using forecasted trends (Script 3)")
    print(f"   2. Hierarchical forecasting by vehicle type/model (Script 4)")
    print(f"   3. Advanced RUL with survival analysis concepts (Script 5)")


if __name__ == "__main__":
    main()