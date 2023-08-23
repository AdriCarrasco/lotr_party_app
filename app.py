import streamlit as st
import pandas as pd 
from streamlit_option_menu import option_menu
import json
import boto3
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from PIL import Image
from st_aggrid import AgGrid
import time
from streamlit_autorefresh import st_autorefresh
import os
import random



st.set_page_config(page_title="111 Birthday", 
                   page_icon="logo.jpg",
                   layout= "wide")
# CONFIG DATA


aws_access_key_id = st.secrets["aws_key"]
aws_secret_access_key = st.secrets["aws_secret_key"]

with open("colores_lotr.json") as file:
    colors_lotr = json.load(file)

# FUNCTIONS

def GetAllPoints(dict_test):
    all_points = []
    all_races = []
    for key_ in dict_test.keys():
        points = 0
        for key_game in dict_test[key_].keys():
            points = points + dict_test[key_][key_game]
        
        all_points.append(points)
        all_races.append(key_)
    return {"race": all_races, "points": all_points}

def GetJSON(key_ , aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key):
    client = boto3.client('s3',aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
    f = client.get_object(Bucket = 'summer-song', Key= key_)
    text = f["Body"].read().decode()
    return json.loads(text)

def PutJSON(key_, data_votes,aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key):
    client = boto3.client('s3',aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
    response = client.put_object(
                Body=json.dumps(data_votes),
                Bucket='summer-song',
                Key=key_
    )
    return response

def MarcarPuntos(position):
    if position == 1:
        return 10
    elif position == 2:
        return 8
    elif position == 3:
        return 5
    elif position == 4:
        return 1

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
def color_func(list_colors):
    return rgb_to_hex(list_colors[0], list_colors[1], list_colors[2])


puntos_juegos = GetJSON("dict_points_part1.json")

selected3 = option_menu("",["Juegos", "Tabla"], 
        icons=['file-bar-graph-fill', 'lightning-fill'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": color_func(colors_lotr["marron"])},
            "icon": {"color": "#ffffff", "font-size": "25px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": color_func(colors_lotr["oro"])},
            "nav-link-selected": {"background-color":color_func(colors_lotr["marron_oscuro"])}
        }
    )

if selected3 == "Juegos":
    col_0_0, col_0_1 = st.columns(2)

    dict_juegos = {
        "UAPTM": ["Equilibrio", "Escenas", "Comida", "Musica", "Twister", "Softcombat"],
        "Comunidades": ["Nazgul", "Sigilo", "Lorien", "Helm", "Pelennor", "Mordor"]
        }
    
    with col_0_0:
        choice_part = st.selectbox("Parte", ["UAPTM", "Comunidades"])
    with col_0_1:
        choice_game = st.selectbox("Juego", dict_juegos[choice_part])
    
    if choice_part == "UAPTM" and choice_game == "Equilibrio":
        
        st.title("Equilibrio")

        with st.expander("Descripción"):
            st.text("Explicación del juego")

        col_1_0, col_1_1 = st.columns(2)

        with col_1_0:
            with st.expander("Normas"):
                st.text("Hello")

        with col_1_1:
            with st.expander("Puntos"):
                st.text("Hello")

        st.title("Marcador")

        points_humans = st.number_input("Puntos Hombres", 0, 10, value = puntos_juegos["Hombres"][choice_game])
        points_elfs = st.number_input("Puntos Elfos", 0, 10, value = puntos_juegos["Elfos"][choice_game])
        points_dwarves = st.number_input("Puntos Enanos", 0, 10, value = puntos_juegos["Enanos"][choice_game])
        points_hobbits = st.number_input("Puntos Hobbits", 0, 10, value = puntos_juegos["Hobbits"][choice_game])
        
        if st.button("Actualizar"):
            puntos_juegos["Hombres"][choice_game] = points_humans
            puntos_juegos["Elfos"][choice_game] = points_elfs
            puntos_juegos["Enanos"][choice_game] = points_dwarves
            puntos_juegos["Hobbits"][choice_game] = points_hobbits

            response = PutJSON("dict_points_part1.json", puntos_juegos)

            count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

    elif choice_part == "UAPTM" and choice_game == "Escenas":
        
        if "list_escenas" not in st.session_state:
            st.session_state["list_escenas"] = []

        st.title("Escenas")

        with st.expander("Descripción"):
            st.text("Explicación del juego")

        col_1_0, col_1_1 = st.columns(2)

        with col_1_0:
            with st.expander("Normas"):
                st.text("Hello")

        with col_1_1:
            with st.expander("Puntos"):
                st.text("Hello")

        st.title("Escenas aleatorias")

        if "escenas_adivinar" not in st.session_state:
            dict_escenas = GetJSON("escenas_adivinar.json")
        else:
            dict_escenas = st.session_state["escenas_adivinar"]

        
        if "index_photo" not in st.session_state:
            rand_index = np.random.randint(0,len(dict_escenas["Escena"]))
            st.session_state["index_photo"] = rand_index
        else:
            rand_index = st.session_state["index_photo"]

        col_2_0, col_2_1, col_2_2, col_2_3 = st.columns([3,1,1,3])


        if len(pd.unique(st.session_state["list_escenas"])) == len(dict_escenas["Frase"]):
            st.warning("Ya se han usado todas las escenas")
        
        else:
            with col_2_0:
                st.header(dict_escenas["Escena"][rand_index])
            with col_2_1:
                if dict_escenas["Frase"][rand_index] != "":
                    st.markdown('*{texto_pelicula}*'.format(texto_pelicula = dict_escenas["Frase"][rand_index]))
            with col_2_2:
                st.caption(dict_escenas["Película"][rand_index])
            with col_2_3:
                st.image(os.path.join("pics_escenas", dict_escenas["Imagen"][rand_index]+ ".png"))

        col_button_0, col_button_1 = st.columns(2)
        with col_button_0:
            if st.button("Resetear"):
                st.session_state["list_escenas"] = []
                count_2 = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter2")
        with col_button_1:
            if st.button("Siguiente"):
                if len(pd.unique(st.session_state["list_escenas"])) != len(dict_escenas["Frase"]):
                    if rand_index in st.session_state["list_escenas"]:
                        while rand_index in st.session_state["list_escenas"]:
                            rand_index = np.random.randint(0,len(dict_escenas["Escena"]))
                    list_ = st.session_state["list_escenas"]
                    list_.append(rand_index)
                    list_ = list(pd.unique(list_))
                    st.session_state["list_escenas"] = list_
                    st.session_state["index_photo"] = rand_index

                    count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounternext")
        
        st.title("Marcador")

        points_humans = st.number_input("Puntos Hombres", 0, 10, value = puntos_juegos["Hombres"][choice_game])
        points_elfs = st.number_input("Puntos Elfos", 0, 10, value = puntos_juegos["Elfos"][choice_game])
        points_dwarves = st.number_input("Puntos Enanos", 0, 10, value = puntos_juegos["Enanos"][choice_game])
        points_hobbits = st.number_input("Puntos Hobbits", 0, 10, value = puntos_juegos["Hobbits"][choice_game])
        
        if st.button("Actualizar"):
            puntos_juegos["Hombres"][choice_game] = points_humans
            puntos_juegos["Elfos"][choice_game] = points_elfs
            puntos_juegos["Enanos"][choice_game] = points_dwarves
            puntos_juegos["Elfos"][choice_game] = points_hobbits

            response = PutJSON("dict_points_part1.json", puntos_juegos)

            count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

    elif choice_part == "UAPTM" and choice_game == "Comida":
        st.title("Equilibrio")

        with st.expander("Descripción"):
            st.text("Explicación del juego")

        col_1_0, col_1_1 = st.columns(2)

        with col_1_0:
            with st.expander("Normas"):
                st.text("Hello")

        with col_1_1:
            with st.expander("Puntos"):
                st.text("Hello")

        st.title("Marcador")

        points_humans = st.selectbox("Puesto Hombres", [1,2,3,4])
        points_elfs = st.selectbox("Puntos Elfos", [1,2,3,4])
        points_dwarves = st.selectbox("Puntos Enanos", [1,2,3,4])
        points_hobbits = st.selectbox("Puntos Hobbits", [1,2,3,4])
        
        

        if st.button("Actualizar"):
            puntos_juegos["Hombres"][choice_game] = MarcarPuntos(points_humans)
            puntos_juegos["Elfos"][choice_game] = MarcarPuntos(points_elfs)
            puntos_juegos["Enanos"][choice_game] = MarcarPuntos(points_dwarves)
            puntos_juegos["Hobbits"][choice_game] = MarcarPuntos(points_hobbits)

            response = PutJSON("dict_points_part1.json", puntos_juegos)

            count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

    elif choice_part == "UAPTM" and choice_game == "Musica":

        st.title("Marcador")

        points_humans = st.number_input("Puntos Hombres", 0, 10, value = puntos_juegos["Hombres"][choice_game])
        points_elfs = st.number_input("Puntos Elfos", 0, 10, value = puntos_juegos["Elfos"][choice_game])
        points_dwarves = st.number_input("Puntos Enanos", 0, 10, value = puntos_juegos["Enanos"][choice_game])
        points_hobbits = st.number_input("Puntos Hobbits", 0, 10, value = puntos_juegos["Hobbits"][choice_game])
        
        if st.button("Actualizar"):
            puntos_juegos["Hombres"][choice_game] = points_humans
            puntos_juegos["Elfos"][choice_game] = points_elfs
            puntos_juegos["Enanos"][choice_game] = points_dwarves
            puntos_juegos["Hobbits"][choice_game] = points_hobbits

            response = PutJSON("dict_points_part1.json", puntos_juegos)

            count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

    elif choice_part == "UAPTM" and choice_game == "Twister":
        st.title("Twister")

        with st.expander("Descripción"):
            st.text("Explicación del juego")

        col_1_0, col_1_1 = st.columns(2)

        with col_1_0:
            with st.expander("Normas"):
                st.text("Hello")

        with col_1_1:
            with st.expander("Puntos"):
                st.text("Hello")

        st.title("Marcador")

        points_humans = st.selectbox("Puesto Hombres", [1,2,3,4])
        points_elfs = st.selectbox("Puntos Elfos", [1,2,3,4])
        points_dwarves = st.selectbox("Puntos Enanos", [1,2,3,4])
        points_hobbits = st.selectbox("Puntos Hobbits", [1,2,3,4])
        
        

        if st.button("Actualizar"):
            puntos_juegos["Hombres"][choice_game] = MarcarPuntos(points_humans)
            puntos_juegos["Elfos"][choice_game] = MarcarPuntos(points_elfs)
            puntos_juegos["Enanos"][choice_game] = MarcarPuntos(points_dwarves)
            puntos_juegos["Hobbits"][choice_game] = MarcarPuntos(points_hobbits)

            response = PutJSON("dict_points_part1.json", puntos_juegos)

            count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

    elif choice_part == "UAPTM" and choice_game == "Softcombat":
        
        if "matches_soft" not in st.session_state:
            list_teams = ["Elfos", "Humanos", "Enanos", "Hobbits"]
            random.shuffle(list_teams)
            st.session_state["matches_soft"] = list_teams
            

        if "results" not in st.session_state:
            st.session_state["results"] = {}

        st.title("Softcombat")

        with st.expander("Descripción"):
            st.text("Explicación del juego")

        col_1_0, col_1_1 = st.columns(2)

        with col_1_0:
            with st.expander("Normas"):
                st.text("Hello")

        with col_1_1:
            with st.expander("Puntos"):
                st.text("Hello")

        # Figure Bracket

        def GetBracket(list_teams, results = {"match_1": {"Humanos": "5", "Hobbits": "2"},
                                              "match_2": {"Enanos": "2", "Elfos": "5"},
                                              "match_3": {"Humanos": "4", "Elfos": "5"}}):
            
            winner_1 = "None"
            winner_2 = "None"

            fig = go.Figure()
            fig.add_shape(
                type='rect', line=dict(dash='dash', color = "white"),
                fillcolor = "#ffffff",
                layer = "below",
                x0=0, x1=7, y0=4, y1=5
            )

            fig.add_annotation(x= 3.5, y=4.5,
                    text=list_teams[0], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 18,
                        color="#000000"
                        ))
            fig.add_shape(
                type='rect', line=dict(dash='dash', color = "white"),
                fillcolor = "#ffffff",
                layer = "below",
                x0=0, x1=7, y0=3, y1=4
            )

            fig.add_annotation(x= 3.5, y=3.5,
                    text=list_teams[1], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 18,
                        color="#000000"
                        ))
            
            fig.add_shape(
                type='rect', line=dict(dash='dash', color = "white"),
                fillcolor = "#ffffff",
                layer = "below",
                x0=0, x1=7, y0=1, y1=2
            )

            fig.add_annotation(x= 3.5, y=1.5,
                    text=list_teams[2], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 18,
                        color="#000000"
                        ))
            fig.add_shape(
                type='rect', line=dict(dash='dash', color = "white"),
                fillcolor = "#ffffff",
                layer = "below",
                x0=0, x1=7, y0=0, y1=1
            )

            fig.add_annotation(x= 3.5, y=0.5,
                    text=list_teams[3], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 18,
                        color="#000000"
                        ))
            
            if "match_1" not in results.keys():
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = "#ffffff",
                    layer = "below",
                    x0=7, x1=9, y0=4, y1=5
                )

                fig.add_annotation(x= 8, y=4.5,text= "0", showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = "#ffffff",
                    layer = "below",
                    x0=7, x1=9, y0=3, y1=4
                )

                fig.add_annotation(x= 8, y=3.5,text= "0", showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))
            
            else:
                if int(results["match_1"][list_teams[0]]) > int(results["match_1"][list_teams[1]]):
                    color_1 = "green"
                    color_2 = "#ffffff"
                    winner_1 = list_teams[0]
                else:
                    color_1 = "#ffffff"
                    color_2 = "green"
                    winner_1 = list_teams[1]
                
                fig.add_shape(type="line",
                        x0=9, y0=4, x1=11, y1=4,
                        line=dict(
                            color="#ffffff",
                            width=4,
                            dash="dot",
                        )
                )

                fig.add_shape(type="line",
                        x0=11, y0=4, x1=11, y1=3,
                        line=dict(
                            color="#ffffff",
                            width=4,
                            dash="dot",
                        )
                )

                fig.add_shape(type="line",
                        x0=11, y0=3, x1=13, y1=3,
                        line=dict(
                            color="#ffffff",
                            width=4,
                            dash="dot",
                        )
                )
                
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = color_1,
                    layer = "below",
                    x0=7, x1=9, y0=4, y1=5
                )

                fig.add_annotation(x= 8, y=4.5,text= results["match_1"][list_teams[0]], showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))
                
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = color_2,
                    layer = "below",
                    x0=7, x1=9, y0=3, y1=4
                )

                fig.add_annotation(x= 8, y=3.5,text= results["match_1"][list_teams[1]], showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))


                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = "#ffffff",
                    layer = "below",
                    x0=13, x1=20, y0=2.5, y1=3.5
                )

                fig.add_annotation(x= 16.5, y=2.95,
                        text=winner_1, showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))
            
            if "match_2" not in results.keys():
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = "#ffffff",
                    layer = "below",
                    x0=7, x1=9, y0=1, y1=2
                )

                fig.add_annotation(x= 8, y=1.5,text= "0", showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = "#ffffff",
                    layer = "below",
                    x0=7, x1=9, y0=0, y1=1
                )

                fig.add_annotation(x= 8, y=0.5,text= "0", showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))
            
            else:
                if int(results["match_2"][list_teams[2]]) > int(results["match_2"][list_teams[3]]):
                    color_1 = "green"
                    color_2 = "#ffffff"
                    winner_2 = list_teams[2]
                else:
                    color_1 = "#ffffff"
                    color_2 = "green"
                    winner_2 = list_teams[3]
                
                
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = color_1,
                    layer = "below",
                    x0=7, x1=9, y0=1, y1=2
                )
                
                fig.add_shape(type="line",
                        x0=9, y0=1, x1=11, y1=1,
                        line=dict(
                            color="#ffffff",
                            width=4,
                            dash="dot",
                        )
                )

                fig.add_shape(type="line",
                        x0=11, y0=1, x1=11, y1=2,
                        line=dict(
                            color="#ffffff",
                            width=4,
                            dash="dot",
                        )
                )

                fig.add_shape(type="line",
                        x0=11, y0=2, x1=13, y1=2,
                        line=dict(
                            color="#ffffff",
                            width=4,
                            dash="dot",
                        )
                )

                fig.add_annotation(x= 8, y=1.5,text= results["match_2"][list_teams[2]], showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))
                
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = color_2,
                    layer = "below",
                    x0=7, x1=9, y0=0, y1=1
                )

                fig.add_annotation(x= 8, y=0.5,text= results["match_2"][list_teams[3]], showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))


                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = "#ffffff",
                    layer = "below",
                    x0=13, x1=20, y0=1.5, y1=2.5
                )

                fig.add_annotation(x= 16.5, y=1.95,
                        text=winner_2, showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))

            if "match_3" in results.keys():
                if results["match_3"][winner_1] > results["match_3"][winner_2]:
                    winner = winner_1
                    color_1 = "green"
                    color_2 = "#ffffff"
                else:
                    winner = winner_2
                    color_2 = "green"
                    color_1 = "#ffffff"
                
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = color_1,
                    layer = "below",
                    x0=20, x1=22, y0=2.5, y1=3.5
                )

                fig.add_annotation(x= 21, y=3,text= results["match_3"][winner_1], showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))
                fig.add_shape(
                    type='rect', line=dict(dash='dash', color = "white"),
                    fillcolor = color_2,
                    layer = "below",
                    x0=20, x1=22, y0=1.5, y1=2.5
                )

                fig.add_annotation(x= 21, y=2,text= results["match_3"][winner_2], showarrow=False,
                        font=dict(
                            family="Times New Roman, monospace",
                            size = 18,
                            color="#000000"
                            ))

            fig.update_layout(
                    xaxis=dict(
                        showline=True,
                        showgrid=False,
                        showticklabels=False,
                        linecolor='#f04641',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Poppins',
                            size=12,
                            color='#f04641'
                        )
                    ),
                    yaxis = dict(
                        showgrid = False,
                        linewidth = 2,
                        linecolor='#00aa9b',
                        ticks = "outside",
                        tickfont = dict(
                            family = "Poppins",
                            size = 14,
                            color = '#00aa9b'
                        ),
                        showticklabels = True
                    ),
                    showlegend=False,
                    title = "Clasificación",
                    plot_bgcolor='rgb(15,18,22)',
                    xaxis_title='',
                    yaxis_title='Puntos',
                )
            fig = fig.update_xaxes(range = [0,22])
            fig = fig.update_yaxes(range = [0,6])


            return fig, winner_1, winner_2

        fig_bracket, winner_1, winner_2 = GetBracket(st.session_state["matches_soft"], results = st.session_state["results"])
        st.plotly_chart(fig_bracket, use_container_width=True)
        st.title("Marcador")

        if "results" not in st.session_state:
            try: 
                results_init = GetJSON("resultados_softcombat.json")
            except:
                results_init = {}
            st.session_state["results"] = results_init
        
        if "match_1" not in st.session_state["results"] or "match_2" not in st.session_state["results"]:
            match_boxscore = st.selectbox("Elegir combate", ["match_1", "match_2"])
        else:
            match_boxscore = st.selectbox("Elegir combate", ["match_1", "match_2", "match_3"])
        
        if match_boxscore == "match_1":
            points_1 = st.number_input(st.session_state["matches_soft"][0],0, 5, 0)
            points_2 = st.number_input(st.session_state["matches_soft"][1],0, 5, 0)

            if st.button("Validar Partido 1"):
                resultado = st.session_state["results"]
                resultado["match_1"] = {
                    st.session_state["matches_soft"][0]: points_1,
                    st.session_state["matches_soft"][1]: points_2
                }

                st.session_state["results"] = resultado

                count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter1")
        
        elif match_boxscore == "match_2":
            points_1 = st.number_input(st.session_state["matches_soft"][2],0, 5, 0)
            points_2 = st.number_input(st.session_state["matches_soft"][3],0, 5, 0)

            if st.button("Validar Partido 2"):
                resultado = st.session_state["results"]
                resultado["match_2"] = {
                    st.session_state["matches_soft"][2]: points_1,
                    st.session_state["matches_soft"][3]: points_2
                }
                st.session_state["results"] = resultado

                count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter3")
            
            
        
        elif match_boxscore == "match_3":
            points_1 = st.number_input(winner_1,0, 10, 0)
            points_2 = st.number_input(winner_2,0, 10, 0)

            if st.button("Validar Partido Final"):
                resultado = st.session_state["results"]
                resultado["match_3"] = {
                    winner_1: points_1,
                    winner_2: points_2
                }
                st.session_state["results"] = resultado

                count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter2")
        # Figure Bracket

        if st.button("Validar Resultados"):
            
            puntos_hombres = 0
            puntos_enanos = 0
            puntos_elfos = 0
            puntos_hobbits = 0

            for key_match in st.session_state["results"].keys():
                if "Humanos" in st.session_state["results"][key_match].keys():
                    puntos_hombres = puntos_hombres + st.session_state["results"][key_match]["Humanos"]
                if "Elfos" in st.session_state["results"][key_match].keys():
                    puntos_elfos = puntos_elfos + st.session_state["results"][key_match]["Elfos"]
                if "Enanos" in st.session_state["results"][key_match].keys():
                    puntos_enanos = puntos_enanos + st.session_state["results"][key_match]["Enanos"]
                if "Hobbits" in st.session_state["results"][key_match].keys():
                    puntos_hobbits = puntos_hobbits + st.session_state["results"][key_match]["Hobbits"]
            
            puntos_juegos["Hombres"][choice_game] = puntos_hombres
            puntos_juegos["Elfos"][choice_game] = puntos_elfos
            puntos_juegos["Enanos"][choice_game] = puntos_enanos
            puntos_juegos["Hobbits"][choice_game] = puntos_hobbits

            response = PutJSON("dict_points_part1.json", puntos_juegos)

            response = PutJSON("resultados_softcombat.json", st.session_state["results"])

            count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter4")

        if st.button("Resetear partidas"):
            st.session_state["results"] = {}
            list_teams = ["Elfos", "Humanos", "Enanos", "Hobbits"]
            seed_index = np.random.randint(1,2000)
            random.seed(seed_index)
            random.shuffle(list_teams)
            st.info("Reseteo")
            st.session_state["matches_soft"] = list_teams
            count_final = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter5")
        

