import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from jupyter_dash import JupyterDash
from datetime import datetime, timedelta
import plotly.graph_objs as go
import numpy as np
import country_converter as coco

import plotly.figure_factory as ff
import chart_studio.plotly as py
from chart_studio.grid_objs import Column, Grid
from IPython.display import IFrame
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
app.title = 'AEROPUNTUAL'
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df_importance = pd.read_csv('FEATURE_IMPORTANCES.csv')
df_importance = df_importance[df_importance['importance'] >= 0.04]
df_importance['var'] = df_importance['var'].replace(
  ['opera_Sky Airline','opera_Grupo LATAM','dia_nomi_Mi','dia_nomi_Ju','dia_nomi_Sa',
  'ori_pr','orig_tas','dia_nomi_Ma','mes', 'orig_vas','orig_uas'],
  ['Sky Airline','Grupo LATAM','Miércoles','Jueves','Sábado',
  'Precipitación origen','Temperatura origen',
  'Martes','Mes', 'Velocidad viento meridional origen',
  'Velocidad viento zonal origen']
)
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.read_csv('data_final.csv')

df_bar['atraso2'] = df_bar['atraso'].replace([0, 1], ['puntual', 'atrasado'])

df_bar_atraso = df_bar[df_bar['atraso'] == 1]

df_bar_puntual = df_bar[df_bar['atraso'] == 0]

df_bar_atraso_chile = df_bar_atraso[df_bar_atraso['dest_pais'] == 'CL']

df_chile = df_bar[df_bar['dest_pais'] == 'CL']

data1 = [
    go.Bar(
        y=df_bar_puntual['mes'].value_counts(),
        x=df_bar_puntual['mes'].value_counts().keys(),
        orientation='v',
        text="",
        name='Puntual',
    ),
    go.Bar(
        y=df_bar_atraso['mes'].value_counts(),
        x=df_bar_puntual['mes'].value_counts().keys(),
        orientation='v',
        text="",
        name='Atrasado',
    )]
layout1 = go.Layout(
    height=500,
    title='Vuelos nacionales e internacionales por mes para el año en estudio',
    hovermode='closest',
    xaxis=dict(title='Meses', ticklen=5, zeroline=False, gridwidth=2, domain=[0.1, 1]),
    yaxis=dict(title='Cantidad', ticklen=5, gridwidth=2),
    showlegend=True
)
fig1 = go.Figure(data=data1, layout=layout1)

data2 = [
   
    go.Pie(labels=df_bar['atraso2'].value_counts().keys(), values=df_bar['atraso2'].value_counts())
]

layout2 = go.Layout(
    height=500,
    title='Cantidad porcentual de vuelos atrasados para el año de estudio',
    hovermode='closest',
    xaxis=dict(title='Atraso', ticklen=5, zeroline=False, gridwidth=2, domain=[0.1, 1]),
    yaxis=dict(title='Porcentaje %', ticklen=5, gridwidth=2),
    showlegend=True

)


#fig = px.bar(df_bar, x="", y="Amount", color="City", barmode="group")
fig2 = go.Figure(data=data2, layout=layout2)
 
#fig2 = #px.bar(df_bar, x="mes",y=count() 
       #      color="atraso", barmode = 'stack')
data3 = [
    go.Bar(
        y=df_bar_puntual['opera'].value_counts(),
        x=df_bar_puntual['opera'].value_counts().keys(),
        orientation='v',
        text="",
        name="Puntual"
    ),
    go.Bar(
        y=df_bar_atraso['opera'].value_counts(),
        x=df_bar_atraso['opera'].value_counts().keys(),
        orientation='v',
        text="",
        name="Atraso"
    )]
layout3 = go.Layout(
    height=500,
    title='Aerolineas con o sin atraso en el año de estudio',
    hovermode='closest',
    xaxis=dict(title='Aerolineas', ticklen=5, zeroline=False, gridwidth=2, domain=[0.1, 1]),
    yaxis=dict(title='', ticklen=5, gridwidth=2),
    showlegend=True
)
#fig3 = px.bar(df_bar, x="opera", color="atraso2", barmode="group")
fig3 = go.Figure(data=data3, layout=layout3)

