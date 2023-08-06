
import os
import trimesh

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from .vertice import *
from .edge import *
from .edge_loop import *
from .face import *
from .building import *
from .material import *

# mesh = trimesh.load('../models/featuretype.STL')


def import_stl(file=None):
    mesh = trimesh.load(file)
    pass


if __name__ == '__main__':

    # file picker for debugging surposes
    Tk().withdraw()
    file = askopenfilename()

    MyBuilding = import_stl(file)

    print('done')