import pandas as pd
from pathlib import Path
from dateutil import parser
from datetime import datetime

filename = input("Enter File Name: ")

if filename[-4:] != '.csv':
    filename = filename + '.csv'

df = pd.read_csv(filename, usecols = ['Subject','Session','SessionDate','SessionTime','GoProbe.CRESP','GoProbe.RESP','GoProbe.RT','NogoProbe.RESP','Procedure[SubTrial]'])

df.columns = df.columns.str.replace('.', '_')
df.columns = df.columns.str.replace(']','')
df.columns = df.columns.str.replace('[','_')

NoGoResps = df['NogoProbe_RESP'].count()

NoRespToGoDF = df[(df["GoProbe_CRESP"] == "{SPACE}") ^ (df["GoProbe_RESP"] =="{SPACE}")]
NoRespToGo = len(NoRespToGoDF)

GoRTMean = df[["GoProbe_RT"]].mean()
GoRTMeanInt = int(GoRTMean)

NoGoCount = df.Procedure_SubTrial.value_counts().NogoProc
GoCount = df.Procedure_SubTrial.value_counts().GoProc

NoGoRespPerc = NoGoResps / NoGoCount

participant = str(df.iat[0,0])
session = str(df.iat[0,1])

output = [{'Participant': participant, 'Session': session, 'Go_Responses_to_NoGo': NoGoResps, \
           'NoGo_Responses_to_Go': NoRespToGo, 'Go_Average_Response_Time': GoRTMeanInt, 'Number_of_Go_Stimuli': GoCount, \
           'Number_of_NoGo_Stimuli': NoGoCount, 'Percent_of_NoGo_Stimuli_Responded_With_Go': NoGoRespPerc}]

output_df = pd.DataFrame(output)

test_date = df.iloc[0,2]
test_time = df.iloc[0,3]
test_dateTime = test_date + ' ' + test_time
dateTime_dateTime = parser.parse(test_dateTime)
dateTime_string = dateTime_dateTime.strftime("%Y-%m-%d_%H%M")

output_name = 'P' + participant + '_S' + session + '_' + dateTime_string + '.csv'

output_df.to_csv(output_name, index=False)