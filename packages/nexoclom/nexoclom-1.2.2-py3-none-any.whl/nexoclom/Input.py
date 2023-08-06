"""Read the model inputs from a file and create the Input object.

The Input object is build from smaller objects defining different model
options.

Geometry
    Defines the Solar System geometry for the Input.

StickingInfo
    Defines the surface interactions.

Forces
    Set which forces act on model particles.

SpatialDist
    Define the initial spatial distribution of particles.

SpeedDist
    Define the initial speed distribution of particles.

AngularDist
    Define the initial angular distribtuion of particles.

Options
    Configure other model parameters
"""
import os
import os.path

import pandas as pd
from astropy.io import ascii

from .configure_model import configfile
from .database_connect import database_connect
from .input_classes import (Geometry, StickingInfo, Forces, SpatialDist,
                            SpeedDist, AngularDist, Options)
from .modeldriver import modeldriver
from .produce_image import ModelImage


class Input():
    def __init__(self, infile):
        """Read the input options from a file.

        **Parameters**
        infile
            Plain text file containing model input parameters.

        **Class Attributes**

        * geometry
        * sticking_info
        * forces
        * spatialdist
        * speeddist
        * angulardist
        * options

        **Class Methods**

        * findpackets()
        * run(npackets, overwrite=False, compress=True)
        * produce_image(format_, filenames=None)
        """
        # Read the configuration file
        self._savepath = configfile()

        # Read in the input file:
        self._inputfile = infile
        if os.path.isfile(infile):
            data = ascii.read(infile, delimiter='=', comment=';',
                              data_start=0, names=['Param', 'Value'])
        else:
            assert 0, 'Input file {} does not exist.'.format(infile)

        section = [d.split('.')[0].casefold() for d in data['Param']]
        param = [d.split('.')[1].casefold() for d in data['Param']]
        values = [v.split(';')[0].strip().casefold()
                  if ';' in v else v.casefold() for v in data['Value']]

        # Extract the geometry parameters
        gparam = {b:c for (a,b,c) in zip(section, param, values)
                  if a == 'geometry'}
        self.geometry = Geometry(gparam)

        # Extract the sticking information
        sparam = {b:c for a,b,c in zip(section, param, values)
                  if a == 'sticking_info'}
        self.sticking_info = StickingInfo(sparam)

        # Extract the forces
        fparam = {b:c for a,b,c in zip(section, param, values)
                  if a == 'forces'}
        self.forces = Forces(fparam)

        # Extract the spatial distribution
        sparam = {b:c for a,b,c in zip(section, param, values)
                  if a == 'spatialdist'}
        self.spatialdist = SpatialDist(sparam)

        # Extract the speed distribution
        sparam = {b:c for a,b,c in zip(section, param, values)
                  if a == 'speeddist'}
        self.speeddist = SpeedDist(sparam)

        # Extract the angular distribution
        aparam = {b:c for a,b,c in zip(section, param, values)
                  if a == 'angulardist'}
        self.angulardist = AngularDist(aparam, self.spatialdist)

        # Extract the options
        oparam = {b:c for a,b,c in zip(section, param, values)
                  if a == 'options'}
        self.options = Options(oparam, self.geometry.planet)
        
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = (self.geometry.__str__() + '\n' +
                  self.sticking_info.__str__() + '\n' +
                  self.forces.__str__() + '\n' +
                  self.spatialdist.__str__() + '\n' +
                  self.speeddist.__str__() + '\n' +
                  self.angulardist.__str__() + '\n' +
                  self.options.__str__())
        
        return result

    def findpackets(self):
        """ Search the database for identical inputs """
        georesult = self.geometry.search(startlist=None)
        if georesult is not None:
            stickresult = self.sticking_info.search(startlist=georesult)
        else:
            return [], 0, 0

        if stickresult is not None:
            forceresult = self.forces.search(startlist=stickresult)
        else:
            return [], 0, 0

        if forceresult is not None:
            spatresult = self.spatialdist.search(startlist=forceresult)
        else:
            return [], 0, 0

        if spatresult is not None:
            spdresult = self.speeddist.search(startlist=spatresult)
        else:
            return [], 0, 0

        if spdresult is not None:
            angresult = self.angulardist.search(startlist=spdresult)
        else:
            return [], 0, 0

        if angresult is not None:
            finalresult = self.options.search(startlist=angresult)
        else:
            return [], 0, 0

        if finalresult is not None:
            result_ = [str(s) for s in finalresult]
            resultstr = f"({', '.join(result_)})"
            with database_connect() as con:
                result = pd.read_sql(
                    f'''SELECT filename, npackets, totalsource
                        FROM outputfile
                        WHERE idnum in {resultstr}''', con)
            npackets = result.npackets.sum()
            totalsource = result.totalsource.sum()

            return result.filename.to_list(), npackets, totalsource
        else:
            return [], 0, 0

    def run(self, npackets, packs_per_it=None, overwrite=False, compress=True):
        modeldriver(self, npackets, packs_per_it=packs_per_it,
                    overwrite=overwrite, compress=compress)

    def produce_image(self, format_, filenames=None):
        return ModelImage(self, format_, filenames=filenames)
