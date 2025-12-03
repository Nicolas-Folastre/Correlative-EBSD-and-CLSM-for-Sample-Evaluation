import matplotlib.pyplot as plt
import numpy as np

from orix import plot, sampling
from orix.crystal_map import Phase
from orix.quaternion import Orientation, symmetry
from orix.vector import Vector3d

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

#csvlist = ['/home/NFOLASTRE/Pictures/Figure_Sc13_Isosurface/SC13_Positions_XYZ_E123_micron_ROI_01_rotated_centered_rotZ.csv', 
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
    # print(df)

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
plt.rcParams.update(new_params)
plot.IPFColorKeyTSL(symmetry.D3d).plot()

pg_laue = [
    symmetry.S6,
    symmetry.D3d,
]

S = pg_laue[1]
# ipfkey = plot.IPFColorKeyTSL(S)
# ipfkey.plot()

# v = Vector3d([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
# kwargs = {"projection": "ipf", "direction": v}
# O = Orientation.from_euler([325, 48, 163], S, degrees=True)
# O.scatter(**kwargs)
# plt.rcParams["axes.grid"] = False

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


