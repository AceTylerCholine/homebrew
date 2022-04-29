# homebrew
Various scripts I've written or any other data etc. that I might want to share

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ReadMe.txt for export_data_func.py
The Stroop Test on PsychoPy automatically saves data files in this folder.
It saves as a format of [participant ID]_date_time. It also saves multiple kinds
of files (csv, xslx, log, etc.). 

You can instantly delete all but the csv.

Run the "export_data_func.py" script (by double clicking it) to analyze the data.
You will need to enter the file name that you want to analyze (with/without .csv)

It will then create a file in the format of:
	P[Participant ID]_S[Session #]_Date_Time.csv

The script will also move the NEW file to the "Processed_Data" folder
and move the OLD file to the "Raw_Processed_Data" folder

This will give us a folder w/ all of the useful information
and a folder w/ backup full data

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
