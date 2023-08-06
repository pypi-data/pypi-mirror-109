# ctpros <!-- omit in toc -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![coverage](http://gitlab.com/caosuna/ctpros/-/jobs/artifacts/master/raw/.test_results/coverage.svg?job=coverage)](https://gitlab.com/caosuna/ctpros/-/jobs/artifacts/master/file/.test_results/coverage_html/index.html?job=coverage)

A handy graphic user interface (GUI) and application programming interface (API) to apply common imaging techniques to your research images.

<img src="docs/images/guiexample.png">
Two micro-CT images of a single specimen are shown post-registration of their overlapping region before being stitched.

## Summary <!-- omit in toc -->
This program's goal is to ease the utilization of Python's powerful imaging library in medical imaging research. By combining raw image data with paired affine matrices to describe their real-world orientations, relationships and properly scaled metrics can be applied between images of varying resolutions, easing common image processing pipelines. Enabling manipulation of these affine transformations with intuitive dragging and rotating operations allows researchers to better visualize and explore their data.
## Index <!-- omit in toc -->
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Requirements
All:
- [Python 3.7 64-bit](https://www.python.org/downloads/release/python-379/)
  - Development occurred in 3.7. Use later versions at your own discretion.
  
Windows:
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) for C++ compilation
  
Headless:
- `xvfb`
  - X virtual frame buffer to mimic a screen
- OpenGL
  ```
  apt-get install -y libgl1-mesa-dev  xvfb
  ```
## Installation
Install `ctpros` using `pip` in your preferred Python environment:
```bash
"path\to\venv\Scripts\activate"
pip install ctpros
```
See the [Windows guide](docs/install_win_helpme.md) for a comprehensive look at the requirements and project installation.
##  Usage
Use either the user-friendly graphic user interface or the more advanced application programming interface for experienced programmers.

### Graphic User Interface <!-- omit in toc -->
Upon installation on Windows, `ctpros.bat` is generated on the user's desktop. Select that file to run `ctpros`.

Alternatively, call `ctpros` as a module from the Python (virtual) environment which it is installed in:
```bash
"path\to\venv\Scripts\activate"
python -m ctpros
```
This will open the GUI associated to the program. See the [GUI Controls](docs/gui_helpme.md) for more details.

### Application Programming Interface <!-- omit in toc -->
Import `ctpros` like any other Python module to access the GUI and NumPy-derived image classes.
```python
import ctpros

myaim = ctpros.AIM(shape=(50,50,50),dtype='int16')
```
See the [notebooks](notebooks/README.MD) for examples of API usage.

## Contributors
See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
[GPL 3.0](docs/gnu_gpl_3-0.txt)