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


# Assign means & stds besides BrainAQ (because AQ is a vastly different scale)
data = [dfhqactive_mean[:-1],
dfhqsham_mean[:-1]]

std = [dfhqactive_std[:-1],
dfhqsham_std[:-1]]

# Plot
tests = ['Attention Stars', 'Intelligence Stars', 'Total Stars Earned', 'Levels Complete', 'Percentile']

# Perform t-tests for 'Attention_Stars' and 'Total_Stars_Earned'
att_tstat, att_pvalue = ttest_ind(dfhqactive['Attention_Stars'], dfhqsham['Attention_Stars'])
total_tstat, total_pvalue = ttest_ind(dfhqactive['Total_Stars_Earned'], dfhqsham['Total_Stars_Earned'])
lvls_tstat, lvls_pvalue = ttest_ind(dfhqactive['Levels_Complete'], dfhqsham['Levels_Complete'])

# Plot
tests = ['Attention Stars', 'Intelligence Stars', 'Total Stars Earned', 'Levels Complete', 'Percentile']

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
if att_pvalue < 0.05:
    col = 'red'
    plt.plot([0*0.25, 1*0.3], [90,90], lw=1.5, c=col)
    plt.text(0+0.15, 90, "*", ha='center', va='bottom', color=col, fontsize=16)

# Mark 'Total_Stars_Earned' significance
if total_pvalue < 0.05:
    col = 'red'
    plt.plot([2, 2.3], [135, 135], lw=1.5, c=col)
    plt.text(2.15, 135, "*", ha='center', va='bottom', color=col, fontsize=16)
    
# Mark 'Levels_Complete' significance
if lvls_pvalue < 0.05:
    col = 'red'
    plt.plot([3, 3.3], [32, 32], lw=1.5, c=col)
    plt.text(3.15, 32, "*", ha='center', va='bottom', color=col, fontsize=16)

fig.tight_layout()
fig.set_size_inches(14, 7)
plt.savefig('taVNS_BrainHQ_Analysis_1.png', dpi=600)
