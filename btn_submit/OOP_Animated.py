#!/usr/bin/env python

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

spin_choice = np.array([-1, 1])

class IsingArray:
    def __init__(self, shape, T=2.2, J = 1, kb = 1):
        # Physical parameters
        self.kbT = T*kb
        self.J = J
        self.shape = shape

        # Set up array 
        self.spins = np.random.choice(spin_choice, shape)
        self.spins0 = self.spins.copy() 

        # Monte Carlo Measurements
        self.rejected = 0
        self.accepted = 0

    def __repr__(self):
    	description = f"Ising Array of size {shape} with average energy density {self.get_energy} and magnetization {self.get_mag}"
    	return description

	def delta_energy(self, p_inds):
		"""
		Returns the change in energy if the spin at p_ind were flipped
		"""

		# Spin to be flipped
		s = self.spins[p_inds[0], p_inds[1]]     
		# Find the neighboring spins (left, right, up, down)
		l = self.spins[(p_inds[0] + 1)%self.shape[0], p_inds[1]] 
		r = self.spins[(p_inds[0] - 1)%self.shape[0], p_inds[1]]
		u = self.spins[p_inds[0], (p_inds[1] + 1)%self.shape[1]]
		d = self.spins[p_inds[0], (p_inds[1] - 1)%self.shape[1]]
		# Change in Energy is given by dE_i = 2*J*s_i*sum(s_j)
		return 2*(self.J)*s*(l+r+u+d)

	def get_energy(self):
		"""
		Returns the energy density of the array [E/A]
		"""

	def get_mag(self):
		"""
		Returns the magnetization density of the array [M/A]
		"""
		return np.mean(self.spins)

	def animate(self):
		"""
		produces an animation of the array's thermal fluctuations
		"""

	def sweep(self):
		"""
		sweeps the array for one round of thermal fluctuations
		"""

	def _upate(self, frame):
		"""
		internal function for updating each frame of the animation
		"""
		self.sweep()
		# Update Graph
		return #Image Object,



