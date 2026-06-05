#!/usr/bin/env python

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

kb = 1.380649e-23
def total_energy(spins, J):
    spins_horiz = spins[:, :-1]*spins[:, 1:]
    spins_vert = spins[:-1, :]*spins[1:, :]
    return (np.sum(spins_vert) + np.sum(spins_horiz)) * (-J)

def flip_spins(p_inds, spins):
    p_spins = spins.copy()
    p_spins[p_inds] *= -1
    return p_spins

class IsingArray:
    def __init__(self, shape, T=300, J = (300*kb)):
        

        spin_choice = np.array([-1, 1])
        self.shape = shape
        self.spins = np.random.choice(spin_choice, shape)
        self.spins0 = self.spins.copy() 
        self.kbT = T*kb
        self.J = J

        self.E = total_energy(self.spins, J)
        self.M = self.get_mag()
        self.M_v = []
        self.E_v = []

        self.rejected = 0
        self.accepted = 0


    

    def __repr__(self):
        print(self.spins)
        return "Spin Array with total energy %g J"%self.E

    def acceptance(self, p_inds, verbose = False):
        #proposed_change will be to an index of a spins to be flipped
        p_spins = flip_spins(p_inds, self.spins)
        E = total_energy(self.spins, self.J)
        PE = total_energy(p_spins, self.J)
        # Do something with E vs. PE
        dE = PE - E
        

        v = min(1, np.exp(-dE/self.kbT))
        p = np.random.rand() 
        if verbose:
            print("E = ", E, ", PE = ", PE, ", dE = ", dE)
            print("p = ", p, ", v = ", v)
        if p < v:
            if verbose:
                print("flip accepted")
            return True
        else:
            if verbose:
                print("flip rejected")
            return False

    def get_mag(self):
        return np.sum(self.spins)

    def update(self, frame):
        if frame == 0:
            self.spins = self.spins0.copy()

        if len(self.E_v) <=frame:
            self.E_v.append(self.E)
            self.M_v.append(self.M)

        cont = True
        while cont:
            p_ind0 = np.random.randint(low = 0, high = self.shape[0])
            p_ind1 = np.random.randint(low = 0, high = self.shape[1])
            p_inds = (p_ind0, p_ind1)

            accept = self.acceptance(p_inds)
            if accept:
                self.spins = flip_spins(p_inds, self.spins)
                self.E     = total_energy(self.spins, self.J)
                self.M     = self.get_mag()
                cont = False


        self.im.set_data(self.spins)
        return self.im,

    def animate(self, steps = 1e4, f=None, ax=None):
        if (f == None):
            if ax != None:
                print('must specify Figure in order to specify axis')

            f, ax = plt.subplots()
            self.f = f
            self.ax = ax
        elif ax == None:
            self.ax = plt.axes(f)
        self.im = ax.imshow(self.spins, aspect = 'auto')
        
        self.steps = 1e4
        ani = animation.FuncAnimation(self.f, self.update, interval=20, frames = int(self.steps), blit=True, repeat = True)
        plt.show()

    def get_data(self, steps = 1e4):
        iternum = len(self.E_v)
        print("initial data is %i long"%iternum)
        while iternum < steps:
            if iternum % 1000==0:
                print("iteration ", iternum)
            cont = True
            while cont:
                p_ind0 = np.random.randint(low = 0, high = self.shape[0])
                p_ind1 = np.random.randint(low = 0, high = self.shape[1])
                p_inds = (p_ind0, p_ind1)

                accept = self.acceptance(p_inds)
                if accept:
                    self.accepted += 1
                    self.spins = flip_spins(p_inds, self.spins)
                    self.E     = total_energy(self.spins, self.J)
                    self.M     = self.get_mag()
                    cont = False
                else:
                    self.rejected += 1
            iternum += 1

            self.E_v.append(self.E)
            self.M_v.append(self.M)

    def plot_data(self):
        f, (ax_E, ax_M) = plt.subplots(1, 2)
        
        ax_E.plot(np.arange(len(self.E_v)), np.array(self.E_v) )
        ax_M.plot(np.arange(len(self.E_v)), np.array(self.M_v) )

        ax_E.set_title("Energy Fluctuation")
        ax_E.set_xlabel("Iteration Number")
        ax_E.set_ylabel("Energy (J)")

        ax_M.set_title("Magnetization Fluctuation")
        ax_M.set_xlabel("Iteration Number")
        ax_M.set_ylabel("Energy (J)")

        plt.show()

    def debug_acceptance(self):
        print(self.J/self.kbT)
        while True:
            p_ind0 = np.random.randint(low = 0, high = self.shape[0])
            p_ind1 = np.random.randint(low = 0, high = self.shape[1])
            p_inds = (p_ind0, p_ind1)
            print("proposed inds: ", p_inds)

            accept = self.acceptance(p_inds, verbose = True)
            if accept:
                self.spins = flip_spins(p_inds, self.spins)
                self.E     = total_energy(self.spins, self.J)
                self.M     = self.get_mag()

            input("Press Enter to Continue and Ctrl+C to quit")
                




if __name__ == '__main__':
    MyArray = IsingArray((10,10), T = 2000)
    # MyArray.debug_acceptance()
    print(MyArray)
    MyArray.animate()
    MyArray.get_data()
    MyArray.plot_data()

    print("accepted:", MyArray.accepted)
    print("rejected:", MyArray.rejected)




        
    
