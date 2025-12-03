#Plot histograms together for euler

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
xE1 = df1['E1'].tolist()
xE2 = df1['E2'].tolist()
xE3 = df1['E3'].tolist()

df2 = pd.read_csv(csv2, sep=',', header='infer',  index_col=None, usecols=None, engine='c', skiprows=None, nrows=None)
df2.columns = ['X', 'Y', 'Z', 'E1', 'E2', 'E3']
yE1 = df2['E1'].tolist()
yE2 = df2['E2'].tolist()
yE3 = df2['E3'].tolist()

mean2 =  np.mean(df2['Z'], axis=0)

beam_width = 1
hb = beam_width/2
# ratio of : counts in a 1um layer / total count
ratio = 0
counts1 = df2['E1'].shape[0]
for mean in np.arange(-0.5, 0.5, 0.01):
    df2_1um = df2.loc[(df2['Z'] >= mean-hb) & (df2['Z'] <= mean+hb)]
    counts2 = df2_1um['E1'].shape[0]
    if (counts2/counts1 > ratio):
        ratio = counts2/counts1
        mean2 = mean
        print(mean2, counts2, counts1, ratio)


fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(131)

#add histograms
datas = [xE1, yE1]
colors = ['black', 'blue']
alphas = [0.5, 0.5]
labels = ['xE1', 'yE1']
zorder = [0, 1]
for data, label, color, alpha, zorder in zip(datas, labels, colors, alphas, zorder):
    #ax.hist(data, bins=1000, label=label, color=color, alpha=alpha, range=[-7, 5], zorder = 2)
    ax.hist(data, bins=360, label=label, color=color, alpha=alpha, range=[0, 360], zorder = zorder)
    ax.set_ybound(0, 6000)
ybound = ax.get_ybound()[1]

ax = fig.add_subplot(132)
datas = [xE2, yE2]
colors = ['black', 'blue']
alphas = [0.5, 0.5]
labels = ['xE1', 'yE1']
zorder = [0, 1]
for data, label, color, alpha, zorder in zip(datas, labels, colors, alphas, zorder):
    #ax.hist(data, bins=1000, label=label, color=color, alpha=alpha, range=[-7, 5], zorder = 2)
    ax.hist(data, bins=180, label=label, color=color, alpha=alpha, range=[0, 180], zorder = zorder)
    ax.set_ybound(0, 6000)
ybound = ax.get_ybound()[1]

ax = fig.add_subplot(133)
datas = [xE3, yE3]
colors = ['black', 'blue']
alphas = [0.5, 0.5]
labels = ['xE1', 'yE1']
zorder = [0, 1]
for data, label, color, alpha, zorder in zip(datas, labels, colors, alphas, zorder):
    #ax.hist(data, bins=1000, label=label, color=color, alpha=alpha, range=[-7, 5], zorder = 2)
    ax.hist(data, bins=360, label=label, color=color, alpha=alpha, range=[0, 360], zorder = zorder)

    ax.set_ybound(0, 6000)
ybound = ax.get_ybound()[1]

#save figure
plt.savefig('/home/NFOLASTRE/Pictures/sc3_histo_E123.png', transparent=True)

# plt.show()


