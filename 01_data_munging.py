"""
Data munging script for DPF maintenance analysis
Filters RTA data for DPF-related maintenance and creates master dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path

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

def load_vehicle_stats():
    """Load vehicle statistics data"""
    print("\nLoading vehicle statistics data...")
    
    # Load in chunks due to large file size
    chunk_size = 50000
    chunks = []
    
    for chunk in pd.read_csv('data/vehicle-stats.csv', chunksize=chunk_size):
        chunks.append(chunk)
        if len(chunks) % 10 == 0:
            print(f"Loaded {len(chunks) * chunk_size} rows...")
    
    vehicle_stats = pd.concat(chunks, ignore_index=True)
    print(f"Total vehicle stats records: {len(vehicle_stats)}")
    print(f"Unique VINs in vehicle stats: {vehicle_stats['vin'].nunique()}")
    
    return vehicle_stats

def load_diagnostic_data():
    """Load diagnostic data"""
    print("\nLoading diagnostic data...")
    diagnostic_df = pd.read_csv('data/diagnostic-data.csv')
    
    print(f"Total diagnostic records: {len(diagnostic_df)}")
    print(f"Unique Asset Names: {diagnostic_df['Asset Name'].nunique()}")
    
    return diagnostic_df

def create_master_dataset(dpf_rta, vehicle_stats, diagnostic_df):
    """Merge all datasets to create master dataset for analysis"""
    print("\nCreating master dataset...")
    
    # Get unique VINs and Vehicle Numbers from DPF maintenance
    dpf_vins = dpf_rta['VIN Number'].dropna().unique()
    dpf_vehicle_numbers = dpf_rta['Vehicle_Number'].dropna().unique()
    
    print(f"Filtering vehicle stats for {len(dpf_vins)} VINs...")
    
    # Filter vehicle stats for DPF-affected vehicles
    dpf_vehicle_stats = vehicle_stats[vehicle_stats['vin'].isin(dpf_vins)].copy()
    print(f"Vehicle stats records for DPF vehicles: {len(dpf_vehicle_stats)}")
    
    # Filter diagnostic data for DPF-affected vehicles
    # Convert vehicle numbers to strings for matching
    dpf_vehicle_numbers_str = [str(x) for x in dpf_vehicle_numbers]
    dpf_diagnostic = diagnostic_df[diagnostic_df['Asset Name'].astype(str).isin(dpf_vehicle_numbers_str)].copy()
    print(f"Diagnostic records for DPF vehicles: {len(dpf_diagnostic)}")
    
    # Convert time columns to datetime
    if 'time' in dpf_vehicle_stats.columns:
        dpf_vehicle_stats['time'] = pd.to_datetime(dpf_vehicle_stats['time'])
    
    if 'Time' in dpf_diagnostic.columns:
        dpf_diagnostic['Time'] = pd.to_datetime(dpf_diagnostic['Time'])
    
    if 'Date of Issue' in dpf_rta.columns:
        dpf_rta['Date of Issue'] = pd.to_datetime(dpf_rta['Date of Issue'])
    
    return dpf_rta, dpf_vehicle_stats, dpf_diagnostic

def save_processed_data(dpf_rta, dpf_vehicle_stats, dpf_diagnostic):
    """Save processed datasets"""
    print("\nSaving processed datasets...")
    
    dpf_rta.to_csv('data/dpf_maintenance_records.csv', index=False)
    dpf_vehicle_stats.to_csv('data/dpf_vehicle_stats.csv', index=False)
    dpf_diagnostic.to_csv('data/dpf_diagnostic_data.csv', index=False)
    
    print("Saved:")
    print(f"- dpf_maintenance_records.csv ({len(dpf_rta)} records)")
    print(f"- dpf_vehicle_stats.csv ({len(dpf_vehicle_stats)} records)")
    print(f"- dpf_diagnostic_data.csv ({len(dpf_diagnostic)} records)")

def main():
    """Main data munging pipeline"""
    print("=== DPF Data Munging Pipeline ===")
    
    # Load and filter data
    dpf_rta = load_and_filter_rta_data()
    vehicle_stats = load_vehicle_stats()
    diagnostic_df = load_diagnostic_data()
    
    # Create master dataset
    dpf_rta, dpf_vehicle_stats, dpf_diagnostic = create_master_dataset(
        dpf_rta, vehicle_stats, diagnostic_df
    )
    
    # Save processed data
    save_processed_data(dpf_rta, dpf_vehicle_stats, dpf_diagnostic)
    
    print("\n=== Data Munging Complete ===")
    
    # Summary statistics
    print(f"\nSummary:")
    print(f"- DPF maintenance events: {len(dpf_rta)}")
    print(f"- Vehicles with DPF issues: {dpf_rta['VIN Number'].nunique()}")
    print(f"- Vehicle stats records: {len(dpf_vehicle_stats)}")
    print(f"- Diagnostic records: {len(dpf_diagnostic)}")

if __name__ == "__main__":
    main()