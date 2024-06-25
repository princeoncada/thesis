import pandas as pd

dcwd_data = pd.read_csv("dcwd_data.csv")

dcwd_data['Month'] = dcwd_data['Month'] + 1
dcwd_data['Date'] = pd.to_datetime(dcwd_data[['Year', 'Month']].assign(DAY=1))

dcwd_data['Year'] = dcwd_data['Date'].dt.year
dcwd_data['Month'] = dcwd_data['Date'].dt.month

monthly_data = dcwd_data.groupby(['Year', 'Month'])['Billed Consumption (cu.m.)'].sum().reset_index()

monthly_data['Growth Rate'] = monthly_data['Billed Consumption (cu.m.)'].pct_change()

last_year = monthly_data['Year'].iloc[-1]
last_month = monthly_data['Month'].iloc[-1]

average_growth_rate = monthly_data['Growth Rate'].mean()
last_billed_consumption = monthly_data['Billed Consumption (cu.m.)'].iloc[-1]
predicted_billed_consumption_2024_01_01 = last_billed_consumption * (1 + average_growth_rate)

print(f"Predicted Billed Consumption for 2024-01-01: {predicted_billed_consumption_2024_01_01}")

