# BRUTE FORCE find orientation

    # Description of the code
# Input: csv file of projected EBSD data on confocal map ['#EBSD X', 'Y', 'Z', 'E1', 'E2', 'E3']
# Output: csv file of projected EBSD data on confocal map with the following modifications:
#           - ROI is oriented so the surface is the most normal possible to the Z axis (Z variation minimized by rotating XYZ around X,Y,Z axis)
#           - Euler Angles are corrected accordingly ['#EBSD X', 'Y', 'Z', 'E1', 'E2', 'E3']
# Note: the local variation of Z is not considered yet to correct the euler angles 

# importing libraries
import time
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.spatial.transform import Rotation as R
from math import sin, cos, acos, sqrt, fabs, atan
from scipy.optimize import minimize
from scipy import ndimage
from pathlib import Path
import os

# Initialisation

csvfile='/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_ROI_01_rotated_centered_rotZ.csv'
#csvfile='/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_out_centered_rotZ.csv'

#csvfile='/home/NFOLASTRE/Pictures/FIgure_Sc3_isosurface/SC3_Positions_XYZ_E123_micron-cropped_rotated_ROI_01_centered_rotZ.csv'
#csvfile='/home/NFOLASTRE/Pictures/FIgure_Sc3_isosurface/SC3_Positions_XYZ_E123_micron_rotated_ROI_00_centered_rotZ.csv'

plot_positions_2=True

def add_suffix_to_filename(path, suffix):
    index_ = path.rfind('.')
    if index_ == -1:
        return path + suffix
    return path[:index_] + suffix + path[index_:]
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

csvfile_out_centered = add_suffix_to_filename(csvfile, "_centered")
csvfile_out_centered_rotZ = add_suffix_to_filename(csvfile, "_centered_rotZ")

# Read position XYZ + Euler Angles from EBSD
df_XYZ_Full = pd.read_csv(csvfile, sep=',', header='infer',  index_col=None, usecols=None, engine='c', skiprows=None, nrows=None)
df_XYZ_Full.columns = ['X', 'Y', 'Z', 'E1', 'E2', 'E3']

# Reduce data
data_part = 1
df_XYZ_Full = df_XYZ_Full.iloc[::int(1/data_part)]
print('data ', round(100*data_part, 2), '%')

# filter in Z
filter_Z = -20
df_XYZ_Full = df_XYZ_Full[df_XYZ_Full['Z'] > filter_Z]
print('filter_Z >', filter_Z)

# Create a list of colors correspondin to E1 E2 E3 (RGB)
#df_XYZ_Full['norm'] = round((3/2)*sqrt(df_XYZ_Full['E1']/360 + df_XYZ_Full['E2']/180 + df_XYZ_Full['E3']/360)/(sqrt(3))).astype('float', errors = 'ignore')





#norm1 = df_XYZ_Full['E1']/360 + df_XYZ_Full['E2']/180 + df_XYZ_Full['E3']/360
#norm2 = round((3/2)*sqrt(x)/sqrt(3)) for x in norm1

#df_XYZ_Full['norm'] = norm2

#df_XYZ_Full['norm'] = np.where(sqrt(df_XYZ_Full['E1']/360 + df_XYZ_Full['E2']/180 + df_XYZ_Full['E3']/360)/(sqrt(3))>=1/3, 1, 0)

print(df_XYZ_Full)

rgb = df_XYZ_Full[['E1', 'E2', 'E3']]
rgb2 = df_XYZ_Full[['E1', 'E2', 'E3']]

## Nor;alize and filter by diagonal of cube norm 9 TO AVOID DARK COLORS (under 1/3 of diagonal)
#rgb['E1'] = df_XYZ_Full['norm']*df_XYZ_Full['E1']*255/360
#rgb['E2'] = df_XYZ_Full['norm']*df_XYZ_Full['E2']*255/180
#rgb['E3'] = df_XYZ_Full['norm']*df_XYZ_Full['E3']*255/360


def E1_to_RGB(E1, E2, E3):
    if sqrt((E1/360)**2 + (E2/180)**2 + (E3/360)**2)/sqrt(3) <= 0.5:
        if E1 < 360/2: E1 = 360 - E1
    return E1

def E2_to_RGB(E1, E2, E3):
    if sqrt((E1/360)**2 + (E2/180)**2 + (E3/360)**2)/sqrt(3) <= 0.5:
        if E2 < 180/2: E2 = 180 - E2
    return E2

def E3_to_RGB(E1, E2, E3):
    if sqrt((E1/360)**2 + (E2/180)**2 + (E3/360)**2)/sqrt(3) <= 0.5:
        if E3 < 360/2: E3 = 360 - E3
    return E3

rgb2['E1'] = rgb.apply(lambda r: E1_to_RGB(*r), axis=1)
#rgb2['E2'] = rgb.apply(lambda r: E2_to_RGB(*r), axis=1)
rgb2['E3'] = rgb.apply(lambda r: E3_to_RGB(*r), axis=1)

rgb2['E1'] = rgb2['E1']*255/360
rgb2['E2'] = rgb2['E2']*255/180
rgb2['E3'] = rgb2['E3']*255/360

def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

rgb2 = rgb2.astype('int')
rgb2['hex'] = rgb2.apply(lambda r: rgb_to_hex(*r), axis=1)

print(rgb)
print('plotting')

#coloring = df_XYZ_Full['Z']
#coloring_norm = [-2 + 4 * float(i)/sum(coloring) for i in coloring]

# PLOT positions XYZ ROTATED
if plot_positions_2==True:
    fig2 = plt.figure(figsize=(10, 5))
    """ 
    ax1 = fig2.add_subplot(121, projection='3d')
    ax1.scatter3D(df_XYZ_Full['E1'], df_XYZ_Full['E2'], df_XYZ_Full['E3'], facecolors = rgb2['hex'])
    ax1.set_title("INITIAL")
    ax1.set_xlabel('X-axis', fontweight ='bold') 
    ax1.set_ylabel('Y-axis', fontweight ='bold') 
    ax1.set_zlabel('Z-axis', fontweight ='bold') """
    
    
    ax2 = fig2.add_subplot(121, projection='3d')
    ax2.scatter3D(df_XYZ_Full['X'], df_XYZ_Full['Y'], df_XYZ_Full['Z'], facecolors = rgb2['hex'], s = 1)
    ax2.set_title("Colored Euler as RGB")
    ax2.set_xlabel('X-axis', fontweight ='bold') 
    ax2.set_ylabel('Y-axis', fontweight ='bold') 
    ax2.set_zlabel('Z-axis', fontweight ='bold')
    ax2.set_zlim([-20, 20])
    #ax2.set_xlim([-100, 100])
    ax2.set_ylim([-100, 100])


    ax3 = fig2.add_subplot(122, projection='3d')
    ax3.scatter3D(df_XYZ_Full['X'], df_XYZ_Full['Y'], df_XYZ_Full['Z'], c=df_XYZ_Full['Z'], s=1)
    #ax3.scatter3D(df_XYZ_Full['X'], df_XYZ_Full['Y'], df_XYZ_Full['Z'], c=df_XYZ_Full['Z'], s=1, vmin=-1, vmax =1)
    ax3.set_title("Colored Euler as RGB")
    ax3.set_xlabel('X-axis', fontweight ='bold')
    ax3.set_ylabel('Y-axis', fontweight ='bold')
    ax3.set_zlabel('Z-axis', fontweight ='bold')
    ax3.set_zlim([-20, 20])
    #ax3.set_xlim([-100, 100])
    ax3.set_ylim([-100, 100])
    

    facecolors=rgb

    plt.show()


