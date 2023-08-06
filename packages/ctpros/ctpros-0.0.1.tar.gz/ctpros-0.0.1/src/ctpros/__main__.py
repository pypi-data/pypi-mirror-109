import lazy_import

for module in [
    "mayavi",
    "pandas",
    "scipy.linalg",
    "scipy.ndimage",
    "scipy.optimize",
    "scipy.stats",
    "scipy.signal",
    "skimage.measure",
    "skimage.morphology",
    "scipy",
    "skimage",
    "vtk",
]:
    lazy_import.lazy_module(module)

from ctpros.graphics import GUI
import sys

if __name__ == "__main__":  # pragma: no cover
    gui = GUI(*sys.argv[1:])
    gui.mainloop()
