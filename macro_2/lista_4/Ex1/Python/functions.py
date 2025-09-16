
import numpy as np

def linear_dens_fun(a1,a2,w):

    return a1 + a2*w

def compute_policy(V,TV,g,den,beta,pi,N,b,wgrid):
    
    u = lambda c: c**0.5

    dist  = 10
    tol   = 1e-5
    it    = 0
    itmax = 1000

    while (dist > tol) and (it < itmax):

        it = it + 1

        U  = u(b) + beta* np.sum( V*den )

        for i in range(0,N):

            TV[i] = np.max(np.array([(u(wgrid[i]) + beta*pi*sum(V*den))/(1-beta*(1-pi)),U]))
            g[i]  = np.argmax(TV[i])

        dist = np.max( np.abs( TV - V ))

        V = TV.copy()

    return V,g