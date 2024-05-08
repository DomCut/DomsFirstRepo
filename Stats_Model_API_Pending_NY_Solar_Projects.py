# Homework Assignment 4 Dominic Cutrara 4/18/2024
# This script performs multiple regression and logistic regression analyses using data from 'pending_NY_solar_energy_projects_data.json'.
# The multiple regression model predicts project costs based on the application year and county,
# while the logistic regression model predicts project status as a binary outcome.
# Import necessary packages. 
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load data from JSON into a DataFrame
data = pd.read_json("C:/Users/dcutrara/Desktop/pending_NY_solar_energy_projects_data.json")

# Convert 'date_application_received' from string to datetime format and extract the year
data['date_application_received'] = pd.to_datetime(data['date_application_received'], errors='coerce')
data['application_year'] = data['date_application_received'].dt.year

# Convert project 'project_cost' to numeric and prepare a binary outcome for logistic regression
data['project_cost'] = pd.to_numeric(data['project_cost'], errors='coerce')
data['is_pipeline'] = (data['project_status'] == 'Pipeline').astype(int)

# Create dummy variables for 'county'
county_dummies = pd.get_dummies(data['county'], prefix='County', drop_first=True).astype(float)
data = pd.concat([data, county_dummies], axis=1)

# Setup for multiple regression
X_mult = data[['application_year'] + list(county_dummies.columns)]
X_mult = sm.add_constant(X_mult)  # Adding a constant
X_mult = X_mult.apply(pd.to_numeric, errors='coerce')
Y_mult = pd.to_numeric(data['project_cost'], errors='coerce')

# Clean NaN values from data for multiple regression model
X_mult.dropna(inplace=True)
Y_mult = Y_mult.loc[X_mult.index].dropna()

# Setup for logistic regression with regularization
X_logit = data[['application_year'] + list(county_dummies.columns)]
X_logit = sm.add_constant(X_logit)  # Adding a constant
X_logit = X_logit.apply(pd.to_numeric, errors='coerce')
Y_logit = data['is_pipeline']

# Clean NaN values from data for logistic regression model 
X_logit.dropna(inplace=True)
Y_logit = Y_logit.loc[X_logit.index].dropna()

# Fit the multiple regression model
try:
    model_mult = sm.OLS(Y_mult, X_mult).fit()
    print("Multiple Regression Model Summary:")
    print(model_mult.summary())
except Exception as e:
    print("Error in fitting the multiple regression model:", e)

# Fit the logistic regression model with L1 regularization
try:
    # Using L1 regularization with alpha for regularization strength
    model_logit = sm.Logit(Y_logit, X_logit).fit_regularized(method='l1', alpha=1.0, disp=True)
    print("\nLogistic Regression Model Summary (Regularized):")
    print(model_logit.summary())
except Exception as e:
    print("Error in fitting the logistic regression model (Regularized):", e)
