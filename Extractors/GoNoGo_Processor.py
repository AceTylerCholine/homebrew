import pandas as pd
from pathlib import Path
from dateutil import parser
from datetime import datetime

filename = input("Enter File Name: ")

if filename[-4:] != '.csv':
    filename = filename + '.csv'

df = pd.read_csv(filename, usecols = ['Subject','Session','SessionDate','SessionTime','GoProbe.ACC','GoProbe.RT','NogoProbe.RESP','Procedure[SubTrial]'])

df.columns = df.columns.str.replace(']','')
df.columns = df.columns.str.replace('[','_')

NoGoResps = df['NogoProbe.RESP'].count()

NoRespToGo = len(df[df["GoProbe.ACC"]==0])

GoRTMean = df[["GoProbe.RT"]].mean()
GoRTMeanInt = int(GoRTMean)

NoGoCount = df.Procedure_SubTrial.value_counts().NogoProc
GoCount = df.Procedure_SubTrial.value_counts().GoProc

NoGoRespPerc = NoGoResps / NoGoCount
GoMissPerc = NoRespToGo / GoCount

participant = str(df.iat[0,0])
session = str(df.iat[0,1])

output = [{'Participant': participant, 'Session': session, 'Go_Responses_to_NoGo': NoGoResps, \
           'NoGo_Responses_to_Go': NoRespToGo, 'Go_Average_Response_Time': GoRTMeanInt, 'Number_of_Go_Stimuli': GoCount, \
           'Number_of_NoGo_Stimuli': NoGoCount, 'Percent_of_NoGo_Stimuli_Responded_With_Go': NoGoRespPerc, 'Percent_of_Go_Missed': GoMissPerc}]

output_df = pd.DataFrame(output)

test_date = df['SessionDate'].iat[1]
test_time = df['SessionTime'].iat[1]
test_dateTime = test_date + ' ' + test_time
dateTime_dateTime = parser.parse(test_dateTime)
dateTime_string = dateTime_dateTime.strftime("%Y-%m-%d_%H%M")

output_name = 'GoNoGo_' + 'P' + str(participant) + '_S' + str(session) + '_' + dateTime_string + '.csv'

output_df.to_csv(output_name, index=False)
