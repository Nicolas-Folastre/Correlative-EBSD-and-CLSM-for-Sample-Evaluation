

import tempfile

from diffpy.structure import Atom, Lattice, Structure
import matplotlib.pyplot as plt
import numpy as np

from orix import data, io, plot
from orix.crystal_map import CrystalMap, Phase, PhaseList
from orix.quaternion import Orientation, Rotation, symmetry
from orix.vector import Vector3d


plt.rcParams.update({"figure.figsize": (7, 7), "font.size": 15})
tempdir = tempfile.mkdtemp() + "/"

xmap = data.sdss_ferrite_austenite(allow_download=True)

# Directly access *private* cache data path from module
_target = data._fetcher.path / "sdss/sdss_ferrite_austenite.ang"

# Read each column from the file
eu1, eu2, eu3, x, y, iq, dp, phase_id = np.loadtxt(_target, unpack=True)

# Create a Rotation object from Euler angles
euler_angles = np.column_stack((eu1, eu2, eu3))
rotations = Rotation.from_euler(euler_angles)

# Create a property dictionary
properties = dict(iq=iq, dp=dp)

# Create unit cells of the phases
structures = [
    Structure(
        title="austenite",
        atoms=[Atom("fe", [0] * 3)],
        lattice=Lattice(0.360, 0.360, 0.360, 90, 90, 90),
    ),
    Structure(
        title="ferrite",
        atoms=[Atom("fe", [0] * 3)],
        lattice=Lattice(0.287, 0.287, 0.287, 90, 90, 90),
    ),
]
phase_list = PhaseList(
    names=["austenite", "ferrite"],
    point_groups=["432", "432"],
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

xmap.plot(
    overlay="dp"
)  # Dot product values added to the alpha (RGBA) channel

xmap