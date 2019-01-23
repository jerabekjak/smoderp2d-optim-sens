from diff_evol import DiffEvol

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from diff_evol.mod_data_handling import RecModData
from tools.plots import plot_sa
import model.smoderp2d.main as sm

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
        self._cfgs = cfgs
        self._mod_conf = pars.mod_conf
        self._mod_file = self._cfgs.model_file

        self._out_dir = pars.out_dir

        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate

        self._plot = True

        # generates p parameter sets
        self._gen_param_sets(cfgs)
        # base scenarios matrix
        self._B = self._make_base_array(cfgs)
        # array of elementary effects
        self._E = np.zeros_like(self._B)
        self._delta = 1.-1./(self._cfgs.p-1.)

    def _make_base_array(self, cfgs):
        """ Creates matrix of base scenarios.

        ncols = number of parameters
        nrows = number of replications
        """

        B = np.zeros([self._cfgs.R, self._cfgs.k], float)
        for i in range(self._cfgs.R):
            params = self._get_param_set(cfgs)
            B[i][:] = params

        return B

    def _gen_param_sets(self, cfgs):
        """ Creates p levels of each parameter.

        NOTE
        Ks and S are generated basen on mean and sd of exponent normal distribution.
        """

        self._X_levels = [uniform(self._cfgs.X[0], self._cfgs.X[1])
                          for p in range(0, self._cfgs.p)]
        self._Y_levels = [uniform(self._cfgs.Y[0], self._cfgs.Y[1])
                          for p in range(0, self._cfgs.p)]
        self._b_levels = [uniform(self._cfgs.b[0], self._cfgs.b[1])
                          for p in range(0, self._cfgs.p)]
        self._ret_levels = [uniform(self._cfgs.ret[0], self._cfgs.ret[1])
                            for p in range(0, self._cfgs.p)]

        self._Ks_levels = 10.**np.random.normal(
            self._cfgs.Ks[0], self._cfgs.Ks[1], self._cfgs.p)
        self._S_levels = 10.**np.random.normal(
            self._cfgs.S[0], self._cfgs.S[1], self._cfgs.p)

    def _get_param_set(self, cfgs):

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

    def _single_el_effect(self, irep, ipar):
        """ calculates elementary effect of a single ipar parameter in irep replication """

        # base scenario
        par_0 = self._B[irep][:]

        # changed scenario
        par_d = par_0.copy()
        par_d[ipar] = par_d[ipar] + self._delta

        ss_0 = self.model(par_0)
        ss_d = self.model(par_d)

        print (ss_0)
        print (ss_d)

    def model(self, params):

        sm.run(self._mod_conf, params, self._cfgs)

        mod_data = self._read_mod_file(self._mod_file)
        mod_interp = self._interp_mod_data(mod=mod_data, obs=self._mask_data)

    def do_sa(self, cfgs):

        for irep in range(self._cfgs.R):
            for ipar in range(self._cfgs.k):
                el_effect = self._single_el_effect(irep, ipar)
                #self._E[irep][ipar] = el_effect

    def __del__(self):
        path = '{}{sep}base_scen_array'.format(self._out_dir, sep=os.sep)
        np.savetxt(path, self._B, fmt='%1.4e', delimiter='\t')
        path = '{}{sep}sens_ana_out.log'.format(self._out_dir, sep=os.sep)
        with open(path, 'w') as out:
            out.write('{}\n'.format('Done...'))
