#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Coffee Dataset Cleaning Script
------------------------------
This script processes coffee data, extracts key attributes from reviews,
and saves a cleaned dataset with important features for ML applications.
"""

# Try importing required libraries with error handling
try:
    import pandas as pd
    import numpy as np
    from textblob import TextBlob
    import os
    import sys
except ImportError as e:
    print(f"Error: Missing required dependency: {e}")
    print("Please install required packages with: pip install pandas numpy textblob openpyxl")
    sys.exit(1)

def load_data(file_path):
    """Load the coffee dataset from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
        print(f"Available columns: {', '.join(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def detect_process(review):
    """Extract processing method from review text."""
    if not isinstance(review, str):
        return np.nan
        
    review = review.lower()
    process_keywords = {
        'washed': ['washed', 'wet process', 'water process'],
        'natural': ['natural', 'dry process', 'sun-dried', 'sun dried'],
        'honey': ['honey', 'pulped', 'semi-washed']
    }
    
    for process, keywords in process_keywords.items():
        if any(keyword in review for keyword in keywords):
            return process
            
    return np.nan

def infer_variety(origin):
    """Infer coffee variety based on country of origin."""
    arabica_primary = ['Ethiopia', 'Kenya', 'Colombia', 'Guatemala', 'Costa Rica', 
                       'Panama', 'Rwanda', 'Peru', 'Hawai\'I', 'Nicaragua', 'El Salvador']
    robusta_primary = ['Vietnam', 'Indonesia', 'Uganda', 'India']
    
    if pd.isna(origin):
        return 'unknown'
    
    if origin in arabica_primary:
        return 'arabica'
    elif origin in robusta_primary:
        return 'robusta'
    else:
        return 'unknown'  # Default to unknown for ambiguous origins

def extract_flavor_profile(review):
    """Extract flavor profile categories from review text."""
    if not isinstance(review, str):
        return {}
    
    review = review.lower()
    flavor_categories = {
        'fruity': ['berry', 'fruit', 'citrus', 'apple', 'cherry', 'lemon', 'orange', 
                  'peach', 'apricot', 'plum', 'mango', 'raspberry'],
        'floral': ['floral', 'jasmine', 'rose', 'flower', 'lavender', 'honeysuckle', 'lilac'],
        'nutty': ['nut', 'almond', 'hazelnut', 'walnut', 'peanut', 'cashew', 'pistachio'],
        'chocolaty': ['chocolate', 'cocoa', 'cacao', 'mocha', 'fudge'],
        'spicy': ['spice', 'cinnamon', 'nutmeg', 'clove', 'pepper', 'peppercorn']
    }
    
    profile = {}
    for category, keywords in flavor_categories.items():
        profile[category] = any(keyword in review for keyword in keywords)
        
    return profile

def clean_data(df):
    """Clean and preprocess the coffee dataset."""
    try:
        # Check if required columns exist
        required_columns = ['origin', 'roast', 'review']
        for col in required_columns:
            if col not in df.columns:
                print(f"Error: Required column '{col}' not found in dataset.")
                return None
        
        # Create new dataframe with required columns
        cleaned_df = df[required_columns].copy()
        
        # Rename columns for consistency
        cleaned_df.rename(columns={'roast': 'roast_level'}, inplace=True)

        print("\nHandling missing values...")
        print(f"Before cleaning: {cleaned_df.isnull().sum()}")
        
        # Add process column based on review text
        cleaned_df['process'] = cleaned_df['review'].apply(detect_process)
        
        # Add variety column based on origin
        cleaned_df['variety'] = cleaned_df['origin'].apply(infer_variety)
        
        # Drop rows with missing critical data
        cleaned_df.dropna(subset=['origin', 'roast_level', 'review'], inplace=True)

        # Standardize roast levels
        roast_mapping = {
            "Light": "light",
            "Medium-Light": "medium_light",
            "Medium": "medium",
            "Medium-Dark": "medium_dark",
            "Dark": "dark"
        }
        cleaned_df['roast_level'] = cleaned_df['roast_level'].map(roast_mapping)

        # Add sentiment analysis for reviews
        print("\nAdding sentiment analysis...")
        try:
            cleaned_df['sentiment'] = cleaned_df['review'].apply(
                lambda x: TextBlob(str(x)).sentiment.polarity if pd.notna(x) else np.nan
            )
        except Exception as e:
            print(f"Warning: Error during sentiment analysis: {e}")
            cleaned_df['sentiment'] = np.nan
        
        # Extract flavor profiles
        print("Extracting flavor profiles...")
        flavor_profiles = cleaned_df['review'].apply(extract_flavor_profile)
        
        flavor_categories = ['fruity', 'floral', 'nutty', 'chocolaty', 'spicy']
        for category in flavor_categories:
            cleaned_df[f'flavor_{category}'] = flavor_profiles.apply(
                lambda x: x.get(category, False) if isinstance(x, dict) else False
            )

        # Add aggregate score as sum of flavors detected (optional feature)
        cleaned_df['flavor_richness'] = cleaned_df[[f'flavor_{cat}' 
                                                  for cat in flavor_categories]].sum(axis=1)

        print(f"After cleaning: {cleaned_df.isnull().sum()}")
        process_counts = cleaned_df['process'].value_counts().to_dict()
        variety_counts = cleaned_df['variety'].value_counts().to_dict()
        
        print(f"Inferred process methods: {process_counts}")
        print(f"Inferred varieties: {variety_counts}")
        
        return cleaned_df
        
    except Exception as e:
        print(f"Error during data cleaning: {e}")
        return None

def save_cleaned_data(df, output_file):
    """Save the cleaned dataset to an Excel file."""
    if df is None:
        print("No data to save.")
        return False
        
    try:
        # Create directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save data
        df.to_excel(output_file, index=False)
        print(f"Cleaned dataset saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def main():
    """Main function to execute the data cleaning workflow."""
    input_file = "simplified_coffee.csv"
    output_file = "cleaned_coffee_data.xlsx"

    # Load data
    df = load_data(input_file)
    
    if df is not None:
        # Clean data
        cleaned_df = clean_data(df)
        
        # Save cleaned data
        if cleaned_df is not None:
            save_cleaned_data(cleaned_df, output_file)
        else:
            print("Data cleaning failed. No output file created.")
    else:
        print("Data loading failed. Process aborted.")

if __name__ == "__main__":
    main()
