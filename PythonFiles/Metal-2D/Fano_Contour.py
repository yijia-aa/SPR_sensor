# -*- coding: utf-8 -*-
"""
Examples of plots and calculations using the tmm package.
"""
from __future__ import division, print_function, absolute_import

from tmm_core import (coh_tmm, unpolarized_RT, ellips,
                       position_resolved, find_in_structure_with_inf)

from numpy import pi, linspace, inf, array
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

try:
    import colorpy.illuminants
    import colorpy.colormodels
    from . import color
    colors_were_imported = True
except ImportError:
    # without colorpy, you can't run sample5(), but everything else is fine.
    colors_were_imported = False

import numpy as np

# "5 * degree" is 5 degrees expressed in radians
# "1.2 / degree" is 1.2 radians expressed in degrees
degree = pi/180

def contour():
    """
    An example reflection plot with a surface plasmon resonance (SPR) dip.
    Compare with http://doi.org/10.2320/matertrans.M2010003 ("Spectral and
    Angular Responses of Surface Plasmon Resonance Based on the Kretschmann
    Prism Configuration") Fig 6a
    """
    lam_vac = 633
    n_list = [1.7847, 0.0798 + 4.1960j, 1.458, 1.62, 1.333]
    theta_list = linspace(59*degree, 67*degree, num=300)
    x = theta_list/degree
    T = []
    # Rp = np.empty(shape=(300,300), dtype = 'object')
    Rp = []
    a = 0
    for t in range (0,1200,4):
        T.append(t/1000)
        lis = []
        Rp.append(lis)
        d_list = [inf, 48, t, 1300, inf]
        a = a+1
        for theta in theta_list:
            Rp[a-1].append(coh_tmm('p', n_list, d_list, theta, lam_vac)['R'])

    # X,Y = np.meshgrid(x,T)
    # Z = np.sqrt(X**2+Y**2)
    
    # Z = np.array(Rp)
    # Z = np.asmatrix(Rp)
    plt.figure()
    plt.contour(x, T, Rp)
    plt.xlabel('Angle in degrees')
    plt.ylabel('t in μm')
    plt.xlim(59, 67)
    plt.ylim(0, 1)
    plt.title('Contour plots of the reflection versus incident angle and the thickness of the SiO2 layer')
    plt.show()
    # print(len(Rp))
    # print(len(Rp[0]))

contour()
