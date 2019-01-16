from exceptions import IncorrectDataInObsFile
from diff_evol.obs_data_handler import ObsData as DEObsData
import numpy as np
from configparser import ConfigParser


class ObsData(DEObsData):
    """ ObsData handle obs data reading 

    public list self.data of RecObsData instances
    """

    def __init__(self, config_path):

        DEObsData.__init__(self, config_path)

        self._n_scenarios = self._config.getint('SensAna', 'n_scenarios')
        scenario_def = self._config.get('SensAna', 'scenario_def')
        self.scenario = [None]*self._n_scenarios

        i = 0
        with open(scenario_def, 'r') as sc:
            sc_ls = sc.readlines()
            for line in sc_ls:
                vals = self._read_line_vals_sc(line)
                self.scenario[i] = vals
                i += 1

    def _read_line_vals_sc(self, _line):

        _line = _line.replace('\n', '').split('\t')
        if not(len(_line) == 3):
            raise IncorrectDataInObsFile(_line)

        try:
            val = list(_line)
        except ValueError:
            raise IncorrectDataInObsFile(_line)

        val_out = val
        i = 0
        for ival in val:
            try:
                val_out[i] = float(ival)
                i += 1
            except ValueError:
                raise IncorrectDataInObsFile(ival)

        return val_out
