import os
import numpy as np
from configparser import ConfigParser


class RecFitData(object):
    """ RecFitData contains data of best fit  """

    def __init__(self, n):

        self.time = np.zeros(n, float)
        self.val = np.zeros(n, float)
        self.fit_vals = np.zeros(n, float)
        self._n = n

    def set_vals(self, times, vals, fit_vals):

        self.time = times
        self.val = vals
        self.fit_vals = fit_vals


class ReadConfig(object):
    """ read cfg file """

    def __init__(self, config_path):

        self._config = ConfigParser()
        self._config.read(config_path)

        # number of monte carlo runs
        self.mcruns = self._config.getint('SensParams', 'mcruns')

        # X,Y,b,ret are evenly ditributer within margins
        self.X = [float(par) for par in self._config.get(
            'ParamsMargins', 'X').split(',')]
        self.Y = [float(par) for par in self._config.get(
            'ParamsMargins', 'Y').split(',')]
        self.b = [float(par) for par in self._config.get(
            'ParamsMargins', 'b').split(',')]
        self.ret = [float(par) for par in self._config.get(
            'ParamsMargins', 'ret').split(',')]

        # Ks and S are distributed based on normal ditribution
        # of its exponent
        self.Ks = [float(par) for par in self._config.get(
            'ParamsMargins', 'Ks').split(',')]
        self.S = [float(par) for par in self._config.get(
            'ParamsMargins', 'S').split(',')]

        self.model_file = self._config.get('Model', 'mod_file')

        # set instance of RecFitData with filled data from obs_mod.dat
        best_fit_dir = self._config.get('BestFit', 'dir')
        self.data = self._read_obs_fit_mod(best_fit_dir)

        # set read best fit params from params.dat
        bfparams = self._read_best_fit_params(best_fit_dir)
        self.bfX = bfparams[0]
        self.bfY = bfparams[1]
        self.bfb = bfparams[2]
        self.bfKs = bfparams[3]
        self.bfS = bfparams[4]
        self.bfret = bfparams[5]
        self.slope = bfparams[6]
        self.rainfall = bfparams[7]
        self.bfss = bfparams[8]

    def _read_obs_fit_mod(self, dir_):
        """ make RecFitData instance

        :param dir_: directory with best fit data (obs_mod.dat)
        :return instance(RecFitData): instance containing the bod and best fit data
        """
        file_ = '{}{sep}obs_mod.dat'.format(dir_, sep=os.sep)
        with open(file_, 'r') as f:
            lines = f.readlines()

        n = 0
        times = []
        vals = []
        fit_vals = []
        first_ = True
        for line in lines:
            if not(first_):
                n += 1
                l = line.replace('\n', '').split(';')
                times.append(float(l[0]))
                vals.append(float(l[1]))
                fit_vals.append(float(l[2]))
            first_ = False

        fit_data = RecFitData(n)
        fit_data.set_vals(times, vals, fit_vals)

        return fit_data

    def _read_best_fit_params(self, dir_):
        """ read best params rainfall and slope data

        :param dir_: directory with best fit data (params.dat)
        :return:  list of best fit params
        """
        file_ = '{}{sep}params.dat'.format(dir_, sep=os.sep)
        with open(file_, 'r') as f:
            lines = f.readlines()

        first_ = True
        for line in lines:
            if not(first_):
                l = line.replace('\n', '').split(';')
                X = float(l[0])
                Y = float(l[1])
                b = float(l[2])
                Ks = float(l[3])
                S = float(l[4])
                ret = float(l[5])
                slope = float(l[6])
                rainfall = float(l[7])
                ss = float(l[8])
            first_ = False

        return X, Y, b, Ks, S, ret, slope, rainfall, ss
