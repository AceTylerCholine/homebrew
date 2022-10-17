import pandas as pd
from pathlib import Path
from dateutil import parser
from datetime import datetime

filename = input("Enter File Name: ")

if filename[-4:] != '.csv':
    filename = filename + '.csv'

columns = ['Session', 'Handedness', 'NARGUID', 'PracticeRT', 'SessionDate', 'SessionTime', 'Condition', 'meanrt', 'moneyamt', 'percentacc', 'prbacc', 'prbrt', 'ResponseCheck', 'Result']

df = pd.read_csv(filename, usecols = columns)

df = df.iloc[2:]   # Removes the top 2 rows

lowReward = df['Condition'] == "SmallReward"
lowRewardDF = df[lowReward]

highReward = df['Condition'] == "LgReward"
highRewardDF = df[highReward]

lowPun = df['Condition'] == "SmallPun"
lowPunDF = df[lowPun]

highPun = df['Condition'] == "LgPun"
highPunDF = df[highPun]

neutral = df['Condition'] == "Triangle"
neutralDF = df[neutral]

def MID_dictFunc():
    
    participant = df['NARGUID'].iat[1]
    session = df['Session'].iat[1]
    
    overallCount = df['prbacc'].count()
    overallCorrCount = df['prbacc'].sum()
    overallPerCorr = overallCorrCount / overallCount
    overallRT = df['meanrt'].iat[-1]
    
    lowRewardCorr = lowRewardDF["prbacc"].sum()
    lowRewardTot = len(lowRewardDF)
    lowRewardPerCorr = lowRewardCorr / lowRewardTot
    lowRewardRT = lowRewardDF[lowRewardDF["prbrt"] != 0]["prbrt"].mean()
    
    highRewardCorr = highRewardDF["prbacc"].sum()
    highRewardTot = len(highRewardDF)
    highRewardPerCorr = highRewardCorr / highRewardTot
    highRewardRT = highRewardDF[highRewardDF["prbrt"] != 0]["prbrt"].mean()
    
    lowPunCorr = lowPunDF["prbacc"].sum()
    lowPunTot = len(lowPunDF)
    lowPunPerCorr = lowPunCorr / lowPunTot
    lowPunRT = lowPunDF[lowPunDF["prbrt"] != 0]["prbrt"].mean()
    
    highPunCorr = highPunDF["prbacc"].sum()
    highPunTot = len(highPunDF)
    highPunPerCorr = highPunCorr / highPunTot
    highPunRT = highPunDF[highPunDF["prbrt"] != 0]["prbrt"].mean()
    
    neutralCorr = neutralDF["prbacc"].sum()
    neutralTot = len(neutralDF)
    neutralPerCorr = neutralCorr / neutralTot
    neutralRT = neutralDF[neutralDF["prbrt"] != 0]["prbrt"].mean()
    
    moneyEarned = df['moneyamt'].iat[-1]
    
    return locals()

MID_dict = MID_dictFunc()
output = [MID_dict]
output_df = pd.DataFrame(output)

participant = df['NARGUID'].iat[1]
session = df['Session'].iat[1]
test_date = df['SessionDate'].iat[1]
test_time = df['SessionTime'].iat[1]
test_dateTime = test_date + ' ' + test_time
dateTime_dateTime = parser.parse(test_dateTime)
dateTime_string = dateTime_dateTime.strftime("%Y-%m-%d_%H%M")

output_name = 'MID_' + 'P' + str(participant) + '_S' + str(session) + '_' + dateTime_string + '.csv'

output_df.to_csv(output_name, index=False)