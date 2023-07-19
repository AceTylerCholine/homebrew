import pandas as pd
from scipy.stats import ttest_ind

filename = input("Enter File Name: ")

if filename[-4:] != '.csv':
    filename = filename + '.csv'

columns = ['record_id', 'redcap_event_name', 'drug_result', 'impss_s0003_impsstotal_mjx', 'bdi_s0001_bditotal_mjx', 'baicog_022', 'naart_errors', 'tavns_setting', 'hq_1', 'hq_3', 'hq_4', 'hq_5', 'hq_6', 'hq_7', 'go_average_response_time', 'mid_overall_correct', 'mid_meanrt1', 'mid_meanrt2', 'mid_overall_rt', 'mid_lowrwrd_correct', 'mid_lowrwrd_rt', 'mid_highrwd_correct', 'mid_highrwd_rt', 'mid_lowpun_correct', 'mid_lowpun_rt', 'mid_highpun_correct', 'mid_highpun_rt', 'mid_neutral_correct', 'mid_neutral_rt', 'mid_earning_1', 'mid_earnings_2', 'mid_earnings_paid', 'nihcogcog_044', 'nihcogcog_045', 'nihcogcog_046', 'nihcogcog_047', 'nihcogcog_048', 'nihcogcog_017', 'nihcogcog_021', 'nihcogcog_022', 'nihcogcog_023', 'nihcogcog_024', 'nihcogcog_049', 'nihcogcog_052', 'nihcogcog_053', 'nihcogcog_054', 'nihcogcog_055', 'nihcogcog_056', 'stroop_per_corr', 'stroop_cong_rt', 'stroop_incog_rt', 'stroop_mean_rt', 'hrv_no_tavns_combined', 'hrv_no_tavns_rmssd', 'hrv_no_tavns_sdnn', 'hrv_no_tavns_mean_rr', 'hrv_no_tavns_lfhf_ratio', 'tavns_hrv_combined', 'tavns_rmssd', 'tavns_sdnn', 'tavns_mean_rr', 'tavns_lfhf_ratio']

# Load the data into a DataFrame
df = pd.read_csv(filename, usecols = columns)

# Remove Pilot data
df = df[~df['record_id'].str.contains('_Pilot')]

# Remove participant ids
df = df.drop(columns=['record_id'])

# Rename columns/measures to more accurate names
df = df.rename(columns={'impss_s0003_impsstotal_mjx':'Overall_ImpSS_Score', 'bdi_s0001_bditotal_mjx':'BDI_Total', 'baicog_022':'BAI_Total',
                        'hq_1':'BrainHQ_Attention_Stars', 'hq_3':'BrainHQ_Intelligence_Stars', 'hq_4':'BrainHQ_Total_Stars', 'hq_5':'BrainHQ_Levels_Complete', 
                        'hq_6':'BrainHQ_Percentile', 'hq_7':'Brain_AQ', 'go_average_response_time':'Go_RT', 
                        'mid_overall_correct':'MID_Correct', 'mid_meanrt1':'MID_Mean_RT1', 'mid_meanrt2':'MID_Mean_RT2', 
                        'mid_overall_rt':'MID_Overall_RT', 'mid_lowrwrd_correct':'MID_Low_Reward_Correct', 
                        'mid_lowrwrd_rt':'MID_Low_Reward_RT', 'mid_highrwd_correct':'MID_High_Reward_Correct', 
                        'mid_highrwd_rt':'MID_High_Reward_RT', 'mid_lowpun_correct':'MID_Low_Punishment_Correct', 
                        'mid_lowpun_rt':'MID_Low_Punishment_RT', 'mid_highpun_correct':'MID_High_Punishment_Correct', 
                        'mid_highpun_rt':'MID_High_Punishment_RT', 'mid_neutral_correct':'MID_Neutral_Correct', 
                        'mid_neutral_rt':'MID_Neutral_RT', 'mid_earning_1':'MID_Earning1', 'mid_earnings_2':'MID_Earning2', 
                        'mid_earnings_paid':'MID_Earning_Paid', 'nihcogcog_044':'Inhibit_Control_&_Attent_Computed', 
                        'nihcogcog_045':'Inhibit_Control_&_Attent_Uncorrected_Std_Score', 
                        'nihcogcog_046':'Inhibit_Control_&_Attent_Age_Corrected', 
                        'nihcogcog_047':'Inhibit_Control_&_Attent_Age_Percentile', 
                        'nihcogcog_048':'Inhibit_Control_&_Attent_Corrected_T_Score', 'nihcogcog_017':'Working_Memory_Raw', 
                        'nihcogcog_021':'Working_Memory_Uncorrected_Std_Score', 'nihcogcog_022':'Working_Memory_Age_Corrected', 
                        'nihcogcog_023':'Working_Memory_Age_Percentile', 'nihcogcog_024':'Working_Memory_Corrected_T_Score', 
                        'nihcogcog_049':'Executive_Function_Raw', 'nihcogcog_052':'Executive_Function_Computed', 
                        'nihcogcog_053':'Executive_Function_Uncorrected_Std_Score', 
                        'nihcogcog_054':'Executive_Function_Age_Corrected', 'nihcogcog_055':'Executive_Function_Age_Percentile', 
                        'nihcogcog_056':'Executive_Function_Corrected_T_Score', 'stroop_per_corr':'Stroop_%_Correct', 
                        'stroop_cong_rt':'Stroop_Congruent_RT', 'stroop_incog_rt':'Stroop_Incongruent_RT', 
                        'stroop_mean_rt':'Stroop_Mean_RT'})

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

    # Add the results to the results DataFrame
    results = results.append({'Test': col, 'Active Mean': Active_mean, 'Active SD': Active_std, 'Sham Mean': Sham_mean, 'Sham SD': Sham_std, 'P-Value': p}, ignore_index=True)

    # Save the results to a new CSV file
results.to_csv('taVNS_output.csv', index=False)
