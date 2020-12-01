import pandas as pd
import country_converter as coco

df_bar = pd.read_csv('data.csv') 
df_bar = pd.read_csv('data.csv')
#print(df_bar['opera'].value_counts())
#df_country = df.groupby(['Country_Region']).sum().reset_index()
#df_country.replace('US', 'United States', inplace=True)
df_dia = df_bar[df_bar['dia_nomi']== 'Lu']
df_mes = df_dia[df_dia['mes']== 1]
df_mes['atraso_total'] = df_mes['atraso'].replace([0], [1])
df_country_total=df_mes.groupby(['dest_pais']).sum().reset_index()

#df_country = df_mes.groupby(['dest_pais']).sum().reset_index()
#print(df_mes.atraso_total.value_counts())
df_country_total=df_mes.groupby(['dest_pais']).sum().reset_index()
df_mes = df_mes[df_mes['atraso']== 1]
#print(df_country_total)

df_country = df_mes.groupby(['dest_pais']).sum().reset_index()
#print(df_country)
#df_country = coco.convert(names=df_bar.dest_pais.tolist(), to='name_short', not_found=None)
#print(df_country)
df_bar2 = df_bar['atraso'].replace([0, 1], ['puntual', 'atrasado'])

#        options=[{'label': "Grupo LATAM", 'value':"Grupo LATAM"},
#                                                         {'label': "Sky Airline", 'value':"Sky Airline"},
#                                                         {'label': "Aerolineas Argentinas", 'value':"Aerolineas Argentinas"},
#                                                         {'label': "Copa Air", 'value':"Copa Air"},
#                                                         {'label': "Latin American Wings", 'value':"Latin American Wings"},
#                                                         {'label': "Avianca", 'value':"Avianca"},
#                                                         {'label': "JetSmart SPA", 'value':"JetSmart SPA"},
#                                                         {'label': "Gol Trans", 'value':"Gol Trans"},
#                                                         {'label': "American Airlines", 'value':"American Airlines"},
#                                                         {'label': "Air Canada", 'value':"Air Canada"},
#                                                         {'label': "Iberia", 'value':"Iberia"},
#                                                         {'label': "Air France", 'value':"Air France"},
#                                                         {'label': "Delta Air", 'value':"Delta Air"},
#                                                         {'label': "Aeromexico", 'value':"Aeromexico"}
#                                                         {'label': "United Airlines", 'value':"United Airlines"},
#                                                         {'label': "Oceanair Linhas Aereas", 'value':"Oceanair Linhas Aereas"},
#                                                         {'label': "Alitalia", 'value':"Alitalia"},
#                                                         {'label': "K.L.M.", 'value':"K.L.M."},
#                                                         {'label': "British Airways", 'value':"British Airways"},
#                                                         {'label': "Qantas Airways", 'value':"Qantas Airways"},
#                                                         {'label': "Lacsa", 'value':"Lacsa"},
#                                                         {'label': "Austral", 'value':"Austral"},
#                                                         {'label': "Plus Ultra Lineas Aereas", 'value':"Plus Ultra Lineas Aereas"}],

df_importance = pd.read_csv('FEATURE_IMPORTANCES.csv')
df_importance = df_importance[df_importance['importance'] >= 0.04]

import pandas as pd
import pyreadstat
#import pyreadstat

df_model = pd.read_csv('y_pred.csv')
#print(df_model['y_pred'])
df_bar['y_pred']= df_model['y_pred']
df_bar.to_csv('data_final.csv')