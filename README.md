# 🌍 World Bank Economic Analysis

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Last Updated](https://img.shields.io/badge/Last%20Updated-March%202026-orange)

## 📋 Overview
This project analyzes global economic development trends using World Bank open data. The goal is to identify patterns in GDP growth, education spending, and other indicators to provide actionable insights for business strategy.

**Key Questions Answered:**
- Which countries show the highest GDP growth and why?
- What's the relationship between education spending and economic growth?
- How did COVID-19 impact different economies?

## 🎯 Business Problem
Multinational companies need to identify high-growth markets for expansion. This analysis helps prioritize countries based on economic indicators and stability.

## 📊 Data Source
- **Primary Data:** World Bank Open Data API (2010-2023)
- **Indicators Used:** GDP growth, education expenditure, life expectancy, unemployment
- **Countries Covered:** 50+ countries across all income groups

## 🛠️ Methodology

### 1. Data Collection
```python
# Example code snippet
import pandas as pd
import wbdata

indicators = {'NY.GDP.MKTP.KD.ZG': 'gdp_growth'}
data = wbdata.get_dataframe(indicators)
