"""
Enhanced visualization module for economic analysis.
Creates publication-quality figures and interactive dashboards.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os

# Set style for better looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def setup_output_dirs():
    """Create output directories if they don't exist."""
    os.makedirs('outputs/figures', exist_ok=True)
    os.makedirs('outputs/dashboards', exist_ok=True)
    print("✅ Output directories ready")

def plot_gdp_trends(df, save=True):
    """
    Plot GDP growth trends for top countries.
    
    Parameters:
    -----------
    df : DataFrame
        DataFrame with columns: country, year, gdp_growth
    save : bool
        Whether to save the figure
    """
    # Get top 8 countries by average growth
    top_countries = df.groupby('country')['gdp_growth'].mean().nlargest(8).index
    
    plt.figure(figsize=(14, 8))
    
    for country in top_countries:
        country_data = df[df['country'] == country].sort_values('year')
        plt.plot(country_data['year'], country_data['gdp_growth'], 
                marker='o', linewidth=2.5, markersize=6, label=country)
    
    # Add COVID-19 highlight
    plt.axvspan(2019.5, 2020.5, alpha=0.2, color='red', label='COVID-19 Period')
    
    plt.title('📈 GDP Growth Trends - Top 8 Economies (2010-2023)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('GDP Growth (%)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
    
    plt.tight_layout()
    
    if save:
        plt.savefig('outputs/figures/gdp_trends.png', dpi=300, bbox_inches='tight')
        plt.savefig('outputs/figures/gdp_trends.pdf', bbox_inches='tight')
        print("💾 Saved: outputs/figures/gdp_trends.png")
    
    return plt

def plot_education_vs_growth(df, save=True):
    """
    Scatter plot of education spending vs GDP growth.
    """
    plt.figure(figsize=(12, 8))
    
    # Use latest year's data
    latest_year = df['year'].max()
    recent_df = df[df['year'] == latest_year].copy()
    
    # Create scatter plot with regression line
    scatter = plt.scatter(recent_df['edu_expenditure'], recent_df['gdp_growth'],
                         c=recent_df['gdp_growth'], cmap='RdYlGn', 
                         s=200, alpha=0.7, edgecolors='black', linewidth=1)
    
    # Add regression line
    z = np.polyfit(recent_df['edu_expenditure'], recent_df['gdp_growth'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(recent_df['edu_expenditure'].min(), 
                         recent_df['edu_expenditure'].max(), 100)
    plt.plot(x_line, p(x_line), "r--", alpha=0.8, label=f'Trend line (r={np.corrcoef(recent_df["edu_expenditure"], recent_df["gdp_growth"])[0,1]:.2f})')
    
    # Add country labels
    for idx, row in recent_df.iterrows():
        plt.annotate(row['country'], 
                    (row['edu_expenditure'], row['gdp_growth']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    plt.colorbar(scatter, label='GDP Growth (%)')
    plt.title(f'💡 Education Spending vs GDP Growth ({latest_year})', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Education Expenditure (% of GDP)', fontsize=12)
    plt.ylabel('GDP Growth (%)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    if save:
        plt.savefig('outputs/figures/education_vs_growth.png', dpi=300, bbox_inches='tight')
        print("💾 Saved: outputs/figures/education_vs_growth.png")
    
    return plt

def plot_correlation_heatmap(df, save=True):
    """
    Plot correlation heatmap of economic indicators.
    """
    # Select numeric columns
    numeric_cols = ['gdp_growth', 'edu_expenditure', 'life_expectancy', 
                    'unemployment', 'inflation'] if 'inflation' in df.columns else \
                   ['gdp_growth', 'edu_expenditure', 'life_expectancy', 'unemployment']
    
    # Only use columns that exist
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    corr_df = df[numeric_cols].copy()
    
    # Calculate correlation
    corr = corr_df.corr()
    
    # Create mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    plt.figure(figsize=(10, 8))
    
    # Create heatmap
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                annot_kws={'size': 12})
    
    plt.title('📊 Correlation Matrix of Economic Indicators', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save:
        plt.savefig('outputs/figures/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        print("💾 Saved: outputs/figures/correlation_heatmap.png")
    
    return plt

def plot_covid_recovery(df, save=True):
    """
    Plot COVID-19 impact and recovery by country.
    """
    # Get data for 2019, 2020, 2021
    covid_years = [2019, 2020, 2021]
    covid_df = df[df['year'].isin(covid_years)].pivot_table(
        index='country', columns='year', values='gdp_growth'
    ).dropna()
    
    # Calculate recovery (2021 vs 2019)
    covid_df['recovery'] = covid_df[2021] - covid_df[2019]
    covid_df = covid_df.nlargest(10, 'recovery')
    
    plt.figure(figsize=(14, 8))
    
    x = range(len(covid_df))
    width = 0.25
    
    plt.bar([i - width for i in x], covid_df[2019], width, label='2019 (Pre-COVID)', 
            color='#2ecc71', alpha=0.8)
    plt.bar(x, covid_df[2020], width, label='2020 (COVID Shock)', 
            color='#e74c3c', alpha=0.8)
    plt.bar([i + width for i in x], covid_df[2021], width, label='2021 (Recovery)', 
            color='#3498db', alpha=0.8)
    
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('GDP Growth (%)', fontsize=12)
    plt.title('🦠 COVID-19 Impact and Recovery by Country', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xticks(x, covid_df.index, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (idx, row) in enumerate(covid_df.iterrows()):
        plt.text(i - width, row[2019] + 0.1, f'{row[2019]:.1f}', 
                ha='center', va='bottom', fontsize=9)
        plt.text(i, row[2020] + 0.1, f'{row[2020]:.1f}', 
                ha='center', va='bottom', fontsize=9)
        plt.text(i + width, row[2021] + 0.1, f'{row[2021]:.1f}', 
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    if save:
        plt.savefig('outputs/figures/covid_recovery.png', dpi=300, bbox_inches='tight')
        print("💾 Saved: outputs/figures/covid_recovery.png")
    
    return plt

def create_interactive_dashboard(df, save=True):
    """
    Create an interactive Plotly dashboard.
    """
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('GDP Growth Over Time', 'Education vs Growth (2022)',
                       'Growth Distribution', 'Country Rankings'),
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'box'}, {'type': 'bar'}]]
    )
    
    # 1. GDP Growth Over Time
    for country in df['country'].unique()[:5]:
        country_data = df[df['country'] == country]
        fig.add_trace(
            go.Scatter(x=country_data['year'], y=country_data['gdp_growth'],
                      name=country, mode='lines+markers'),
            row=1, col=1
        )
    
    # 2. Education vs Growth (latest year)
    latest_year = df['year'].max()
    recent_df = df[df['year'] == latest_year]
    fig.add_trace(
        go.Scatter(x=recent_df['edu_expenditure'], y=recent_df['gdp_growth'],
                  mode='markers+text', text=recent_df['country'],
                  textposition="top center", marker=dict(size=12)),
        row=1, col=2
    )
    
    # 3. Growth Distribution
    fig.add_trace(
        go.Box(y=df['gdp_growth'], name='All Countries'),
        row=2, col=1
    )
    
    # 4. Top 10 Countries by Average Growth
    top_10 = df.groupby('country')['gdp_growth'].mean().nlargest(10)
    fig.add_trace(
        go.Bar(x=top_10.values, y=top_10.index, orientation='h',
               marker_color='lightgreen'),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(height=800, showlegend=True, 
                     title_text="🌍 World Bank Economic Analysis Dashboard",
                     title_font_size=20)
    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="Education Spending (% of GDP)", row=1, col=2)
    fig.update_xaxes(title_text="GDP Growth (%)", row=2, col=2)
    fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1)
    fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=2)
    fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1)
    
    if save:
        fig.write_html('outputs/dashboards/interactive_dashboard.html')
        print("💾 Saved: outputs/dashboards/interactive_dashboard.html")
    
    return fig

def generate_all_visualizations(df):
    """Generate all visualizations at once."""
    print("🎨 Generating all visualizations...")
    
    # Setup directories
    setup_output_dirs()
    
    # Generate plots
    plot_gdp_trends(df)
    plot_education_vs_growth(df)
    plot_correlation_heatmap(df)
    plot_covid_recovery(df)
    create_interactive_dashboard(df)
    
    print("\n✅ All visualizations generated successfully!")
    print("📁 Check 'outputs/figures/' for static images")
    print("📁 Check 'outputs/dashboards/' for interactive HTML files")

# Test the module
if __name__ == "__main__":
    # Create sample data for testing
    from data_loader import generate_sample_data
    df = generate_sample_data()
    generate_all_visualizations(df)
