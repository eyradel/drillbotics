import streamlit as st
from streamlit_option_menu import option_menu
import  streamlit_toggle as tog
from streamlit_card import card
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pio
import plotly.express as px
df = pd.read_csv(r"C:\Users\eyram\Downloads\planData.csv")
session_state = st.session_state
session_state.cache = False
#functions
def simu():
    dac = pd.read_csv(r"C:\Users\eyram\Desktop\uisData.csv")
    

    well_trace = go.Scatter3d(
                x=dac["east"],
                y=dac["north"],
                z=dac["tvd"],
                mode='lines',
                line=dict(
                    color='red',
                    width=10               )
            )
    # target_trace = go.Scatter3d(
    #             x=df["Eastings"],
    #             y=df["Northings"],
    #             z=df["TVD"],
    #             mode='markers',
    #             markers=dict(
    #                 color='blue',
    #                 width=10               )
    #         )
    layout = go.Layout(
                scene=dict(
                    xaxis=dict(title='Eastings'),
                    yaxis=dict(title='Northings'),
                    zaxis=dict(title='TVD', autorange='reversed')
                ),
                margin=dict(l=0, r=0, b=0, t=0)
            )

            
   
    fig = go.Figure(data=[well_trace], layout=layout)
    with st.container():            
        st.plotly_chart(fig, use_container_width=True)
def simulation():
        col1,col2,col3 = st.columns(3)
        with col1:
            def create_speedometer(value, title, unit):
                max_value = 100
                fig = go.Figure(go.Indicator(
                    domain={'x': [0, 1], 'y': [0, 1]},
                    value=value,
                    mode="gauge+number",
                    title={'text': title},
                    gauge={'axis': {'range': [None, max_value]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [1, max_value * 0.25], 'color': "lightgray"},
                            {'range': [max_value * 0.25, max_value * 0.75], 'color': "gray"}],
                        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': value}}
                ))
                fig.update_layout(height=300, width=500)
                return fig

           
            
            speed_value = st.slider("Speed Value", 0, 100, 50)
            speedometer_chart = create_speedometer(speed_value, "Speed", "km/h")
            st.plotly_chart(speedometer_chart)
        with col2:
            st.slider("Speed", 0, 100, 50)
            spe = create_speedometer(speed_value, "Speed", "km/h")
            st.plotly_chart(spe)
        with col3:
            st.slider("Sped", 0, 100, 50)
            sp = create_speedometer(speed_value, "Speed", "km/h")
            st.plotly_chart(sp)
        labels = ['Label 1', 'Label 2', 'Label 3', 'Label 4']
        values = [10, 30, 20, 40]

        x = ['A', 'B', 'C', 'D']
        y = [10, 8, 12, 6]

        # Create line chart
        line_chart = go.Scatter(x=x, y=y, mode='lines+markers')

        # Layout configuration
        layout = go.Layout(title="Simple Line Chart")

        # Create Figure object
        fig = go.Figure(data=[line_chart], layout=layout)

        st.plotly_chart(fig)
def graph():
    
    # c,l = st.columns([1, adjust]) 
    # with c:
    #     card2 = hasClicked = card(
    #         title=" ",
    #         text="",
    #         image="https://scx2.b-cdn.net/gfx/news/2018/smartmudtosm.jpg",
    #         url="https://github.com/gamcoh/st-card"
    #         )
    # with l:
    daf = pd.read_csv(r"C:\Users\eyram\Downloads\planData.csv")
    tvd = (daf['TVD'])
    N = (daf['Northings'])**2
    E = (daf['Eastings'])**2
    HD = (np.sqrt(N+E))
    pl = st.checkbox("2D")
    if pl:
            # Create the plot
        figure = px.line(daf, x=HD, y=tvd)

            
        figure.update_layout(yaxis=dict(autorange="reversed"))
    
        st.plotly_chart(figure)
            

    well_trace = go.Scatter3d(
                x=df["Eastings"],
                y=df["Northings"],
                z=df["TVD"],
                mode='lines',
                line=dict(
                    color='blue',
                    width=10               )
            )
    # target_trace = go.Scatter3d(
    #             x=df["Eastings"],
    #             y=df["Northings"],
    #             z=df["TVD"],
    #             mode='markers',
    #             markers=dict(
    #                 color='blue',
    #                 width=10               )
    #         )
    layout = go.Layout(
                scene=dict(
                    xaxis=dict(title='Eastings'),
                    yaxis=dict(title='Northings'),
                    zaxis=dict(title='TVD', autorange='reversed')
                ),
                margin=dict(l=0, r=0, b=0, t=0)
            )

            
   
    fig = go.Figure(data=[well_trace], layout=layout)
    with st.container():            
        st.plotly_chart(fig, use_container_width=True)

    toggle = tog.st_toggle_switch(label="Data Frame", 
                        key="Key1", 
                        default_value=False, 
                        label_after = False, 
                        inactive_color = 'green', 
                        active_color="#11567f", 
                        track_color="#29B5E8"
                        )        
    if toggle :
        st.dataframe(df)
