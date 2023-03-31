import pandas as pd
from scipy.stats import ttest_ind

columns = ['record_id', 'redcap_event_name', 'impss_s0003_impsstotal_mjx', 'bdi_s0001_bditotal_mjx', 'naart_errors', 'hq_1', 'hq_3', 'hq_4', 'hq_5', 'hq_6', 'hq_7', 'go_average_response_time', 'mid_overall_correct', 'mid_meanrt1', 'mid_meanrt2', 'mid_overall_rt', 'mid_lowrwrd_correct', 'mid_lowrwrd_rt', 'mid_highrwd_correct', 'mid_highrwd_rt', 'mid_lowpun_correct', 'mid_lowpun_rt', 'mid_highpun_correct', 'mid_highpun_rt', 'mid_neutral_correct', 'mid_neutral_rt', 'mid_earning_1', 'mid_earnings_2', 'mid_earnings_paid', 'nihcogcog_041', 'nihcogcog_044', 'nihcogcog_045', 'nihcogcog_046', 'nihcogcog_047', 'nihcogcog_048', 'nihcogcog_017', 'nihcogcog_021', 'nihcogcog_022', 'nihcogcog_023', 'nihcogcog_024', 'nihcogcog_049', 'nihcogcog_052', 'nihcogcog_053', 'nihcogcog_054', 'nihcogcog_055', 'nihcogcog_056', 'stroop_per_corr', 'stroop_cong_rt', 'stroop_incog_rt', 'stroop_mean_rt', 'hrv_no_tavns_combined', 'hrv_no_tavns_rmssd', 'hrv_no_tavns_sdnn', 'hrv_no_tavns_mean_rr', 'hrv_no_tavns_lfhf_ratio', 'tavns_hrv_combined', 'tavns_rmssd', 'tavns_sdnn', 'tavns_mean_rr', 'tavns_lfhf_ratio']

# Load the data into a DataFrame
df = pd.read_csv('TaVNS_DATA_2023-03-30_1411.csv', usecols = columns)

# Remove Pilot data
df = df[~df['record_id'].str.contains('_Pilot')]

# Remove participant ids
df = df.drop(columns=['record_id'])

# Group the participants by arm
Active = df[df['redcap_event_name'] == 'session_1_arm_2']
Sham = df[df['redcap_event_name'] == 'session_1_arm_3']

# Create a new DataFrame to store the results
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

    # Add the results to the results DataFrame
    results = results.append({'Test': col, 'Active Mean': Active_mean, 'Active SD': Active_std, 'Sham Mean': Sham_mean, 'Sham SD': Sham_std, 'P-Value': p}, ignore_index=True)

    # Save the results to a new CSV file
results.to_csv('taVNS_output.csv', index=False)
