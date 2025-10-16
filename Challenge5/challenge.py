import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


df = pd.read_csv('weather_tokyo_data.csv')

df['temperature'] = df['temperature'].astype(str).apply(lambda x: re.search(r'-?\d+\.?\d*', x).group() if re.search(r'-?\d+\.?\d*', x) else None).astype(float)
df['date'] = pd.to_datetime(df['year'].astype(str) + '/' + df['day'])

avg_temp = df['temperature'].mean()
print(f'Overall average temperature: {avg_temp:.2f}°C')

df['month'] = df['date'].dt.month
df['year_month'] = df['date'].dt.to_period('M')
monthly_avg = df.groupby('year_month')['temperature'].mean().round(2)
print('\nMonthly average temperatures:')
print(monthly_avg)


floor = 20.0
plt.figure(figsize=(10,5))
colors = ['red' if temp > floor else 'blue' for temp in monthly_avg]
monthly_avg.plot(kind='bar', color=colors)
plt.axhline(floor, color='gray', linestyle='--', label=f'Floor: {floor}°C')
plt.title('Monthly Average Temperatures')
plt.ylabel('Temperature (°C)')
plt.xlabel('Month')
plt.legend()
plt.tight_layout()
plt.show()


highs = df.nlargest(3, 'temperature')[['date', 'temperature']]
lows = df.nsmallest(3, 'temperature')[['date', 'temperature']]
print('\nThree highest temperatures:')
print(highs)
print('\nThree lowest temperatures:')
print(lows)


hottest = df.loc[df['temperature'].idxmax()]
coldest = df.loc[df['temperature'].idxmin()]
print(f"\nHottest day: {hottest['date'].date()} ({hottest['temperature']}°C)")
print(f"Coldest day: {coldest['date'].date()} ({coldest['temperature']}°C)")


plt.figure(figsize=(12,5))
plt.plot(df['date'], df['temperature'], label='Temperature')
plt.title('Temperature Changes Over Time')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.tight_layout()
plt.show()


def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'
df['season'] = df['month'].apply(get_season)
seasonal_avg = df.groupby('season')['temperature'].mean().round(2)
print('\nSeasonal average temperatures:')
print(seasonal_avg)


plt.figure(figsize=(6,4))
sns.barplot(x=seasonal_avg.index, y=seasonal_avg.values, palette='coolwarm')
plt.title('Seasonal Average Temperatures')
plt.ylabel('Temperature (°C)')
plt.xlabel('Season')
plt.tight_layout()
plt.show()
