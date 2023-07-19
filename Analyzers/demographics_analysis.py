import pandas as pd
from scipy.stats import ttest_ind

filename = input("Enter File Name: ")

if filename[-4:] != '.csv':
    filename = filename + '.csv'

columns = ['record_id', 'redcap_event_name', 'demo_1', 'demo_3', 'demo_4', 'demo_5___1', 'demo_5___2', 'demo_5___3', 'demo_5___4', 'demo_5___5', 'demo_5___6', 'demo_7', 'demo_19', 'demo_21', 'demo_22', 'demo_27', 'demo_28']

# Load the data into a DataFrame
df = pd.read_csv(filename, usecols=columns)

# Remove Pilot data
df = df[~df['record_id'].str.contains('_Pilot')]

# Remove participant ids
df = df.drop(columns=['record_id'])

# Rename columns/measures to more accurate names
df = df.rename(columns={'demo_1': 'Gender', 'demo_3': 'Age', 'demo_4': 'Ethnicity', 'demo_5___1': 'Native_American', 'demo_5___2': 'Asian', 'demo_5___3': 'Black', 'demo_5___4': 'Pacific_Islander', 'demo_5___5': 'White', 'demo_5___6': 'Other_Race', 'demo_7': 'American_Born', 'demo_19': 'Education', 'demo_21': 'Mother_education', 'demo_22': 'Employed', 'demo_27': 'Income', 'demo_28': 'Marital_Status'})

# Group the participants by arm
Active = df[df['redcap_event_name'] == 'session_1_arm_2']
Sham = df[df['redcap_event_name'] == 'session_1_arm_3']

# Create a new DataFrame to store the results (each row is a measurement, columns are stats of each measure)
results = pd.DataFrame(columns=['Test', 'Active Mean', 'Active SD', 'Sham Mean', 'Sham SD', 'P-Value'])

# Iterate over each column in the DataFrame
for col in df.columns[1:]:  # Get the scores for the current test for each arm
    Active_scores = Active[col]
    Sham_scores = Sham[col]

    # Calculate the mean and standard deviation for each arm
    Active_mean = Active_scores.mean()
    Active_std = Active_scores.std()
    Sham_mean = Sham_scores.mean()
    Sham_std = Sham_scores.std()

    # Perform a t-test
    t, p = ttest_ind(Active_scores, Sham_scores, nan_policy='omit')

    # Create a DataFrame for the current test
    test_results = pd.DataFrame({'Test': [col],
                                 'Active Mean': [Active_mean],
                                 'Active SD': [Active_std],
                                 'Sham Mean': [Sham_mean],
                                 'Sham SD': [Sham_std],
                                 'P-Value': [p]})

    # Concatenate the test results to the results DataFrame
    results = pd.concat([results, test_results], ignore_index=True)

# Save the results to a new CSV file
results.to_csv('taVNS_demographics.csv', index=False)
