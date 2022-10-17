import pandas as pd
import os
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
    # When copy and pasting the filename, it typically won't include .csv at the end. The .csv is necessary,
    # so this if statement adds the .csv, unless .csv is already included

col_list = ["congruent", "trials.thisRepN", "resp.corr", "resp.rt", "participant", "session", "date"]
    # List of only the columns that are needed to import from the csv

df = pd.read_csv(filename, usecols=col_list)

df = df.dropna()
    # Uses the "trials.thisRepN" column to remove the practice trials
    
df_num_corr = df['resp.corr'].sum()
    # Counts the number of correct responses
df_num_incor = len(df['resp.corr']) - df_num_corr
    # Subtracts number of correct responses from total number of responses to find incorrect responses
perc_corr = df_num_corr / 60
    
congr_df = df.loc[df['congruent'] == 'cong']
incongr_df = df.loc[df['congruent'] == 'incong']

overall_mean = df['resp.rt'].mean()
congr_rt_mean = congr_df['resp.rt'].mean()
incongr_rt_mean = incongr_df['resp.rt'].mean()

participant = str(int(df['participant'].iloc[0]))
session = str(int(df['session'].iloc[0]))

output = [{'Participant': participant, 'Session': session, 'Total Correct':df_num_corr, \
           'Total Incorrect':df_num_incor, 'Percent Correct': perc_corr,'Average Congruent RT':congr_rt_mean, \
           'Average Incongruent RT':incongr_rt_mean, 'Average RT':overall_mean}]

output_df = pd.DataFrame(output)

test_TimeDate = df['date'].iloc[0]
test_TimeDate = test_TimeDate[0:13] + test_TimeDate[14:16]

output_name = 'Stroop_' + 'P' + participant + '_S' + session + '_' + str(test_TimeDate) + '.csv'

output_df.to_csv(output_name, index=False)

Path(filename).rename("Raw_Processed_Data/" + filename)
Path(output_name).rename("Processed_Data/" + output_name)

filenamebase = filename[:-4]

filenamelog = filenamebase + '.log'
filenamepsy = filenamebase + '.psydat'
filenamexlsx = filenamebase + '.xlsx'

os.rename(filenamelog, "Raw_Processed_Data/" + filenamelog)
os.rename(filenamepsy, "Raw_Processed_Data/" + filenamepsy)
os.rename(filenamexlsx, "Raw_Processed_Data/" + filenamexlsx)