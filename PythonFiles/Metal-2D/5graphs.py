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
    d_list_1 = [inf, 31, 12, 0.65, inf]
    d_list_2 = [inf, 31, 12, 1.3, inf]
    d_list_3 = [inf, 31, 12, 1.95, inf]
    d_list_4 = [inf, 31, 12, 2.6, inf]
    d_list_5 = [inf, 31, 12, 3.25, inf]
    
    # list of refractive indices
    n_list = [1.52, 0.0806+4.221j, 0.2198+3.321j, 5.0807+1.172j, 1.374] # 3% increase in RI
    s_list = [1.52, 0.0806+4.221j, 0.2198+3.321j, 5.0807+1.172j, 1.334] # original RI
    # wavelength in nm
    lam_vac = 632.8
    # list of angles to plot
    theta_list = linspace(60*degree, 90*degree, num=300)
    # initialize lists of y-values to plot
    
    Rp = []
    Rp_1 = []
    Rp_2 = []
    Rp_3 = []
    Rp_4 = []
    Rp_5 = []
    Rp_6 = []
    Rp_7 = []
    Rp_8 = []
    Rp_9 = []

    
    for theta in theta_list:
        Rp.append(coh_tmm('p', n_list, d_list_1, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_1.append(coh_tmm('p', s_list, d_list_1, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_2.append(coh_tmm('p', n_list, d_list_2, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_3.append(coh_tmm('p', s_list, d_list_2, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_4.append(coh_tmm('p', n_list, d_list_3, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_5.append(coh_tmm('p', s_list, d_list_3, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_6.append(coh_tmm('p', n_list, d_list_4, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_7.append(coh_tmm('p', s_list, d_list_4, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_8.append(coh_tmm('p', n_list, d_list_5, theta, lam_vac)['R'])
    for theta in theta_list:
        Rp_9.append(coh_tmm('p', s_list, d_list_5, theta, lam_vac)['R'])  

    
    x = theta_list/degree
    plt.figure()
    plt.plot(x, Rp, 'b--')
    plt.plot(x, Rp_1, 'b')
    plt.plot(x, Rp_2, 'k--')
    plt.plot(x, Rp_3, 'k')
    plt.plot(x, Rp_4, 'm--')
    plt.plot(x, Rp_5, 'm')
    plt.plot(x, Rp_6, 'r--')
    plt.plot(x, Rp_7, 'r')
    plt.plot(x, Rp_8, 'g--')
    plt.plot(x, Rp_9, 'g')

    
    plt.xlabel('theta (degree)')
    plt.ylabel('Fraction reflected')
    plt.xlim(60, 90)
    plt.ylim(0, 1)

    #plt.title('Reflection of p-polarized light with Surface Plasmon Resonance')

    #half = (max(Rp)+min(Rp))/2
    #m = Rp.index(min(Rp))
    #x_value = []

    #mid = Rp[m]
    
    #for y in range (m,0,-1):
        #if abs(Rp[y]-half) <= abs(mid-half):
            #mid = Rp[y]
        #else:
            #x_value.append(x[y+1])
        #if len(x_value) == 1:
            #break
    #mid = Rp[m]
    #for z in range (m,len(Rp),1):
        #if abs(Rp[z]-half) <= abs(mid-half):
            #mid = Rp[z]
        #else:
            #x_value.append(x[z-1])
        #if len(x_value) == 2:
            #break
    
    #a = x[Rp.index(min(Rp))]
    #b = x[Rp_1.index(min(Rp_1))]
    #c = x_value[1]-x_value[0]
    #d = a-b
    #print ("FWHM = " + str(c) + " degrees")
    #print ("Sensitivity = " + str(d) +" degrees")
    #print ("FoM = " + str(d/c))
    plt.show()

FoM()
