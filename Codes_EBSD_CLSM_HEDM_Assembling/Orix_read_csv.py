#%matplotlib inline
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

import tempfile

from diffpy.structure import Atom, Lattice, Structure
import matplotlib.pyplot as plt
import numpy as np

from orix import data, io, plot
from orix.crystal_map import CrystalMap, Phase, PhaseList
from orix.quaternion import Orientation, Rotation, symmetry
from orix.vector import Vector3d
from orix.quaternion.symmetry import get_point_group
pgOh = get_point_group(166)
pgO = get_point_group(166, proper=True)
print(pgOh.name, pgO.name)

csvlist = ['/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_ROI_01_rotated_centered_rotZ.csv', 
           '/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_out_centered_rotZ.csv']

#csvlist = ['/home/NFOLASTRE/Pictures/FIgure_Sc3_isosurface/SC3_Positions_XYZ_E123_micron-cropped_rotated_ROI_01_centered_rotZ.csv',
#    '/home/NFOLASTRE/Pictures/FIgure_Sc3_isosurface/SC3_Positions_XYZ_E123_micron_rotated_ROI_00_centered_rotZ.csv']

# Read position XYZ + Euler Angles from EBSD
for csvfile in csvlist:
    df = pd.read_csv(csvfile, sep=',', header='infer',  index_col=None, usecols=None, engine='c', skiprows=None, nrows=None)
    df.columns = ['X', 'Y', 'Z', 'E1', 'E2', 'E3']
    print(df.shape)

    # Reduce data ( keep 1/datapart lines)
    data_part =1
    df = df.iloc[::int(1/data_part)]
    print('data ', round(100*data_part, 2), '%')
    print(df.shape)

    # filter in Z
    filter_Z = -5
    df = df[df['Z'] > filter_Z]
    print('filter_Z >', filter_Z)

    plt.rcParams.update({"figure.figsize": (7, 7), "font.size": 15})
    tempdir = tempfile.mkdtemp() + "/"

    # Directly access *private* cache data path from module
    #_target = data._fetcher.path / "sdss/sdss_ferrite_austenite.ang"

    # Read each column from the file
    ##eu1, eu2, eu3, x, y, iq, dp, phase_id = np.loadtxt(_target, unpack=True)
    # iq = np.array(df.shape[0]).fill(1)
    # print(iq)
    # dp = np.array(df.shape[0]).fill(1)
    # phase_id = np.array(df.shape[0]).fill(0)
    df['iq'] = 1
    df['dp'] = 1
    df['phase_id'] = 0
    eu1, eu2, eu3, x, y, iq, dp, phase_id = df['E1'], df['E2'], df['E3'], df['X'], df['Y'], df['iq'], df['dp'], df['phase_id']
    print(eu1, eu2, eu3, x, y, iq, dp, phase_id)
    print(max)

    # Create a Rotation object from Euler angles
    euler_angles = np.column_stack((eu1, eu2, eu3))
    rotations = Rotation.from_euler(euler_angles, degrees=True)

    # Create a property dictionary
    properties = dict(iq=iq, dp=dp)

    # Create unit cells of the phases
    structures = [
        Structure(
            title="NMC811",
            lattice=Lattice(2.8691, 2.8691, 14.212, 90, 90, 120),
        ),
    ]
    phase_list = PhaseList(
        names=["NMC811"],
        space_groups=[166],
        point_groups=["-3m"],
        structures=structures,
    )

    # Create a CrystalMap instance
    xmap2 = CrystalMap(
        rotations=rotations,
        phase_id=phase_id,
        x=x,
        y=y,
        phase_list=phase_list,
        prop=properties,
    )
    xmap2.scan_unit = "um"

    pg_m3m = pgOh.laue
    # pg_m3m = xmap2.phases[0].point_group.laue

    O_nmc = xmap2["NMC811"].orientations

    # Orientation colors
    ckey_m3m = plot.IPFColorKeyTSL(pg_m3m)
    rgb_nmc = ckey_m3m.orientation2color(O_nmc)

    df['red'], df['green'], df['blue']  =  rgb_nmc[:, 0], rgb_nmc[:, 1], rgb_nmc[:, 2]
    def label_race(row):
        rgb_nmc_hex = "#{:02X}{:02X}{:02X}".format(int(255*row['red']), int(255*row['green']), int(255*row['blue']))
        return rgb_nmc_hex
    df['rgb_nmc_hex'] = df.apply(label_race, axis=1)
    print(df)

    if csvfile == csvlist[0]:
        df2 = df.copy(deep = True)


