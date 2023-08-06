This directory is a Python package containing code to create a simple ludo simulator to settle a bet between Pip and Anna.

The root folder contains `TermsOfBet.md`, a file outlining the terms of the bet, `StandardLudoBoard.png`, an image of the standard ludo board used and the positions favored by Anna and Pip for the bet, `__init__.py`, for marking this repository as a package and initializing the package when importing, `ludoSim_env.yml`, a file for setting a virtual environment in Anaconda in which to use this package, `ClassOrganization.txt`, a file with early-stage notes on source code organization, and the source code (`Board.py`, `Player.py`, `Piece.py`) that executes when running the ludo simulator. 

The `analysis` folder contains a script (`gameAnalysis.py`) that when run, runs a set number of ludo games and displays results to determine the outcome of the bet. The `analysis` folder also contains images (`playerStats.png`, `binomialPMF.png`) and data (`gamesResults.out.dat`, `gamesResults.out.dir`, `gamesResults.out.bak`) from previously running 10000 game simulations. The data from the `gamesResults` files can be loaded by following the instructions at the bottom of the `gameAnalysis.py` file.

To run a game of ludo, navigate to the local folder where you have cloned or installed this repository (unnecessary if you have installed via `pip install ludoSim-jaib1` or `conda install ludoSim-jaib1 -c conda-forge`), launch python, and run:
```
from ludoSim import *
b = Board() # look at the optional input args to set the board however you'd like
b.playGame()
```

*Note, this package was created using the Anaconda (5.3) package manager distribution (running Python 3.7), and imports some packages native to Anaconda. For best results, download and install [Anaconda](https://www.anaconda.com/distribution), navigate to the local folder where you have cloned or installed this ludoSim repository (unnecessary if you have installed via `conda install ludoSim-jaib1 -c conda-forge`), and in your conda terminal run:*

*`conda activate ludoSim_env`*

*to activate the environment with the appropriate package dependencies which were used at the time this package was created*