# Reads a ctf or csv file containing (x y E! E2 E3)
# Orient the grains correcting SEM angle with surface normal (70 degrees)
# Write dataframe in an Image (8 bits and 32 bits) and a csv File

list_of_elements = ['/home/NFOLASTRE/Downloads/SC3_Project 1 Specimen 2 Site 1 Map Data 4.ctf',
'/home/NFOLASTRE/Downloads/SC13_Specimen 1 Site 1 Map Data 1.ctf']
#path = '/home/NFOLASTRE/Downloads/SC3_Project 1 Specimen 2 Site 1 Map Data 4.ctf'

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
from PIL import Image
import csv

def add_suffix_to_filename(path, suffix):
    index_ = path.rfind('.')
    if index_ == -1:
        return path + suffix
    return path[:index_] + suffix

for path in list_of_elements:

    csvfile_out = add_suffix_to_filename(path, '_EBSD_tilted') + '.csv'
    print('Opening Ctf file:', path)
    with open(path) as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)
    print(d[1][0]) # [line] [column]

    #metadata
    for line in range (1, 11):
        print(d[line][0], d[line][1])
    for col in range(6):
        print(d[11][2*col+1], d[11][2*col+2])

    TiltAngle = math.degrees(float(d[11][10])) #reads the tilt angle between stage and SEM detector in radians and convert in degrees
    print(TiltAngle, 'degrees tilt correction')

    # Data Table
    df_EBSD = pd.read_csv(path, sep='\t', header=1,  index_col=None, usecols=None, engine='c', skiprows=13, nrows=None)
    #print(df_EBSD)

    # Aligning Euler Angles to SEM point of view considering tiltAngle
    df_EBSD['Euler1'] -= TiltAngle
    #print(df_EBSD)

    #Writing modified EBSD dataframe
    print('writing...')
    df_EBSD.to_csv(csvfile_out, index=False)