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

def EFD():
    """
    Here is an example where we plot absorption and Poynting vector
    as a function of depth.
    """
    d_list = [inf, 31, 12, 0.8, 0.34, 150, inf] #in nm
    n_list = [1.52, 0.0806+4.221j, 0.2198+3.321j, 4.8936+0.313j, 3+1.149j, 1.374, 1] 
    th_0 = pi/4
    lam_vac = 632.8
    pol = 'p'
    coh_tmm_data = coh_tmm(pol, n_list, d_list, th_0, lam_vac)

    ds = linspace(0, 200, num=1000) #position in structure
    poyn = []
    absor = []
    for d in ds:
        layer, d_in_layer = find_in_structure_with_inf(d_list, d)
        data = position_resolved(layer, d_in_layer, coh_tmm_data)
        poyn.append(data['poyn'])
        absor.append(data['absor'])
    # convert data to numpy arrays for easy scaling in the plot
    poyn = array(poyn)
    absor = array(absor)
    plt.figure()
    plt.plot(ds, 200*absor, 'purple')
    plt.xlabel('depth (nm)')
    plt.ylabel('AU')
    plt.title('Local absorption of electric field')
    plt.show()


EFD()
