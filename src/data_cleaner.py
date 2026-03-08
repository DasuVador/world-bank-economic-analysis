"""
Data cleaning module.
"""

import pandas as pd

def clean_economic_data(df):
    """Clean and preprocess the data."""
    print("🔧 Cleaning data...")
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.fillna(df.median(numeric_only=True))
    
    # Create new features
    df['growth_category'] = pd.cut(df['gdp_growth'], 
                                    bins=[-10, 0, 2, 5, 15],
                                    labels=['Negative', 'Low', 'Medium', 'High'])
    
    print(f"✅ Cleaned {len(df)} records")
    return df

def get_summary_stats(df):
    """Generate summary statistics."""
    stats = {
        'total_countries': df['country'].nunique(),
        'years': f"{df['year'].min()}-{df['year'].max()}",
        'avg_growth': round(df['gdp_growth'].mean(), 2),
        'avg_education': round(df['edu_expenditure'].mean(), 2),
        'avg_life_exp': round(df['life_expectancy'].mean(), 1)
    }
    return stats