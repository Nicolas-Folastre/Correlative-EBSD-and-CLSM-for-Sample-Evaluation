#Plot histograms together

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
#plt.style.use('seaborn-white')


csv1 = '/home/NFOLASTRE/Pictures/FIgure_Sc3_isosurface/SC3_Positions_XYZ_E123_micron_rotated_ROI_00_centered_rotZ.csv'
csv2 = '/home/NFOLASTRE/Pictures/FIgure_Sc3_isosurface/SC3_Positions_XYZ_E123_micron-cropped_rotated_ROI_01_centered_rotZ.csv'

# csv1 = '/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_out_centered_rotZ.csv'
# csv2 = '/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_ROI_01_rotated_centered_rotZ.csv'

# Read position XYZ + Euler Angles from EBSD
df1 = pd.read_csv(csv1, sep=',', header='infer',  index_col=None, usecols=None, engine='c', skiprows=None, nrows=None)
df1.columns = ['X', 'Y', 'Z', 'E1', 'E2', 'E3']
# keep only Z
x1 = df1['Z'].tolist()

df2 = pd.read_csv(csv2, sep=',', header='infer',  index_col=None, usecols=None, engine='c', skiprows=None, nrows=None)
df2.columns = ['X', 'Y', 'Z', 'E1', 'E2', 'E3']
x2 = df2['Z'].tolist()

mean2 =  np.mean(df2['Z'], axis=0)

beam_width = 1
hb = beam_width/2
# ratio of : counts in a 1um layer / total count
ratio = 0
counts1 = df2['Z'].shape[0]
for mean in np.arange(-0.5, 0.5, 0.01):
    df2_1um = df2.loc[(df2['Z'] >= mean-hb) & (df2['Z'] <= mean+hb)]
    counts2 = df2_1um['Z'].shape[0]
    if (counts2/counts1 > ratio):
        ratio = counts2/counts1
        mean2 = mean
        print(mean2, counts2, counts1, ratio)


fig = plt.figure()
ax = fig.add_subplot(111)

#add histograms
datas = [x1, x2]
colors = ['black', 'blue']
alphas = [0.5, 0.5]
labels = ['Data 1', 'Data 2']
for data, label, color, alpha in zip(datas, labels, colors, alphas):
    #ax.hist(data, bins=1000, label=label, color=color, alpha=alpha, range=[-7, 5], zorder = 2)
    ax.hist(data, bins=1000, label=label, color=color, alpha=alpha, range=[-4.5, 2.5], zorder = 2)

    ax.set_ybound(0, 4000)
ybound = ax.get_ybound()[1]

#add rectangle
left, bottom, width, height = (mean2-hb, 0, 2*hb, ybound)
rect = plt.Rectangle((left, bottom), width, height,
                     facecolor="green", alpha = 0.2, zorder = 0)
ax.add_patch(rect)
#add some vertical lines
xcoords = [mean2-hb, mean2+hb]
for xc in xcoords:
    plt.axvline(x=xc, color = 'darkgreen', zorder = 1)

#save figure
plt.savefig('/home/NFOLASTRE/Pictures/sc3_histo_bla.png', transparent=True)

# plt.show()


