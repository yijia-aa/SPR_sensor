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


# "5 * degree" is 5 degrees expressed in radians
# "1.2 / degree" is 1.2 radians expressed in degrees
degree = pi/180

def FoM():
    """
    An example reflection plot with a surface plasmon resonance (SPR) dip.
    Compare with http://doi.org/10.2320/matertrans.M2010003 ("Spectral and
    Angular Responses of Surface Plasmon Resonance Based on the Kretschmann
    Prism Configuration") Fig 6a
    """
    # list of layer thicknesses in nm
    d_list = [inf, 0, 52, inf]
    # list of refractive indices
    n_list = [1.52, 0.220+3.32j, 0.08+4.22j, 1.372]
    s_list = [1.52, 0.220+3.32j, 0.08+4.22j, 1.332]
    # wavelength in nm
    lam_vac = 633
    # list of angles to plot
    theta_list = linspace(60*degree, 90*degree, num=300)
    # initialize lists of y-values to plot
    Rp = []
    Rp_1 = []
    for theta in theta_list:
        Rp.append(coh_tmm('p', n_list, d_list, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_1.append(coh_tmm('p', s_list, d_list, theta, lam_vac)['R'])
    x = theta_list/degree
    plt.figure()
    plt.plot(x, Rp, 'red')
    plt.plot(x, Rp_1, 'blue')
    plt.xlabel('theta (degree)')
    plt.ylabel('Fraction reflected')
    plt.xlim(60, 90)
    plt.ylim(0, 1)
    plt.title('Reflection of p-polarized light with Surface Plasmon Resonance')

    half = (max(Rp_1)+min(Rp_1))/2
    m = Rp_1.index(min(Rp_1))
    x_value = []

    mid = Rp_1[m]
    
    for y in range (m,0,-1):
        if abs(Rp_1[y]-half) <= abs(mid-half):
            mid = Rp_1[y]
        else:
            x_value.append(x[y+1])
        if len(x_value) == 1:
            break
    mid = Rp_1[m]
    for z in range (m,len(Rp_1),1):
        if abs(Rp_1[z]-half) <= abs(mid-half):
            mid = Rp_1[z]
        else:
            x_value.append(x[z-1])
        if len(x_value) == 2:
            break
    
    a = x[Rp.index(min(Rp))]
    b = x[Rp_1.index(min(Rp_1))]
    c = x_value[1]-x_value[0]
    d = (a-b)/0.04
    print ("FWHM = " + str(c) + " degrees")
    print ("Sensitivity = " + str(d) +" degrees")
    print ("FoM = " + str(d/c))
    plt.show()

FoM()
