# Ising Model
Raymond Hughes - Phys 129L(S26) Final Project

## Contents:
1. IsingExample.ipynb
2. IsingArray.py
3. IsingEnsemble.py

## IsingExample.ipynb
This jupyter notebook contains examples of all functions conatined within both classes as well as highlighting best usage practices.

## IsingArray Library
### Overview:
This file contains the "IsingArray" classes used to observe/animate runs of Ising Models. It assumes periodic boundary conditions on a rectangular array, and by default uses "normalized" physical constants (kb = J = 1)

### IsingArray Class Functions:
The Ising Array Class has several options for the user to analyze single runs of a Ising Model array of magnetic spins.

#### To initialize a IsingArray:

	MyArray = IsingArray(shape, T=2.2, J = 1., kb = 1.))

- shape (tuple, length 2) specifying the width and height of the array
- T (float) is the temperature, needs to be a float, by default set to 2.2 which is around the critical temp for kb=J=1
- J (float) is the interaction strength between the spins, differs by materials but for computation simplicity assumed to be 1
- kb (float) is the boltzmann constant, for computation simplicity assumed to be 1

#### Thermal fluctuations can be performed with sweep function. Each round of thermal fluctionation is performed in a batch (a "sweep") to avoid biasing the array :
	MyArray.sweep(num = 1)

- num (int) is the number of sweeps to perform

#### To get energy density (average energy per spin):
	E = MyArray.get_energy()

#### To get magnetization density (average value of spins):
	M = MyArray.get_mag()

#### To create an animation of a run of one of the magnetization array -- note this requires ipympl to work on a jupyter notebook and even then it runs forever, ignoring the frames/repeat options, it works normally on when run in an ordinary script, so I'm not sure exactly why that is:
	ani = MyArray.animate(f = None, inter = 50, loop = True, show = True, frames = 100)
- f (matplotlib figure object) is the figure to draw the animations on, by default creates a new figure to do so (specified by None)
- inter (int) is the interval between frames, measured in milliseconds
- loop (T/F boolean) determines whether the animation will be looping
- show (T/F boolean) decides whether or not to call plt.show(), set to false when you want to return the animation object but not immediately view it
- frames (int) decides how long the animation should be 


### Dependencies:
- Numpy
- Matplotlib



## IsingEnsemble Library
### Overview:
This file contains the "IsingEnsemble" class used to observe many differnet runs of Ising Models, not necessarily all at the same temperatures. It assumes periodic boundary conditions on a rectangular array, and by default uses "normalized" physical constants (kb = J = 1)

### IsingEnsemble Class Functions:
The Ising Ensemble Class has several options for the user to analyze many runs of Ising Models.

#### To initialize an IsingEnsemble:

	MyEnsemble = IsingEnsemble(n = 100, shape = (20, 20), T = np.linspace(0.5, 5, 100), J = 1, kb = 1))

- n (int) is the number of arrays in the ensemble
- shape (tuple, length 2) specifying the width and height of the arrays
- T (numpy array) is a numpy aray containing the temperatures of each array in the ensemble, must be 1-d and length n, note that if J=kb=1, then critical temperature Tc~2.2
- J (float) is the interaction strength between the spins, differs by materials but for computation simplicity assumed to be 1
- kb (float) is the boltzmann constant, for computation simplicity assumed to be 1

#### Thermal fluctuations can be performed with sweep function. Each round of thermal fluctionation is performed in a batch (a "sweep") to avoid biasing the array :
	MyEnsemble.sweep(num = 1)

- num (int) is the number of sweeps to perform

#### To get energy density (average energy per spin):
	E = MyEnsemble.get_energy()

- E is numpy array of Energy Densities for each ising array in the ensemble

#### To get magnetization density (average value of spins):
	M = MyEnsemble.get_mag()

- M is numpy array of Magnetization Densities for each Ising array in the ensemble
 


### Dependencies:
- Numpy
- Matplotlib
