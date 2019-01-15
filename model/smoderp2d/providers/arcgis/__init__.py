import sys
import logging

import arcpy

from model.smoderp2d.core.general import Globals
from model.smoderp2d.providers.base import BaseProvider
from model.smoderp2d.providers.arcgis import constants
from model.smoderp2d.providers.arcgis.logger import ArcPyLogHandler
from model.smoderp2d.providers.base import Logger

class ArcGisProvider(BaseProvider):
    
    def __init__(self):
        super(ArcGisProvider, self).__init__()

        self._print_fn = arcpy.AddMessage

        # ArcGIS provider is designed to support only 'full' type of
        # computation
        self._args.typecomp = 'full'

        # must be defined for _cleanup() method
        Globals.outdir = self._get_argv(constants.PARAMETER_PATH_TO_OUTPUT_DIRECTORY)

        # logger
        handler = ArcPyLogHandler()
        formatter = logging.Formatter("%(levelname)-8s %(message)s")
        handler.setFormatter(formatter)
        Logger.addHandler(handler)
        Logger.setLevel(logging.DEBUG)

    @staticmethod
    def _get_argv(idx):
        return sys.argv[idx+1]

    def _load_dpre(self):
        """Load configuration data from data preparation procedure.

        :return dict: loaded data
        """
        from model.smoderp2d.providers.arcgis.data_preparation import PrepareData
       
        prep = PrepareData()
        return prep.run()
