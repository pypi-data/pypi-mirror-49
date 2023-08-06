# Simulation of Queuing Models with Simulus

**Jason Liu, July 2019.**

<img src="notebooks/figs/queue.jpg" width="35%" alt="queue">

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/liuxfiu/qmodels.git/master?filepath=notebooks%2Findex.ipynb)

This repository contains a tutorial describing how to use [simulus](https://simulus.readthedocs.io/en/latest/) to model queuing systems. Simulus is an open-source discrete-event simulator in Python. The tutorial consists of several Jupyter notebooks, on which we develop and run simulation code.

## How to Read this Tutorial

You have three options:

1. Launch a live notebook server with these notebooks using [Binder](https://beta.mybinder.org/), which provides an executable environment for running Jupyter notebooks. Access the binder at the following URL: https://mybinder.org/v2/gh/liuxfiu/qmodels.git/master?filepath=notebooks%2Findex.ipynb

2. Run these notebooks on your own machine. The notebooks are available in this repository's 'notebooks' directory. To run the notebooks, you need to first have the following packages installed:
   * **jupyter**: a web application for sharing interactive documents that contain text, code, and data visualization
   * **numpy**: a library for efficient representation of multi-dimensional arrays
   * **scipy**: a library for numerical computations, including linear algebra and statistics
   * **matplotlib**: a 2-D plotting library

   You can install these packages using the `pip` command, such as the following:

   ```
   python -m pip install --user jupyter numpy scipy matplotlib
   ```

   You'll also need to install simulus. Check out [simulus quick start](https://simulus.readthedocs.io/en/latest/readme.html) for installation instructions. The simplest way to install simulus is to run the `pip` command, such as:

   ```
   python -m pip install --user simulus
   ```
   
3.  Read the online documentation: http://qmodels.readthedocs.io/. However, you won't be able to run the code within the notebooks with this option.