data4 = [
    go.Bar(
        y=df_importance['importance'],
        x=df_importance['var'],
        orientation='v',
        text=" ",
    )]
layout4 = go.Layout(
    height=500,
    title='',
    hovermode='closest',
    xaxis=dict(title='', ticklen=5, zeroline=False, showgrid=True, domain=[0.2, 1]),
    yaxis=dict(title='Importancia', ticklen=5,  showgrid=False),
    showlegend=False
)
#fig = px.bar(df_bar, x="Fruit", y="Amount", color="City", barmode="group")
#fig4 = go.Figure(data=data4, layout=layout4)
#layout4 = go.Layout(
#    height=500,
#    title='Importancia de las variables en el modelo')
fig4 = go.Figure(data=go.Scatter(
    x=df_importance['var'],
    y=df_importance['importance'],
    mode='markers',
    marker=dict(size=[45,45,35,35,35,30,28,24,24,20,20],
                color=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11])
),layout=layout4)
# layout4 = go.Layout(
#     height=500,
#     title='Importancia de las variables en el modelo')



dftable = pd.read_csv('modelo.csv')





def prepare_daily_report(mes,dia):

    current_date = (datetime.today() - timedelta(days=1)).strftime('%m-%d-%Y')

    #df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + current_date + '.csv')
    df_bar = pd.read_csv('data_final.csv')
    #df_country = df.groupby(['Country_Region']).sum().reset_index()
    #df_country.replace('US', 'United States', inplace=True)
    df_dia = df_bar[df_bar['dia_nomi']== dia]
    df_mes = df_dia[df_dia['mes']== mes]

    #atraso+puntual
    df_mes['atraso_total'] = df_mes['atraso'].replace([0], [1])
    
    df_country = df_mes.groupby(['dest_pais']).sum().reset_index()

    df_country = df_country[df_country['dest_pais']!= 'CL']

    
    #code_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
    code_df = pd.read_csv('code.csv')
    df_country['pais']= coco.convert(names=df_country.dest_pais.tolist(), to='name_short', not_found=None)
    df_country_code = df_country.merge(code_df, left_on='pais', right_on='COUNTRY', how='left')
    
    return(df_country_code)


