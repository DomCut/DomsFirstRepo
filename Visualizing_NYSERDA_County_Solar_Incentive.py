#Homework 5 Dominic Cutrara 4/25/2024
#Import all necessary packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import requests
from datetime import datetime

#Load solar eletric programs JSON from the url
url = "https://data.ny.gov/resource/3x8r-34rs.json"
data = requests.get(url).json()

#Convert JSON data to pandas dataframe
df = pd.DataFrame(data)

#Convert 'project_cost' and 'total_nyserda_incentive' to float
df['project_cost'] = pd.to_numeric(df['project_cost'], errors='coerce')
df['total_nyserda_incentive'] = pd.to_numeric(df['total_nyserda_incentive'], errors='coerce')
df['date_install'] = pd.to_datetime(df['date_install'])

#Prepare data for the stacked bar chart to distinguish 'total_nyserda_incentive' and 'project_cost'
grouped_data = df.groupby('county').agg({'project_cost': 'mean', 'total_nyserda_incentive': 'mean'}).reset_index()

# Visualization 1: Stacked Bar Chart of Average Project Cost and Average NYSERDA Incentive by County
plt.figure(figsize=(12, 6))
#Bottom bar (project_cost) formatted in tableau colorblind palette
plt.bar(grouped_data['county'], grouped_data['project_cost'], color=sns.color_palette("tab10")[0], label='Avg. Project Cost')
# Top bar (total_nyserda_incentive), stacked on top of project_cost tableau colorblind palette
plt.bar(grouped_data['county'], grouped_data['total_nyserda_incentive'], bottom=grouped_data['project_cost'], color=sns.color_palette("tab10")[1], label='Avg. NYSERDA Incentive')
plt.title('Stacked Bar Chart of Average Project Cost and NYSERDA Incentives by County')
plt.ylabel('Average Amount ($)')
plt.xticks(rotation=45)
plt.legend()
plt.show()

#Convert 'date_install' to a bi-annual period for Visualization 2
#Custom grouping by six-month periods, defining H1 as Jan-Jun and H2 as Jul-Dec
df['install_biannual'] = df['date_install'].dt.to_period('M').dt.strftime('%Y') + '-' + \
                         df['date_install'].dt.month.map(lambda x: 'H1' if x <= 6 else 'H2')
df_grouped = df.groupby('install_biannual').agg({'total_nyserda_incentive': 'mean'}).reset_index()
df_grouped.set_index('install_biannual', inplace=True)
installation_counts_biannual = df['install_biannual'].value_counts().sort_index()

#Find the year with the most installations
yearly_counts = df['date_install'].dt.year.value_counts()
max_year = yearly_counts.idxmax()
max_year_count = yearly_counts.max()

fig, ax1 = plt.subplots(figsize=(12, 6))

#Visualization 2: Timeline of Project Installations by Bi-Annual Period with line element to show best years for 'total_nyserda_incentive'
color = 'tab:gray'
ax1.set_xlabel('Bi-Annual Period')
ax1.set_ylabel('Number of Installations', color=color)
bars = ax1.bar(installation_counts_biannual.index, installation_counts_biannual, color=[color if str(max_year) not in idx else 'tab:orange' for idx in installation_counts_biannual.index])
ax1.tick_params(axis='y', labelcolor=color)

#Line chart element for average 'total_nyserda_incentive' for each bi-annual period since 2001
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Average NYSERDA Incentive ($)', color=color)
ax2.plot(df_grouped.index, df_grouped['total_nyserda_incentive'], color=color, marker='o', linestyle='-')
ax2.tick_params(axis='y', labelcolor=color)

#Use FixedLocator for x-axis ticks to limit x-axis overlap for viewrship 
tick_positions = range(len(installation_counts_biannual))
ax1.xaxis.set_major_locator(ticker.FixedLocator(tick_positions))  # Ensure each bi-annual period is labeled clearly
ax1.set_xticklabels(installation_counts_biannual.index, rotation=45, horizontalalignment='right')

plt.title('Number of Project Installations and Average Incentives by Bi-Annual Period')

#Extra annotation for the year with the most installations
highlight = f'Year {max_year} had the most installations: {max_year_count}'
ax1.annotate(highlight, xy=(0.5, 0.9), xycoords='axes fraction', ha='center', va='bottom',
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='orange', facecolor='yellow', alpha=0.5))

plt.show()
