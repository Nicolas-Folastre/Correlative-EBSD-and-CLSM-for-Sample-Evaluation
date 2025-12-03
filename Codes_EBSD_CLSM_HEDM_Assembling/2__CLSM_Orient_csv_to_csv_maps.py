# Reads a ctf or csv file containing (x y E! E2 E3)
# Orient the grains correcting SEM angle with surface normal (70 degrees)
# Write dataframe in an Image (8 bits and 32 bits) and a csv File

list_of_CLSM_Height_csv_files = ['/home/NFOLASTRE/Documents/Codes_EBSD_CLSM_HEDM_Assembling/data/SC13_Height.csv',
'/home/NFOLASTRE/Documents/Codes_EBSD_CLSM_HEDM_Assembling/data/SC3-03_Height.csv']
#path = '/home/NFOLASTRE/Downloads/SC3_Project 1 Specimen 2 Site 1 Map Data 4.ctf'

# importing libraries
import time
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.image
from matplotlib.image import imread
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

for path in list_of_CLSM_Height_csv_files:

    csvfile_out = add_suffix_to_filename(path, '_CLSM_tilted') + '.csv'
    print('Opening Ctf file:', path)
    with open(path) as f:
        reader = csv.reader(f, delimiter=",")
        d = list(reader)

    #metadata
    for line in range (0, 12):
        print(d[line][0], d[line][1])


    # I have to detect the canvas size and inject zeros in dataframe ---- OK
    # Data Table
    df_CLSM = pd.read_csv(path, sep=',', header=None,  index_col=None, usecols=None, engine='c', skiprows=15, nrows=None)
    df_CLSM = df_CLSM.fillna(0)
    
    df_CLSM = df_CLSM.apply(pd.to_numeric) # convert all columns of DataFrame in floats
    print(df_CLSM)
    # I Have to rotate the confocal/Lser Image too 

    #Draw a 32 bits 
     #Image size defined by Xcells and Ycells in ctf
    Image_X = int(d[8][1])
    Image_Y = int(d[9][1])
    PixelSize = float(d[6][1])
    
    #print(df_CLSM.shape)
    #print(df_CLSM)
    #df_CLSM.to_numpy()
    #print(df_CLSM.shape)
    #print(df_CLSM)

    # 32 bits image
    image32bits_out = add_suffix_to_filename(path, '_CLSM_tilted_32b') + '.tif'
    df = df_CLSM.to_numpy()
    grey32 = df.astype(np.float32)                                           

    # Convert to PIL Image and save
    Image.fromarray(grey32).save(image32bits_out)                                                   



    from tifffile import TiffWriter
    from imageio import imread
    resolution = 1
    image = imread(image32bits_out)
    with TiffWriter(image32bits_out) as tif_w:
        tif_w.write(image,
                    resolution=resolution)


    # Read back from disk and convert to Numpy array
    reloaded = np.array(Image.open(image32bits_out))  