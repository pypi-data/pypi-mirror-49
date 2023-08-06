This repository contains code to create a simple ludo simulator in Python to settle a bet between Pip and Anna.

The root folder contains this `README.md`, a `LICENSE`, and `setup.py`, for configuring this repository as a distributable package (on PyPI and Anaconda's conda-forge channel). The `tests` folder contains unit and integration tests for confirming the source code is functioning as expected. (These tests are to be run in the pytest package testing framework: to run these tests, follow the instructions in the `runTest.py` file.) The `ludoSim` folder contains the source code package and a README detailing its contents. The `build` folder contains the latest build of the `ludoSim` source code package, and the `dist` folder contains distributions of this build in different compressed file formats.

Running the `ludoSim/analysis/gameAnalysis.py` script runs 10000 games and displays results to determine the outcome of the [bet](https://github.com/jaib1/ludoSim/blob/master/ludoSim/TermsOfBet.md). Running this script took less than a minute on a Windows10 PC with an Intel core i5-6500 CPU with 16 GB DDR4-2133 RAM. 

To run a game of ludo, navigate to the local folder where you have cloned or installed this repository (unnecessary if you have installed via `pip install ludoSim-jaib1` or `conda install ludoSim-jaib1 -c conda-forge`), launch python, and run:
```
from ludoSim import *
b = Board() # look at the optional input args to set the board however you'd like
b.playGame()
```

*Note, this package was created using the Anaconda (5.3) package manager distribution (running Python 3.7), and imports some packages native to Anaconda. For best results, download and install [Anaconda](https://www.anaconda.com/distribution), navigate to the local folder where you have cloned or installed this ludoSim repository (unnecessary if you have installed via `conda install ludoSim-jaib1 -c conda-forge`), and in your conda terminal run:*

*`conda activate ludoSim_env`*

*to activate the environment with the appropriate package dependencies which were used at the time this package was created*

