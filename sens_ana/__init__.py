from diff_evol import DiffEvol
from diff_evol import sum_of_squares

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from diff_evol.mod_data_handling import RecModData
from tools.plots import plot_sa
from tools.plots import plot_rep
import model.smoderp2d.main as sm

import os
import numpy as np
import math
from random import uniform
from random import randint


class SensAna(DiffEvol):

    def __init__(self, pars, cfgs):
        """ init SensAnal

        :param pars: parser namespace
        """
        self._bf_data = cfgs.data
        self._mod_data = None
        self._mod_data_interp = None
        self._cfgs = cfgs
        self._mod_conf = pars.mod_conf
        self._mod_file = self._cfgs.model_file

        self._out_dir = pars.out_dir

        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate

        self._plot = False

    def _get_param_set(self):

        params = np.zeros([self._cfgs.k], float)

        i = randint(0, self._cfgs.p-1)
        params[0] = self._X_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[1] = self._Y_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[2] = self._b_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[3] = self._Ks_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[4] = self._S_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[5] = self._ret_levels[i]

        return (params)

    def model(self, params):

        sm.run(self._mod_conf, params, self._cfgs)

        mod_data = self._read_mod_file(self._mod_file)
        self._mod_data_interp = self._interp_mod_data(
            mod=mod_data, obs=self._bf_data)

        ss = sum_of_squares(self._bf_data.val, self._mod_data_interp.val)

        return(ss)

    def do_sa(self):

        #ss_d = self.model(par_d)


    def __del__(self):
        
        print ('sens.py done')
