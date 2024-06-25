import pandas as pd
import numpy as np

# Load the datasets
dcwd_data = pd.read_csv("dcwd_data.csv")
population_data = pd.read_csv("population_data.csv")
pagasa_data = pd.read_csv("pagasa_data.csv")

# Population Data Processing
# Convert population data to daily
population_data['Date'] = pd.to_datetime(population_data['Year'], format='%Y')
population_data = population_data.set_index('Date').resample('D').interpolate(method='linear').reset_index()

# Generate a date range
date_range = pd.date_range(start='2023-01-02', end='2023-12-31', freq='D')
date_range = pd.DataFrame(date_range, columns=['Date'])

# Calculate the daily growth rate based on the last year's growth
daily_growth_rate = (population_data['Population'].iloc[-1] - population_data['Population'].iloc[-366]) / 365

# Create new population data for the date range
new_population_data = population_data['Population'].iloc[-1] + daily_growth_rate * np.arange(1, len(date_range) + 1)

# Create a DataFrame for the new population data
new_population_data = pd.DataFrame({'Date': date_range['Date'], 'Population': new_population_data})

# Concatenate the old and new population data
full_population_data = pd.concat([population_data, new_population_data], ignore_index=True)

# Drop column Year
full_population_data = full_population_data.drop(columns=['Year'])
full_population_data.to_csv("population_extended.csv", index=False)

# DCWD Data Processing
# Convert DCWD data to daily
dcwd_data['Month'] = dcwd_data['Month'] + 1
dcwd_data['Date'] = pd.to_datetime(dcwd_data[['Year', 'Month']].assign(DAY=1))
dcwd_data = dcwd_data.set_index('Date').resample('D').interpolate(method='linear').reset_index()

# Calculate daily consumption
dcwd_data['Daily Consumption'] = dcwd_data['Billed Consumption (cu.m.)'] / dcwd_data['Date'].dt.days_in_month
dcwd_data.to_csv("dcwd_extended", index=False)

# Convert PAGASA data to daily datetime
pagasa_data['Date'] = pd.to_datetime(pagasa_data[['YEAR', 'MONTH', 'DAY']], format='%Y%m%d')
pagasa_data.to_csv("pagasa_transformed.csv", index=False)



