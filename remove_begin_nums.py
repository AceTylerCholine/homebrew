# I had a folder with a ton of files named '[#] [name].[ext]' and wanted to get rid of the numbers and space at the beginning of the name. Some names might've been duplicated with the numbers already removed, so this script removes those duplicates and continuously removes the first character of the each file's name until it's a letter

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
