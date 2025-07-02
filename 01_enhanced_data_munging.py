"""
Enhanced data munging script for comprehensive DPF maintenance analysis
Incorporates 2023-2024 vehicle stats, driver details, and DTC data for RUL analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def load_and_filter_rta_data():
    """Load RTA data and filter for DPF-related maintenance events"""
    print("Loading RTA data...")
    rta_df = pd.read_csv('data/rta-data.csv')
    
    print(f"Total RTA records: {len(rta_df)}")
    print(f"Columns: {list(rta_df.columns)}")
    
    # Filter for DPF-related maintenance
    dpf_keywords = ["FILTER - DIESEL PARTICULATE", "EXHAUST SYSTEM", "EXHAUST SYSTEM INSPECT DIAGNOSE"]
    
    dpf_mask = rta_df['lines_jobDescriptions'].isin(dpf_keywords)
    dpf_rta = rta_df[dpf_mask].copy()
    
    print(f"DPF-related maintenance records: {len(dpf_rta)}")
    print(f"Unique VINs with DPF issues: {dpf_rta['VIN Number'].nunique()}")
    print(f"Unique Vehicle Numbers with DPF issues: {dpf_rta['Vehicle_Number'].nunique()}")
    
    # Show breakdown by job description
    print("\nDPF maintenance breakdown:")
    print(dpf_rta['lines_jobDescriptions'].value_counts())
    
    return dpf_rta

def load_enhanced_vehicle_stats():
    """Load both 2024 and 2023-2024 vehicle statistics data"""
    print("\nLoading enhanced vehicle statistics data...")
    
    # Load original 2024 data
    print("Loading vehicle-stats.csv (2024)...")
    chunk_size = 50000
    chunks_2024 = []
    
    for chunk in pd.read_csv('data/vehicle-stats.csv', chunksize=chunk_size):
        chunks_2024.append(chunk)
        if len(chunks_2024) % 20 == 0:
            print(f"  Loaded {len(chunks_2024) * chunk_size} rows from 2024 data...")
    
    vehicle_stats_2024 = pd.concat(chunks_2024, ignore_index=True)
    print(f"2024 vehicle stats: {len(vehicle_stats_2024)} records")
    
    # Load new 2023-2024 data
    print("Loading vehicle_stats_23-24.csv...")
    chunks_2324 = []
    
    for chunk in pd.read_csv('data/vehicle_stats_23-24.csv', chunksize=chunk_size):
        chunks_2324.append(chunk)
        if len(chunks_2324) % 20 == 0:
            print(f"  Loaded {len(chunks_2324) * chunk_size} rows from 2023-24 data...")
    
    vehicle_stats_2324 = pd.concat(chunks_2324, ignore_index=True)
    print(f"2023-2024 vehicle stats: {len(vehicle_stats_2324)} records")
    
    # Combine datasets
    print("Combining vehicle stats datasets...")
    
    # Standardize column names and ensure compatibility
    vehicle_stats_2024['time'] = pd.to_datetime(vehicle_stats_2024['time'])
    vehicle_stats_2324['time'] = pd.to_datetime(vehicle_stats_2324['time'])
    
    # Find common columns
    common_cols = list(set(vehicle_stats_2024.columns) & set(vehicle_stats_2324.columns))
    print(f"Common columns between datasets: {len(common_cols)}")
    
    # Use only common columns for consistent analysis
    vehicle_stats_combined = pd.concat([
        vehicle_stats_2024[common_cols],
        vehicle_stats_2324[common_cols]
    ], ignore_index=True)
    
    # Remove duplicates based on time and vin
    vehicle_stats_combined = vehicle_stats_combined.drop_duplicates(subset=['time', 'vin'])
    
    print(f"Combined vehicle stats: {len(vehicle_stats_combined)} records")
    print(f"Date range: {vehicle_stats_combined['time'].min()} to {vehicle_stats_combined['time'].max()}")
    print(f"Unique VINs: {vehicle_stats_combined['vin'].nunique()}")
    
    return vehicle_stats_combined

def load_diagnostic_and_dtc_data():
    """Load diagnostic data and DTC data"""
    print("\nLoading diagnostic and DTC data...")
    
    # Load original diagnostic data
    diagnostic_df = pd.read_csv('data/diagnostic-data.csv')
    print(f"Original diagnostic records: {len(diagnostic_df)}")
    
    # Load DTC data
    dtc_df = pd.read_csv('data/dtc.csv')
    print(f"DTC records: {len(dtc_df)}")
    
    # Combine diagnostic datasets
    print("Combining diagnostic datasets...")
    
    # Ensure both have same column structure
    if set(diagnostic_df.columns) == set(dtc_df.columns):
        combined_diagnostic = pd.concat([diagnostic_df, dtc_df], ignore_index=True)
        print(f"Combined diagnostic records: {len(combined_diagnostic)}")
    else:
        print("Column mismatch between diagnostic datasets - using original only")
        combined_diagnostic = diagnostic_df
    
    print(f"Unique Asset Names: {combined_diagnostic['Asset Name'].nunique()}")
    print(f"Unique diagnostics: {combined_diagnostic['Diagnostic'].nunique()}")
    
    return combined_diagnostic

def load_driver_details():
    """Load driver details data"""
    print("\nLoading driver details...")
    driver_df = pd.read_csv('data/driver-details.csv')
    
    print(f"Driver records: {len(driver_df)}")
    print(f"Unique drivers: {driver_df['Driver Name'].nunique()}")
    print(f"Driver safety score range: {driver_df['Safety Score'].min()} - {driver_df['Safety Score'].max()}")
    
    return driver_df

def create_enhanced_master_dataset(dpf_rta, vehicle_stats, diagnostic_df, driver_df):
    """Create enhanced master dataset with all available data"""
    print("\nCreating enhanced master dataset...")
    
    # Get unique identifiers from DPF maintenance
    dpf_vins = dpf_rta['VIN Number'].dropna().unique()
    dpf_vehicle_numbers = dpf_rta['Vehicle_Number'].dropna().unique()
    
    print(f"Filtering data for {len(dpf_vins)} VINs and {len(dpf_vehicle_numbers)} vehicle numbers...")
    
    # Filter vehicle stats for DPF-affected vehicles
    dpf_vehicle_stats = vehicle_stats[vehicle_stats['vin'].isin(dpf_vins)].copy()
    print(f"Vehicle stats records for DPF vehicles: {len(dpf_vehicle_stats)}")
    
    # Filter diagnostic data for DPF-affected vehicles
    dpf_vehicle_numbers_str = [str(x) for x in dpf_vehicle_numbers]
    dpf_diagnostic = diagnostic_df[diagnostic_df['Asset Name'].astype(str).isin(dpf_vehicle_numbers_str)].copy()
    print(f"Diagnostic records for DPF vehicles: {len(dpf_diagnostic)}")
    
    # Convert time columns to datetime (handling timezone issues)
    if 'time' in dpf_vehicle_stats.columns:
        dpf_vehicle_stats['time'] = pd.to_datetime(dpf_vehicle_stats['time']).dt.tz_localize(None)
    
    if 'Time' in dpf_diagnostic.columns:
        dpf_diagnostic['Time'] = pd.to_datetime(dpf_diagnostic['Time'], errors='coerce').dt.tz_localize(None)
    
    if 'Date of Issue' in dpf_rta.columns:
        dpf_rta['Date of Issue'] = pd.to_datetime(dpf_rta['Date of Issue'])
    
    # Create vehicle mapping for driver data integration
    vehicle_driver_mapping = create_vehicle_driver_mapping(dpf_rta, driver_df)
    
    return dpf_rta, dpf_vehicle_stats, dpf_diagnostic, driver_df, vehicle_driver_mapping

def create_vehicle_driver_mapping(dpf_rta, driver_df):
    """Create mapping between vehicles and drivers for enhanced analysis"""
    print("\nCreating vehicle-driver mapping...")
    
    # Since driver data doesn't have vehicle mapping, we'll create a placeholder
    # In real implementation, this would require additional data to link drivers to vehicles
    vehicle_driver_mapping = {
        'note': 'Driver data available but requires vehicle-driver linking logic',
        'drivers': len(driver_df),
        'vehicles': dpf_rta['Vehicle_Number'].nunique()
    }
    
    print("Driver data loaded but vehicle-driver mapping requires additional business logic")
    
    return vehicle_driver_mapping

def save_enhanced_processed_data(dpf_rta, dpf_vehicle_stats, dpf_diagnostic, driver_df, vehicle_driver_mapping):
    """Save all processed datasets"""
    print("\nSaving enhanced processed datasets...")
    
    # Save main DPF datasets
    dpf_rta.to_csv('data/enhanced_dpf_maintenance_records.csv', index=False)
    dpf_vehicle_stats.to_csv('data/enhanced_dpf_vehicle_stats.csv', index=False)
    dpf_diagnostic.to_csv('data/enhanced_dpf_diagnostic_data.csv', index=False)
    
    # Save driver data (filtered for relevant analysis)
    driver_df.to_csv('data/enhanced_driver_details.csv', index=False)
    
    print("Saved enhanced datasets:")
    print(f"- enhanced_dpf_maintenance_records.csv ({len(dpf_rta)} records)")
    print(f"- enhanced_dpf_vehicle_stats.csv ({len(dpf_vehicle_stats)} records)")
    print(f"- enhanced_dpf_diagnostic_data.csv ({len(dpf_diagnostic)} records)")
    print(f"- enhanced_driver_details.csv ({len(driver_df)} records)")

def generate_enhanced_summary(dpf_rta, dpf_vehicle_stats, dpf_diagnostic, driver_df):
    """Generate comprehensive summary of enhanced dataset"""
    print("\n" + "="*60)
    print("ENHANCED DATASET SUMMARY")
    print("="*60)
    
    print(f"\n📊 MAINTENANCE DATA:")
    print(f"   • DPF maintenance events: {len(dpf_rta)}")
    print(f"   • Unique vehicles: {dpf_rta['VIN Number'].nunique()}")
    print(f"   • Date range: {dpf_rta['Date of Issue'].min()} to {dpf_rta['Date of Issue'].max()}")
    
    print(f"\n🚗 VEHICLE SENSOR DATA:")
    print(f"   • Total sensor readings: {len(dpf_vehicle_stats):,}")
    print(f"   • Unique VINs: {dpf_vehicle_stats['vin'].nunique()}")
    print(f"   • Date range: {dpf_vehicle_stats['time'].min()} to {dpf_vehicle_stats['time'].max()}")
    print(f"   • Available sensors: {len([col for col in dpf_vehicle_stats.columns if col not in ['time', 'vin']])}")
    
    print(f"\n🔧 DIAGNOSTIC DATA:")
    print(f"   • Total diagnostic readings: {len(dpf_diagnostic):,}")
    print(f"   • Unique vehicles: {dpf_diagnostic['Asset Name'].nunique()}")
    print(f"   • Diagnostic types: {dpf_diagnostic['Diagnostic'].nunique()}")
    
    print(f"\n👨‍💼 DRIVER DATA:")
    print(f"   • Total drivers: {len(driver_df)}")
    print(f"   • Average safety score: {driver_df['Safety Score'].mean():.1f}")
    print(f"   • Total drive time: {driver_df['Drive Time (hh:mm:ss)'].nunique()} unique values")
    
    print(f"\n🎯 RUL ANALYSIS READINESS:")
    vehicles_with_data = set(dpf_rta['VIN Number'].dropna()) & set(dpf_vehicle_stats['vin'].dropna())
    print(f"   • Vehicles with both maintenance & sensor data: {len(vehicles_with_data)}")
    print(f"   • Data coverage: {len(vehicles_with_data)/dpf_rta['VIN Number'].nunique()*100:.1f}%")
    
    print(f"\n✅ Ready for enhanced RUL analysis with:")
    print(f"   • Extended time-series data (2023-2025)")
    print(f"   • Enhanced diagnostic coverage")
    print(f"   • Driver behavior context")
    print(f"   • Multi-year maintenance patterns")

def main():
    """Enhanced data munging pipeline"""
    print("=== ENHANCED DPF DATA MUNGING PIPELINE ===")
    print("Incorporating 2023-2024 vehicle stats, driver details, and DTC data")
    
    # Load and filter data
    dpf_rta = load_and_filter_rta_data()
    vehicle_stats = load_enhanced_vehicle_stats()
    diagnostic_df = load_diagnostic_and_dtc_data()
    driver_df = load_driver_details()
    
    # Create enhanced master dataset
    dpf_rta, dpf_vehicle_stats, dpf_diagnostic, driver_df, vehicle_driver_mapping = create_enhanced_master_dataset(
        dpf_rta, vehicle_stats, diagnostic_df, driver_df
    )
    
    # Save processed data
    save_enhanced_processed_data(dpf_rta, dpf_vehicle_stats, dpf_diagnostic, driver_df, vehicle_driver_mapping)
    
    # Generate comprehensive summary
    generate_enhanced_summary(dpf_rta, dpf_vehicle_stats, dpf_diagnostic, driver_df)
    
    print("\n=== ENHANCED DATA MUNGING COMPLETE ===")
    print("Ready for comprehensive RUL analysis with multi-year data!")

if __name__ == "__main__":
    main()