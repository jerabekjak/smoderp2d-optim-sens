import os
import sys
import argparse
import logging
import numpy as np
if sys.version_info.major >= 3:
    from configparser import ConfigParser, NoSectionError
else:
    from ConfigParser import ConfigParser, NoSectionError

from model.smoderp2d.core.general import GridGlobals, DataGlobals, Globals
from model.smoderp2d.providers.base import BaseProvider, Logger, CompType, BaseWritter
from model.smoderp2d.exceptions import ConfigError
from argparse import Namespace

class CmdWritter(BaseWritter):
    def __init__(self):
        super(CmdWritter, self).__init__()

    def write_raster(self, array, output_name, directory='core'):
        """Write raster (numpy array) to ASCII file.

        :param array: numpy array
        :param output_name: output filename
        :param directory: directory where to write output file
        """
        file_output = self._raster_output_path(output_name, directory)

        np.savetxt(file_output, array, fmt='%.6e')

        self._print_array_stats(
            array, file_output
        )

class OptimSensProvider(BaseProvider):
    def __init__(self, indata_path):
        """Create argument parser."""
        super(OptimSensProvider, self).__init__()
        
        ## define CLI parser
        #parser = argparse.ArgumentParser(description='Run Smoderp2D.')

        ## type of computation
        #parser.add_argument(
        #    '--typecomp',
        #    help='type of computation',
        #    type=str,
        #    choices=['full',
        #             'dpre',
        #             'roff'],
        #    required=True
        #)

        ## data file (only required for runoff)
        #parser.add_argument(
        #    '--indata',
        #    help='file with prepared data',
        #    type=str
        #)
        #self.args = parser.parse_args()
        #self.args.typecomp = CompType()[self.args.typecomp]

        self.args = Namespace(indata=indata_path, typecomp='roff')

        # load configuration
        self._config = ConfigParser()
        if self.args.typecomp == CompType.roff:
            if not self.args.indata:
                parser.error('--indata required')
            if not os.path.exists(self.args.indata):
                raise ConfigError("{} does not exist".format(
                    self.args.indata
                ))
            self._config.read(self.args.indata)

        try:
            # set logging level
            Logger.setLevel(self._config.get('Other', 'logging'))
            # sys.stderr logging
            self._add_logging_handler(
                logging.StreamHandler(stream=sys.stderr)
            )

            # must be defined for _cleanup() method
            Globals.outdir = self._config.get('Other', 'outdir')
        except NoSectionError as e:
            raise ConfigError('Config file {}: {}'.format(
                self.args.indata, e
            ))

        # define storage writter
        self.storage = CmdWritter()

    def load(self, philip, params, obs):
        """Load configuration data.

        Only roff procedure supported.
        """
        if self.args.typecomp == 'roff':
            # cleanup output directory first
            self._cleanup()

            data = self._load_roff(
                self._config.get('Other', 'indata')
            )

            self._set_globals(data)

            #
            #
            #
            #
            # Change vals in globs for optimalization
            #self._adjust_domain_size()
            self._set_philips_to_glob(params)
            self._set_rainfall_to_glob(obs.rainfall)
            self._set_slope_to_glob(obs.slope)
            self._set_optim_params_to_glob(params,obs.slope)
            self._set_total_raster_area()
            self._set_surface_retention(params)
            #
            #
            #
            #
            #
            #
        else:
            raise ProviderError('Unsupported partial computing: {}'.format(
                self._args.typecomp
            ))

    def _set_surface_retention(self,params):
        Globals.mat_reten.fill(params[5])

    def _set_point_loc(self,ii,jj):
        """ set location of point000.dat to the bottom of the plot """
        Globals.array_points[0][1] = jj
        Globals.array_points[0][2] = ii
            
            
    def _set_philips_to_glob(self, params):
        """ read philip paramaters from hidden file """
        ks = params[3]
        s  = params[4]
            
        for l in Globals.combinatIndex:
            l[1] = ks
            l[2] = s
            
    def _set_philips_to_glob_from_file(self, philip):
        """ read philip paramaters from hidden file """
        with open(philip, 'r') as pf:
            lines = pf.readlines()
            s = float(lines[1].replace('\n', ''))
            ks = float(lines[2].replace('\n', ''))

        for l in Globals.combinatIndex:
            l[1] = ks
            l[2] = s

    def _set_rainfall_to_glob(self, rainfall):
        """ change rainfall intensity in globals.sr """
        for l in Globals.sr:
            l[0] = 3600
            l[1] = rainfall

    def _set_slope_to_glob(self,slope):
        """ change surface slope in globals.mat_slope """
        Globals.mat_slope.fill(slope)
        
    def _set_optim_params_to_glob(self,params,slope):
        """ change surface slope in globals.mat_aa a globals.mat_aa """
        X = params[0]
        Y = params[1]
        b = params[2]
        Globals.mat_aa = X*Globals.mat_slope**Y
        Globals.mat_b.fill(b)
        
    def _adjust_domain_size(self):
        """ set domain size to lab rainfal simulator plot """
        GridGlobals.dx =0.9/4.
        GridGlobals.dy =8.0/13.
        GridGlobals.pixel_area =  0.9*8.0
        
    def _set_total_raster_area(self):
        rr = GridGlobals.rr
        rc = GridGlobals.rc
        A = 0.0
        for i in rr :
            for j in rc[i]:
                A += GridGlobals.pixel_area
        GridGlobals.domain_area = A
            

