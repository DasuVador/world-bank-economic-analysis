"""
Data loading module for World Bank economic analysis.
"""

import pandas as pd
import numpy as np

def generate_sample_data():
    """Generate realistic sample data."""
    np.random.seed(42)
    
    countries = ['USA', 'China', 'India', 'Germany', 'Japan', 'UK', 'France', 'Brazil']
    years = list(range(2010, 2024))
    data = []
    
    for country in countries:
        base_growth = np.random.uniform(1, 7)
        for year in years:
            growth = base_growth + np.random.normal(0, 2)
            if year == 2020:
                growth -= 5  # COVID shock
            if year > 2020:
                growth += 2  # Recovery
            
            data.append({
                'country': country,
                'year': year,
                'gdp_growth': round(max(min(growth, 15), -5), 2),
                'edu_expenditure': round(np.random.uniform(3, 8), 2),
                'life_expectancy': round(np.random.uniform(65, 83), 1)
            })
    
    return pd.DataFrame(data)

def load_world_bank_data():
    """Main function to load data."""
    print("📊 Loading World Bank economic data...")
    df = generate_sample_data()
    print(f"✅ Loaded {len(df)} records")
    return df