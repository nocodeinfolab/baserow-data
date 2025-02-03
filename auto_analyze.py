import json
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import os

# Load reservation data
with open('data.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data['results'])

df['Date of Booking'] = pd.to_datetime(df['Date of Booking'])
df['Expected Check-in Date'] = pd.to_datetime(df['Expected Check-in Date'])
df['Expected Check-out Date'] = pd.to_datetime(df['Expected Check-out Date'])
df['Duration of Stay'] = pd.to_numeric(df['Duration of Stay'])
df['Payable Amount'] = pd.to_numeric(df['Payable Amount'])
df['Amount Paid'] = pd.to_numeric(df['Amount Paid'])
df['Pending Amount'] = pd.to_numeric(df['Pending Amount'])

df['Booking Month'] = df['Date of Booking'].dt.to_period('M')

df['Occupancy'] = 1  # Assume each reservation contributes to occupancy

# Booking Trend Analysis
booking_trend = df.groupby('Booking Month').size()
plt.figure(figsize=(10, 5))
booking_trend.plot(kind='line', marker='o')
plt.title('Monthly Booking Trends')
plt.xlabel('Month')
plt.ylabel('Number of Bookings')
plt.grid()
plt.savefig('booking_trend.png')
plt.close()

# Revenue Trend Analysis
revenue_trend = df.groupby('Booking Month')['Payable Amount'].sum()
plt.figure(figsize=(10, 5))
revenue_trend.plot(kind='bar', color='blue')
plt.title('Monthly Revenue Trends')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.grid()
plt.savefig('revenue_trend.png')
plt.close()

# Predictive Analysis: Occupancy Forecast
occupancy_series = df.groupby('Expected Check-in Date').size()
occupancy_series = occupancy_series.asfreq('D').fillna(0)
model = ExponentialSmoothing(occupancy_series, trend='add', seasonal=None).fit()
forecast = model.forecast(30)

plt.figure(figsize=(10, 5))
occupancy_series.plot(label='Historical Occupancy')
forecast.plot(label='Forecasted Occupancy', linestyle='dashed')
plt.title('Occupancy Forecast for Next 30 Days')
plt.xlabel('Date')
plt.ylabel('Occupancy Count')
plt.legend()
plt.grid()
plt.savefig('occupancy_forecast.png')
plt.close()

# Save Analysis Summary
analysis_results = {
    "booking_trend_chart": "booking_trend.png",
    "revenue_trend_chart": "revenue_trend.png",
    "occupancy_forecast_chart": "occupancy_forecast.png",
    "summary_statistics": df.describe().to_dict()
}

with open('analysis_results.json', 'w') as file:
    json.dump(analysis_results, file, indent=4)

print("Analysis completed and results saved.")
