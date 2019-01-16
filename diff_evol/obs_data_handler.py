from exceptions import IncorrectDataInObsFile
import numpy as np
from configparser import ConfigParser

class RecObsData(object):
    """ RecObsData contains data of one observed record """

    def __init__(self, n):

        self.time = np.zeros(n, float)
        self.val = np.zeros(n, float)
        self.infilt = np.zeros(n, float)
        self._n = n

    def set_vals(self, i, time, val):

        self.time[i] = time
        self.val[i] = val

    def calc_infiltration(self, rainfall):
        """ calculate infiltration based on the water level of runoff """

        self.infilt = rainfall - self.val


class ObsData(object):
    """ ObsData handle obs data reading 

    public list self.data of RecObsData instances
    """

    def __init__(self, config_path):
        
        self._config = ConfigParser()
        self._config.read(config_path)
        
        self.rainfall = self._config.getfloat('Params', 'rainfall')
        self.slope = self._config.getfloat('Params', 'slope')
        self.n = self._config.getint('Data', 'rows')
        file_ = self._config.get('Data', 'file')
        self.model_file = self._config.get('Model', 'mod_file')
        
        self.data = RecObsData(self.n)
        
        i = 0
        with open(file_, 'r') as ob_ls:
            ob_ls = ob_ls.readlines()
            for line in ob_ls:
                time = (self._read_line_vals(line)[0])
                val = (self._read_line_vals(line)[1])
                self.data.set_vals(i=i, time=time, val=val)
                i += 1
        
        # time minutes to sec
        self.data.time = self.data.time*60.
        # rainfall intensity from mm/hour to m/sec
        self.rainfall = self.rainfall/1000./60./60.
        # runoff intensity from mm/minute to m/sec
        self.data.val = self.data.val/1000./60.
        
        self.data.calc_infiltration(self.rainfall)
        
    def _read_line_int(self, _line):
        try:
            val = int(_line)
        except ValueError:
            raise IncorrectDataInObsFile(_line)
        return val

    def _read_line_float(self, _line):
        try:
            val = int(_line)
        except ValueError:
            raise IncorrectDataInObsFile(_line)
        return val

    def _read_line_vals(self, _line):

        _line = _line.replace('\n', '').split('\t')
        if not(len(_line) == 2):
            raise IncorrectDataInObsFile(_line)

        try:
            val = list(_line)
        except ValueError:
            raise IncorrectDataInObsFile(_line)

        try:
            time = float(val[0])
        except ValueError:
            raise IncorrectDataInObsFile(val[0])

        try:
            obs = float(val[1])
        except ValueError:
            raise IncorrectDataInObsFile(val[1])
        return time, obs
