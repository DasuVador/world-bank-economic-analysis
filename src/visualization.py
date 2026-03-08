"""
Visualization functions.
"""

import matplotlib.pyplot as plt
import seaborn as sns

def plot_gdp_trends(df):
    """Plot GDP growth trends."""
    plt.figure(figsize=(12, 6))
    
    for country in df['country'].unique()[:5]:
        country_data = df[df['country'] == country]
        plt.plot(country_data['year'], country_data['gdp_growth'], 
                marker='o', label=country)
    
    plt.title('GDP Growth Trends (Selected Countries)')
    plt.xlabel('Year')
    plt.ylabel('GDP Growth (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_correlation_heatmap(df):
    """Plot correlation matrix."""
    numeric_cols = df.select_dtypes(include=[float, int]).columns
    corr = df[numeric_cols].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, fmt='.2f')
    plt.title('Correlation Matrix')
    plt.tight_layout()
    return plt