
import os
import csv

os.chdir('/Users/larrys/Dropbox-Personal/Dropbox/QGIS/fossildigtools/DonleyTrics/ident-files')

GENUSINDENTS = {}

with open('genus-idents.txt', 'rb') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONE)
    for row in reader:
        GENUSINDENTS[row[0].strip()] = row[1].strip()

print repr(GENUSINDENTS)
