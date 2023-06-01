import numpy as np

# For now...
E = 30000000*(10**(9))/(0.145*10**6)
I = 5.2
a = 4
b = 3
forces_k = 3 * E * I / (a**2 * b)


def calOffset(
    current_azi, current_incli, target_azi, target_incli, max_offset=1, max_deviation=60
) -> tuple:
    """
    This function calculates the offset inclination and azimuth

    Input
    -----
        - current_az: Azimuth of current possition in degrees
        - current_inc: Inclination of current possition in degrees
        - target_az: Azimuth of target position in degrees
        - target_inc: Inclination of target position in degrees
        - max_offset: Maximum offset in degrees
        - max_deviation: maximun deviation to trigger max_offfset in degrees.

    Output
    ------
        - offset_inc: Offset inclination in degrees
        - offset_az: Offset azimuth in degrees
    """

    max_deviation = np.deg2rad(max_deviation)

    # Calculate deviations in azimuth and inclination
    az_deviation = abs(target_azi - current_azi)
    inc_deviation = abs(target_incli - current_incli)

    # Offset in azimuth should be max_offset if the deviation is greater than
    # max_deviation and a fraction of the max_offset if it's less. This
    # fration is proportional to the diviation. It should be zero if there
    # is no deviation
    abs_azi_offset = 0
    if az_deviation > max_deviation:
        abs_azi_offset = max_offset
    if az_deviation < max_deviation:
        abs_azi_offset = (az_deviation / max_deviation) * max_offset

    # same azimuth offset logic is applied to the inclination offset
    abs_inl_offset = 0
    if inc_deviation > max_deviation:
        abs_inl_offset = max_offset
    if inc_deviation < max_deviation:
        abs_inl_offset = (inc_deviation / max_deviation) * max_offset

    offsetResultantAzAngle = np.arctan2(abs_inl_offset, abs_azi_offset)

    # If all the deviations are below the max_deviation, then the resultant
    # offset is a fractino of the max_offset proportional to the average of
    # the two deviations
    # TODO: Try plain logic later
    resultant_offset = max_offset
    if (az_deviation < max_deviation) and (inc_deviation < max_deviation):
        ave_deviation = (az_deviation + inc_deviation) / 2
        resultant_offset = (ave_deviation / max_deviation) * max_offset

    # Calculate the offset
    offset_az = resultant_offset * np.cos(offsetResultantAzAngle)
    offset_inc = resultant_offset * np.sin(offsetResultantAzAngle)

    # Change signs of az and incl offsets if target values are greater
    offset_az = offset_az if target_azi > current_azi else -offset_az
    offset_inc = offset_inc if target_incli > current_incli else -offset_inc

    return offset_inc, offset_az


def calIncliAziNatDis(current_az, current_incli, target_az, target_incli):
    incli_nat_disp = np.cos(target_incli - current_incli) * 10
    az_nat_disp = np.cos(target_az - current_az) * 10

    return incli_nat_disp, az_nat_disp


def getDiplacementPoints(x, y, z):
    """
    Finds the offset point and it's original points which constitutes
    the displacement
    
    Inputs
    ------
        x: x coordinates
        y: y coordinates
        z: z coordinates
    
    Output
    ------
        A dictionary of:
            offset point: (x, y, z)
            orignal point: (x, y, z)
    """

    bit_point = (x[-1], y[-1], z[-1])
    


def calHDisplacement():
    pass


def _offset_Force(offset_disp):
    """
    Calculates the force caused by the RSS Actuator either in inclination or
    azimuth

    Inputs
    ------
        - offset_disp: Offset displacement either inclination or azimuth

    Output
    ------
        Force caused by the RSS Actuator
    """

    return offset_disp * forces_k


def _natDisp_Force(nat_disp):
    """
    Calculates the force caused by the natural displacement due to RSS bending
    either in inclination or azimuth

    Inputs
    ------
        - nat_disp: Natural displacement either inclination or azimuth

    Output
    ------
        Force causing natural displacement due to RSS
    """

    return nat_disp * forces_k


