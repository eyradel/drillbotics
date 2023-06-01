import pandas as pd
import numpy as np
from drillstring.select_drill_string import SelectDrillString

drill_strings_data = pd.read_excel("drillstring/drill_strings_api_sheet.xlsx")
drill_strings_data = drill_strings_data[
    ["Nominal Weight (lb/ft)",
    "OD (in)",
    "TUBE ID (in)",
    "Connection",
    "Grade",
    "Range",
    "Wall (in)",
    "Adjusted Weight (lb/ft)",
    "TJ OD (in)",
    "TJ ID (in)",
    "TJ YIELD (ft-lbs)",
    "MUT Min (ft-lbs) ",
    "MUT Max (ft-lbs)",
    "Prem Tube Tensile (lbs)"]
]
# TODO: Investigate removing above reordering
drill_strings_data[
    ["Nominal Weight (lb/ft)", "OD (in)", "TUBE ID (in)"]
] = drill_strings_data[["Nominal Weight (lb/ft)", "OD (in)", "TUBE ID (in)"]].astype(
    "float"
)

well_data = pd.read_csv("planData.csv")
# well_data[['azimuth', 'inclination']] =exit()(
# np.rad2deg(well_data[['azimuth', 'inclination']])

# NOTE: we also have negative torques and drags. NaN strings are removed
string_selection = SelectDrillString(
    friction_co=0.2,
    string_force=324,
    youngs_modulus=30000000,
    inner_mud_weight=15,
    outer_mud_weight=7.3,
    hole_diameter=10,
    internal_fluid_pressure=12800,
    external_fluid_pressure=4790,
    buoyancy_factor=0.8,
    well_data=well_data,
    drill_strings_data=drill_strings_data,
)
x = string_selection.get_optimum()
# print(x)
# print(x.get("Best strings")[0].buckles)
# print(x.get("Best strings")[1].buckles)
# print(x.get("Best strings")[2].buckles)
# print(x.get("Best strings")[3].buckles)
# print(x.get("Best strings")[4].buckles)

# print(x.get("Best strings")[0].pipe_weight)
# print(x.get("Best strings")[0].drags)
# print(x.get("Best strings")[0].torques)

# print(x.get("Best strings")[0].buckles)
# print(x.get("Best strings")[0].drags)

