"""
================
The Bayes update
================

This animation displays the posterior estimate updates as it is refitted when
new data arrives.
The vertical line represents the theoretical value to which the plotted
distribution should converge.
"""

import math

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as spstat
from matplotlib.animation import FuncAnimation


def beta_pdf(x, a, b):
    return (x**(a-1) * (1-x)**(b-1) * math.gamma(a + b)
            / (math.gamma(a) * math.gamma(b)))


def normal_pdf(x, mu, sd):    
    return spstat.norm.pdf(x,mu,sd)



class UpdateDist:
    def __init__(self, ax, mu1, sd1,n1, mu2,sd2,n2):
        self.p1 = [mu1,sd1,n1]
        self.p2 = [mu2,sd2,n2]
        #  l12 is two plots [x],[y1],[x],[y2]
        self.l1, = ax.plot([], [], 'b-')
        self.l2, = ax.plot([], [], 'r-')
        self.lines = [self.l1, self.l2]
        self.ax = ax

        self.npts = 200
        self.xm = 150
        self.x = np.linspace(0, self.xm, self.npts)
        # Set up plot parameters
        self.ax.set_xlim(0, np.max(self.x))
        #self.ax.set_ylim(0, 0.050*np.max([n1,n2]))
        self.ax.set_ylim(0, 10)
        self.ax.grid(True) 

    def init(self):
        #self.l1.set_data( [], [])
        for line in self.lines:
            line.set_data( [], [])
        return self.lines

    def __call__(self, i):
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process
        if i == 0:
            return self.init()
        mu1 = self.p1[0]
        sd1 = self.p1[1]
        n1  = self.p1[2]
        mu2 = self.p2[0]
        sd2 = self.p2[1]
        n2  = self.p2[2]
        sep = (mu2-mu1)
        dx = (i/self.npts)* sep   # animate the two pdfs together
        y1 = n1*normal_pdf(self.x,mu1+dx,sd1)
        y2 = n2*normal_pdf(self.x,mu2-dx,sd2)
        
        self.l1.set_data(self.x, y1)
        self.l2.set_data(self.x, y2)
        return self.lines

# Fixing random state for reproducibility
np.random.seed(19680801)


fig, ax = plt.subplots()

stan_dev_1 = 3
stan_dev_2 = 5

ud = UpdateDist(ax, 70,stan_dev_1,50,120,stan_dev_2,30)
anim = FuncAnimation(fig, ud, frames=np.arange(100), init_func=ud.init,
                     interval=200, repeat=True, blit=True)
plt.show()