def well():    
        
    graph()        
            
            
    cl1,cl2 = st.sidebar.columns(2)
    
    with cl1:
        option = tog.st_toggle_switch(label="File/Input", 
                key="Key2", 
                default_value=False, 
                label_after = False, 
                inactive_color = 'red', 
                active_color="#11567f", 
                track_color="#29B5E8"
                )
    if option:
        Target  = st.sidebar.file_uploader("Upload Target Data",['csv','excel'])
        Formation = st.sidebar.file_uploader("Upload Formation Data",['csv','excel'])
        if Target is not None:
            try:
                data = pd.read_csv(Target)
                
            
            except:
                
                data = pd.read_excel(Target)
            
            cols = st.sidebar.selectbox("select",data.columns)
            chk  =st.sidebar.checkbox("show/hide")
            
            if  chk:
                mul  = st.sidebar.multiselect("select coordinates",data[cols])
                #st.text(mul[0])
            else:
                st.sidebar.text("Agigon")
    else:
        

        st.sidebar.subheader("Targets")
        tr = st.sidebar.number_input("Please enter number of targets",0)
        if tr:
            for i in range(int(tr)):
                t = st.sidebar.text_input(f"Target {i} (E,N,Z) ")
        st.sidebar.text("  ")
        st.sidebar.subheader("KickOff Point")        
        tvd =  st.sidebar.slider("Adjust Graph",0,1000)
        st.sidebar.subheader("Formations")

        st.text("  ")
        tr = st.sidebar.number_input("Please enter number of Formations",0)
        
        if tr:
            for i in range(int(tr)):
                f = st.sidebar.text_input(f"Formation {i} (Depth,Form_agr) ")

        st.sidebar.button("Run")

    
           
 
      
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.19.1/css/mdb.min.css" rel="stylesheet">', unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""

""", unsafe_allow_html=True)
hide_streamlit_style = """
            <style>
     
            header{visibility:hidden;}
             .main {
            margin-top: -120px;
            padding-top:10px;
            

        
           
        }

   

   
        }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            </style>
            
            """
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: green;">
  <a class="navbar-brand" href="#"  target="_blank"> [ <0> ]   SPE Drillbotics</a>

  
</nav>
""", unsafe_allow_html=True)

    
  

st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def streamlit_menu(example=1):
    if example == 1:
       
        with st.sidebar:
            selected = option_menu(
                menu_title="Section", 
                options=["Well Path", "RSS","Simulation"], 
                icons=["house", "play"],  
                menu_icon="cast",  
                default_index=0, 
            )
        return selected

    if example == 2:
        
        selected = option_menu(
            menu_title=None,  # required
            options=["Well Path","Simulation"],  # required
            icons=["house", "play"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
    
        selected = option_menu(
            menu_title=None, 
            options=["Well Path","Simulation"],  
            icons=["house", "play"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "5px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected



selected = streamlit_menu(example=2)

st.subheader("Well Path")

if selected == "Well Path":
    well()

if selected == "Simulation":
    simu()
    simulation()
# toggle = tog.st_toggle_switch(label="Label", 
#                     key="Key1", 
#                     default_value=False, 
#                     label_after = False, 
#                     inactive_color = 'green', 
#                     active_color="#11567f", 
#                     track_color="#29B5E8"
#                     )
# if toggle :
#     st.text("ON")
#     with col1: 
#         card1 = hasClicked = card(
#         title="Hello World!",
#         text="Some description",
#         image="http://placekitten.com/200/300",
#         url="https://github.com/gamcoh/st-card"
#         )
#     with col2:
#         card2 = hasClicked = card(
#         title="Hello ",
#         text="Some description",
#         image="http://placekitten.com/200/300",
#         url="https://github.com/gamcoh/st-card"
#         )
# else:
#     st.text("OFF")
