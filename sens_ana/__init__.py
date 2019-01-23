from diff_evol import DiffEvol

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from tools.plots import plot_sa

import os
import numpy as np
from random import uniform
from random import randint


class SensAna(DiffEvol):

    def __init__(self, pars, cfgs):
        """ init SensAnal

        :param pars: parser namespace
        """

        self._mod_data = None
        self._mod_data_interp = None
        self._mod_conf = pars.mod_conf
        self._mod_file = cfgs.model_file

        self._out_dir = pars.out_dir

        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate

        self._plot = True

        # generates p parameter sets
        self._gen_param_sets(cfgs)
        # base scenarios matrix
        self._B = self._make_base_array(cfgs)
        print (self._B)

    def _make_base_array(self, cfgs):
        """ Creates matrix of base scenarios.

        ncols = number of parameters
        nrows = number of replications
        """

        B = np.zeros([cfgs.R, cfgs.k], float)
        for i in range(cfgs.R):
            params = self._get_param_set(cfgs)
            B[i][:] = params
            
        return B

    def _gen_param_sets(self, cfgs):
        """ Creates p levels of each parameter.

        NOTE
        Ks and S are generated basen on mean and sd of exponent normal distribution.
        """

        self._X_levels = [uniform(cfgs.X[0], cfgs.X[1])
                          for p in range(0, cfgs.p)]
        self._Y_levels = [uniform(cfgs.Y[0], cfgs.Y[1])
                          for p in range(0, cfgs.p)]
        self._b_levels = [uniform(cfgs.b[0], cfgs.b[1])
                          for p in range(0, cfgs.p)]
        self._ret_levels = [uniform(cfgs.ret[0], cfgs.ret[1])
                            for p in range(0, cfgs.p)]

        self._Ks_levels = 10.**np.random.normal(cfgs.Ks[0], cfgs.Ks[1], cfgs.p)
        self._S_levels = 10.**np.random.normal(cfgs.S[0], cfgs.S[1], cfgs.p)

    def _get_param_set(self, cfgs):

        params = np.zeros([cfgs.k], float)

        i = randint(0, cfgs.p-1)
        params[0] = self._X_levels[i]
        i = randint(0, cfgs.p-1)
        params[1] = self._Y_levels[i]
        i = randint(0, cfgs.p-1)
        params[2] = self._b_levels[i]
        i = randint(0, cfgs.p-1)
        params[3] = self._Ks_levels[i]
        i = randint(0, cfgs.p-1)
        params[4] = self._S_levels[i]
        i = randint(0, cfgs.p-1)
        params[5] = self._ret_levels[i]

        return (params)

    def do_sa(self):
        pass

    def __del__(self):
        path = '{}{sep}sens_ana_out.log'.format(self._out_dir, sep=os.sep)
        with open(path, 'w') as out:
            out.write('{}\n'.format('Done...'))
