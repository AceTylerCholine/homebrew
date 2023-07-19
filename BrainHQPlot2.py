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

# Group BrainHQ data
dfhq = df[['redcap_event_name', 'hq_1', 'hq_3', 'hq_4', 'hq_5', 'hq_6', 'hq_7']]
dfhq = dfhq.dropna()
dfhq.loc[df['redcap_event_name'] == 'session_1_arm_2', 'redcap_event_name'] = 'Active'
dfhq.loc[df['redcap_event_name'] == 'session_1_arm_3', 'redcap_event_name'] = 'Sham'
dfhq = dfhq.rename({'redcap_event_name':'Condition', 'hq_1':'Attention_Stars', 'hq_3':'Intelligence_Stars', 'hq_4':'Total_Stars_Earned', 'hq_5':'Levels_Complete', 'hq_6':'Percentile', 'hq_7':'Brain_AQ'}, axis='columns')

dfhqactive = dfhq[dfhq['Condition'] == 'Active']
dfhqsham = dfhq[dfhq['Condition'] == 'Sham']

# Get means as lists
dfhqsham_mean = dfhqsham.mean()
dfhqactive_mean = dfhqactive.mean()
dfhqsham_mean = pd.Series(dfhqsham_mean).tolist()
dfhqactive_mean = pd.Series(dfhqactive_mean).tolist()

# Get standard deviations as lists
dfhqsham_std = dfhqsham.std()
dfhqactive_std = dfhqactive.std()
dfhqsham_std = pd.Series(dfhqsham_std).tolist()
dfhqactive_std = pd.Series(dfhqactive_std).tolist()


# Assign means & stds for Brain_AQ
data = [dfhqactive_mean[-1:],
dfhqsham_mean[-1:]]

std = [dfhqactive_std[-1:],
dfhqsham_std[-1:]]

# Perform t-tests for 'Attention_Stars' and 'Total_Stars_Earned'
BrainAQ_tstat, BrainAQ_pvalue = ttest_ind(dfhqactive['Brain_AQ'], dfhqsham['Brain_AQ'])

# Plot
tests = ['Brain_AQ']

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
y = max(max(data[0]), max(data[1])) + max(max(std[0]), max(std[1])) + 0.5
h = 0.5

# Mark 'Attention_Stars' significance
if BrainAQ_pvalue < 0.05:
    col = 'red'
    plt.plot([0*0.25, 1*0.3], [1100,1100], lw=1.5, c=col)
    plt.text(0+0.15, 1100, "*", ha='center', va='bottom', color=col, fontsize=16)

fig.tight_layout()
fig.set_size_inches(14, 7)
# plt.show()
plt.savefig('taVNS_BrainHQ_Analysis_2.png', dpi=600)