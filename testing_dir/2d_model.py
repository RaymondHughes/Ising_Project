#!/usr/bin/env python

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
animate = True
J = 1
kbT = 1
## -1 = down, 1 = up
spins_0= np.array([-1,-1,1,1,1,1,-1,1,-1])
steps = 1e2
spins = spins_0.copy()
if animate:
    spins_v = [spins_0]
def total_energy(spins):
	#Somehow totals energy
    spins_prod = spins[:-1]*spins[1:]
    return np.sum(spins_prod)*(-J)



def acceptance(p_inds, spins, ax):
    #proposed_change will be a set of indices of the spins to be flipped
    p_spins = flip_spins(p_inds, spins)
    E = total_energy(spins)
    PE = total_energy(p_spins)
    # Do something with E vs. PE
    dE = PE - E
    v = min(1, np.exp(-dE/kbT))
    p = np.random.rand() 
    if p < v:
        print("flip accepted")
        return True
    else:
        print("flip rejected")
        return False

def flip_spins(p_inds, spins):

    p_spins = spins.copy()
    p_spins[p_inds] *= -1
    return p_spins


    
f, ax = plt.subplots()
print(spins)
def update(frame):
    spins = spins_v[frame-1]
    p_ind = np.random.randint(low = 0, high = len(spins)) 

    a = acceptance(p_ind, spins, ax)
    if a:
        spins = flip_spins(p_ind, spins)
        #if animate:
    spins_v.append(spins)
    #spins = spins_v[frame]
    pl = ax.scatter(np.arange(len(spins)), spins)
    
    return pl, 

ani = animation.FuncAnimation(f, update, interval=1000, blit=True, repeat = False)
plt.show()
