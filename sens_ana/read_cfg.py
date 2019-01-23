import numpy as np
from configparser import ConfigParser
from diff_evol.obs_data_handler import ObsData

class ReadConfig(ObsData):
    """ read cfg file """

    def __init__(self, config_path):
        
        ObsData.__init__(self,config_path)
        
        # number of replications
        self.R = self._config.getint('SensAna', 'R')
        # number of levels of parameter
        self.p = self._config.getint('SensAna', 'p')
        # number of parameters
        self.k = self._config.getint('SensAna', 'k')

        # X,Y,b,ret are evenly ditributer within margins
        self.X = [float(par) for par in self._config.get(
            'ParamsDef', 'X').split(',')]
        self.Y = [float(par) for par in self._config.get(
            'ParamsDef', 'Y').split(',')]
        self.b = [float(par) for par in self._config.get(
            'ParamsDef', 'b').split(',')]
        self.ret = [float(par) for par in self._config.get(
            'ParamsDef', 'ret').split(',')]

        # Ks and S are distributed based on normal ditribution
        # of its exponent
        self.Ks = [float(par) for par in self._config.get(
            'ParamsDef', 'Ks').split(',')]
        self.S = [float(par) for par in self._config.get(
            'ParamsDef', 'S').split(',')]

        
