import pandas as pd
from scipy.stats import ttest_ind

filename = input("Enter File Name: ")

if filename[-4:] != '.csv':
    filename = filename + '.csv'

pomscolumns = ['record_id', 'redcap_event_name', 'poms1_0_friendly', 'poms1_t1_tense', 'poms1_a_angry', 'poms1_f_worn_out', 'poms1_d_unhappy', 'poms1_0_clear_headed', 'poms1_v_lively', 'poms1_c1_confused', 'poms1_d_sorry_for_things', 'poms1_t1_shaky', 'poms1_f_listless', 'poms1_a_peeved', 'poms1_0_considerate', 'poms1_d_sad', 'poms1_v_active', 'poms1_t1_on_edge', 'poms1_a_grouchy', 'poms1_d_blue', 'poms1_v_energetic', 'poms1_t1_panicky', 'poms1_d_hopeless', 'poms1_t2_relaxed', 'poms1_d_unworthy', 'poms1_a_spiteful', 'poms1_0_sympathetic', 'poms1_t1_uneasy', 'poms1_t1_restless', 'poms1_c1_unable_concentrat', 'poms1_f_fatigued', 'poms1_0_helpful', 'poms1_a_annoyed', 'poms1_d_discouraged', 'poms1_a_resentful', 'poms1_t1_nervous', 'poms1_d_lonely', 'poms1_d_miserable', 'poms1_c1_muddled', 'poms1_v_cheerful', 'poms1_a_bitter', 'poms1_f_exhausted', 'poms1_t1_anxious', 'poms1_a_ready_to_fight', 'poms1_0_good_natured', 'poms1_d_gloomy', 'poms1_d_desperate', 'poms1_f_sluggish', 'poms1_a_rebellious', 'poms1_d_helpless', 'poms1_f_weary', 'poms1_c1_bewildered', 'poms1_v_alert', 'poms1_a_deceived', 'poms1_a_furious', 'poms1_c2_efficient', 'poms1_0_trusting', 'poms1_v_full_of_pep', 'poms1_a_bad_tempered', 'poms1_d_worthless', 'poms1_c1_forgetful', 'poms1_v_carefree', 'poms1_d_terrified', 'poms1_d_guilty', 'poms1_v_vigorous', 'poms1_c1_uncertain', 'poms1_f_bushed', 'poms2_0_friendly', 'poms2_t1_tense', 'poms2_a_angry', 'poms2_f_worn_out', 'poms2_d_unhappy', 'poms2_0_clear_headed', 'poms2_v_lively', 'poms2_c1_confused', 'poms2_d_sorry_for_things', 'poms2_t1_shaky', 'poms2_f_listless', 'poms2_a_peeved', 'poms2_0_considerate', 'poms2_d_sad', 'poms2_v_active', 'poms2_t1_on_edge', 'poms2_a_grouchy', 'poms2_d_blue', 'poms2_v_energetic', 'poms2_t1_panicky', 'poms2_d_hopeless', 'poms2_t2_relaxed', 'poms2_d_unworthy', 'poms2_a_spiteful', 'poms2_0_sympathetic', 'poms2_t1_uneasy', 'poms2_t1_restless', 'poms2_c1_unable_concentrat', 'poms2_f_fatigued', 'poms2_0_helpful', 'poms2_a_annoyed', 'poms2_d_discouraged', 'poms2_a_resentful', 'poms2_t1_nervous', 'poms2_d_lonely', 'poms2_d_miserable', 'poms2_c1_muddled', 'poms2_v_cheerful', 'poms2_a_bitter', 'poms2_f_exhausted', 'poms2_t1_anxious', 'poms2_a_ready_to_fight', 'poms2_0_good_natured', 'poms2_d_gloomy', 'poms2_d_desperate', 'poms2_f_sluggish', 'poms2_a_rebellious', 'poms2_d_helpless', 'poms2_f_weary', 'poms2_c1_bewildered', 'poms2_v_alert', 'poms2_a_deceived', 'poms2_a_furious', 'poms2_c2_efficient', 'poms2_0_trusting', 'poms2_v_full_of_pep', 'poms2_a_bad_tempered', 'poms2_d_worthless', 'poms2_c1_forgetful', 'poms2_v_carefree', 'poms2_d_terrified', 'poms2_d_guilty', 'poms2_v_vigorous', 'poms2_c1_uncertain', 'poms2_f_bushed']

