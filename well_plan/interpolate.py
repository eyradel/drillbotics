"""
Interpolators module

This module provides different kinds of interpolation functions
"""
import numpy as np
from scipy.interpolate import (
    interp1d,
    CubicSpline,
    Rbf,
    LinearNDInterpolator,
    CloughTocher2DInterpolator,
    NearestNDInterpolator,
    Akima1DInterpolator,
    PchipInterpolator,
    InterpolatedUnivariateSpline,
)


class WPInterpolator:
    def __init__(self, x, y, z):
        """
        Initialize the WellProfileInterpolator class with known well profile data.

        Args:
            depths (array-like): Depths of the known well profile data.
            northings (array-like): Corresponding northings at each depth.
            eastings (array-like): Corresponding eastings at each depth.
        """
        self.x = x
        self.y = y
        self.z = z

    def interpolate1D(self, station_delta=10, method='Akima1DInterpolator', *args, **kwargs):
        """
        Perform 1D interpolations to estimate the coordinates at every
        station_delta units deep. default method is the Akima1DInterpolator

        Args:
        -----
            method (interpolating funtion name): Kind of interpolation to do
            station_delta (float): difference between two stations

        Returns:
        --------
            float: Estimated coordinates at every station.

        Available Interpolation funtions:
        ---------------------------------
            - interp1d
            - CubicSpline
            - Rbf, radial basis function
            - Akima1DInterpolator
            - PchipInterpolator
            - InterpolatedUnivariateSpline
        
        """
        z = np.arange(self.z[0], self.z[-1], station_delta)

        interp_func = globals().get(method)
        if interp_func is None:
            raise Exception(f"Invalid interpolation funtion name, '{method}'!")

        x_func = interp_func(self.z, self.x, *args, **kwargs)
        y_func = interp_func(self.z, self.y, *args, **kwargs)
        
        x_coords = x_func(z)
        y_coords = y_func(z)
        
        return x_coords, y_coords, z

    # def interpolateND(self, station_delta=10, method='LinearNDInterpolator', oneD= 'Akima1DInterpolator', *args, **kwargs):
    #     """
    #     Perform multi dimensional interpolations to estimate the coordinates at every
    #     station_depth units deep. default method is the Akima1DImterpolator

    #     Args:
    #     -----
    #         method (interpolating funtion name): Kind of interpolation to do
    #         station_delta (float): difference between two stations

    #     Returns:
    #     --------
    #         float: Estimated coordinates at every station.

    #     Available Interpolation funtions:
    #     ---------------------------------
    #         - LinearNDInterpolator
    #         - CloughTocher2DInterpolator
    #         - NearestNDInterpolator
    #     """
    #     depths = np.arange(self.depths[0], self.depths[-1], station_delta)

    #     interp_func = globals().get(method)
    #     if interp_func is None:
    #         raise Exception(f"Invalid interpolation funtion name, '{method}'!")

    #     # Make 1D interpolation for eastings
    #     eastings, _, _ = self.interpolate1D(method=oneD)

    #     northings_func = interp_func([self.depths, eastings], [self.northings], *args, **kwargs)
        
    #     easting_coords = eastings
    #     northing_coords = northings_func(depths)
        
    #     return easting_coords, northing_coords, depths

