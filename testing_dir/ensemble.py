#!/usr/bin/env python

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from two_d_model import *

debug = False
steps = 1000100

# Stuff I will need
kb = 1
J = 1
L = 20

def total_energy(ensemble):
	""" 
	This is slow because it sums of the entire ensemble
	For looping it would be better if I had a delta_energy function
	"""
	spins_horiz = ensemble[:, :, :-1] * ensemble[:, :, 1:]
	spins_vert  = ensemble[:, :-1, :] * ensemble[:, 1:, :]
	return (np.sum(spins_vert, axis = (1,2)) + np.sum(spins_horiz, axis = (1,2))) * (-J)

def delta_energy(ensemble, p_inds):
	s = ensemble[:, p_inds[0], p_inds[1]]     #spin to be flipped

	#find the neighboring spins (left, right, up, down)
	l = ensemble[:, (p_inds[0] + 1)%L, p_inds[1]] 
	r = ensemble[:, (p_inds[0] - 1)%L, p_inds[1]]
	u = ensemble[:, p_inds[0], (p_inds[1] + 1)%L]
	d = ensemble[:, p_inds[0], (p_inds[1] - 1)%L]

	return 2*(J)*s*(l+r+u+d)


def total_mag(ensemble):
	return np.sum(ensemble, axis = (1, 2))

def flip_ensemble(a_v, p_inds, ensemble):
    """
		Flips some of the spins in the ensemble according to the acceptance vector and indicies:
			-a_v is  the T/F acceptance vector, length of ensemble dim0
			-p_inds is a tuple of the location of the spins to be flipped
			-ensemble is the ensemble array to change
    """
    ensemble[a_v, p_inds[0], p_inds[1]] = -ensemble[a_v, p_inds[0], p_inds[1]]
    return None

# Define Ensemble
n = 100
shape = (n, L, L)
spin_choice = np.array([-1, 1])
ensemble = np.random.choice(spin_choice, shape)
T = np.linspace(0.5, 5, n)
if debug:
	print(f"Sizes :")
	print(f"\t ensemble | {np.shape(ensemble)}")
	print(f"\t T        | {len(T)}")

E_vals = np.zeros((100, n))
M_vals = np.zeros((100, n))
for i in range(steps):
	# if i % 100 == 0:
	# 	debug = True
	# 	print('')
	# 	print("iternum", i)
	# else:
	# 	debug = False
	# Generate indicy of lattice to check
	p_ind0 = np.random.randint(low = 0, high = shape[1])
	p_ind1 = np.random.randint(low = 0, high = shape[1])
	p_inds = (p_ind0, p_ind1)
	# p_ensemble = flip_spins(p_inds, ensemble)

	# if debug:
	# 	print(f"\tp_ensemble| {np.shape(p_ensemble)}")
	# 	print(f"p_inds = {p_inds}")

	# Generate Acceptance Variables
	dE_v= delta_energy(ensemble, p_inds)
	# print(dE_v)
	p_v = np.random.random(n)
	v_v = np.exp(-dE_v/(kb*T))
	a_v = p_v < v_v

	ensemble[a_v, p_inds[0], p_inds[1]] = -ensemble[a_v, p_inds[0], p_inds[1]]
	idx = 100 - (steps-i)
	if idx > 0:
		E_vals[idx, :] = (total_energy(ensemble))
		M_vals[idx, :] = (abs(total_mag(ensemble)))
	# if debug:
		
	# 	print("change in energy: ",(dE_v/(kb*T))[::200])
	# 	print("v:", v_v[::200])
	# 	print("p:", p_v[::200])
	# 	print("a:", a_v[::200])



f, (ax_E, ax_M) = plt.subplots(1, 2, figsize = (10, 6))

ax_E.scatter(T, np.mean(E_vals, axis = 0))
ax_E.set_xlabel("Temperature (K)")
ax_E.set_ylabel("Energy (Units?)")
ax_E.set_title("Energy vs Temperature")

ax_M.scatter(T, (np.mean(M_vals, axis = 0)))
ax_M.set_xlabel("Temperature (K)")
ax_M.set_ylabel("Magnetization (Units?)")
ax_M.set_title("Magnetization vs Temperature")

plt.show()
np.savetxt("ensemble.txt", ensemble)