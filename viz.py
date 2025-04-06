#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Coffee Dataset Visualization Script
-----------------------------------
This script creates compelling visualizations from cleaned coffee data
to provide insights for brewing recommendations and flavor analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap

# Set style for better visualizations
sns.set(style="whitegrid")
plt.rcParams.update({'font.size': 12})
custom_palette = sns.color_palette("YlOrBr", 8)
custom_cmap = LinearSegmentedColormap.from_list("coffee_browns", ["#FFF8E1", "#4E342E"])

def load_cleaned_data(file_path="cleaned_coffee_data.xlsx"):
    """Load the cleaned coffee dataset."""
    try:
        df = pd.read_excel(file_path)
        print(f"Visualization data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"Error loading cleaned data: {e}")
        return None

def create_flavor_heatmap(df, output_dir="visualizations"):
    """
    Create heatmap showing flavor profile correlation with origins and roast levels.
    This visualization helps identify which origins produce specific flavor profiles.
    """
    print("Creating flavor profile heatmap...")
    
    # Create a directory for visualizations if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Prepare data - aggregate flavor profiles by origin
    flavor_cols = ['flavor_fruity', 'flavor_floral', 'flavor_nutty', 
                  'flavor_chocolaty', 'flavor_spicy']
    
    # Group by origin and calculate percentage of each flavor profile
    flavor_by_origin = df.groupby('origin')[flavor_cols].mean()
    
    # Sort by total flavor presence for better visualization
    flavor_by_origin['total'] = flavor_by_origin.sum(axis=1)
    flavor_by_origin = flavor_by_origin.sort_values('total', ascending=False).drop('total', axis=1)
    
    # Keep only top 15 origins for readability
    flavor_by_origin = flavor_by_origin.head(15)
    
    # Create heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(flavor_by_origin, annot=True, fmt='.0%', cmap=custom_cmap, 
                linewidths=0.5, cbar_kws={'label': 'Flavor Presence %'})
    
    plt.title('Coffee Flavor Profiles by Origin (Top 15 Origins)', fontsize=16, pad=20)
    plt.ylabel('Origin Country', fontsize=14)
    plt.tight_layout()
    
    # Save visualization
    output_path = os.path.join(output_dir, 'flavor_by_origin_heatmap.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Flavor heatmap saved to {output_path}")
    return output_path

def create_roast_process_radar(df, output_dir="visualizations"):
    """
    Create radar charts showing flavor profiles by roast level and processing method.
    This helps understand how roast level and processing method affect flavor.
    """
    print("Creating roast level and processing method radar charts...")
    
    # Create a directory for visualizations if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    flavor_cols = ['flavor_fruity', 'flavor_floral', 'flavor_nutty', 
                   'flavor_chocolaty', 'flavor_spicy']
    
    # Calculate average flavor profiles by roast level and process
    roast_flavors = df.groupby('roast_level')[flavor_cols].mean()
    process_flavors = df.groupby('process')[flavor_cols].mean()
    
    # Function to create a radar chart
    def create_radar(data, title, output_filename):
        categories = flavor_cols
        categories = [cat.replace('flavor_', '') for cat in categories]
        
        # Number of categories
        N = len(categories)
        
        # Create angles for each category
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        
        # Draw one axis per variable and add labels
        plt.xticks(angles[:-1], categories, size=14)
        
        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([0.25, 0.5, 0.75], ["25%", "50%", "75%"], color="grey", size=12)
        plt.ylim(0, 1)
        
        # Plot each roast level or process
        for idx, (name, values) in enumerate(data.iterrows()):
            values_list = values.tolist()
            values_list += values_list[:1]  # Close the loop
            ax.plot(angles, values_list, linewidth=2, linestyle='solid', label=name)
            ax.fill(angles, values_list, alpha=0.1)
        
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=14)
        
        plt.title(title, size=20, pad=20)
        
        # Save radar chart
        output_path = os.path.join(output_dir, output_filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    # Create radar charts
    roast_radar_path = create_radar(
        roast_flavors, 
        'Flavor Profiles by Roast Level', 
        'roast_flavor_radar.png'
    )
    
    process_radar_path = create_radar(
        process_flavors, 
        'Flavor Profiles by Processing Method', 
        'process_flavor_radar.png'
    )
    
    print(f"Roast level radar chart saved to {roast_radar_path}")
    print(f"Processing method radar chart saved to {process_radar_path}")
    
    return roast_radar_path, process_radar_path

def create_brewing_parameters_chart(df, output_dir="visualizations"):
    """
    Create a visualization showing recommended brewing parameters 
    based on coffee characteristics.
    """
    print("Creating brewing parameters recommendation chart...")
    
    # Create a directory for visualizations if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Simulated brewing parameters based on coffee attributes
    # In a real scenario, these would be derived from your model or expert knowledge
    
    # Map roast levels to brewing temperatures
    roast_temps = {
        'light': 94, 
        'medium_light': 92, 
        'medium': 90, 
        'medium_dark': 88, 
        'dark': 86
    }
    
    # Map processing methods to grind size (relative to reference)
    process_grind = {
        'washed': 1.0,    # 120μm
        'natural': 1.1,   # 132μm
        'honey': 0.9      # 108μm
    }
    
    # Map origins to recommended brew ratios
    # Based on typical recommendations for different regions
    origin_mapping = {
        'Ethiopia': 'Africa',
        'Kenya': 'Africa',
        'Colombia': 'Americas',
        'Guatemala': 'Americas',
        'Costa Rica': 'Americas',
        'Panama': 'Americas',
        'Indonesia': 'Asia-Pacific',
        'Hawai\'I': 'Pacific'
    }
    
    region_ratio = {
        'Africa': 1/15,      # 1:15
        'Americas': 1/16,    # 1:16
        'Asia-Pacific': 1/14,# 1:14
        'Pacific': 1/15.5    # 1:15.5
    }
    
    # Add these brewing parameters to the dataframe
    df['region'] = df['origin'].map(lambda x: origin_mapping.get(x, 'Other'))
    df['brew_temp'] = df['roast_level'].map(lambda x: roast_temps.get(x, 90))
    df['grind_size'] = df['process'].map(lambda x: process_grind.get(x, 1.0) * 120)
    df['brew_ratio'] = df['region'].map(lambda x: region_ratio.get(x, 1/16))
    df['brew_ratio_display'] = df['brew_ratio'].map(lambda x: f"1:{int(1/x)}")
    
    # Create multi-panel visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # 1. Brewing temperature by roast level
    sns.boxplot(x='roast_level', y='brew_temp', data=df, 
                order=['light', 'medium_light', 'medium', 'medium_dark', 'dark'],
                palette=custom_palette, ax=axes[0, 0])
    axes[0, 0].set_title('Brewing Temperature by Roast Level', fontsize=16)
    axes[0, 0].set_xlabel('Roast Level', fontsize=14)
    axes[0, 0].set_ylabel('Temperature (°C)', fontsize=14)
    
    # 2. Grind size by processing method
    sns.barplot(x='process', y='grind_size', data=df, palette=custom_palette, ax=axes[0, 1])
    axes[0, 1].axhline(y=120, color='r', linestyle='--', label='Reference (120μm)')
    axes[0, 1].set_title('Recommended Grind Size by Processing Method', fontsize=16)
    axes[0, 1].set_xlabel('Processing Method', fontsize=14)
    axes[0, 1].set_ylabel('Grind Size (μm)', fontsize=14)
    axes[0, 1].legend()
    
    # 3. Brew ratio by region
    region_order = ['Africa', 'Americas', 'Asia-Pacific', 'Pacific', 'Other']
    ratio_display = [f"1:{int(1/region_ratio.get(r, 1/16))}" for r in region_order]
    
    sns.barplot(x=region_order, y=[1/region_ratio.get(r, 1/16) for r in region_order], 
                palette=custom_palette, ax=axes[1, 0])
    axes[1, 0].set_title('Recommended Brew Ratio by Region', fontsize=16)
    axes[1, 0].set_xlabel('Region', fontsize=14)
    axes[1, 0].set_ylabel('Brew Ratio (1:x)', fontsize=14)
    axes[1, 0].set_ylim(0, 20)
    
    # 4. Flow rate recommendation based on flavor profile
    # Simplified model: more fruity/floral coffees benefit from slower flow
    df['flow_rate'] = 0.5  # Default flow rate in ml/s
    
    # Adjust flow rate based on flavor profile
    df.loc[df['flavor_fruity'] & df['flavor_floral'], 'flow_rate'] = 0.4  # Slower for fruity & floral
    df.loc[df['flavor_chocolaty'] & df['flavor_nutty'], 'flow_rate'] = 0.6  # Faster for chocolaty & nutty
    
    # Group by origin region and flavor combination
    df['flavor_group'] = 'Balanced'
    df.loc[df['flavor_fruity'] & df['flavor_floral'], 'flavor_group'] = 'Fruity & Floral'
    df.loc[df['flavor_chocolaty'] & df['flavor_nutty'], 'flavor_group'] = 'Chocolaty & Nutty'
    df.loc[df['flavor_spicy'], 'flavor_group'] = 'Spicy'
    
    flow_by_flavor = df.groupby('flavor_group')['flow_rate'].mean().reset_index()
    
    sns.barplot(x='flavor_group', y='flow_rate', data=flow_by_flavor, 
                palette=custom_palette, ax=axes[1, 1])
    axes[1, 1].set_title('Recommended Flow Rate by Flavor Profile', fontsize=16)
    axes[1, 1].set_xlabel('Flavor Profile', fontsize=14)
    axes[1, 1].set_ylabel('Flow Rate (ml/s)', fontsize=14)
    
    plt.suptitle('Coffee Brewing Parameter Recommendations', fontsize=20, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save visualization
    output_path = os.path.join(output_dir, 'brewing_parameters.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Brewing parameters chart saved to {output_path}")
    return output_path

def main():
    """Main function to execute the visualization workflow."""
    # Create output directory
    output_dir = "coffee_visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Load cleaned data
    df = load_cleaned_data()
    
    if df is not None:
        # Create visualizations
        flavor_heatmap_path = create_flavor_heatmap(df, output_dir)
        roast_radar_path, process_radar_path = create_roast_process_radar(df, output_dir)
        brewing_chart_path = create_brewing_parameters_chart(df, output_dir)
        
        print("\nVisualization Summary:")
        print(f"1. Flavor Profile Heatmap: {flavor_heatmap_path}")
        print(f"2. Roast Level & Processing Method Radar Charts: {roast_radar_path}")
        print(f"3. Brewing Parameters Recommendation Chart: {brewing_chart_path}")
        print("\nAll visualizations saved to the 'coffee_visualizations' directory.")
    else:
        print("Visualization process aborted due to data loading failure.")

if __name__ == "__main__":
    main()
