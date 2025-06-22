"""
Data exploration script for DPF maintenance analysis
Explores patterns in vehicle sensor data leading to maintenance events
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def load_processed_data():
    """Load the processed DPF datasets"""
    print("Loading processed DPF datasets...")
    
    dpf_maintenance = pd.read_csv('data/dpf_maintenance_records.csv')
    dpf_vehicle_stats = pd.read_csv('data/dpf_vehicle_stats.csv')
    dpf_diagnostic = pd.read_csv('data/dpf_diagnostic_data.csv')
    
    # Convert time columns and handle timezone
    dpf_maintenance['Date of Issue'] = pd.to_datetime(dpf_maintenance['Date of Issue']).dt.tz_localize(None)
    dpf_vehicle_stats['time'] = pd.to_datetime(dpf_vehicle_stats['time']).dt.tz_localize(None)
    dpf_diagnostic['Time'] = pd.to_datetime(dpf_diagnostic['Time'], errors='coerce')
    
    print(f"Maintenance records: {len(dpf_maintenance)}")
    print(f"Vehicle stats records: {len(dpf_vehicle_stats)}")
    print(f"Diagnostic records: {len(dpf_diagnostic)}")
    
    return dpf_maintenance, dpf_vehicle_stats, dpf_diagnostic

def explore_maintenance_patterns(dpf_maintenance):
    """Explore maintenance event patterns"""
    print("\n=== MAINTENANCE PATTERNS ===")
    
    # Maintenance frequency by vehicle
    vehicle_counts = dpf_maintenance['Vehicle_Number'].value_counts()
    print(f"\nVehicles with most DPF issues:")
    print(vehicle_counts.head(10))
    
    # Maintenance by job type
    print(f"\nMaintenance by job description:")
    print(dpf_maintenance['lines_jobDescriptions'].value_counts())
    
    # Maintenance costs
    if 'Total_Cost' in dpf_maintenance.columns:
        maintenance_costs = dpf_maintenance.groupby('lines_jobDescriptions')['Total_Cost'].agg(['count', 'mean', 'std', 'min', 'max']).round(2)
        print(f"\nMaintenance costs by job type:")
        print(maintenance_costs)
    
    # Downtime analysis
    if 'Downtime Days' in dpf_maintenance.columns:
        downtime_stats = dpf_maintenance.groupby('lines_jobDescriptions')['Downtime Days'].agg(['mean', 'std', 'min', 'max']).round(2)
        print(f"\nDowntime by job type:")
        print(downtime_stats)
    
    return vehicle_counts

def explore_vehicle_stats_patterns(dpf_vehicle_stats, vehicle_counts):
    """Explore vehicle statistics patterns"""
    print("\n=== VEHICLE STATISTICS PATTERNS ===")
    
    # Data availability by sensor
    sensor_cols = [col for col in dpf_vehicle_stats.columns if col not in ['time', 'vin']]
    data_availability = {}
    
    for col in sensor_cols:
        non_null_count = dpf_vehicle_stats[col].notna().sum()
        total_count = len(dpf_vehicle_stats)
        data_availability[col] = {
            'non_null_count': non_null_count,
            'availability_pct': (non_null_count / total_count) * 100
        }
    
    # Sort by availability
    availability_df = pd.DataFrame(data_availability).T
    availability_df = availability_df.sort_values('availability_pct', ascending=False)
    
    print(f"\nSensor data availability (top 15):")
    print(availability_df.head(15))
    
    # Focus on high-availability sensors relevant to DPF
    key_sensors = [
        'engineLoadPercent', 'engineRpm', 'ecuSpeedMph', 
        'engineOilPressureKPa', 'engineCoolantTemperatureMilliC',
        'ambientAirTemperatureMilliC', 'intakeManifoldTemperatureMilliC',
        'barometricPressurePa', 'fuelPercents', 'defLevelMilliPercent'
    ]
    
    available_key_sensors = [sensor for sensor in key_sensors if sensor in availability_df.index and availability_df.loc[sensor, 'availability_pct'] > 1]
    print(f"\nKey DPF-relevant sensors with >1% data availability:")
    for sensor in available_key_sensors:
        pct = availability_df.loc[sensor, 'availability_pct']
        print(f"- {sensor}: {pct:.2f}%")
    
    return available_key_sensors, availability_df

def explore_diagnostic_patterns(dpf_diagnostic):
    """Explore diagnostic data patterns"""
    print("\n=== DIAGNOSTIC PATTERNS ===")
    
    # Diagnostic types
    diagnostic_counts = dpf_diagnostic['Diagnostic'].value_counts()
    print(f"\nTop diagnostic parameters:")
    print(diagnostic_counts.head(15))
    
    # Focus on DPF-related diagnostics
    dpf_related_diagnostics = dpf_diagnostic[
        dpf_diagnostic['Diagnostic'].str.contains('Exhaust|DPF|Particulate|EGR|NOx', case=False, na=False)
    ]
    
    if len(dpf_related_diagnostics) > 0:
        print(f"\nDPF-related diagnostic parameters:")
        print(dpf_related_diagnostics['Diagnostic'].value_counts())
        
        # Check for non-null values in DPF diagnostics
        dpf_with_values = dpf_related_diagnostics[dpf_related_diagnostics['Value'].notna()]
        print(f"\nDPF diagnostics with actual values: {len(dpf_with_values)}")
        
        if len(dpf_with_values) > 0:
            print("Sample DPF diagnostic values:")
            print(dpf_with_values[['Asset Name', 'Diagnostic', 'Value', 'Unit']].head(10))
    
    return diagnostic_counts

def analyze_maintenance_timing(dpf_maintenance, dpf_vehicle_stats, available_sensors):
    """Analyze sensor patterns before maintenance events"""
    print("\n=== MAINTENANCE TIMING ANALYSIS ===")
    
    # For each maintenance event, look at sensor data in the weeks before
    results = []
    
    for idx, maintenance_event in dpf_maintenance.iterrows():
        vin = maintenance_event['VIN Number']
        vehicle_num = maintenance_event['Vehicle_Number']
        maintenance_date = maintenance_event['Date of Issue']
        job_type = maintenance_event['lines_jobDescriptions']
        
        if pd.isna(maintenance_date) or pd.isna(vin):
            continue
            
        # Get sensor data for this vehicle
        vehicle_data = dpf_vehicle_stats[dpf_vehicle_stats['vin'] == vin].copy()
        
        if len(vehicle_data) == 0:
            continue
            
        # Look at data 30 days before maintenance
        start_date = maintenance_date - timedelta(days=30)
        pre_maintenance_data = vehicle_data[
            (vehicle_data['time'] >= start_date) & 
            (vehicle_data['time'] < maintenance_date)
        ]
        
        if len(pre_maintenance_data) == 0:
            continue
            
        # Calculate statistics for available sensors
        sensor_stats = {}
        for sensor in available_sensors:
            if sensor in pre_maintenance_data.columns:
                sensor_data = pre_maintenance_data[sensor].dropna()
                if len(sensor_data) > 0:
                    sensor_stats[sensor] = {
                        'mean': sensor_data.mean(),
                        'std': sensor_data.std(),
                        'min': sensor_data.min(),
                        'max': sensor_data.max(),
                        'count': len(sensor_data)
                    }
        
        results.append({
            'vin': vin,
            'vehicle_number': vehicle_num,
            'maintenance_date': maintenance_date,
            'job_type': job_type,
            'days_of_data': len(pre_maintenance_data),
            'sensor_stats': sensor_stats
        })
    
    print(f"Analyzed {len(results)} maintenance events with pre-maintenance sensor data")
    
    # Aggregate patterns by job type
    job_type_patterns = {}
    for result in results:
        job_type = result['job_type']
        if job_type not in job_type_patterns:
            job_type_patterns[job_type] = {'events': [], 'sensor_data': {}}
        
        job_type_patterns[job_type]['events'].append(result)
        
        # Aggregate sensor statistics
        for sensor, stats in result['sensor_stats'].items():
            if sensor not in job_type_patterns[job_type]['sensor_data']:
                job_type_patterns[job_type]['sensor_data'][sensor] = []
            job_type_patterns[job_type]['sensor_data'][sensor].append(stats['mean'])
    
    # Print patterns for each job type
    for job_type, patterns in job_type_patterns.items():
        print(f"\n--- {job_type} ---")
        print(f"Events analyzed: {len(patterns['events'])}")
        
        for sensor, values in patterns['sensor_data'].items():
            if len(values) > 2:  # Only show sensors with enough data
                avg_value = np.mean(values)
                std_value = np.std(values)
                print(f"{sensor}: avg={avg_value:.2f}, std={std_value:.2f}, n={len(values)}")
    
    return results, job_type_patterns

def main():
    """Main exploration pipeline"""
    print("=== DPF DATA EXPLORATION ===")
    
    # Load processed data
    dpf_maintenance, dpf_vehicle_stats, dpf_diagnostic = load_processed_data()
    
    # Explore patterns
    vehicle_counts = explore_maintenance_patterns(dpf_maintenance)
    available_sensors, availability_df = explore_vehicle_stats_patterns(dpf_vehicle_stats, vehicle_counts)
    diagnostic_counts = explore_diagnostic_patterns(dpf_diagnostic)
    
    # Analyze timing patterns
    timing_results, job_patterns = analyze_maintenance_timing(
        dpf_maintenance, dpf_vehicle_stats, available_sensors
    )
    
    print("\n=== EXPLORATION COMPLETE ===")
    print(f"Key findings:")
    print(f"- {len(dpf_maintenance)} DPF maintenance events across {dpf_maintenance['Vehicle_Number'].nunique()} vehicles")
    print(f"- {len(available_sensors)} key sensors with >1% data availability")
    print(f"- {len(timing_results)} maintenance events have pre-maintenance sensor data")
    print(f"- {len(job_patterns)} different job types analyzed")

if __name__ == "__main__":
    main()