plot_positions_2 = True
# PLOT positions XYZ ROTATED
if plot_positions_2==True:
    fig2 = plt.figure(figsize=(20, 20))
 
    ax2 = fig2.add_subplot(221, projection='3d')
    ax2.scatter3D(df2['X'], df2['Y'], df2['Z'], facecolors = df2['rgb_nmc_hex'], s = 1)
    ax2.set_xlabel('X-axis', fontweight ='bold') 
    ax2.set_ylabel('Y-axis', fontweight ='bold') 
    ax2.set_zlabel('Z-axis', fontweight ='bold')
    # #SC13 01
    # ax2.set_zlim([-20, 20])
    # #ax2.set_xlim([-100, 100])
    # ax2.set_ylim([-100, 100])

    # #SC13 00
    # ax2.set_zlim([-20, 20])
    # #ax2.set_xlim([-100, 100])
    # ax2.set_ylim([-100, 100])

    # #SC3 01
    # ax2.set_zlim([-20, 20])
    # #ax2.set_xlim([-100, 100])
    # ax2.set_ylim([-100, 100])

    #SC3 01
    ax2.set_zlim([-20, 20])
    #ax2.set_xlim([-100, 100])
    ax2.set_ylim([-100, 100])

    ax3 = fig2.add_subplot(222, projection='3d')
    ax3.scatter3D(df2['X'], df2['Y'], df2['Z'], c=df2['Z'], s=1, vmin = -5, vmax = 5)
    ax3.set_xlabel('X-axis', fontweight ='bold')
    ax3.set_ylabel('Y-axis', fontweight ='bold')
    ax3.set_zlabel('Z-axis', fontweight ='bold')
    ax3.set_zlim([-20, 20])
    #ax3.set_xlim([-100, 100])
    ax3.set_ylim([-100, 100])
    
    ax4 = fig2.add_subplot(223, projection='3d')
    ax4.scatter3D(df['X'], df['Y'], df['Z'], facecolors = df['rgb_nmc_hex'], s = 1)
    ax4.set_xlabel('X-axis', fontweight ='bold') 
    ax4.set_ylabel('Y-axis', fontweight ='bold') 
    ax4.set_zlabel('Z-axis', fontweight ='bold')
    # #SC13 01
    # ax2.set_zlim([-20, 20])
    # #ax2.set_xlim([-100, 100])
    # ax2.set_ylim([-100, 100])

    # #SC13 00
    # ax2.set_zlim([-20, 20])
    # #ax2.set_xlim([-100, 100])
    # ax2.set_ylim([-100, 100])

    # #SC3 01
    # ax2.set_zlim([-20, 20])
    # #ax2.set_xlim([-100, 100])
    # ax2.set_ylim([-100, 100])

    #SC3 01
    ax4.set_zlim([-20, 20])
    #ax2.set_xlim([-100, 100])
    ax4.set_ylim([-100, 100])


    ax5 = fig2.add_subplot(224, projection='3d')
    ax5.scatter3D(df['X'], df['Y'], df['Z'], c=df['Z'], s=1, vmin = -5, vmax = 5)
    ax5.set_xlabel('X-axis', fontweight ='bold')
    ax5.set_ylabel('Y-axis', fontweight ='bold')
    ax5.set_zlabel('Z-axis', fontweight ='bold')
    ax5.set_zlim([-20, 20])
    #ax3.set_xlim([-100, 100])
    ax5.set_ylim([-100, 100])

    #facecolors=rgb

    plt.show()


# # Create figure
# fig = plt.figure(figsize=(8, 8))

# ax0 = fig.add_subplot(221, projection="plot_map")
# ax0.plot_map(xmap2["NMC811"], rgb_nmc)
# ax0.set_title("NMC811 IPF-Z")
# ax0.remove_padding()

# plt.show()

# print(xmap2)
# xmap2.plot(
#     overlay="dp"
# )  # Dot product values added to the alpha (RGBA) channel
