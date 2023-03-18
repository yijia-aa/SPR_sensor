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
    for t in range (43,48,1):
        for g in range (2,7,1):
            for h in range (2,7,1):
    # list of layer thicknesses in nm
                d_list = [inf, t, g, h, inf]
    # list of refractive indices
                n_list = [1.7847, 0.056253+4.2760j, 3.8827+0.019626j, 0.27002+3.4081j, 1.374] # 3% increase in RI
                s_list = [1.7847, 0.056253+4.2760j, 3.8827+0.019626j, 0.27002+3.4081j, 1.334] # original RI
    # wavelength in nm
                lam_vac = 632.8
    # list of angles to plot
                theta_list = linspace(30*degree, 80*degree, num=300)
    # initialize lists of y-values to plot
                Rp = []
                Rp_1 = []
                for theta in theta_list:
                    Rp.append(coh_tmm('p', n_list, d_list, theta, lam_vac)['R'])
                for theta in theta_list:
                    Rp_1.append(coh_tmm('p', s_list, d_list, theta, lam_vac)['R'])
                x = theta_list/degree

                half = (max(Rp)+min(Rp))/2
                m = Rp.index(min(Rp))
                x_value = []

                mid = Rp[m]
                for y in range (m,0,-1):
                    if abs(Rp[y]-half) <= abs(mid-half):
                        mid = Rp[y]
                    else:
                        x_value.append(x[y+1])
                    if len(x_value) == 1:
                        break
                mid = Rp[m]
                for z in range (m,len(Rp),1):
                    if abs(Rp[z]-half) <= abs(mid-half):
                        mid = Rp[z]
                    else:
                        x_value.append(x[z-1])
                    if len(x_value) == 2:
                        break
    
                a = x[Rp.index(min(Rp))]
                b = x[Rp_1.index(min(Rp_1))]
                c = x_value[1]-x_value[0]
                d = a-b
                # print ("FWHM " + str(t) + ", " + str(g) + " = " + str(c))
                # print ("Sensitivity " + str(t) + ", " + str(g) + " = " + str(d))
                print ("FoM " + str(t) + ", " + str(g) + ", " + str(h) + " = " + str(d/c))
                plt.show()

FoM()
