from diff_evol import DiffEvol

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from tools.plots import plot_sa

import os


class SensAna(DiffEvol):

    def __init__(self, pars,  obs):
        """ init SensAnal

        :param pars: parser namespace
        :param obs: list of obs_data_handler.RecObsData instances  
        """
        self._obs = obs
        self._obs_data = obs.data
        self._mod_data = None
        self._mod_data_interp = None
        self._mod_conf = pars.mod_conf
        self._out_dir = pars.out_dir
        self._mod_file = obs.model_file
        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate
        self._plot = True
        self._model_runs = 0
        self._p1 = []
        self._p2 = []
        self._p3 = []
        self._ss = []

    def do_sa(self):

        for sc in self._obs.scenario:
            print ('model run {}/{}...'.format(self._model_runs,
                                               self._obs._n_scenarios))
            self._p1.append(sc[0])
            self._p2.append(sc[1])
            self._p3.append(sc[2])
            self._ss.append(self.model(sc))

    def __del__(self):
        path = '{}{sep}sens_ana_out.dat'.format(self._out_dir, sep=os.sep)
        with open(path, 'w') as out:
            for i in range(self._obs._n_scenarios):
                line = '{:.5e};{:.5e};{:.5e};{:.5e}\n'.format(
                    self._p1[i], self._p2[i], self._p3[i], self._ss[i])
                out.write(line)

        plot_sa(self._out_dir, self._p1, self._p2, self._ss)