# app.layout = html.Div([
#     html.Img(src='data:image/png;base64,{}'.format(encoded_image))
# ])
app.layout = html.Div(children=[
    #html.H1(children='AEROPUNTUAL',style={'textAlign':'center'}),
    # All elements from the top of the page
    html.Div(html.Img(src=app.get_asset_url('white_logo_color_background.jpg'), style={'height':'100%', 'width':'100%'})),
    
    html.Div([
        html.Div([
            html.H3(children=''
                ),

            dcc.Graph(
                id='graph1',
                figure=fig1
            ),
            html.Div(children='''
                .
            '''),
        ], className='six columns'),
         html.Div([
        html.Div(children='''En un viaje siempre hay riesgo de que el vuelo no salga a tiempo o que por el clima u otras posibles situaciones sea cancelado, y aunque las aerolíneas dan compensaciones y hablan con los pasajeros, muy pocas veces les explican con claridad qué fue lo que pasó.

        Si bien las aerolíneas dan compensaciones y explicaciones a los pasajeros, pocas veces expresan con claridad el motivo real del atraso y, lo más importante, no entregan una información precisa respecto al tiempo de atraso del vuelo.

        Para ofrecer una solución a este problema es que proponemos AEROPUNTUAL, cuyo objetivo es generar una herramienta de software utilizando técnicas de Data Science que contribuya a las aerolíneas a mejorar la experiencia del consumidor y permitir proactividad a la hora de gestionar planificación aérea, mediante la detección temprana de retraso en el servicio.
        Esto se puede deber a distintos factores tanto internos como externos como:

        ''',
         style={'textAlign':'left','padding': '5%'}),
        html.Div([
          html.Ul([
            html.Li(children='''Mantenimiento de último minuto.'''),
            html.Li(children='''Cambios de avión.'''),
            html.Li(children='''Tiempos de abordaje no cuantificables.'''),
            html.Li(children='''Precipitación '''),
            html.Li(children='''Velocidad del Viento '''),
            html.Li(children='''Temperaturas o Clima extremo '''),
          ]),
        ],style={"paddingLeft": '5%'}),

        ], className='six columns'),
    
        

    ], className='row',style={"paddingBottom": 60,"fontSize":18}),
    html.Div([
      html.Div([
            html.H3(children=''
                ),

            dcc.Graph(
                id='graph2',
                figure=fig2
            ),
            html.Div(children='''
            '''),
        ], className='six columns'),
        html.Div([
            html.H3(children=''
                ),

            dcc.Graph(
                id='graph3',
                figure=fig3
            ),
            html.Div(children='''
            '''),
        ], className='six columns'),
    ], className='row'),
    html.Div([
        html.Div([
            html.H3(children=''
                ),

            dcc.Graph(
                id='graph4',
                figure=fig4
            ),
            html.Div(children='''
            '''),
        ], className='six columns'),
        html.Div([
            html.P(children=''' AEROPUNTUAL trabaja con el algoritmo Random Forest Classifier, 
              muestra una buena predicción de atraso. Los resultados generales se muestran en la siguiente Tabla.'''),

            html.Table(
              [html.Tr([html.Th(col) for col in dftable.columns])] +
              [html.Tr([
                html.Td(dftable.iloc[i][col]) for col in dftable.columns
              ]) for i in range(min(len(dftable), 1))]  
            ),
            html.Div(children=''' A través de este modelo, se obtuvo la importancia de cada variable para el modelo, con estos parámetros podemos obtener la probabilidad de que su vuelo se atrase.
              A continuación puede realizar la consulta.
            ''', style={ "paddingTop":70}), 
        ], className='six columns', style={ "paddingTop":70}),
    ], className='row',style={"paddingBottom": 60, "paddingTop":60, "fontSize":18}),
    # New Div for all elements in the new 'row' of the page
    # html.Div([
    #     html.H1(children='Hello Dash'),

    #     html.Div(children='''
    #         Dash: A web application framework for Python.
    #     '''),

    #     dcc.Graph(
    #         id='graph3',
    #         figure=fig2
    #     ),  
    # ], className='row'),
     html.H1(children='Averigua si tu vuelo podría tener un atraso',style={'textAlign':'center'}),

    
     html.Div([html.Span("Métrica : ", className="six columns",
                                           style={"textAlign": "right", 
                                           "width": "30%"}),
                                 dcc.Dropdown(id="value-selected1", value='atraso',
                                              options=[{'label': "Vuelos atrasados (datos reales 2017) ", 'value': 'atraso'},
                                                       {'label': "Vuelos atrasados (resultados del modelo) ", 'value': 'y_pred'},
                                                       ],
                                              style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                     "width": "80%"},
                                              className="six columns")], className="row"),

     html.Div([html.Span("Tipo : ", className="six columns",
                                           style={"textAlign": "right", 
                                           "width": "30%"}),
                                 dcc.Dropdown(id="value-selected2", value='Internacional',
                                              options=[{'label': "Nacional ", 'value': 'Nacional'},
                                                       {'label': "Internacional ", 'value': 'Internacional'},
                                                       ],
                                              style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                     "width": "80%"},
                                              className="six columns")], className="row"),
         html.Div([html.Span("Mes : ", className="six columns",
                                           style={"textAlign": "right", 
                                           "width": "30%"}),
                                 dcc.Dropdown(id="value-selected4", value=1,
                                              options=[{'label': "Enero ", 'value': 1},
                                                       {'label': "Febrero ", 'value': 2},
                                                       {'label': "Marzo ", 'value': 3},
                                                       {'label': "Abril ", 'value': 4},
                                                       {'label': "Mayo ", 'value': 5},
                                                       {'label': "Junio ", 'value': 6},
                                                       {'label': "Julio ", 'value': 7},
                                                       {'label': "Agosto ", 'value': 8},
                                                       {'label': "Septiembre ", 'value': 9},
                                                       {'label': "Octubre ", 'value': 10},
                                                       {'label': "Nomviembre ", 'value': 11},
                                                       {'label': "Diciembre ", 'value': 12}],
                                              style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                     "width": "80%"},
                                              className="six columns")], className="row"),

     html.Div([html.Span("Día : ", className="six columns",
                                           style={"textAlign": "right", 
                                           "width": "30%"}),
                                 dcc.Dropdown(id="value-selected5", value='Lu',
                                              options=[{'label': "Lunes ", 'value': 'Lu'},
                                                       {'label': "Martes ", 'value': 'Ma'},
                                                       {'label': "Miércoles ", 'value': 'Mi'},
                                                       {'label': "Jueves ", 'value': 'Ju'},
                                                       {'label': "Viernes ", 'value': 'Vi'},
                                                       {'label': "Sábado ", 'value': 'Sa'},
                                                       {'label': "Domingo ", 'value': 'Do'}
                                                       ],
                                              style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                     "width": "80%"},
                                              className="six columns")], className="row"),


    # html.Div([html.Span("Aerolínea : ", className="six columns",
    #                                        style={"textAlign": "right", 
    #                                        "width": "40%"}),
    #                              dcc.Dropdown(id="", value='atraso',
    #                                           options=[{'label': "Grupo LATAM ", 'value': 'atraso'},
    #                                                    {'label': "Sky Airline ", 'value': 'mes'},
    #                                                    {'label': "Latim American Wings ", 'value': 'Deaths'},
    #                                                    {'label': "Abril ", 'value': 'Active'},
    #                                                    {'label': "Mayo ", 'value': 'Active'},
    #                                                    {'label': "Junio ", 'value': 'Active'},
    #                                                    {'label': "Julio ", 'value': 'Active'},
    #                                                    {'label': "Agosto ", 'value': 'Active'},
    #                                                    {'label': "Septiembre ", 'value': 'Active'},
    #                                                    {'label': "Octubre ", 'value': 'Active'},
    #                                                    {'label': "Nomviembre ", 'value': 'Active'},
    #                                                    {'label': "Diciembre ", 'value': 'Active'}],
    #                                           style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
    #                                                  "width": "70%"},
    #                                           className="six columns")], className="row"),
     
    # html.Div([
    #     html.H1(children='Vuelos nacionales con más atrasos.',style={'textAlign':'center'}),
        
    #     dcc.Graph(
    #         id='graph5',
    #         figure=fig5,

    #     ),
    #     html.Div(children='''
    #         Para este estudio se consideraron tanto vuelos internacionales como nacionales.
    #     '''),  
    # ], className='row'),
    html.Div(children=[
      dcc.Markdown(''' Resultados ''',id='my-title', style={'paddingTop':'6%'})
    ]),
    html.Div(children=[
      html.P(''' Clima promedio en el Aeropuerto de Santiago "Temperatura media promedio diaria" y "Precipitación media promedio diaria". Busca en el mapa tu destino y averigua los resultados de probabilidad de atraso para tu vuelo. ''')
    ],style={'fontSize':18}),
    html.Div([
      html.Div([
            html.Div(html.Img(src=app.get_asset_url('sun_026.jpg'), 
              style={'height':'30%', 'width':'30%'})),
        ], className='three columns',style={'textAlign':'center'}),
        html.Div([
            html.Div(html.Img(src=app.get_asset_url('pngtree-rain-cloud-vector-icon-png-image_1027023.jpg'), 
              style={'height':'30%', 'width':'30%'})),

            
        ], className='three columns',style={'textAlign':'center'}),
    ], className='row'),
    html.Div([
      html.Div([
            
            html.H3(children=[
              dcc.Markdown(''' ''',id='my-temperature')
            ]),
        ], className='three columns', style={'textAlign':'center'}),
        html.Div([
            html.H3(children=[
              dcc.Markdown(''' ''',id='my-precipitation')
            ]),

            
        ], className='three columns'),
    ], className='row', style={'textAlign':'center'}),
    html.Div([
        
        
        #dl.Map(dl.TileLayer(), style={'width': '1000px', 'height': '500px'}),
        dcc.Graph(
            id='my-graph'

        ),
         html.Div(html.Img(src=app.get_asset_url('equipo2.png'), style={'height':'50%', 'width':'50%', 'paddingLeft':'20%'})),
    ], className='row'),

   
],style={'padding':'5%'})

