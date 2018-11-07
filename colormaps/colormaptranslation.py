import csv
from pathlib import Path
import os

# get path of the script
choice = 2
if choice == 1:
    scriptpath = Path(os.path.dirname(os.path.abspath(__file__)))
elif choice == 2:
    scriptpath = Path('./colormaps')

## Inputs:
# Path to the CSV file
csv_path = scriptpath / "./original_csvs/extended-black-body-table-float-0128.csv"
# Name that CFD Post uses to reference the colormap
cfdpostcolormapname = "Extended Black Body"
# Does CSV have header?
csv_has_header = True
# How many decimal places do you want for each number?
numdec = 5

## Translation:

listoflines = []
with csv_path.open() as csvfile:
    csvreader = csv.reader(csvfile)
    for line in csvreader:
        if csv_has_header:
            try:
                # if first entry fails to convert to float, skip the line
                float(line[0])
            except:
                pass
            else:
                # turn string into float, so that it can be rounded, 
                # and then turn back into float
                n = [str(round(float(x), numdec)) for x in line]
                listoflines.append(n)
        else:
            n = [str(round(float(x), numdec)) for x in line]
            listoflines.append(n)

# listoflines is now a list of floating point numbers, where each item
#   represents a colormap data point


def makeColormapCST(listoflines, colormapname, colormappath='.'):
    """ Creates .cst files of color maps for CFD Post

    Function to create a cst of a colormap from a list of colormap 
    data points.

    Parameters
    ----------
    listoflines : list
        List of all the floats that define the colormap. Each item in the 
        main list is one data point. The items in the sublist are [scalar,
        Red, Green, Blue] where all numbers are on a scale of 0->1.
    colormapname : string
        The name of the colormap to be made. This will be put in the cst 
        file itself and is what CFD Post will call the colormap. This will
        also be the name of the '.cst' file that is output.
    colormappath: Path
        The path to where the file should be saved. Default is '.', 
        corresponding to the current directory.

    """
    floats = []
    for n in listoflines:
        floats.extend(n)
        floats.append(float(1))

    initstring = '  Colour Map Colours = ' + ','.join(map(str, floats)) + '\n'

    header = f'COLOUR MAP:{colormapname}\n'
    footer = '  Colour Map Divisions = 2\n  Colour Map Storage Type = Preferences\n  Colour Map Type = Gradient\nEND'

    colormapnamemod = colormapname.replace(' ','_')
    filepath = colormappath / f'{colormapnamemod}.cst'
    with open(filepath, 'w+') as file:
        file.write(header)
        file.write(initstring)
        file.write(footer)


makeColormapCST(listoflines, cfdpostcolormapname, scriptpath)
