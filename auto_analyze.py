import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data from JSON
with open('data.json', 'r') as file:
    data = json.load(file)

# Convert JSON data to a DataFrame
df = pd.DataFrame(data.get('results', []))

if df.empty:
    print("⚠️ No data available for analysis.")
    exit()

# Infer dataset type based on column names and data patterns
column_names = df.columns.str.lower()

# Check for reservation-related data
if {'date of reservation', 'check-in date', 'checkout date', 'room number reserved'}.issubset(column_names):
    dataset_type = "Hotel Reservation Data"
elif {'employee id', 'staff name', 'department', 'role'}.issubset(column_names):
    dataset_type = "Staff Data"
elif {'transaction id', 'amount paid', 'payment date'}.issubset(column_names):
    dataset_type = "Financial Transactions"
else:
    dataset_type = "General Data"

print(f"📊 Detected dataset type: {dataset_type}")

insights = {}

if dataset_type == "Hotel Reservation Data":
    df['check-in date'] = pd.to_datetime(df['check-in date'])
    df['checkout date'] = pd.to_datetime(df['checkout date'])
    
    # Occupancy rate analysis
    df['stay_duration'] = (df['checkout date'] - df['check-in date']).dt.days
    avg_occupancy = df['stay_duration'].mean()
    insights['average_occupancy_days'] = avg_occupancy
    
    # Most popular room
    popular_room = df['room number reserved'].mode()[0]
    insights['most_popular_room'] = popular_room

    # Revenue trends
    df['revenue'] = df['amount paid']
    revenue_trend = df.groupby(df['check-in date'].dt.month)['revenue'].sum()
    
    plt.figure(figsize=(8, 6))
    revenue_trend.plot(kind='bar', color='blue')
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue")
    plt.savefig("revenue_chart.png")
    insights['revenue_chart'] = "revenue_chart.png"

elif dataset_type == "Staff Data":
    # Staff distribution by department
    department_distribution = df['department'].value_counts()
    
    plt.figure(figsize=(8, 6))
    department_distribution.plot(kind='bar', color='green')
    plt.title("Staff Distribution by Department")
    plt.xlabel("Department")
    plt.ylabel("Count")
    plt.savefig("staff_distribution.png")
    insights['staff_distribution_chart'] = "staff_distribution.png"

elif dataset_type == "Financial Transactions":
    df['payment date'] = pd.to_datetime(df['payment date'])
    
    # Total revenue
    total_revenue = df['amount paid'].sum()
    insights['total_revenue'] = total_revenue

    # Revenue trends
    revenue_trend = df.groupby(df['payment date'].dt.month)['amount paid'].sum()
    
    plt.figure(figsize=(8, 6))
    revenue_trend.plot(kind='line', marker='o', color='purple')
    plt.title("Monthly Payment Trends")
    plt.xlabel("Month")
    plt.ylabel("Total Payments")
    plt.savefig("payment_trend.png")
    insights['payment_trend_chart'] = "payment_trend.png"

else:
    # Default analysis: Show general statistics
    insights['summary_statistics'] = df.describe().to_dict()

# Save insights
with open('analysis_results.json', 'w') as file:
    json.dump(insights, file, indent=4)

print("✅ Analysis completed. Insights saved to analysis_results.json.")
