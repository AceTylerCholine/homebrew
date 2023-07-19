import pandas as pd
import numpy as np
from statsmodels.multivariate.manova import MANOVA

# Read the CSV file
data = pd.read_csv('TaVNS_DATA_RAW_2023-07-12_1630.csv', usecols=columns)

# Remove Pre-screens & Pilots
data = data[~data['redcap_event_name'].str.contains('intake')]
data = data[~data['record_id'].str.contains('_')]
data = data.dropna()

# Rename columns
data = data.rename(columns={'hq_1':'BrainHQ_Attention_stars'})

# Specify the dependent variables
dependent_vars = ['BrainHQ_Attention_stars', 'nogo_responses_to_go', 'mid_overall_rt']

# Specify the independent variables
independent_vars = ['demo_1', 'demo_19']

# Filter the data for the active and sham groups
active_data = data[data['redcap_event_name'] == 'session_1_arm_2']
sham_data = data[data['redcap_event_name'] == 'session_1_arm_3']

# Check sample sizes of each group
active_size = len(active_data)
sham_size = len(sham_data)

# Determine the larger and smaller group
if active_size > sham_size:
    larger_group = active_data
    smaller_group = sham_data
else:
    larger_group = sham_data
    smaller_group = active_data

# Calculate the difference in sample sizes
size_diff = abs(active_size - sham_size)

# Randomly select participants from the larger group to match the sample size of the smaller group
random_indices = np.random.choice(larger_group.index, size=size_diff, replace=False)
balanced_larger_group = larger_group.loc[random_indices]

# Assign the balanced datasets to new variables
if active_size > sham_size:
    active_data = balanced_larger_group
else:
    sham_data = balanced_larger_group

# Specify the dependent and independent variables for the active group
active_dependent_vars = active_data[dependent_vars]
active_independent_vars = active_data[independent_vars]

# Specify the dependent and independent variables for the sham group
sham_dependent_vars = sham_data[dependent_vars]
sham_independent_vars = sham_data[independent_vars]

# Perform MANOVA
manova_formula = f'{", ".join(dependent_vars)} ~ {" + ".join(independent_vars)}'
manova_active = MANOVA(active_dependent_vars, active_independent_vars)
print(manova_active.mv_test())

manova_sham = MANOVA(sham_dependent_vars, sham_independent_vars)
print(manova_sham.mv_test())