def calBitForce(offset_disp, nat_disp):
    """
    Calculates the total force on the bit causing either inclination or azimuth

    Inputs
    ------
        - offset_disp: Offset displacement either inclination or azimuth
        - nat_disp: Natural displacement either inclination or azimuth

    Output
    ------
        Total force on bit
    """

    return _offset_Force(offset_disp) + _natDisp_Force(nat_disp)


def calROPAxial(friction_co, bit_diameter, wellbore_area, rock_speEne, rot_speed, wob):
    """
    Calculates the axial rate of penetration

    Inputs
    ------
        - friction_co: Friction Coefficient
        - bit_diameter: Diameter of the bit
        - wellbore_are: Wellbore area
        - rock_speEne: Rock specific energy
        - rot_speed: Rotating speed of the drill string
        - wob: Weight on bit

    Output
    ------
        Axial rate of penetration
    """

    numerator = 13.33 * friction_co * rot_speed
    denominator = bit_diameter * ((rock_speEne / wob) - (1 / wellbore_area))
    return numerator / denominator


def calNonAxialROP(
    friction_co,
    rot_speed,
    bit_diameter,
    rock_speEne,
    bit_force,
    wellbore_area,
    model_para,
    calib_func,
):
    """
    Calculates the non-axial rate of penetration. The kind calculate depends on
    the model parameters. Eg. if the model_parameter and bit_force are on the
    azimuth, then the it calculates *ROP azimuth*

    Calcualtes:
        - ROP Azimuth
        - ROP Inclination
        - ROP Normal

    Inputs
    ------
        - friction_co: Friction Coefficient
        - rot_speed: Rotating speed of the drill string
        - bit_diameter: Diameter of the bit
        - rock_speEne: Rock specific energy
        - bit_force: Force on the bit
        - wellbore_area: Wellbore area
        - model_para: Model parameter
        - cal_func: `calibrating function`

    Output
    ------
        Rate of penetration
    """

    numerator = friction_co * rot_speed * calib_func(model_para)
    denominator = bit_diameter * ((rock_speEne / bit_force) - (1 / wellbore_area))
    return numerator / denominator


def calWellPathData(ROP_axial, ROP_incl, ROP_azi, delta_t, pre_incli, pre_az) -> dict:
    """
    Calculates the well path parameters
    Inputs
    ------
        - ROP_axial: Axial Rate of Penetration
        - ROP_incl: Inclination Rate of Penetration
        - ROP_az: Azimuth Rate of Penetration
        - delta_t: Sampling time interval
        - pre_incli: Previous inclination
        - pre_az: previous azimuth

    Output
    ------
        A dictionary of the well path parameters with the following mapping:
        - inclination -> inclination
        - azimuth -> Azimuth
        - DLS -> Dodge leg sevierity
        - delta_measured_depth -> Change in measured depth
        - delta_north -> change in north
        - delta_east -> change in east


        - measured depth -> Measured Depth

    """

    incli = np.arctan2(ROP_incl, ROP_axial) * delta_t
    delta_az = np.arctan2(ROP_azi, ROP_axial) * delta_t
    az = pre_az + delta_az
    delta_md = np.sqrt(ROP_incl**2 + ROP_azi**2 + ROP_axial**2) * delta_t
    DLS = (
        180
        * np.arccos(
            np.cos(incli) * np.cos(pre_incli)
            + np.sin(incli) * np.sin(pre_incli) * np.cos(delta_az)
        )
    ) / (np.pi * delta_md)

    delta_north = np.cos(az) * np.cos(incli) * delta_md
    delta_east = np.sin(az) * np.cos(incli) * delta_md
    delta_tvd = delta_md * np.cos(incli) * delta_t

    # print("Iclination", incli)
    # print("Azimuth", az)
    # print("DLS", DLS)
    # print("delta_MD", delta_md)
    # print("Delta North", delta_north)
    # print("Delta East", delta_east)

    params = {
        "inclination": np.array([incli]),
        "azimuth": np.array([az]),
        "DLS": np.array([DLS]),
        "delta_MD": np.array([delta_md]),
        "delta_north": np.array([delta_north]),
        "delta_east": np.array([delta_east]),
        "delta_tvd": np.array([delta_tvd]),
    }

    return params
