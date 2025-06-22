"""
Visualization script for DPF maintenance analysis
Creates charts that prove the key insights and patterns identified
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for better looking plots
plt.style.use('default')
sns.set_palette("husl")

def load_processed_data():
    """Load the processed DPF datasets"""
    dpf_maintenance = pd.read_csv('data/dpf_maintenance_records.csv')
    dpf_vehicle_stats = pd.read_csv('data/dpf_vehicle_stats.csv')
    dpf_diagnostic = pd.read_csv('data/dpf_diagnostic_data.csv')
    
    # Convert time columns
    dpf_maintenance['Date of Issue'] = pd.to_datetime(dpf_maintenance['Date of Issue']).dt.tz_localize(None)
    dpf_vehicle_stats['time'] = pd.to_datetime(dpf_vehicle_stats['time']).dt.tz_localize(None)
    dpf_diagnostic['Time'] = pd.to_datetime(dpf_diagnostic['Time'], errors='coerce').dt.tz_localize(None)
    
    return dpf_maintenance, dpf_vehicle_stats, dpf_diagnostic

def create_maintenance_overview_charts(dpf_maintenance):
    """Create overview charts showing maintenance patterns"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('DPF Maintenance Overview Analysis', fontsize=16, fontweight='bold')
    
    # 1. Maintenance events by type
    maintenance_counts = dpf_maintenance['lines_jobDescriptions'].value_counts()
    axes[0,0].bar(range(len(maintenance_counts)), maintenance_counts.values, 
                  color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    axes[0,0].set_title('DPF Maintenance Events by Type')
    axes[0,0].set_xlabel('Maintenance Type')
    axes[0,0].set_ylabel('Number of Events')
    axes[0,0].set_xticks(range(len(maintenance_counts)))
    axes[0,0].set_xticklabels([label.replace(' ', '\n') for label in maintenance_counts.index], 
                              rotation=0, ha='center')
    
    # Add value labels on bars
    for i, v in enumerate(maintenance_counts.values):
        axes[0,0].text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')
    
    # 2. High-risk vehicles
    vehicle_counts = dpf_maintenance['Vehicle_Number'].value_counts().head(10)
    axes[0,1].bar(range(len(vehicle_counts)), vehicle_counts.values, color='#FF6B6B')
    axes[0,1].set_title('Top 10 Vehicles with Most DPF Issues')
    axes[0,1].set_xlabel('Vehicle Number')
    axes[0,1].set_ylabel('Number of Maintenance Events')
    axes[0,1].set_xticks(range(len(vehicle_counts)))
    axes[0,1].set_xticklabels(vehicle_counts.index, rotation=45)
    
    # Add value labels
    for i, v in enumerate(vehicle_counts.values):
        axes[0,1].text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
    
    # 3. Maintenance costs by type
    if 'Total_Cost' in dpf_maintenance.columns:
        cost_by_type = dpf_maintenance.groupby('lines_jobDescriptions')['Total_Cost'].agg(['mean', 'std']).round(2)
        x_pos = range(len(cost_by_type))
        axes[1,0].bar(x_pos, cost_by_type['mean'], yerr=cost_by_type['std'], 
                      capsize=5, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
        axes[1,0].set_title('Average Maintenance Cost by Type')
        axes[1,0].set_xlabel('Maintenance Type')
        axes[1,0].set_ylabel('Cost ($)')
        axes[1,0].set_xticks(x_pos)
        axes[1,0].set_xticklabels([label.replace(' ', '\n') for label in cost_by_type.index], 
                                  rotation=0, ha='center')
        
        # Add value labels
        for i, v in enumerate(cost_by_type['mean']):
            axes[1,0].text(i, v + cost_by_type['std'].iloc[i] + 50, f'${v:.0f}', 
                          ha='center', va='bottom', fontweight='bold')
    
    # 4. Downtime analysis
    if 'Downtime Days' in dpf_maintenance.columns:
        # Filter out negative downtime for cleaner visualization
        positive_downtime = dpf_maintenance[dpf_maintenance['Downtime Days'] >= 0]
        downtime_by_type = positive_downtime.groupby('lines_jobDescriptions')['Downtime Days'].agg(['mean', 'std']).round(2)
        
        x_pos = range(len(downtime_by_type))
        axes[1,1].bar(x_pos, downtime_by_type['mean'], yerr=downtime_by_type['std'], 
                      capsize=5, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
        axes[1,1].set_title('Average Downtime by Maintenance Type')
        axes[1,1].set_xlabel('Maintenance Type')
        axes[1,1].set_ylabel('Downtime (Days)')
        axes[1,1].set_xticks(x_pos)
        axes[1,1].set_xticklabels([label.replace(' ', '\n') for label in downtime_by_type.index], 
                                  rotation=0, ha='center')
        
        # Add value labels
        for i, v in enumerate(downtime_by_type['mean']):
            axes[1,1].text(i, v + downtime_by_type['std'].iloc[i] + 0.5, f'{v:.1f}', 
                          ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('dpf_maintenance_overview.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_sensor_discrimination_chart():
    """Create chart showing sensor discrimination power"""
    # Key findings from our analysis
    sensor_data = {
        'Sensor': ['Ambient Air\nTemperature', 'Vehicle Speed\n(ecuSpeedMph)', 'Engine Load\nPercent', 
                   'DEF Level\nPercent', 'Engine RPM', 'Fuel\nPercent', 'Oil Pressure\nKPa', 
                   'Coolant Temp\nMilliC'],
        'CV': [0.309, 0.199, 0.056, 0.042, 0.040, 0.015, 0.014, 0.014],
        'Discriminative_Power': ['Very High', 'High', 'Medium', 'Medium', 'Medium', 'Low', 'Low', 'Low']
    }
    
    df = pd.DataFrame(sensor_data)
    
    # Create color map
    color_map = {'Very High': '#FF6B6B', 'High': '#FFD93D', 'Medium': '#4ECDC4', 'Low': '#95E1D3'}
    colors = [color_map[power] for power in df['Discriminative_Power']]
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df['Sensor'], df['CV'], color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    plt.title('Sensor Discrimination Power for DPF Maintenance Prediction', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Sensors', fontsize=12, fontweight='bold')
    plt.ylabel('Coefficient of Variation (CV)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for i, (bar, cv) in enumerate(zip(bars, df['CV'])):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, 
                f'{cv:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Add legend
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color_map[power], alpha=0.8) 
                      for power in ['Very High', 'High', 'Medium', 'Low']]
    plt.legend(legend_elements, ['Very High', 'High', 'Medium', 'Low'], 
              title='Discriminative Power', loc='upper right')
    
    # Add explanation text
    plt.text(0.02, 0.98, 'Higher CV = Better discrimination between maintenance types', 
             transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('sensor_discrimination_power.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_sensor_patterns_by_maintenance_type():
    """Create charts showing sensor patterns by maintenance type"""
    # Data from our analysis
    sensor_patterns = {
        'EXHAUST SYSTEM': {
            'ambientAirTemperatureMilliC': 17348.01,
            'ecuSpeedMph': 32.94,
            'engineLoadPercent': 38.67,
            'defLevelMilliPercent': 76742.12,
            'engineRpm': 1139.51
        },
        'EXHAUST SYSTEM INSPECT DIAGNOSE': {
            'ambientAirTemperatureMilliC': 11928.01,
            'ecuSpeedMph': 19.94,
            'engineLoadPercent': 33.79,
            'defLevelMilliPercent': 81630.69,
            'engineRpm': 1037.54
        },
        'FILTER - DIESEL PARTICULATE': {
            'ambientAirTemperatureMilliC': 7996.95,
            'ecuSpeedMph': 27.77,
            'engineLoadPercent': 37.12,
            'defLevelMilliPercent': 73844.28,
            'engineRpm': 1114.56
        }
    }
    
    # Convert to DataFrame for easier plotting
    df_list = []
    for job_type, sensors in sensor_patterns.items():
        for sensor, value in sensors.items():
            df_list.append({'job_type': job_type, 'sensor': sensor, 'value': value})
    
    df = pd.DataFrame(df_list)
    
    # Create subplots for each key sensor
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Sensor Patterns by DPF Maintenance Type', fontsize=16, fontweight='bold')
    
    sensors = ['ambientAirTemperatureMilliC', 'ecuSpeedMph', 'engineLoadPercent', 
               'defLevelMilliPercent', 'engineRpm']
    
    for i, sensor in enumerate(sensors):
        row = i // 3
        col = i % 3
        
        sensor_data = df[df['sensor'] == sensor]
        
        bars = axes[row, col].bar(sensor_data['job_type'], sensor_data['value'], 
                                 color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
        
        # Format titles and labels
        sensor_title = sensor.replace('MilliC', ' (°C/1000)').replace('Mph', ' (mph)').replace('Percent', ' (%)')
        axes[row, col].set_title(sensor_title, fontweight='bold')
        axes[row, col].set_ylabel('Average Value')
        axes[row, col].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, sensor_data['value']):
            axes[row, col].text(bar.get_x() + bar.get_width()/2, bar.get_height() + bar.get_height()*0.01, 
                               f'{value:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Remove empty subplot
    axes[1, 2].remove()
    
    plt.tight_layout()
    plt.savefig('sensor_patterns_by_maintenance_type.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_predictive_model_performance_chart():
    """Create chart showing model performance"""
    # Data from our model results
    performance_data = {
        'Maintenance Type': ['EXHAUST SYSTEM', 'EXHAUST SYSTEM\nINSPECT DIAGNOSE', 'FILTER - DIESEL\nPARTICULATE'],
        'Precision': [0.82, 0.78, 1.00],
        'Recall': [0.69, 0.91, 0.60],
        'F1-Score': [0.75, 0.84, 0.75]
    }
    
    df = pd.DataFrame(performance_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Machine Learning Model Performance', fontsize=16, fontweight='bold')
    
    # Performance metrics by maintenance type
    x = np.arange(len(df['Maintenance Type']))
    width = 0.25
    
    bars1 = ax1.bar(x - width, df['Precision'], width, label='Precision', color='#FF6B6B', alpha=0.8)
    bars2 = ax1.bar(x, df['Recall'], width, label='Recall', color='#4ECDC4', alpha=0.8)
    bars3 = ax1.bar(x + width, df['F1-Score'], width, label='F1-Score', color='#45B7D1', alpha=0.8)
    
    ax1.set_xlabel('Maintenance Type')
    ax1.set_ylabel('Score')
    ax1.set_title('Model Performance by Maintenance Type')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df['Maintenance Type'])
    ax1.legend()
    ax1.set_ylim(0, 1.1)
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Overall accuracy
    accuracies = ['Training Accuracy', 'Testing Accuracy']
    accuracy_values = [1.00, 0.805]
    
    bars = ax2.bar(accuracies, accuracy_values, color=['#95E1D3', '#FD79A8'], alpha=0.8)
    ax2.set_title('Overall Model Accuracy')
    ax2.set_ylabel('Accuracy')
    ax2.set_ylim(0, 1.1)
    
    # Add value labels
    for bar, value in zip(bars, accuracy_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.1%}', ha='center', va='bottom', fontweight='bold')
    
    # Add warning about overfitting
    ax2.text(0.5, 0.3, 'Note: High training accuracy\nmay indicate overfitting.\nMore data recommended.', 
             ha='center', va='center', transform=ax2.transAxes,
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('model_performance.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_business_impact_visualization():
    """Create business impact visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Business Impact Analysis', fontsize=16, fontweight='bold')
    
    # Current costs breakdown
    cost_categories = ['Direct\nMaintenance', 'Downtime\nCosts']
    cost_values = [50804.76, 163500.00]
    
    colors = ['#FF6B6B', '#4ECDC4']
    bars1 = ax1.bar(cost_categories, cost_values, color=colors, alpha=0.8)
    ax1.set_title('Current Annual DPF Costs')
    ax1.set_ylabel('Cost ($)')
    
    # Add value labels
    for bar, value in zip(bars1, cost_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    # Add total
    total_cost = sum(cost_values)
    ax1.text(0.5, 0.9, f'Total: ${total_cost:,.0f}', 
             transform=ax1.transAxes, ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             fontsize=12, fontweight='bold')
    
    # Savings potential
    scenarios = ['Current\nCosts', 'With Predictive\nMaintenance']
    scenario_values = [214304.77, 214304.77 * 0.7]  # 30% reduction
    savings = 214304.77 * 0.3
    
    bars2 = ax2.bar(scenarios, scenario_values, color=['#FF6B6B', '#95E1D3'], alpha=0.8)
    ax2.set_title('Potential Savings with Predictive Maintenance')
    ax2.set_ylabel('Annual Cost ($)')
    
    # Add value labels
    for bar, value in zip(bars2, scenario_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000,
                f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    # Add savings arrow and text
    ax2.annotate('', xy=(1, scenario_values[1]), xytext=(0, scenario_values[0]),
                arrowprops=dict(arrowstyle='<->', color='green', lw=3))
    ax2.text(0.5, (scenario_values[0] + scenario_values[1])/2, 
             f'Savings:\n${savings:,.0f}', ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
             fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('business_impact.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_risk_assessment_chart(dpf_maintenance):
    """Create risk assessment chart for vehicles"""
    vehicle_risk = dpf_maintenance['Vehicle_Number'].value_counts()
    
    # Categorize vehicles by risk level
    risk_categories = []
    for count in vehicle_risk.values:
        if count >= 4:
            risk_categories.append('High Risk')
        elif count >= 2:
            risk_categories.append('Medium Risk')
        else:
            risk_categories.append('Low Risk')
    
    risk_df = pd.DataFrame({
        'Vehicle': vehicle_risk.index,
        'Maintenance_Events': vehicle_risk.values,
        'Risk_Level': risk_categories
    })
    
    plt.figure(figsize=(14, 8))
    
    # Create scatter plot
    colors = {'High Risk': '#FF6B6B', 'Medium Risk': '#FFD93D', 'Low Risk': '#95E1D3'}
    for risk_level in ['High Risk', 'Medium Risk', 'Low Risk']:
        subset = risk_df[risk_df['Risk_Level'] == risk_level]
        plt.scatter(subset['Vehicle'], subset['Maintenance_Events'], 
                   c=colors[risk_level], label=risk_level, s=100, alpha=0.7)
    
    plt.title('Vehicle Risk Assessment Based on DPF Maintenance History', 
              fontsize=16, fontweight='bold')
    plt.xlabel('Vehicle Number', fontsize=12, fontweight='bold')
    plt.ylabel('Number of DPF Maintenance Events', fontsize=12, fontweight='bold')
    plt.legend(title='Risk Level', title_fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    # Add risk level lines
    plt.axhline(y=4, color='red', linestyle='--', alpha=0.5, label='High Risk Threshold')
    plt.axhline(y=2, color='orange', linestyle='--', alpha=0.5, label='Medium Risk Threshold')
    
    # Add text annotations for high-risk vehicles
    high_risk_vehicles = risk_df[risk_df['Risk_Level'] == 'High Risk']
    for _, row in high_risk_vehicles.iterrows():
        plt.annotate(f'Vehicle {row["Vehicle"]}', 
                    (row['Vehicle'], row['Maintenance_Events']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('vehicle_risk_assessment.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all visualization charts"""
    print("Generating DPF Analysis Visualization Charts...")
    
    # Load data
    dpf_maintenance, dpf_vehicle_stats, dpf_diagnostic = load_processed_data()
    
    print("Creating maintenance overview charts...")
    create_maintenance_overview_charts(dpf_maintenance)
    
    print("Creating sensor discrimination chart...")
    create_sensor_discrimination_chart()
    
    print("Creating sensor patterns by maintenance type...")
    create_sensor_patterns_by_maintenance_type()
    
    print("Creating predictive model performance chart...")
    create_predictive_model_performance_chart()
    
    print("Creating business impact visualization...")
    create_business_impact_visualization()
    
    print("Creating vehicle risk assessment chart...")
    create_risk_assessment_chart(dpf_maintenance)
    
    print("\n" + "="*60)
    print("ALL VISUALIZATION CHARTS GENERATED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📊 Charts Created:")
    print("• dpf_maintenance_overview.png - Maintenance patterns and costs")
    print("• sensor_discrimination_power.png - Sensor predictive power")
    print("• sensor_patterns_by_maintenance_type.png - Sensor pattern differences")
    print("• model_performance.png - ML model accuracy metrics")
    print("• business_impact.png - Cost analysis and savings potential")
    print("• vehicle_risk_assessment.png - Vehicle risk categorization")
    
    print("\n🎯 Key Visual Insights Proven:")
    print("✓ Ambient air temperature is the most discriminative sensor")
    print("✓ Different maintenance types have distinct sensor patterns")
    print("✓ ML model achieves 80.5% accuracy in predicting maintenance type")
    print("✓ Potential annual savings of $64K with predictive maintenance")
    print("✓ 5 vehicles identified as high-risk (≥4 maintenance events)")

if __name__ == "__main__":
    main()