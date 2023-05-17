#import exceptions
import numpy as np
import sys

if sys.version_info[0] < 3:
    from ConfigParser import ConfigParser
    from ConfigParser import NoOptionError
else:    
    from configparser import ConfigParser
    from configparser import NoOptionError



class Error(Exception):
    pass


class IncorrectDataInObsFile(Error):

    """Exception raised if the water level goes to negative values.
    """

    def __init__(self, val):
        self.msg = 'Incorrect observation data: '+str(val)

    def __str__(self):
        return repr(self.msg)


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
        self.plotlength = self._config.getfloat('Params', 'plotlength')
        self.plotwidth  = self._config.getfloat('Params', 'plotwidth')

        self.nh = self._config.getint('ObsDataWLevel', 'rows')
        file_h = self._config.get('ObsDataWLevel', 'file')
        self.nq = self._config.getint('ObsDataDischarge', 'rows')
        file_q = self._config.get('ObsDataDischarge', 'file')
        self.model_file = self._config.get('Model', 'mod_file')
        
        self.data_h = RecObsData(self.nh)
        self.data_q = RecObsData(self.nq)
        
        # read water level level data
        i = 0
        with open(file_h, 'r') as ob_ls:
            ob_ls = ob_ls.readlines()
            for line in ob_ls:
                time = (self._read_line_vals(line)[0])
                val = (self._read_line_vals(line)[1])
                self.data_h.set_vals(i=i, time=time, val=val)
                i += 1
        
        i = 0
        with open(file_q, 'r') as ob_ls:
            ob_ls = ob_ls.readlines()
            for line in ob_ls:
                time = (self._read_line_vals(line)[0])
                val = (self._read_line_vals(line)[1])
                self.data_q.set_vals(i=i, time=time, val=val)
                i += 1
        
        # time minutes to sec
        self.data_h.time = self.data_h.time*60.
        self.data_q.time = self.data_q.time*60.
        # rainfall intensity from mm/hour to m/sec
        self.rainfall = self.rainfall/1000./60./60.
        # runoff water level in meter from obs data m
        self.data_h.val = self.data_h.val
        # runoff intensity from mm/minute to m/sec
        self.data_q.val = self.data_q.val/1000./60.
        
        self.data_q.calc_infiltration(self.rainfall)
        
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
        if not(len(_line) > 1):
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





