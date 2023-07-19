import pandas as pd
from scipy.stats import ttest_ind

filename = input("Enter File Name: ")

if filename[-4:] != '.csv':
    filename = filename + '.csv'

sidescolumns = ['record_id', 'redcap_event_name', 'side_effects_headache', 'side_effects_neck_pain', 'side_effects_nausea', 'side_effects_contractions', 'side_effects_stinging', 'side_effects_burning', 'side_effects_uncomfortable', 'side_effects_other', 'side_effects_headache_f49bb9', 'side_effects_neck_pain_1af83c', 'side_effects_nausea_93ab48', 'side_effects_contractions_b9821b', 'side_effects_stinging_fa864e', 'side_effects_burning_3fab3d', 'side_effects_uncomfortable_dc0a40', 'side_effects_other_677a7f']

# Load the data into DataFrames
sidesdf = pd.read_csv(filename, usecols=sidescolumns)

# Rename columns to split Side Effects 1 & 2
sidesdf = sidesdf.rename(columns={'side_effects_headache':'side_effects1_headache', 'side_effects_neck_pain':'side_effects1_neck_pain', \
                        'side_effects_nausea':'side_effects1_nausea', 'side_effects_contractions':'side_effects1_contractions', \
                        'side_effects_stinging':'side_effects1_stinging', 'side_effects_burning':'side_effects1_burning', \
                        'side_effects_uncomfortable':'side_effects1_uncomfortable', 'side_effects_other':'side_effects1_other', \
                        'side_effects_headache_f49bb9':'side_effects2_headache', 'side_effects_neck_pain_1af83c':'side_effects2_neck_pain', \
                        'side_effects_nausea_93ab48':'side_effects2_nausea', 'side_effects_contractions_b9821b':'side_effects2_contractions', \
                        'side_effects_stinging_fa864e':'side_effects2_stinging', 'side_effects_burning_3fab3d':'side_effects2_burning', \
                        'side_effects_uncomfortable_dc0a40':'side_effects2_uncomfortable', 'side_effects_other_677a7f':'side_effects2_other'})

# Remove Pilot data
sidesdf = sidesdf[~sidesdf['record_id'].str.contains('_Pilot')]

# Remove Arm1 & incomplete data
sidesdf = sidesdf.dropna()

# Create Total columns
s1_cols = [col for col in sidesdf if col.startswith('side_effects1')]
s2_cols = [col for col in sidesdf if col.startswith('side_effects2')]
sidesdf.loc[:, 'side_effects_1_sum'] = sidesdf[s1_cols].sum(axis=1)
sidesdf.loc[:, 'side_effects_2_sum'] = sidesdf[s2_cols].sum(axis=1)
sidesdf.loc[:, 'side_effects_avg'] = (sidesdf['side_effects_1_sum'] + sidesdf['side_effects_2_sum']) / 2

# Group the participants by arm
ActiveSides = sidesdf[sidesdf['redcap_event_name'] == 'session_1_arm_2']
ShamSides = sidesdf[sidesdf['redcap_event_name'] == 'session_1_arm_3']

# Create a new DataFrame to store the combined results
combined_results = pd.DataFrame(columns=['Test', 'Active Mean', 'Active SD', 'Sham Mean', 'Sham SD', 'P-Value'])

# Iterate over each column in the DataFrame
for col in sidesdf.columns[2:]:
    Active_scores = ActiveSides[col]
    Sham_scores = ShamSides[col]

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

    # Concatenate the test results to the combined results DataFrame
    combined_results = pd.concat([combined_results, test_results], ignore_index=True)
    
# Save the combined results to a new CSV file
combined_results.to_csv('taVNS_Side_Effects_output.csv', index=False)