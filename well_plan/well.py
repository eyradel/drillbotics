"""
Well module

This module contains the class that defines a well
"""
import numpy as np
import pandas as pd
from .well_data import get_well_data


class InterpWell:
    """
    Generates well profile data using interpolation

    Attributes:
    -----------
        - surface_coordinates [x, y, z] (list)
        - target_coordinates [[x, y, z] for each target] (list of list)
        - station_delta = 10
        - interpolator = "Akima1DInterpolator"
        - units = "meters"
        - min_kop = 600
        - kop = 0
        - kop_form_aggr = 0.6 (Suitable formation aggresiveness for kickoff)
        - interp_args = {} Extra kwargs for the interpolator choosen

    Interpolator Choices
    --------------------
        - interp1d
        - CubicSpline
        - Rbf (radial basis function)
        - Akima1DInterpolator
        - PchipInterpolator
        - InterpolatedUnivariateSpline
    """
    ### - LinearNDInterpolator
    ### - CloughTocher2DInterpolator
    ### - NearestNDInterpolator

    def __init__(self):
        """Initializes a default well"""
        self.surface_coordinates = [0, 0, 0]
        self.target_coordinates = [
            [0, 0, 0],
        ]
        self.station_delta = 10
        self.interpolator = "PchipInterpolator"
        self.units = "meters"
        self.min_kop = 300
        self.kop = 0
        self.kop_form_aggr = 0.6  # Suitable formation aggresiveness for kickoff
        self.interp_args = {}

        # Parse inputs
        self.parse_input()

    def parse_input(self, targets_file=None, form_aggr_file=None):
        """
        Parses the input to set the right well parameter
        Inputs:
        -------
            Input files

        Return:
        -------
            None
        """
        # For now, hard code target coordinates TODO
        # self.target_coordinates = np.array(
        #     [
        #         [238.21, 137.53, 1164.06],
        #         [337.47, 194.84, 1223.73],
        #         [759.59, 438.55, 1327.21],
        #         [1284.59, 741.66, 1677.21],
        #     ]
        # )

        # Change surface coordinates to np array
        # self.surface_coordinates = np.array(self.surface_coordinates)

        # Determines the appropriate kop given the formation aggresiveness
        # self.form_aggre = [
        #     [0, 0.5],
        #     [150, 0.6],
        #     [400, 0.5],
        #     [900, 0.8],
        #     [980, 0.5],
        #     [1100, 0.6],
        #     [1200, 0.4],
        #     [1320, 0.2],
        #     [1450, 0.6],
        #     [1530, 0.5],
        # ]  # For now, hard code TODO
        for station in self.form_aggre[:]:
            if station[0] >= self.min_kop and station[1] >= self.kop_form_aggr:
                self.kop = station[0]
                break

    @property
    def output_data(self):
        """
        Returns a turple of well data and targets coordinates

        Well data columns
        -----------------
        X: Well X
        Y: Well Y
        Z: Well Z
        Azimuth[rad]: Azimuth in radians
        Inclination[rad]: Inclination in radians
        MD: Measured depth

        Targets Coordinates
        -------------------
        X: Targets X
        Y: Targets Y
        Z: Targets Z
        """
        _well_data = get_well_data(
            surface_coords=self.surface_coordinates,
            tvd_kop=self.kop,
            target_coords=self.target_coordinates,
            station_delta=self.station_delta,
            method=self.interpolator,
            **self.interp_args
        )
        well_data = _well_data[0] if self.units == "meters" else _well_data[1]
        targets_data = pd.DataFrame(
            self.target_coordinates, columns=["X", "Y", "Z"]
        )

        return well_data, targets_data
