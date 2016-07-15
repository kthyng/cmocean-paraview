'''
Conversion from rgb files to Paraview colormap files.

This reads in the colormap rgb from github directly, and it is stored
locally by np.genfromtxt.

Adapted code from Phillip Wolfram.
'''

import os
import numpy as np
import cmocean


# number of levels for colormap
N = 256
x = np.linspace(0, 1, N)

# location of local rgb files
# Update to matplotlib from kthyng once matplotlib is updated.
loc = 'https://raw.githubusercontent.com/kthyng/cmocean/master/cmocean/rgb/'

# file list
Files = [loc + name + '-rgb.txt' for name in cmocean.cm.cmapnames]

if not os.path.exists('xml'):
    os.makedirs('xml')

# Loop through rgb files and make xml file
for File in Files:

    # read in rgb values
    rgb = np.genfromtxt(File)

    # convert to colormap
    cmap = cmocean.tools.cmap(rgb, N=N)

    # back to rgb, now correct number of levels
    rgb = cmocean.tools.print_colormaps([cmap], N=N)[0]

    # file name
    fname = File.split('/')[-1].split('-')[0]
    f = open('xml/' + fname + '.xml', 'w')

    # write the first line of syntax
    f.write('<ColorMap name="' + name + '" space="RGB">\n')

    # loop through rgb to write to file
    for j in range(rgb.shape[0]):
        f.write('<Point x="%f" o="1" r="%f" g="%f" b="%f"/>\n' % (x[j], rgb[j, 0], rgb[j, 1], rgb[j, 2]))

    # final line
    f.write('</ColorMap>')

    f.close()
