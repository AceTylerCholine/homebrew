import pandas as pd
from pathlib import Path

filename = input("Enter File Name: ")

if len(filename) < 23:
    print('Are you sure that\'s the right file?')
    answer = input("Enter yes or no: ")
    if answer == "yes":
        print('No, I think you\'re mistaken. Try again')
    elif answer == "no":
        print('I thought so, try again')
        filename = input("Enter File Name: ")

if filename[-4:] != '.csv':
    filename = filename + '.csv'

df = pd.read_csv(filename)

df_num_corr = sum(df.iloc[12:72,17])
df_num_incor = len(df.iloc[12:72,17]) - df_num_corr

df_noTrials = df.drop(range(0,12))

congr_df = df_noTrials.loc[df['congruent'] == 'cong']
incongr_df = df_noTrials.loc[df['congruent'] == 'incong']

overall_mean = df_noTrials['resp.rt'].mean(skipna = True)
congr_rt_mean = congr_df['resp.rt'].mean()
incongr_rt_mean = incongr_df['resp.rt'].mean()

participant = df.iat[0,27]
session = str(int(df.iat[0,28]))

output = [{'Participant': participant, 'Session': session, 'Total Correct':df_num_corr, \
           'Total Incorrect':df_num_incor, 'Average RT':overall_mean, \
           'Average Congruent RT':congr_rt_mean, 'Average Incongruent RT':incongr_rt_mean}]

output_df = pd.DataFrame(output)

test_TimeDate = df.iloc[0,29]
test_TimeDate = test_TimeDate[0:13] + test_TimeDate[14:16]

output_name = 'P' + participant + '_S' + session + '_' + test_TimeDate + '.csv'

output_df.to_csv(output_name, index=False)

Path(filename).rename("Raw_Processed_Data/" + filename)
Path(output_name).rename("Processed_Data/" + output_name)
