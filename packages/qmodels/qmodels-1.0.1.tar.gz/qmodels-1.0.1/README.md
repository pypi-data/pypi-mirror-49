# Simulation of Queuing Models with Simulus

**Jason Liu, July 2019.**

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/liuxfiu/qmodels.git/master?filepath=notebooks%2Fintro.ipynb)

This is a tutorial describing how to use [simulus](https://simulus.readthedocs.io/en/latest/) to model queuing systems. Simulus is an open-source discrete-event simulator in Python. The tutorial consists of several Jupyter notebooks, on which we develop and run simulation code. The tutorial also comes with a python module containing all example code.

## How to Follow this Tutorial

You have three options:

1. Launch a live notebook server with these notebooks using [Binder](https://beta.mybinder.org/), which provides an executable environment for running Jupyter notebooks. Access the binder at the following URL: https://mybinder.org/v2/gh/liuxfiu/qmodels.git/master?filepath=notebooks%2Fintro.ipynb

2. Run the notebooks on your own machine. The notebooks are available in the github repository (https://github.com/liuxfiu/qmodels.git) under the 'notebooks' directory. To run the notebooks, you need to first have the following packages installed:
   * **jupyter**: a web application for sharing interactive documents that contain text, code, and data visualization
   * **numpy**: a library for efficient representation of multi-dimensional arrays
   * **scipy**: a library for numerical computations, including linear algebra and statistics
   * **matplotlib**: a 2-D plotting library
   * **simulus**: the discrete-event simulator for which we developed this tutorial

   You can install all these packages including the examples of this tutorial using the `pip` command, such as the following:
   ```
   python -m pip install --user qmodels
   ```
   
3.  Read the documents online: http://qmodels.readthedocs.io/. However, you won't be able to run the code within the notebooks with this option.