# Load the data into DataFrames
pomsdf = pd.read_csv(filename, usecols=pomscolumns)

# Remove Pilot data
pomsdf = pomsdf[~pomsdf['record_id'].str.contains('_Pilot')]

# Remove Arm1 & incomplete data
pomsdf = pomsdf.dropna()

# Create Tension_Total columns
t1_cols_poms1 = [col for col in pomsdf if col.startswith('poms1_t1')]
t2_cols_poms1 = [col for col in pomsdf if col.startswith('poms1_t2')]
pomsdf['p1t1_sum'] = pomsdf[t1_cols_poms1].sum(axis=1)
pomsdf['p1t2_sum'] = pomsdf[t2_cols_poms1].sum(axis=1)
pomsdf['POMS1_Tension_Total'] = pomsdf['p1t1_sum'] - pomsdf['p1t2_sum']
t1_cols_poms2 = [col for col in pomsdf if col.startswith('poms2_t1')]
t2_cols_poms2 = [col for col in pomsdf if col.startswith('poms2_t2')]
pomsdf['p2t1_sum'] = pomsdf[t1_cols_poms2].sum(axis=1)
pomsdf['p2t2_sum'] = pomsdf[t2_cols_poms2].sum(axis=1)
pomsdf['POMS2_Tension_Total'] = pomsdf['p2t1_sum'] - pomsdf['p2t2_sum']
pomsdf['POMS_Tension_Difference'] = pomsdf['POMS2_Tension_Total'] - pomsdf['POMS1_Tension_Total']

# Create Depression_Total columns
d_cols_poms1 = [col for col in pomsdf if col.startswith('poms1_d')]
pomsdf['POMS1_Depression_Total'] = pomsdf[d_cols_poms1].sum(axis=1)
d_cols_poms2 = [col for col in pomsdf if col.startswith('poms2_d')]
pomsdf['POMS2_Depression_Total'] = pomsdf[d_cols_poms2].sum(axis=1)
pomsdf['POMS_Depression_Difference'] = pomsdf['POMS2_Depression_Total'] - pomsdf['POMS1_Depression_Total']

# Create Anger_Total columns
a_cols_poms1 = [col for col in pomsdf if col.startswith('poms1_a')]
pomsdf['POMS1_Anger_Total'] = pomsdf[a_cols_poms1].sum(axis=1)
a_cols_poms2 = [col for col in pomsdf if col.startswith('poms2_a')]
pomsdf['POMS2_Anger_Total'] = pomsdf[a_cols_poms2].sum(axis=1)
pomsdf['POMS_Anger_Difference'] = pomsdf['POMS2_Anger_Total'] - pomsdf['POMS1_Anger_Total']

# Create Fatigue_Total column for POMS1
f_cols_poms1 = [col for col in pomsdf if col.startswith('poms1_f')]
pomsdf['POMS1_Fatigue_Total'] = pomsdf[f_cols_poms1].sum(axis=1)
f_cols_poms2 = [col for col in pomsdf if col.startswith('poms2_f')]
pomsdf['POMS2_Fatigue_Total'] = pomsdf[f_cols_poms2].sum(axis=1)
pomsdf['POMS_Fatigue_Difference'] = pomsdf['POMS2_Fatigue_Total'] - pomsdf['POMS1_Fatigue_Total']

