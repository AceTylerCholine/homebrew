import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

columns = ['record_id', 'redcap_event_name', 'hq_1', 'nogo_responses_to_go', 'mid_overall_rt', 'demo_1', 'demo_19']

# Read the CSV file
data = pd.read_csv('TaVNS_DATA_RAW_2023-07-12_1630.csv', usecols=columns)

# Remove Pre-screens & Pilots
data = data[~data['redcap_event_name'].str.contains('intake')]
data = data[~data['record_id'].str.contains('_')]
data = data.dropna()

# Rename columns
data = data.rename(columns={'hq_1': 'BrainHQ_Attention_stars', 'demo_1': 'gender', 'demo_19': 'education'})

# Specify the dependent variables
dependent_vars = ['BrainHQ_Attention_stars', 'nogo_responses_to_go', 'mid_overall_rt']

# Specify the independent variables
independent_vars = ['gender', 'education']

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

# Combine the balanced datasets
balanced_data = pd.concat([active_data, sham_data])

# Perform ANCOVA separately for each dependent variable
for dep_var in dependent_vars:
    anova_formula = f'{dep_var} ~ {" + ".join(independent_vars)}'
    anova_model = ols(anova_formula, data=balanced_data).fit()
    anova_table = sm.stats.anova_lm(anova_model, typ=2)
    print(f"ANCOVA for {dep_var}")
    print(anova_table)
    print()
