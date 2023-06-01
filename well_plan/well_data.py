"""
Well data Module
----------------

This module contains functions for generating the well data
"""
import pandas as pd
import numpy as np
from .interpolate import WPInterpolator


def calAzimuthInc(x, y, z) -> dict:
    """
    Calculates the azimuth and inlination along a well

    Inputs:
    -------
        x: x coordinates of well
        y: y coordinates of well
        z: z coordinates of well

    Output:
    -------
        A dictionary of the azimuth and inclination in rad
        result['azimuth'] = np array
        result['inclination'] = np array
    """

    inclination = np.arctan2(np.sqrt(y**2 + x**2), z)
    azimuth = np.arctan2(x, y)

    return {"azimuth": azimuth, "inclination": inclination}


def calMeasuredDepths(x, y, z):
    """
    Calculates the measured depths from the eastings, northings and depths
    
    Inputs:
    -------
        x: x coordinates of well
        y: y coordinates of well
        z: z coordinates of well
    
    Output:
    -------
        An np array of the measured depth at every station of the coordinates
    """
    measured_depths = np.sqrt(y**2 + x**2 + z**2)

    return measured_depths


def get_well_data(
    surface_coords,
    tvd_kop,
    target_coords,
    station_delta=10,
    method="Akima1DInterpolator",
    *args,
    **kwargs
):
    """
    Computes well data

    Inputs:
    -------
        surface_coords:  Surface coodinates as an np arr[x, y, z]
        target_coords: Target coodinates as an np arr[[x, y, z] for each target]
        tvd_kop: Depth to kick off point
        Input oneD interpolator in kwargs if the interpolation is 3D, the default
        is Akima

    Output:
    -------
        Two Pd data frames in meters and feet each with eastings, northings, depths,
        inclination(rad) and azimuth (rad)
    """
    surface_x, surface_y, surface_z = surface_coords
    kop_x, kop_y, kop_z = (
        surface_x,
        surface_y,
        tvd_kop,
    )
    targets_x = target_coords[:, 0]
    targets_y = target_coords[:, 1]
    targets_z = target_coords[:, 2]

    # Interpolation starts at kop to last target.
    x = np.insert(targets_x, 0, kop_x)
    y = np.insert(targets_y, 0, kop_y)
    z = np.insert(targets_z, 0, kop_z)

    interpolator = WPInterpolator(x, y, z)

    interp_coords = interpolator.interpolate1D(
        station_delta=station_delta, method=method, *args, **kwargs
    )  # Interpolated coordinates

    final_x, final_y, final_z = interp_coords

    # Add the vertical point section's coordinates
    # For depths, it's just increasing by 10; eastings and northings, it's
    # maintaing surface values
    surface_to_kop_z_coords = np.arange(surface_z, kop_z, station_delta)
    final_z = np.concatenate((surface_to_kop_z_coords, final_z))
    final_x = np.concatenate(
        (np.full((len(surface_to_kop_z_coords),), surface_x), final_x)
    )
    final_y = np.concatenate(
        (np.full((len(surface_to_kop_z_coords),), surface_y), final_y)
    )

    incliazimuth_dict = calAzimuthInc(final_x, final_y, final_z)
    measured_depths = calMeasuredDepths(final_x, final_y, final_z)

    well_data = {
        "X": final_x,
        "Y": final_y,
        "Z": final_z,
        "Azimuth[rad]": incliazimuth_dict["azimuth"],
        "Inclination[rad]": incliazimuth_dict["inclination"],
        "MD": measured_depths
    }

    well_data_in_meters = pd.DataFrame(well_data)

    well_data_in_feet = well_data_in_meters.copy()
    well_data_in_feet["X"] = well_data_in_feet["X"].apply(
        lambda x: x * 3.28084
    )
    well_data_in_feet["Y"] = well_data_in_feet["Y"].apply(
        lambda x: x * 3.28084
    )
    well_data_in_feet["Z"] = well_data_in_feet["Z"].apply(
        lambda x: x * 3.28084
    )

    return well_data_in_meters, well_data_in_feet
