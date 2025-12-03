# importing libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import math
from scipy.spatial.transform import Rotation as R
from math import sin, cos, acos, sqrt, fabs, atan
from scipy.optimize import minimize
from scipy import ndimage
from pathlib import Path
import tempfile
from diffpy.structure import Atom, Lattice, Structure
from orix import plot, sampling
from orix.crystal_map import Phase
from orix.vector import Vector3d
from orix import data, io, plot
from orix.crystal_map import CrystalMap, Phase, PhaseList
from orix.quaternion import Orientation, Rotation, symmetry
from orix.quaternion.symmetry import get_point_group

# Define point group to compute symmetries
pgOh = get_point_group(166)
pgO = get_point_group(166, proper=True)
print(pgOh.name, pgO.name)

# csvlist = ['/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_ROI_01_rotated_centered_rotZ.csv', 
#           '/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_out_centered_rotZ.csv']

csvlist = ['/home/NFOLASTRE/Pictures/FIgure_Sc3_isosurface/SC3_Positions_XYZ_E123_micron-cropped_rotated_ROI_01_centered_rotZ.csv',
    '/home/NFOLASTRE/Pictures/FIgure_Sc3_isosurface/SC3_Positions_XYZ_E123_micron_rotated_ROI_00_centered_rotZ.csv']

# Read position XYZ + Euler Angles from EBSD
Mlines = 0
for csvfile in csvlist:
    df = pd.read_csv(csvfile, sep=',', header='infer',  index_col=None, usecols=None, engine='c', skiprows=None, nrows=None)
    df.columns = ['X', 'Y', 'Z', 'E1', 'E2', 'E3']
    print(df.shape)

    # Reduce data ( keep 1/datapart lines)
    data_part = 1
    # if csvfile == csvlist[1]:
    #     data_part = data_part*(Mlines / df.shape[0])
    df = df.iloc[::int(1/data_part)]
    print('data ', round(100*data_part, 2), '%')
    print(df.shape)

    # filter in Z
    filter_Z = -10000
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
    # print(eu1, eu2, eu3, x, y, iq, dp, phase_id)
    # print(max)

    # Create a Rotation object from Euler angles
    euler_angles = np.column_stack((eu1, eu2, eu3))
    rotations = Rotation.from_euler(euler_angles, degrees=True)
    O1 = Orientation.from_euler(euler_angles, degrees=True)
    # Create a property dictionary
    properties = dict(iq=iq, dp=dp)

    # Create unit cells of the phases ( 1 phase for now)
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
    O_nmc = xmap2["NMC811"].orientations

    # Orientation colors
    ckey_m3m = plot.IPFColorKeyTSL(pg_m3m)
    rgb_nmc = ckey_m3m.orientation2color(O_nmc)

    if csvfile == csvlist[0]:
        df2 = df.copy(deep = True)
        O2 = O1
        Mlines = df2.shape[0]

# We'll want our plots to look a bit larger than the default size
new_params = {
    "figure.facecolor": "w",
    "figure.figsize": (20, 7),
    "lines.markersize": 10,
    "font.size": 15,
    "axes.grid": True,
}

# Create plot for Inverse Pole figure Density (IPFd)
plt.rcParams.update(new_params)
plot.IPFColorKeyTSL(symmetry.D3d).plot()

pg_laue = [
    symmetry.S6,
    symmetry.D3d,
]

S = pg_laue[1]

O_fe=O1
O_au=O2

# Some sample direction, v
v = Vector3d([0, 0, 1])
v_title = "Z"

# Rotate sample direction v into every crystal orientation O
t_fe = O_fe * v
t_au = O_au * v

# Set IPDF range
vmin, vmax = (0, 3.0)

subplot_kw = {"projection": "ipf", "symmetry": pg_m3m, "direction": v}
fig = plt.figure(figsize=(9, 8))

ax0 = fig.add_subplot(221, **subplot_kw)
ax0.scatter(O_fe, alpha=0.01, s=1)
_ = ax0.set_title(f"Full, {v_title}")

ax1 = fig.add_subplot(222, **subplot_kw)
ax1.scatter(O_au, alpha=0.01, s=1)
_ = ax1.set_title(f"ROI, {v_title}")

ax2 = fig.add_subplot(223, **subplot_kw)
ax2.pole_density_function(t_fe, vmin=vmin, vmax=vmax)
_ = ax2.set_title(f"Full, {v_title}")

ax3 = fig.add_subplot(224, **subplot_kw)
ax3.pole_density_function(t_au, vmin=vmin, vmax=vmax)
_ = ax3.set_title(f"ROI, {v_title}")

for O in O1, O2:
    print(O)
    
    ipfkey = plot.IPFColorKeyTSL(S)
    O.symmetry = ipfkey.symmetry
    rgb_z = ipfkey.orientation2color(O)
    # O.scatter("ipf", c=rgb_z, direction=ipfkey.direction,s = 10, alpha = 0.05)

    alpha = 0.01
    # if O == O2:
    #     alpha = Mlines/df.shape[0]
    O.scatter("ipf", c=rgb_z, direction=ipfkey.direction,s = 1, alpha = alpha)

plt.show()

