import sys
import argparse
if sys.version_info > (3, 0):
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

from model.smoderp2d.core.general import Globals, GridGlobals
from model.smoderp2d.providers.base import BaseProvider, Logger
from argparse import Namespace


class CmdProvider(BaseProvider):
    def __init__(self, indata_path):
        """Create argument parser."""
        super(CmdProvider, self).__init__()

        # create parser "by hard"
        self._args = Namespace(indata=indata_path, typecomp='roff')

        # load configuration
        self._config = ConfigParser()
        if self._args.typecomp == 'roff':
            if not self._args.indata:
                parser.error('--indata required')
            self._config.read(self._args.indata)

        # set logging level
        Logger.setLevel(self._config.get('Other', 'logging'))

        # must be defined for _cleanup() method
        Globals.outdir = self._config.get('Other', 'outdir')

    def load(self, philip, params, obs):
        """Load configuration data.

        Only roff procedure supported.
        """
        if self._args.typecomp == 'roff':
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
            self._set_philips_to_glob(philip)
            self._set_rainfall_to_glob(obs.rainfall)
            self._set_slope_to_glob(obs.slope)
            self._set_optim_params_to_glob(params,obs.slope)
            self._set_total_raster_area()
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

    def _set_philips_to_glob(self, philip):
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

    def _set_total_raster_area(self):
        rr = GridGlobals.rr
        rc = GridGlobals.rc
        A = 0.0
        for i in rr :
            for j in rc[i]:
                A += GridGlobals.pixel_area
        GridGlobals.domain_area = A
            

