from PIL import Image
import numpy as np
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
import csv


path = '/home/NFOLASTRE/Downloads/SC13_Specimen 1 Site 1 Map Data 1.ctf'
df_EBSD = pd.read_csv(path, sep='\t', header=1,  index_col=None, usecols=None, engine='c', skiprows=13, nrows=None)
df_EBSD = df_EBSD[["BC"]]
Image_X, Image_Y = 399, 4096
df_EBSD.to_numpy()
print(df_EBSD)













import numpy as np
import matplotlib.pyplot as plt

dpi = 80 # Arbitrary. The number of pixels in the image will always be identical
data = np.reshape(df_EBSD, (int(Image_X), int(Image_Y))) 

height, width = np.array(data.shape, dtype=float) / dpi

fig = plt.figure(figsize=(width, height), dpi=dpi)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

ax.imshow(data, interpolation='none')
fig.savefig('test.tif', dpi=dpi)


