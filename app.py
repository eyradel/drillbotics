import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_toggle as tog

import pandas as pd
import numpy as np
import plotly.graph_objects as go

from drillmodules.well_plan.well import InterpWell


if "ENTERED_DATA" not in st.session_state:
    st.session_state.ENTERED_DATA = False
if "gen_well" not in st.session_state:
    st.session_state.gen_well = InterpWell()

session_state = st.session_state
# session_state.cache = True


def simu():
    dac = pd.read_csv(r"C:\Users\eyram\Desktop\uisData.csv")

    well_inputs_trace = go.Scatter3d(
        x=dac["east"],
        y=dac["north"],
        z=dac["tvd"],
        mode="lines",
        line=dict(color="red", width=10),
    )
    layout = go.Layout(
        scene=dict(
            xaxis=dict(title="Eastings"),
            yaxis=dict(title="Northings"),
            zaxis=dict(title="TVD", autorange="reversed"),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
    )

    fig = go.Figure(data=[well_inputs_trace], layout=layout)
    with st.container():
        st.plotly_chart(fig, use_container_width=True)


def simulation():
    col1, col2 = st.columns(2)
    with col1:

        def create_speedometer(value, title, unit):
            max_value = 100
            fig = go.Figure(
                go.Indicator(
                    domain={"x": [0, 1], "y": [0, 1]},
                    value=value,
                    mode="gauge+number",
                    title={"text": title},
                    gauge={
                        "axis": {"range": [None, max_value]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [1, max_value * 0.25], "color": "lightgray"},
                            {
                                "range": [max_value * 0.25, max_value * 0.75],
                                "color": "gray",
                            },
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": value,
                        },
                    },
                )
            )
            fig.update_layout(height=300, width=500)
            return fig

        speed_value = st.slider("Speed Value", 0, 100, 50)
        speedometer_chart = create_speedometer(speed_value, "Speed", "km/h")
        st.plotly_chart(speedometer_chart)
    with col2:
        st.slider("Speed", 0, 100, 50)
        spe = create_speedometer(speed_value, "Speed", "km/h")
        st.plotly_chart(spe)

    labels = ["Label 1", "Label 2", "Label 3", "Label 4"]
    values = [10, 30, 20, 40]

    x = ["A", "B", "C", "D"]
    y = [10, 8, 12, 6]

    # Create line chart
    line_chart = go.Scatter(x=x, y=y, mode="lines+markers")

    # Layout configuration
    layout = go.Layout(title="Simple Line Chart")

    # Create Figure object
    fig = go.Figure(data=[line_chart], layout=layout)

    st.plotly_chart(fig)