@app.callback(
    [dash.dependencies.Output("my-title", "children"),
    dash.dependencies.Output("my-graph", "figure"),
    dash.dependencies.Output("my-temperature", "children"),
    dash.dependencies.Output("my-precipitation", "children"),],
    [dash.dependencies.Input("value-selected1", "value"),
    dash.dependencies.Input("value-selected2", "value"),
    dash.dependencies.Input("value-selected4", "value"),
    dash.dependencies.Input("value-selected5", "value")]
)


def update_multioutput(selected1,selected2,selected4,selected5):
    #dff = prepare_confirmed_data()
    df_bar = pd.read_csv('data_final.csv')
    if selected2 == 'Internacional':
      dff = prepare_daily_report(selected4,selected5)
      print(dff)
      dff['hover_text'] = dff["pais"] + " Probabilidad de atraso : " + (round(dff[selected1]/dff['atraso_total'],3)).apply(str)

      trace = go.Choropleth(locations=dff['CODE'],z=np.log(dff[selected1]/dff['atraso_total']),
                            text=dff['hover_text'],
                            hoverinfo="text",
                            marker_line_color='white',
                            autocolorscale=False,
                            reversescale=True,
                            colorscale="Viridis",
                            marker={'line': {'color': 'rgb(180,180,180)','width': 0.5}},
                            colorbar={"thickness": 10,"len": 0.3,"x": 0.9,"y": 0.7,
                                      'title': {"text": 'atrasos', "side": "bottom"},
                                      'tickvals': [ 1],
                                      'ticktext': ['1']})   
      layout = go.Layout(height=800,
              geo={'showframe': False,'showcoastlines': True,'projection': {'type': "miller"}})
      
      df_dia = df_bar[df_bar['dia_nomi']== selected5]
      df_mes = df_dia[df_dia['mes']== selected4]
      temperature = str(round(df_mes.orig_tas.mean(),2))+' ºC'
      precipitation = str(round(df_mes.ori_pr.mean(),2))+' mm'


    elif selected2 == 'Nacional':

      df_dia = df_chile[df_chile['dia_nomi']== selected5]
      df_mes = df_dia[df_dia['mes']== selected4]
      df_mes['atraso_total'] = df_mes[selected1].replace([0], [1])
      df_bar_atraso_chile = df_mes.groupby(['dest_ciudad']).sum().reset_index()
      list_count = []
      list_count_total =[]
      for n in range(len(df_bar_atraso_chile[selected1])):
        for m in df_mes['dest_ciudad']:
          if m == df_bar_atraso_chile['dest_ciudad'][n]:
            list_count.append(df_bar_atraso_chile[selected1][n])
            list_count_total.append(df_bar_atraso_chile['atraso_total'][n])

      df_mes['atraso5'] = list_count
      df_mes['atraso5_total'] = list_count_total
      df_mes['text'] =  df_mes['dest_ciudad'] + ', '  + '' + ' Probabilidad de atrasos: ' + (round(df_mes['atraso5']/df_mes['atraso5_total'],3)).astype(str).astype(str)

      trace = go.Scattergeo(
              lon = df_mes['dest_lon'],
              lat = df_mes['dest_lat'],
              text = df_mes['text'],
              mode = 'markers',
              marker_color = round(df_mes['atraso5']/df_mes['atraso5_total'],3),
             
              marker={'colorscale': 'Viridis','reversescale': True,'line': {'color': 'rgb(180,180,180)','width': 0.5}},
              showlegend=False,
              marker_size=15,
       
              )

      layout= go.Layout(
              
              geo_scope='south america'
          )
      df_dia = df_bar[df_bar['dia_nomi']== selected5]
      df_mes = df_dia[df_dia['mes']== selected4]
      temperature = str(round(df_mes.orig_tas.mean(),2))+' ºC'
      precipitation = str(round(df_mes.ori_pr.mean(),2))+' mm'


    figure ={"data": [trace],
            "layout": layout}
    children = ''' ### Resultados para tu vuelo '''+selected2+''' desde el Aeropuerto de Santiago '''

    return children, figure, temperature, precipitation




if __name__ == '__main__':
    app.run_server(debug=True)
