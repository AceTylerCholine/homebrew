# Homebrew
Various scripts I've written

## Analyzers

Some scripts I wrote to analyze data. Not the scripts used for final data analysis.

## Extractors

GoNoGo_Processor.py & MID_Processor.py used to extract relevant data from EPrime data files and export the results to a csv.

Stroop_Processor.py used to extract relevant data from PsychoPy data files (.csv format) and export results to a new csv.

## Figure-Scripts

Some scripts I wrote to visualize specific data results. Not the scripts used to make final figures.

## MATLAB_Stroop

Color word Stroop program I made in a MATLAB class. Learning MATLAB helped me learn :snake:, but it was too bulky for my preference, so I haven't used it much since.
> [!WARNING]
> Functional, but barely

## Home Dir Files

### remove_begin_nums.py
I had a folder with a ton of files named '[#] [name].[ext]' and wanted to get rid of the numbers and space at the beginning of the name. Some names might've been duplicated with the numbers already removed, so this script removes those duplicates and continuously removes the first character of the each file's name until it's a letter

Looks like:
```python
import os

files = os.listdir()

for filename in files:
    if filename[0] != '.' and len(filename) > 1:
        while filename[0].isalpha() == False:
            if os.path.isfile(filename[1:]):
                os.remove(filename[1:])
            else:
                os.rename(filename, filename[1:])
                filename = filename[1:]
```

### shuffle_num_list.py
Creates a .txt of a range of numbers shuffled. Useful for creating a document to pull random subject ID's from.

The script contains to functions and variables with default min and max of 100 & 999. Edit these numbers before running the script:
```python
start_num = 100
end_num = 999
```