def well_inputs():
    well = st.session_state.gen_well
    start_coord = []
    target_coord = []
    formation_aggr = []
    cl1, _ = st.sidebar.columns(2)

    with cl1:
        option = tog.st_toggle_switch(
            label="KeyInput/FileInput",
            key="targets_coords_input_type",
            default_value=False,
            label_after=False,
            inactive_color="red",
            active_color="#11567f",
            track_color="#29B5E8",
        )
    if option:
        Target = st.sidebar.file_uploader("Upload Target Data", ["csv", "excel"])
        Formation = st.sidebar.file_uploader("Upload Formation Data", ["csv", "excel"])

        if Target is not None:
            try:
                data = pd.read_csv(Target)

            except:
                data = pd.read_excel(Target)

            cols = st.sidebar.selectbox("select", data.columns)
            chk = st.sidebar.checkbox("show/hide")

            if chk:
                mul = st.sidebar.multiselect("select coordinates", data[cols])
                # st.text(mul[0])
            else:
                st.sidebar.text("Agigon")
    else:
        st.sidebar.subheader("Start Coordinates")
        start_coord = st.sidebar.text_input(
            "Enter Start Coordinates(X,Y,Z)",
            f"{well.surface_coordinates[0]},{well.surface_coordinates[1]},{well.surface_coordinates[2]}",
        ).split(",")

        st.sidebar.markdown(
            '<hr style="border: 1px solid #ccc">', unsafe_allow_html=True
        )

        tr = st.sidebar.number_input(
            "Please enter number of targets", len(well.target_coordinates)
        )
        
        if tr:
            for i in range(int(tr)):
                try:
                    current_tc = well.target_coordinates[i]
                    current_tc = f"{current_tc[0]},{current_tc[1]},{current_tc[2]}"
                except IndexError:
                    current_tc = ""

                t = st.sidebar.text_input(
                    f"Target {i} (X,Y,Z)",
                    current_tc,
                )
                target_coord.append(t.split(","))

                if i == 0:
                    try:
                        first_target_depth = float(t.split(",")[2])
                    except TypeError:
                        first_target_depth = 5

        st.sidebar.text("")

        st.sidebar.subheader("KickOff Point")
        kop = st.sidebar.slider(
            "Leave blank for auto KOP suggestion", 0.0, first_target_depth + 0.000001
        )

        st.sidebar.subheader("Formations")
        st.text("  ")
        tr = st.sidebar.number_input(
            "Please enter number of Formations", len(well.form_aggr)
        )
        if tr:
            for i in range(int(tr)):
                try:
                    current_formation = well.form_aggr[i]
                except IndexError:
                    current_formation = ""

                f = st.sidebar.text_input(
                    f"Formation {i} (Depth,Form_aggr)",
                    f"{current_formation[0]},{current_formation[1]}",
                )
                formation_aggr.append(f.split(","))

        survey_station = st.sidebar.number_input("Survey station", well.station_delta)

        units = st.sidebar.selectbox(
            "Select Units", [well.units, "feet" if well.units == "meters" else "meters"]
        )

        least_form_aggr_kop = st.sidebar.number_input(
            "Least formation hardness for kickoff", well.kop_form_aggr
        )

        interpolators = [
            "PchipInterpolator",
            "Akima1DInterpolator",
            "interp1d",
            "CubicSpline",
            "Rbf",
            "InterpolatedUnivariateSpline",
        ]
        # Make current well interpolator the first in the list
        interpolators[interpolators.index(well.interpolator)] = interpolators[0]
        interpolators[0] = well.interpolator

        interpolator = st.sidebar.selectbox("Choose interpolator", interpolators)

    inputted_data = {
        "start_coord": start_coord,
        "target_coord": target_coord,
        "kop": kop,
        "formation_aggr": formation_aggr,
        "least_form_aggr_kop": least_form_aggr_kop,
        "survey_station": survey_station,
        "units": units,
        "interpolator": interpolator,
    }

    return inputted_data


def validate_float_list(lst, expected_no, listoflist=True):
    try:
        list_check = lst[0] if listoflist else lst

        if len(list_check) == expected_no:
            try:
                array = np.array(lst).astype("float")
                return array
            except ValueError:
                pass

    except IndexError:
        pass
    st.markdown(
        f"<span style='color: red'>Error at {lst}</span>", unsafe_allow_html=True
    )
    return []


def validate_input(inputted_data):
    errors = []

    start_coord = validate_float_list(inputted_data["start_coord"], 3, listoflist=False)
    if len(start_coord) == 0:
        errors.append("Start Coordinates")

    target_coord = validate_float_list(inputted_data["target_coord"], 3)
    if len(target_coord) == 0:
        errors.append("Target Coordinates")

    try:
        kop = float(inputted_data["kop"])
    except:
        errors.append("KickOff Point")

    formation_aggr = validate_float_list(inputted_data["formation_aggr"], 2)
    if len(formation_aggr) == 0:
        errors.append("Formation Aggresiveness")

    try:
        least_form_aggr_kop = float(inputted_data["least_form_aggr_kop"])
    except:
        errors.append("Formation Aggresiveness")

    try:
        survey_station = float(inputted_data["survey_station"])
    except:
        errors.append("Survey Station")

    units = inputted_data["units"]

    interpolator = inputted_data["interpolator"]

    validated_data = {
        "start_coord": start_coord,
        "target_coord": target_coord,
        "kop": kop,
        "formation_aggr": formation_aggr,
        "least_form_aggr_kop": least_form_aggr_kop,
        "survey_station": survey_station,
        "units": units,
        "interpolator": interpolator,
        "errors": errors,
    }

    return validated_data


