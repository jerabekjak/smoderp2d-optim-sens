from exceptions import IncorrectDataInObsFile
import numpy as np


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

    def __init__(self, obs_path):

        ob_f = open(obs_path, 'r')
        ob_ls = ob_f.readlines()

        i = 0
        n_read = False
        intensit_read = False

        for line in ob_ls:
            if ('#' in line[0:4]):
                continue
            else:
                if (not(n_read) and not(intensit_read)):
                    self.rainfall = self._read_line_float(line)
                    intensit_read = True
                elif (not(n_read) and intensit_read):
                    self.n = self._read_line_int(line)
                    self.data = RecObsData(self.n)
                    n_read = True
                else:
                    time = (self._read_line_vals(line)[0])
                    val = (self._read_line_vals(line)[1])
                    self.data.set_vals(i=i, time=time, val=val)
                    i += 1

        self.data.calc_infiltration(self.rainfall)

        ob_f.close()

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