elif selected3 == "Tabla":
    all_points = GetAllPoints(puntos_juegos)
    data_points = pd.DataFrame(all_points).sort_values("points", ascending= False).reset_index()
    fig = go.Figure()
    i = 0
    for index, row in data_points.iterrows():
        if i == 0:
            fig.add_shape(
                type='rect', line=dict(dash='dash', color = "white"),
                fillcolor = "#FFD700",
                layer = "below",
                x0=1, x1=2, y0=0, y1=row["points"]
            )

            if (row["points"] < 12) and (row["points"] > 0):
                y_max = row["points"] + 4

                fig.add_annotation(x= 1.5, y=y_max,
                    text="1." + row["race"], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#ffffff"
                        ))
                
                fig.add_annotation(x=1.5 , y=y_max - 2,
                        text="{points} pto(s)".format(points = row["points"]), showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#ffffff"
                        ))
            elif row["points"] >= 12:
                max_points = row["points"]
                y_max = row["points"]*2/3
                fig.add_annotation(x= 1.5, y=y_max,
                    text="1." + row["race"], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#000000"
                        ))
            
                fig.add_annotation(x=1.5 , y= y_max/2,
                        text="{points} pto(s)".format(points = row["points"]), showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#000000"
                        ))

            

        elif i == 1:
            fig.add_shape(
                type='rect', line=dict(dash='dash', color = "white"),
                fillcolor = "#c0c0c0",
                layer = "below",
                x0=0, x1=1, y0=0, y1=row["points"]
            )

            if (row["points"] < 12) and (row["points"] > 0):
                y_max = row["points"] + 4

                fig.add_annotation(x= 0.5, y=y_max,
                    text="2." + row["race"], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#ffffff"
                        ))
                
                fig.add_annotation(x=0.5 , y=y_max - 2,
                        text="{points} pto(s)".format(points = row["points"]), showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#ffffff"
                        ))
            elif row["points"] >= 12:
                max_points = row["points"]
                y_max = row["points"]*2/3
                fig.add_annotation(x= 0.5, y=y_max,
                    text="2." + row["race"], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#000000"
                        ))
            
                fig.add_annotation(x=0.5 , y= y_max/2,
                        text="{points} pto(s)".format(points = row["points"]), showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#000000"
                        ))

        elif i == 2:
            fig.add_shape(
                type='rect', line=dict(dash='dash', color = "white"),
                fillcolor = "#cd7f32",
                layer = "below",
                x0=2, x1=3, y0=0, y1=row["points"]
            )

            if (row["points"] < 12) and (row["points"] > 0):
                y_max = row["points"] + 4

                fig.add_annotation(x= 2.5, y=y_max,
                    text="3." + row["race"], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#ffffff"
                        ))
                
                fig.add_annotation(x=2.5 , y=y_max - 2,
                        text="{points} pto(s)".format(points = row["points"]), showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#ffffff"
                        ))
            elif row["points"] >= 12:
                max_points = row["points"]
                y_max = row["points"]*2/3
                fig.add_annotation(x= 2.5, y=y_max,
                    text="3." + row["race"], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#000000"
                        ))
            
                fig.add_annotation(x=2.5 , y= y_max/2,
                        text="{points} pto(s)".format(points = row["points"]), showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#000000"
                        ))

        elif i == 3:
            fig.add_shape(
                type='rect', line=dict(dash='dash', color = "white"),
                fillcolor = "white",
                layer = "below",
                x0=3, x1=4, y0=0, y1=row["points"]
            )

            if (row["points"] < 12) and (row["points"] > 0):
                y_max = row["points"] + 4

                fig.add_annotation(x= 3.5, y=y_max,
                    text="4." + row["race"], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#ffffff"
                        ))
                
                fig.add_annotation(x=3.5 , y=y_max - 2,
                        text="{points} pto(s)".format(points = row["points"]), showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#ffffff"
                        ))
            elif row["points"] >= 12:
                max_points = row["points"]
                y_max = row["points"]*2/3
                fig.add_annotation(x= 3.5, y=y_max,
                    text="4." + row["race"], showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#000000"
                        ))
                fig.add_annotation(x=3.5 , y= y_max/2,
                        text="{points} pto(s)".format(points = row["points"]), showarrow=False,
                    font=dict(
                        family="Times New Roman, monospace",
                        size = 22,
                        color="#000000"
                        ))
        

        i = i +1

    fig.update_layout(
                    xaxis=dict(
                        showline=True,
                        showgrid=False,
                        showticklabels=False,
                        linecolor='#f04641',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Poppins',
                            size=12,
                            color='#f04641'
                        )
                    ),
                    yaxis = dict(
                        showgrid = False,
                        linewidth = 2,
                        linecolor='#00aa9b',
                        ticks = "outside",
                        tickfont = dict(
                            family = "Poppins",
                            size = 14,
                            color = '#00aa9b'
                        ),
                        showticklabels = True
                    ),
                    showlegend=False,
                    title = "Clasificación",
                    plot_bgcolor='rgb(15,18,22)',
                    xaxis_title='',
                    yaxis_title='Puntos',
                )
    fig = fig.update_xaxes(range = [0,4])
    fig = fig.update_yaxes(range = [0,max(data_points.points)+5])

    dict_points = {}
    for race_ in puntos_juegos.keys():
        points_list = []
        for game_ in puntos_juegos[race_].keys():
            points_list.append(puntos_juegos[race_][game_])
        
        dict_points[race_] = points_list
    
    data_points = pd.DataFrame(dict_points)
    data_points = data_points.transpose()
    data_points.columns = list(puntos_juegos[race_].keys())
    with st.expander("Tablas"):
        st.dataframe(data_points, use_container_width= True)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("Resetear puntos"):
        puntos_juegos = {
            "Hombres":{
                "Equilibrio": 0,
                "Escenas": 0,
                "Comida": 0,
                "Musica": 0,
                "Twister": 0, 
                "Softcombat": 0
            },
            "Elfos": {
                "Equilibrio": 0,
                "Escenas": 0,
                "Comida": 0,
                "Musica": 0,
                "Twister": 0, 
                "Softcombat": 0
            },
            "Enanos": {
                "Equilibrio": 0,
                "Escenas": 0,
                "Comida": 0,
                "Musica": 0,
                "Twister": 0, 
                "Softcombat": 0
            },
            "Hobbits":{
                "Equilibrio": 0,
                "Escenas": 0,
                "Comida": 0,
                "Musica": 0,
                "Twister": 0, 
                "Softcombat": 0
            },
        }

        response = PutJSON("dict_points_part1.json", puntos_juegos)
        if response["ResponseMetadata"]['HTTPStatusCode'] == 200:
            st.success("Puntos reseteados")
            time.sleep(2)
            count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

