#!/usr/bin/env python

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

kb = 1.380649e-23

class IsingArray:
    """docstring for ClassName"""
    def __init__(self, size, T=300, J = 1):
        f, ax = plt.subplots()
        self.ax 

        spin_choice = np.array([-1, 1])
        self.spins = np.random.choice(spin_choice, size)

        self.kbT = T*kb
        self.J = J

    def __repr__(self):
        return self.spins