def setup_well(inputted_data, well):
    validated_input = validate_input(inputted_data)
    errors = validated_input["errors"]

    if len(errors) == 0:
        start_coord = validated_input["start_coord"]
        target_coord = validated_input["target_coord"]
        kop = validated_input["kop"]
        formation_aggr = validated_input["formation_aggr"]
        least_form_aggr_kop = validated_input["least_form_aggr_kop"]
        survey_station = validated_input["survey_station"]
        units = validated_input["units"]
        interpolator = validated_input["interpolator"]

        st.subheader("Well Path")

        well.interpolator = interpolator
        well.kop = kop
        well.surface_coordinates = start_coord
        well.target_coordinates = target_coord
        well.kop_form_aggr = least_form_aggr_kop
        well.units = units
        well.station_delta = survey_station
        well.form_aggr = formation_aggr

        if kop == 0:
            well.suggest_kop()

    return well, errors


def disp_plan(well_coords, targets_coords):
    # 2D
    with st.expander("View 2D Graph"):
        n = (well_coords["Y"]) ** 2
        e = (well_coords["X"]) ** 2
        hd = np.sqrt(n + e)

        tn = (targets_coords["Y"]) ** 2
        te = (targets_coords["X"]) ** 2
        thd = np.sqrt(tn + te)

        well_2d_trace = go.Scatter(
            x=hd,
            y=well_coords["Z"],
            mode="lines",
            name="Well Path",
            line=dict(color="blue"),
        )
        targets_2d_trace = go.Scatter(
            x=thd,
            y=targets_coords["Z"],
            mode="markers",
            marker=dict(size=10, color="red"),
            name="Targets",
        )

        layout2d = go.Layout(
            xaxis=dict(title="Horizontal Displacement"),
            yaxis=dict(title="TVD", autorange="reversed"),
            margin=dict(l=0, r=0, b=0, t=0),
        )
        fig2d = go.Figure(data=[well_2d_trace, targets_2d_trace], layout=layout2d)

        st.plotly_chart(fig2d)

    # 3D
    well_3d_trace = go.Scatter3d(
        x=well_coords["X"],
        y=well_coords["Y"],
        z=well_coords["Z"],
        mode="lines",
        line=dict(color="blue", width=10),
        name="Well Path",
    )
    targets_3d_trace = go.Scatter3d(
        x=targets_coords["X"],
        y=targets_coords["Y"],
        z=targets_coords["Z"],
        mode="markers",
        marker=dict(size=10, color="red"),
        name="Targets",
    )

    layout3d = go.Layout(
        scene=dict(
            xaxis=dict(title="Eastings"),
            yaxis=dict(title="Northings"),
            zaxis=dict(title="TVD", autorange="reversed"),
        ),
        scene_camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=0.7, y=2, z=0.7),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
    )
    fig3d = go.Figure(data=[well_3d_trace, targets_3d_trace], layout=layout3d)

    with st.container():
        st.subheader("Three Dimensional[3D]")
        st.plotly_chart(fig3d, use_container_width=True)

    with st.expander("View 2D Graph"):
        st.dataframe(well_coords)


st.markdown(
    '<link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.19.1/css/mdb.min.css" rel="stylesheet">',
    unsafe_allow_html=True,
)
st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
st.markdown("""""", unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
    
                header{visibility:hidden;}
                .main {
                    margin-top: -120px;
                    padding-top:10px;
                }
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}

            </style>
            
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: green;">
    <a class="navbar-brand" href="#"  target="_blank"> [ <0> ]   SPE Drillbotics</a>  
    </nav>
""",
    unsafe_allow_html=True,
)


def streamlit_menu():
    selected = option_menu(
        menu_title=None,  # required
        options=["Well Plan", "Drill String", "Simulation"],  # required
        icons=["house", "pencil", "play"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
    )
    
    return selected

selected = streamlit_menu()

if selected == "Well Plan":
    inputted_data = well_inputs()

    if st.sidebar.button("Run"):
        st.session_state.ENTERED_DATA = True
    
    if st.sidebar.button("Reset"):
        st.session_state.gen_well = InterpWell()

    if st.session_state.ENTERED_DATA:
        gen_well, errors = setup_well(inputted_data, st.session_state.gen_well)
        if len(errors) > 0:
            for error in errors:
                st.header(f"Invalid format for {error}!]")
        else:
            disp_plan(gen_well.output_data[0], gen_well.output_data[1])
    else:
        st.header("Enter well data in the side bar and click run")

if selected == "Simulation":
    simu()
    simulation()
