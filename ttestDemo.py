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


def debprt(x,str):
    print(str + ': {} type: {} shape: {}'.format(x,type(x),np.shape(x)))
    pass

def beta_pdf(x, a, b):
    return (x**(a-1) * (1-x)**(b-1) * math.gamma(a + b)
            / (math.gamma(a) * math.gamma(b)))


def normal_pdf(x, mu, sd):    
    return spstat.norm.pdf(x,mu,sd)


def welchT(mu1,sd1,n1,mu2,sd2,n2):    
    # welch's T-test (https://en.wikipedia.org/wiki/Student%27s_t-test#Independent_two-sample_t-test)
    s_delta = np.sqrt(sd1*sd1/n1 + sd2*sd2/n2)
    T = (mu1 - mu2)/s_delta
    dof = n1+n2-2
    p = spstat.t.sf(np.abs(T), dof)*2 
    return T,p
    
    
    
anim_loop_cnt = 0

class UpdateDist:
    global anim_loop_cnt
    def __init__(self, ax, mu1, psd1,n1, mu2,psd2,n2):
        self.p1 = [mu1,psd1,n1]
        self.p2 = [mu2,psd2,n2]
        #  l12 is two plots [x],[y1],[x],[y2]
        self.l1, = ax.plot([], [], 'b-')
        self.l2, = ax.plot([], [], 'r-')
        self.l_Pval, =  ax.plot([], [], 'g-')
        self.l_mu_diff, = ax.plot([],[], 'k-')
        self.lines = [self.l1, self.l2, self.l_Pval,self.l_mu_diff]
        self.ax = ax
        #anim_loop_cnt = 0
        self.sd_gain = 0.0   # increase StdDevs for each repeat loop
        self.npts = 200    # how many graph pts
        self.xm = 150      # max x value
        self.x = np.linspace(0, self.xm, self.npts)
        self.pvals = np.zeros(self.npts)
        # Set up plot parameters
        self.ax.set_xlim(0, np.max(self.x))
        #self.ax.set_ylim(0, 0.050*np.max([n1,n2]))
        self.ax.set_ylim(0, 10)
        self.ax.set_xlabel('measurement value')
        self.ax.set_ylabel('number of measurements recorded')
        #self.ax.text( 10,8, '>>green = P-value (x100)')
        
        
        # Significance Level P=0.05.
        self.ax.axhline(0.05*100, linestyle='--', color='black')
        
        self.ax.grid(True) 

    def init(self):
        global anim_loop_cnt
        #self.l1.set_data( [], [])
        for l in self.lines:
            l.set_data( [], [])
        self.pvals = np.zeros(self.npts)
        anim_loop_cnt += 1
        self.sd_gain = 1.0*anim_loop_cnt
        #self.ax.text( 10,8, 'green = P-value (x100), sd1:{:5.1f} sd2:{:5.1f}'.format(float(self.p1[1]+self.sd_gain), float(self.p2[1]+self.sd_gain)))
        self.ax.text( 10,8, 'green = P-value (x100), n1:{} n2:{}'.format(self.p1[2],self.p2[2]))
        return self.lines

    def __call__(self, i):
        global anim_loop_cnt
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process 
            
        #self.sd_gain = 1*anim_loop_cnt
        if i == 0:
            return self.init()
        if i == 98:
            x = input('pause')
        mu1 = self.p1[0]
        sd1 = self.p1[1] + self.sd_gain
        n1  = self.p1[2]
        mu2 = self.p2[0]
        sd2 = self.p2[1] + 1.0*anim_loop_cnt
        n2  = self.p2[2]
        sep = (mu2-mu1)   # x-units
        dx = (float(i)/self.npts) * sep   # animate the two pdfs together
        
        y1 = n1*normal_pdf(self.x,mu1+dx,sd1) 
        y2 = n2*normal_pdf(self.x,mu2-dx,sd2)
 
        #debprt(y2,'y2')
        
        #debprt(np.mean(y1),'mean1')
        #debprt(np.mean(y2),'mean2')
        #debprt(sd1,'sd1')
        #debprt(sd2,'sd2')
        
        #T,p = spstat.ttest_ind(y1,y2,equal_var=True)
        #
        T,p = welchT(mu1+dx,sd1,n1,mu2-dx,sd2,n2)

        
        if p < 0.06:  # freeze animation after P >0.05          
            print('{}: sd: {:3.1f} mu1-mu2: {:5.1f} T:{:5.2f} p:{:6.3f}'.format(i,sd1,(mu1+dx) - (mu2-dx),T,p))
            self.pvals[i] = p*100      # scale p-val for full scale == 0.5
            
            self.l1.set_data(self.x, y1)
            self.l2.set_data(self.x, y2)
            self.l_Pval.set_data(self.x,self.pvals)
            # illustrate diff btwn means
            x1 = mu1+dx
            x2 = mu2-dx
            y = 1.82
            dy = 0.25
            self.l_mu_diff.set_data([x1,x1,x1,x2,x2,x2],[y-dy, y+dy, y, y, y+dy, y-dy])
        return self.lines



if __name__=='__main__':
    
    sd1 = sd2 = 5.0
    mu1 = 0.0
    n1=n2 = 30
    
    deltas = [3,2] + list( np.linspace(1.0,0.1,10)) + [0.64] # fractions of stand. Dev
    
    for d in deltas:
        mu2 = mu1 + d*sd1
        T,p = welchT(mu1,sd1,n1,mu2,sd2,n2)
        print('delta: {:4.2f}x std  T: {:4.2f} p: {:7.5f}'.format(d,T,p))

    if False:
        #
        #  Iteratively find delta correpsponding to p=0.05
        #
        d2 = 0.64 * sd1 
        mu2 = mu1 + d2
        dinc = d2/500
        err = 9999.0
        emax = 0.0001
        while err > emax: 
            T,p = welchT(mu1,sd1,n1,mu2,sd2,n2)
            err = np.abs(p-0.05000)
            if err > 0.0:
                mu2 -= dinc
            else:
                mu2 += dinc
            emax *= 1.01  # kind of an escape function!
                
        dfin = np.abs((mu1-mu2)/sd1)  # how many SDs apart for P=0.05
        print(' P < 0.05: ')
        print('delta: {:10.5f}x std  T: {:4.2f} p: {:7.5f}  n pts: {}'.format(dfin,T,p,n1))
        
        quit()
    # Fixing random state for reproducibility
    #np.random.seed(1968298230)


    fig, ax = plt.subplots()

    stan_dev_1 = 2
    stan_dev_2 = 2
    nsamp = 10

    ud = UpdateDist(ax, 70,stan_dev_1,nsamp,120,stan_dev_2,nsamp)
    anim = FuncAnimation(fig, ud, frames=np.arange(100), init_func=ud.init,
                        interval=30, repeat=True, blit=True)
    plt.show()
