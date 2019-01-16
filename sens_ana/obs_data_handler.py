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
