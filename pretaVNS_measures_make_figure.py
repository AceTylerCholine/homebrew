import pandas as pd
from scipy.stats import ttest_ind
import numpy as np
import matplotlib.pyplot as plt

# Load the data into a DataFrame
df = pd.read_csv('TaVNS_DATA_RAW_2023-07-12_1630.csv')

# Remove Pilot data
df = df[~df['record_id'].str.contains('_Pilot')]

# Remove participant ids
df = df.drop(columns=['record_id'])

# Group the participants by arm
Active = df[df['redcap_event_name'] == 'session_1_arm_2']
Sham = df[df['redcap_event_name'] == 'session_1_arm_3']

# Group pre-taVNS data
dfpta = df[['redcap_event_name', 'impss_s0003_impsstotal_mjx', 'bdi_s0001_bditotal_mjx', 'baicog_022', 'naart_errors', 'tavns_setting']]
dfpta = dfpta.dropna()
dfpta.loc[df['redcap_event_name'] == 'session_1_arm_2', 'redcap_event_name'] = 'Active'
dfpta.loc[df['redcap_event_name'] == 'session_1_arm_3', 'redcap_event_name'] = 'Sham'
dfpta = dfpta.rename({'redcap_event_name':'Condition', 'impss_s0003_impsstotal_mjx':'IMPSS_Score', 'bdi_s0001_bditotal_mjx':'BDI_Score', 'baicog_022':'BAI_Score', 'naart_errors':'NAART_Score', 'taVNS_setting':'Stimulation_Setting'}, axis='columns')

dfptaactive = dfpta[dfpta['Condition'] == 'Active']
dfptasham = dfpta[dfpta['Condition'] == 'Sham']

# Get means as lists
dfptasham_mean = dfptasham.mean()
dfptaactive_mean = dfptaactive.mean()
dfptasham_mean = pd.Series(dfptasham_mean).tolist()
dfptaactive_mean = pd.Series(dfptaactive_mean).tolist()

# Get standard deviations as lists
dfptasham_std = dfptasham.std()
dfptaactive_std = dfptaactive.std()
dfptasham_std = pd.Series(dfptasham_std).tolist()
dfptaactive_std = pd.Series(dfptaactive_std).tolist()


# Assign means & stds
data = [dfptaactive_mean, dfptasham_mean]

std = [dfptaactive_std, dfptasham_std]

# Perform t-tests for 'Attention_Stars' and 'Total_Stars_Earned'
# att_tstat, att_pvalue = ttest_ind(dfhqactive['Attention_Stars'], dfhqsham['Attention_Stars'])
# total_tstat, total_pvalue = ttest_ind(dfhqactive['Total_Stars_Earned'], dfhqsham['Total_Stars_Earned'])

# Plot
tests = ['IMPSS', 'BDI', 'BAI', 'NAART', 'Stimulation']

plt.rc('axes', labelsize=16)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)

x_pos = np.arange(len(tests))

fig, ax = plt.subplots()
bar1 = ax.bar(x_pos, data[0], yerr=std[0], label='Active', color='#284b63', width=0.25, edgecolor='black', linewidth=3)
bar2 = ax.bar(x_pos+0.3, data[1], yerr=std[1], label='Sham', color='#c0354a', width=0.25, edgecolor='black', linewidth=3)

ax.set_ylabel('Score')
ax.set_xticks(x_pos+0.15)
ax.set_xticklabels(tests)
leg = ax.legend(loc='upper right', fontsize=16)
for line in leg.get_lines():
    line.set_linewidth(6.0)

# Add significance markers
# y = max(max(data[0]), max(data[1])) + max(max(std[0]), max(std[1])) + 0.5
# h = 0.5

# Mark 'Attention_Stars' significance
# if att_pvalue < 0.05:
#    col = 'red'
#    plt.plot([0*0.25, 1*0.3], [90,90], lw=1.5, c=col)
#    plt.text(0+0.15, 90, "*", ha='center', va='bottom', color=col, fontsize=16)

# Mark 'Total_Stars_Earned' significance
# if total_pvalue < 0.05:
#    col = 'red'
#    plt.plot([2, 2.3], [y, y], lw=1.5, c=col)
#    plt.text(2.15, y+h, "*", ha='center', va='bottom', color=col, fontsize=16)

fig.tight_layout()
fig.set_size_inches(14, 7)
plt.savefig('taVNS_Pre-Measures_Analysis.png', dpi=600)