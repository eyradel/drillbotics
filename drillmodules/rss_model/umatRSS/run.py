from utilities import *
import pandas as pd

max_offset = 1

target_coordinates = np.array(
            [
                [238.21, 137.53, 1164.06],
                [337.47, 194.84, 1223.73],
                [759.59, 438.55, 1327.21],
                [1284.59, 741.66, 1677.21],
            ]
        )
east = target_coordinates[:,0]
north = target_coordinates[:,1]
depth = target_coordinates[:,2]

inclination = np.arctan2(depth, np.sqrt(east**2 + north**2))
azimuth = np.arctan2(east, north)

# #First target points
# T1Azi = azimuth[0]
# T1Incli = inclination[0]
# T1depth = 1164.06
# T1MD = 1196

# #Second target points
# T2Azi = azimuth[1]
# T1Incli = inclination[1]
# T2depth = 1223.73
# T2MD = 1279.5

# #Third target points
# T3Azi = azimuth[2]
# T3Incli = inclination[2]
# T3depth = 1327.21
# T3MD = 1589.1

# #Fourth target points
# T4Azi = azimuth[3]
# T4Incli = inclination[3]
# T4depth = 1677.21
# T4MD = 2240.1

delta_t = 5/3600  # :NOTE

final_data = {
    "inclination": np.array([0]),
    "azimuth": np.array([0]),
    "DLS": np.array([0]),
    "MD": np.array([0]),
    "northings": np.array([0]),
    "eastings": np.array([0]),
    "tvd": np.array([0])
}


def getTargetAzIncli(tvd):
    target_azi, target_incli = azimuth[-1], inclination[-1]
    # print('.', end='')
    for idx, d in enumerate(depth):
        if d > tvd:
            target_azi = azimuth[idx]
            target_incli = inclination[idx]
            # print("broke")
            break

    return target_azi, target_incli


def getCurrentAzIncli():
    cur_az = final_data["azimuth"][-1]
    cur_incli = final_data["inclination"][-1]
    # Calculate current azimuth and Inclination

    # print(cur_az, cur_incli)
    return cur_az, cur_incli


while final_data["tvd"][-1] < depth[-1]:
    print(final_data["eastings"][-1], final_data["northings"][-1], final_data["tvd"][-1])
    current_azi, current_incli = getCurrentAzIncli()
    target_azi, target_incli = getTargetAzIncli(final_data["tvd"][-1])

    offset_incli, offset_az = calOffset(
        current_azi=current_azi,
        current_incli=current_incli,
        target_azi=target_azi,
        target_incli=target_incli,
        max_offset=max_offset,
        max_deviation=40
    )

    incli_nat_disp, az_nat_disp = calIncliAziNatDis(
        current_azi, current_incli, target_azi, target_incli
    )

    incli_bit_force = calBitForce(offset_incli, incli_nat_disp)
    az_bit_force = calBitForce(offset_az, az_nat_disp)

    friction_coefficient = 0.25
    bit_diameter = 12.25
    wellbore_area = np.pi * bit_diameter**2 / 4
    rock_specific_eneregy = 14633.401276
    rotary_speed = 143.44375
    wob = 7.124417

    rop_axial = calROPAxial(
        friction_co=friction_coefficient,
        bit_diameter=bit_diameter,
        wellbore_area=wellbore_area,
        rock_speEne=rock_specific_eneregy,
        rot_speed=rotary_speed,
        wob=wob,
    )

    az_model_para = 0.6  # NOTE:...
    incli_model_para = 0.7  # NOTE:...
    calibration_func = lambda x: x * 0.43  # NOTE: ...

    rop_incli = calNonAxialROP(
        bit_force=az_bit_force,
        friction_co=friction_coefficient,
        bit_diameter=bit_diameter,
        wellbore_area=wellbore_area,
        rock_speEne=rock_specific_eneregy,
        rot_speed=rotary_speed,
        model_para=incli_model_para,
        calib_func=calibration_func,
    )

    rop_az = calNonAxialROP(
        bit_force=incli_bit_force,
        friction_co=friction_coefficient,
        bit_diameter=bit_diameter,
        wellbore_area=wellbore_area,
        rock_speEne=rock_specific_eneregy,
        rot_speed=rotary_speed,
        model_para=az_model_para,
        calib_func=calibration_func,
    )

    previous_incli = final_data["inclination"][-1]
    previous_az = final_data["azimuth"][-1]

    well_data = calWellPathData(
        ROP_incl=rop_incli,
        ROP_azi=rop_az,
        ROP_axial=rop_axial,
        delta_t=delta_t,
        pre_incli=previous_incli,
        pre_az=previous_az,
    )

    final_data["azimuth"] = np.concatenate(
        (final_data["azimuth"], well_data["azimuth"]), axis=0
    )
    final_data["inclination"] = np.concatenate(
        (final_data["inclination"], well_data["inclination"]), axis=0
    )
    final_data["DLS"] = np.concatenate(
        (final_data["DLS"], well_data["DLS"]), axis=0
    )
    final_data["MD"] = np.concatenate(
        (final_data["MD"], well_data["delta_MD"] + final_data["MD"][-1]), axis=0
    )
    final_data["northings"] = np.concatenate(
        (final_data["northings"], well_data["delta_north"] + final_data["northings"][-1]), axis=0
    )
    final_data["eastings"] = np.concatenate(
        (final_data["eastings"], well_data["delta_east"] + final_data["eastings"][-1]), axis=0
    )
    final_data["tvd"] = np.concatenate(
        (final_data["tvd"], well_data["delta_tvd"] + final_data["tvd"][-1]), axis=0
    )
    # print(well_data["delta_MD"])
    # print(well_data["delta_north"])
    # print(well_data["delta_east"])

data = pd.DataFrame(
    final_data, columns=["inclination", "azimuth", "DLS", "MD", "northings", "eastings", "tvd"]
)
data.to_csv("umatData.csv")
