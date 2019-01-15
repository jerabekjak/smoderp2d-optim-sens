#!/usr/bin/env python

"""
Resolves some input variables and start the computing

The computing itself is performed in src.runoff


.. todo::
 - main.py by se asi podle konvenci mel jmenovat smodepr.py
 - mal by tam byl setup.py
"""

import os
from model.smoderp2d.providers.cmd import CmdProvider

def run():
    # initialize provider
    provider = CmdProvider()

    # print logo
    provider.logo()

    # load configuration (set global variables)
    provider.load()

    # must be called after initialization
    from model.smoderp2d.runoff import Runoff
    
    # the computation
    runoff = Runoff(provider)
    runoff.run()

if __name__ == "__main__":
    run()
