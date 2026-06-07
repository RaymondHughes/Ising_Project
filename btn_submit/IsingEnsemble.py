#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

spin_choice = np.array([-1, 1])

class IsingEnsemble:
	def __init__(self, n = 100, shape = (20, 20), T = np.linspace(0.5, 5, 100), J = 1, kb = 1):
		if len(T) != n:
			raise ValueError("T must be an array of length n")
		if (len(shape) != 2) or (type(shape) != type((1,1))):
			raise TypeError("shape must be tuple of length 2")
			
		self.kbT = kb*T
		self.J = J
		self.n = n
		self.shape = shape

		self.ensemble = np.random.choice(spin_choice, (n, shape[0], shape[1]))

	def _delta_energy(self, p_inds):
		"""
		Returns the change in energy as an array of length n if the spin at p_ind were to be flipped
		"""

		s = self.ensemble[:, p_inds[0], p_inds[1]]     #spin to be flipped

		#find the neighboring spins (left, right, up, down)
		l = self.ensemble[:, (p_inds[0] + 1)%self.shape[0], p_inds[1]] 
		r = self.ensemble[:, (p_inds[0] - 1)%self.shape[0], p_inds[1]]
		u = self.ensemble[:, p_inds[0], (p_inds[1] + 1)%self.shape[1]]
		d = self.ensemble[:, p_inds[0], (p_inds[1] - 1)%self.shape[1]]
		return 2*(self.J)*s*(l+r+u+d)


	def _acceptance(self, dE):
		p = np.random.random(self.n)
		v = np.exp(-dE/(self.kbT))
		return p<v

	def get_energy(self):
		"""
		Returns the energy density of the ensemble [E/A] as an array of len n
		"""
		horiz = self.ensemble * np.roll(self.ensemble, 1, axis = 1)
		vert  = self.ensemble * np.roll(self.ensemble, 1, axis = 2)

		return np.mean((-self.J) * (horiz+vert), axis = (1,2))

	def get_mag(self):
		"""
		Returns the magnetization density of the array [M/A] as an array of len n
		"""
		return abs(np.mean(self.ensemble, axis = (1,2)))

	def sweep(self, num = 1):
		"""
		sweeps the ensemble for one round of thermal fluctuations
		"""
		steps = int(self.shape[0]*self.shape[1])
		for i in range(num):
			for i in range(steps):
				p_inds = (np.random.randint(low = 0, high = self.shape[0]), np.random.randint(low = 0, high = self.shape[1]))
				dE = self._delta_energy(p_inds)
				a = self._acceptance(dE)
				self.ensemble[a, p_inds[0], p_inds[1]] *= -1
			
		return None

		
