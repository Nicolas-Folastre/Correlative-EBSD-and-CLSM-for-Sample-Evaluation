# Reads a ctf or csv file containing (x y E! E2 E3)
# Orient the grains correcting SEM angle with surface normal (70 degrees)
# Write dataframe in an Image (8 bits and 32 bits) and a csv File

list_of_elements = ['/home/NFOLASTRE/Documents/Codes_EBSD_CLSM_HEDM_Assembling/data/SC3_Project 1 Specimen 2 Site 1 Map Data 4.ctf',
'/home/NFOLASTRE/Documents/Codes_EBSD_CLSM_HEDM_Assembling/data/SC13_Specimen 1 Site 1 Map Data 1.ctf']
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

for path in list_of_elements:

    csvfile_out = add_suffix_to_filename(path, '_EBSD_tilted') + '.csv'
    print('Opening Ctf file:', path)
    with open(path) as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)

    #metadata
    for line in range (1, 11):
        print(d[line][0], d[line][1])
    for col in range(6):
        print(d[11][2*col+1], d[11][2*col+2])

    TiltAngle = math.degrees(float(d[11][10])) #reads the tilt angle between stage and SEM detector in radians and convert in degrees
    print(TiltAngle, 'degrees tilt correction')

    # Data Table
    df_EBSD = pd.read_csv(path, sep='\t', header=1,  index_col=None, usecols=None, engine='c', skiprows=13, nrows=None)
    df_EBSD = df_EBSD.apply(pd.to_numeric) # convert all columns of DataFrame in floats
    #print(df_EBSD)

    # Aligning Euler Angles to SEM point of view considering tiltAngle
    df_EBSD['Euler1'] -= TiltAngle
    #print(df_EBSD)

    #Writing modified EBSD dataframe
    print('writing...')
    df_EBSD.to_csv(csvfile_out, index=False)

    #Draw a 32 bits and a 8 bits image from band 
     #Image size defined by Xcells and Ycells in ctf
    Image_X = int(d[4][1])
    Image_Y = int(d[5][1])
    PixelSize = float(d[6][1])
    df_BC = df_EBSD[["BC"]]
    df_BC.to_numpy()

    # 8 bits Image
    image8bits_out = add_suffix_to_filename(path, '_EBSD_tilted') + '.png'
    array_data = np.reshape(df_BC, (int(Image_Y), int(Image_X)))
    # Create a NumPy array with random values
    array_data = array_data.astype(np.uint8)
    # Define the file name to save the image
    image_file_name = add_suffix_to_filename(path, '_EBSD_tilted_8b') + '.png'
    # Convert the NumPy array to an image object
    image = Image.fromarray(array_data)
    # Save the image object to a PNG file
    image.save(image_file_name)
    # Verify by loading and displaying the saved image (optional)
    #loaded_image = Image.open(image_file_name)
    #loaded_image.show()

    # 32 bits images
    # Euler 1
    euler_list = ['Euler1', 'Euler2', 'Euler3']
    
    import tifffile
    import tifftools



    for euler in euler_list:
        df_E = df_EBSD[euler]
        df_E.to_numpy()
        image32bits_out = add_suffix_to_filename(path, '_EBSD_tilted_32b_') + euler + '.tif'

        df = df_E.to_numpy()
        df = np.reshape(df, (int(Image_Y), int(Image_X)))
        grey32 = df.astype(np.float32)                                           

        # Convert to PIL Image and save
        Image.fromarray(grey32).save(image32bits_out)
        
        tifftools.tiff_set(
            image32bits_out,
            image32bits_out,
            overwrite=True,
            setlist=[
                (
                    tifftools.Tag.RESOLUTIONUNIT,
                    tifftools.constants.ResolutionUnit.CENTIMETER.value,
                ),
                (tifftools.Tag.XRESOLUTION, PixelSize),
                (tifftools.Tag.YRESOLUTION, PixelSize),
            ],
        )
        #with tifffile(image32bits_out, mode='r+') as tif:
        #    _ = tif.pages[0].tags['XResolution'].overwrite((2000, 1000))                                              

        # Read back from disk and convert to Numpy array
        reloaded = np.array(Image.open(image32bits_out))  