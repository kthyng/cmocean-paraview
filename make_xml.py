'''
Conversion from rgb files to Paraview colormap files.

This reads in the colormap rgb from github directly, and it is stored
locally by np.genfromtxt.

Adapted code from Phillip Wolfram (https://gist.github.com/1c042b2a1382eca5415d3139cf591379).
'''

import os
import numpy as np
import cmocean


# number of levels for colormap
N = 256
x = np.linspace(0, 1, N)

# location of local rgb files
loc = 'https://raw.githubusercontent.com/matplotlib/cmocean/master/cmocean/rgb/'

# file list
Files = [loc + name + '-rgb.txt' for name in cmocean.cm.cmapnames]

if not os.path.exists('xml'):
    os.makedirs('xml')

# make indexed file
fall = open('xml/cmocean_all.xml', 'w')
fall.write('<ColorMaps>\n')

# Loop through rgb files and make xml file
for File, name in zip(Files, cmocean.cm.cmapnames):

    # read in rgb values
    rgb = np.genfromtxt(File)

    # convert to colormap
    cmap = cmocean.tools.cmap(rgb, N=N)

    # back to rgb, now correct number of levels
    rgb = cmocean.tools.print_colormaps([cmap], N=N)[0]

    # file name
    fname = File.split('/')[-1].split('-')[0]
    findv = open('xml/' + fname + '.xml', 'w')

    # write the first line of syntax for individual file
    findv.write('<ColorMaps>\n')

    for af in [findv, fall]:
        af.write('<ColorMap name="cmocean_' + name + '" space="RGB">\n')

    # loop through rgb to write to file
    for j in range(rgb.shape[0]):
        for af in [findv, fall]:
            af.write('<Point x="%f" o="1" r="%f" g="%f" b="%f"/>\n' % (x[j], rgb[j, 0], rgb[j, 1], rgb[j, 2]))

    # final line
    for af in [findv, fall]:
        af.write('</ColorMap>\n')

    findv.write('</ColorMaps>')
    findv.close()

fall.write('</ColorMaps>')
fall.close()
