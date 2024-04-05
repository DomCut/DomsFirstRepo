# Homework Assignment 3, Dominic Cutrara 4/4/2024
# Import all necessary packages
import requests
import json
from collections import defaultdict

# Constants
URL = 'https://data.ny.gov/resource/3x8r-34rs.json'

# Advanced query tailored for fetching the Top 50 most expensive solar panel 'pending' projects following applications after '2016-01-01T00:00:00 in NY'
query = {
    '$select': 'contractor, project_cost, project_status, date_application_received, county',
    '$where': "project_status = 'Pipeline' AND date_application_received > '2016-01-01T00:00:00'",
    '$order': 'project_cost DESC',
    '$limit': 50
}

try:
    # Fetch data from the API
    response = requests.get(URL, params=query)
    response.raise_for_status()  # This raises HTTPError for bad responses
    
    # Load JSON response
    data = response.json()

    # Checking and displaying the fetched data
    if not data:
        print("No pending projects found.")
    else:
        print("Most expensive pending projects:")
        print(f"{'Contractor':<30} {'Cost ($)':>15} {'County':<15} {'Start Date':<15}")
        print("-" * 75)  # Print a separator line
        
        total_cost = 0
        for project in data:
            project_cost = float(project.get('project_cost', 0))
            total_cost += project_cost
            print(f"{project.get('contractor', 'N/A')[:28]:<30} {project_cost:>15,.2f} {project.get('county', 'Unknown')[:13]:<15} {project.get('date_application_received', 'N/A')[:10]:<15}")

        # Summary statistics
        total_projects = len(data)
        average_cost = total_cost / total_projects if total_projects else 0

        print("\nSummary Statistics:")
        print(f"Total Projects: {total_projects}")
        print(f"Total Cost: ${total_cost:,.2f}")
        print(f"Average Project Cost: ${average_cost:,.2f}")

    # Save data to a JSON file
    with open('pending_NY_solar_energy_projects_data.json', 'w') as file:
        json.dump(data, file, indent=4)

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)
except requests.exceptions.ConnectionError as e:
    print("Connection Error:", e)
except requests.exceptions.Timeout as e:
    print("Timeout Error:", e)
except requests.exceptions.RequestException as e:
    print("Unexpected error fetching data:", e)