# Create Confusion_Total columns
c1_cols_poms1 = [col for col in pomsdf if col.startswith('poms1_c1')]
c2_cols_poms1 = [col for col in pomsdf if col.startswith('poms1_c2')]
pomsdf['p1c1_sum'] = pomsdf[c1_cols_poms1].sum(axis=1)
pomsdf['p1c2_sum'] = pomsdf[c2_cols_poms1].sum(axis=1)
pomsdf['POMS1_Confusion_Total'] = pomsdf['p1c1_sum'] - pomsdf['p1c2_sum']
c1_cols_poms2 = [col for col in pomsdf if col.startswith('poms2_c1')]
c2_cols_poms2 = [col for col in pomsdf if col.startswith('poms2_c2')]
pomsdf['p2c1_sum'] = pomsdf[c1_cols_poms2].sum(axis=1)
pomsdf['p2c2_sum'] = pomsdf[c2_cols_poms2].sum(axis=1)
pomsdf['POMS2_Confusion_Total'] = pomsdf['p2c1_sum'] - pomsdf['p2c2_sum']
pomsdf['POMS_Confusion_Difference'] = pomsdf['POMS2_Confusion_Total'] - pomsdf['POMS1_Confusion_Total']

# Create Vigour_Total columns
v_cols_poms1 = [col for col in pomsdf if col.startswith('poms1_v')]
pomsdf['POMS1_Vigour_Total'] = pomsdf[v_cols_poms1].sum(axis=1)
v_cols_poms2 = [col for col in pomsdf if col.startswith('poms2_v')]
pomsdf['POMS2_Vigour_Total'] = pomsdf[v_cols_poms2].sum(axis=1)
pomsdf['POMS_Vigour_Difference'] = pomsdf['POMS2_Vigour_Total'] - pomsdf['POMS1_Vigour_Total']

# Create TMD columns
TMD_v_cols_poms1 = ['POMS1_Tension_Total', 'POMS1_Depression_Total', 'POMS1_Anger_Total', 'POMS1_Fatigue_Total', 'POMS1_Confusion_Total']
pomsdf['POMS1_Total_Mood_Disturbance'] = pomsdf[TMD_v_cols_poms1].sum(axis=1) - pomsdf['POMS1_Vigour_Total']
TMD_v_cols_poms2 = ['POMS2_Tension_Total', 'POMS2_Depression_Total', 'POMS2_Anger_Total', 'POMS2_Fatigue_Total', 'POMS2_Confusion_Total']
pomsdf['POMS2_Total_Mood_Disturbance'] = pomsdf[TMD_v_cols_poms2].sum(axis=1) - pomsdf['POMS2_Vigour_Total']
pomsdf['POMS_TMD_Difference'] = pomsdf['POMS2_Total_Mood_Disturbance'] - pomsdf['POMS1_Total_Mood_Disturbance']

# Select columns for results
poms_results = pomsdf[['redcap_event_name', 'POMS1_Tension_Total', 'POMS1_Depression_Total', 'POMS1_Anger_Total', 'POMS1_Fatigue_Total', 'POMS1_Confusion_Total', 'POMS1_Vigour_Total', 'POMS1_Total_Mood_Disturbance', 'POMS2_Tension_Total', 'POMS2_Depression_Total', 'POMS2_Anger_Total', 'POMS2_Fatigue_Total', 'POMS2_Confusion_Total', 'POMS2_Vigour_Total', 'POMS2_Total_Mood_Disturbance', 'POMS_Tension_Difference', 'POMS_Depression_Difference', 'POMS_Anger_Difference', 'POMS_Fatigue_Difference', 'POMS_Confusion_Difference', 'POMS_Vigour_Difference', 'POMS_TMD_Difference']].copy()

# Group the participants by arm
ActivePOMS = poms_results[poms_results['redcap_event_name'] == 'session_1_arm_2']
ShamPOMS = poms_results[poms_results['redcap_event_name'] == 'session_1_arm_3']

# Create a new DataFrame to store the combined results
combined_results = pd.DataFrame(columns=['Test', 'Active Mean', 'Active SD', 'Sham Mean', 'Sham SD', 'P-Value'])

# Iterate over each column in the DataFrame
for col in poms_results.columns[1:]:
    Active_scores = ActivePOMS[col]
    Sham_scores = ShamPOMS[col]

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
combined_results.to_csv('taVNS_POMS_output.csv', index=False)
