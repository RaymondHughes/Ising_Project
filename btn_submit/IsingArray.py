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

		# Track System Quantities
		self.E_v = [self.get_energy()]
		self.M_v = [self.get_mag()]

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
		horiz = self.spins * np.roll(self.spins, 1, axis = 0)
		vert  = self.spins * np.roll(self.spins, 1, axis = 1)

		return np.mean((-self.J) * (horiz+vert))

	def get_mag(self):
		"""
		Returns the magnetization density of the array [M/A]
		"""
		return abs(np.mean(self.spins))

	def get_acceptance_rate(self):
		return (self.accepted)/(self.accepted + self.rejected)

	

	def sweep(self, iternum = 1):
		"""
		sweeps the array for one round of thermal fluctuations
		"""
		steps = int(self.shape[0]*self.shape[1])
		for i_sweep in range(int(iternum)):
			for i in range(steps):
				p_inds = (np.random.randint(low = 0, high = self.shape[0]), np.random.randint(low = 0, high = self.shape[1]))
				dE = self.delta_energy(p_inds)
				if self._acceptance(dE):
					self.spins[p_inds[0], p_inds[1]] *= -1
					self.accepted += 1
				else:
					self.rejected += 1

			#Track State Variables
			self.E_v.append(self.get_energy())
			self.M_v.append(self.get_mag())

		return None

	def animate(self, f = None, inter = 50, rep = True, show = True, frames = 100):
		"""
		produces an animation of the array's thermal fluctuations

		would be cool to add an option animate state_vars as well
		"""

		if f == None:
			f, ax = plt.subplots(figsize = (10, 6))
		else:
			ax = plt.axes(f)

		self.im = ax.imshow(self.spins, aspect = 'auto')
		ani = animation.FuncAnimation(f, self._update, interval=inter, blit=True, repeat = rep, frames = frames)

		
		if show:
			plt.show()

		return ani

	def _update(self, frame):
		"""
		internal function for updating each frame of the animation
		"""
		self.sweep()
		self.im.set_data(self.spins)		
		return self.im,

	def _acceptance(self, dE):
		p = np.random.random()
		v = np.exp( -dE / (self.kbT))
		return p < v




if __name__ == '__main__':
	shape = (100, 100)
	T = 1
	J = 1
	kb = 1
	Array1 = IsingArray(shape, T, J, kb)
	Array1.animate()

	T = 4
	Array2 = IsingArray(shape, T, J, kb )
	Array2.animate()
	