import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import joblib
from dash.dependencies import Input, Output, State
import base64
import flask
import glob
import os
import json
from urllib.request import urlopen

####################################################################################################
################### TRECHO RELACIONADO AO MODELO ###################################################
####################################################################################################

# MODELO LR
model1 = open("models/LR_Classifier1.pkl", "rb")
model2 = open("models/LR_Classifier2.pkl", "rb")
lr_clf1 = joblib.load(model1)
lr_clf2 = joblib.load(model2)

# MODELO RF
model1 = open("models/RF_Classifier1.pkl", "rb")
model2 = open("models/RF_Classifier2.pkl", "rb")
rf_clf1 = joblib.load(model1)
rf_clf2 = joblib.load(model2)

# ÍCONES
iconp = 'img/pessoas.png'
iconp_base64 = base64.b64encode(open(iconp , 'rb').read()).decode('ascii')
iconv = 'img/veiculos.png'
iconv_base64 = base64.b64encode(open(iconv , 'rb').read()).decode('ascii')

# LISTAS - VALORES DE ATRIBUTOS
causes = ['Falta de atenção', 'Outras', 'Animais na pista', 'Defeito mecânico em veículo', 'Não guardar distância de segurança', 'Velocidade incompatível', 'Desobediência à sinalização', 'Ingestão de álcool', 'Defeito na via', 'Dormindo', 'Ultrapassagem indevida', 'Fenômenos da natureza', 'Avarias e/ou desgaste excessivo no pneu', 'Falta de atenção à condução', 'Desobediência às normas de trânsito pelo condutor', 'Restrição de visibilidade', 'Falta de atenção do pedestre', 'Condutor dormindo', 'Pista escorregadia', 'Sinalização da via insuficiente ou inadequada', 'Mal súbito', 'Carga excessiva e/ou mal acondicionada', 'Objeto estático sobre o leito carroçável', 'Deficiência ou não acionamento do sistema de iluminação/sinalização do veículo', 'Ingestão de substâncias psicoativas', 'Agressão externa', 'Desobediência às normas de trânsito pelo pedestre', 'Ingestão de álcool e/ou substâncias psicoativas pelo pedestre']
tipo = ['Colisão frontal', 'Saída de pista', 'Atropelamento de animal', 'Capotamento', 'Colisão lateral', 'Atropelamento de pessoa', 'Colisão traseira', 'Colisão transversal', 'Tombamento', 'Colisão com objeto fixo', 'Danos eventuais', 'Queda de motocicleta/bicicleta/veículo', 'Derramamento de carga', 'Colisão com bicicleta', 'Colisão com objeto móvel', 'Incêndio', 'Queda de ocupante de veículo', 'Saída de leito carroçável', 'Colisão com objeto estático', 'Atropelamento de pedestre', 'Colisão com objeto em movimento', 'Engavetamento']
condicao = ['Céu claro', 'Chuva', 'Nublado', 'Sol', 'Nevoeiro/neblina', 'Vento', 'Granizo', 'Neve', 'Garoa/chuvisco']
tracado = ['Reta', 'Curva', 'Cruzamento', 'Interseção de vias', 'Rotatória', 'Desvio temporário', 'Viaduto', 'Ponte', 'Retorno regulamentado', 'Túnel']
meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

####################################################################################################
################### TRECHO RELACIONADO AO GRÁFICO MAPA #############################################
####################################################################################################

# Importando a base de dados
df = pd.read_csv('bases/df_ano_uf.csv', encoding='ISO-8859-1')
df_pessoa = pd.read_csv('bases/pessoas_uf_ano.csv', encoding='ISO-8859-1')

####################################################################################################
################### TRECHO RELACIONADO AO GRÁFICO TIPO-CAUSA #######################################
####################################################################################################

# Carrega as bases de dados, coloque ela no caminho que desejar
df_causa_acidente = pd.read_csv('bases/causa_acidente.csv', encoding='ISO-8859-1', sep=';')
df_tipo_acidente = pd.read_csv('bases/tipo_acidente.csv', encoding='ISO-8859-1', sep=';')

####################################################################################################
################### TRECHO RELACIONADO AO GRÁFICO ANO-MES #######################################
####################################################################################################

# Carrega a base de dados
dfano = pd.read_csv('bases/pessoas_mes_ano.csv', encoding='ISO-8859-1')

months = { 1: "Jan", 2: "Fev", 3: "Mar", 4: "Abril", 5: "Maio", 6: "Jun", 7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",}

dfano['mes'] = dfano['mes'].replace(months)

####################################################################################################
# STYLESHEETS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# APP LAYOUT
app.layout = html.Div(children=[
    html.Div(style={'width':'100%','height':'50px','background-color':'#108de4'}),
    html.Div(style={'width': '80%', 'margin': 'auto', 'padding-bottom': '200px'}, children=[
        
        html.Div([
            html.Br(),
            html.Br(),
            html.H1(children='Predição da gravidade de acidentes de trânsito',style={'textAlign': 'center'}),
            html.Br(),

            html.Div([

                html.Div([
                    html.H6('Dia da semana'),
                    dcc.Dropdown(
                        id= 'dia_semana',
                        options=[
                            {'label': 'Domingo', 'value': 1},
                            {'label': 'Segunda', 'value': 2},
                            {'label': 'Terça', 'value': 3},
                            {'label': 'Quarta', 'value': 4},
                            {'label': 'Quinta', 'value': 5},
                            {'label': 'Sexta', 'value': 6},
                            {'label': 'Sábado', 'value': 7}
                        ],
                        value=1
                    ),
                    html.Br(),
                    html.H6('Causa do Acidente'),
                    dcc.Dropdown(
                        id='causa_acidente',
                        options=[{'label': cause, 'value': i} for i, cause in enumerate(causes,1)],
                        value=1
                    ),
                    html.Br(),
                    html.H6('Tipo de Acidente'),
                    dcc.Dropdown(
                        id= 'tipo_acidente',
                        options=[{'label': t, 'value': i} for i, t in enumerate(tipo,1)],
                        value=1
                    ),
                    html.Br(),
                    html.H6('Fase do dia'),
                    dcc.Slider(
                        id= 'fase_dia',
                        min=1,
                        max=4,
                        marks={ 
                            1: {'label': 'pleno dia'},
                            2: {'label': 'plena noite'},
                            3: {'label': 'amanhecer'},
                            4: {'label': 'anoitecer'}
                        },
                        value=1,
                    ),
                    html.Br(),
                    html.H6('Condição Metereológica'),
                    dcc.Dropdown(
                        id= 'condicao_meteorologica',
                        options=[{'label': cond, 'value': i} for i, cond in enumerate(condicao,1)],
                        value=1
                    ),
                    html.Br(),
                    html.H6('Tipo de Pista'),
                    dcc.Slider(
                        id= 'tipo_pista',
                        min=1,
                        max=3,
                        marks={ 
                            1: {'label': 'dupla'},
                            2: {'label': 'simples'},
                            3: {'label': 'múltipla'}
                        },
                        value=1,
                    ),
                    html.Br(),
                    html.H6('Traçado da via'),
                    dcc.Dropdown(
                        id= 'tracado_via',
                        options=[{'label': trac, 'value': i} for i, trac in enumerate(tracado,1)],
                        value=1
                    ),
                    html.Br(),
                    html.H6('Solo'),
                    dcc.Slider(
                        id= 'solo',
                        min=1,
                        max=3,
                        marks={ 
                            1: {'label': 'rural'},
                            2: {'label': 'urbano'},
                            3: {'label': 'indefinido'}
                        },
                        value=1,
                    ),
                    html.Br(),
                    html.H6('Quantidade de Pessoas'),
                    dcc.Input(
                        id="pessoas", type="number", placeholder="input with range",
                        value=1,
                    ),
                    html.Br(),
                    html.H6('Veículos'),
                    dcc.Input(
                        id="veiculos", type="number", placeholder="input with range",
                        value=1,
                    ),
                    html.Br(),
                    html.H6('Mês'),
                    dcc.Dropdown(
                        id= 'mes',
                        options=[{'label': mes, 'value': i} for i, mes in enumerate(meses,1)],
                        value=1
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br()
                ], className="four columns"),

                html.Div([
                    html.Div(id='informacoes',style={'height': '300px', 'width': '100%','background-color': '#ffffff','border': '2px solid #aaaaaa','border-radius': '10px'},children=[
                        
                        html.H6(id='titulo', style={'padding-left': '20px','color':'#8d8d8d'},children='INFORMAÇÕES DO ACIDENTE:'),
                        
                        html.Div([
                            html.H6(id='info_met',children=''),
                        ],className='two columns'),
                        html.Div([
                            html.H2(id='info_dia',children='',style={'color':'#8d8d8d'}),
                            html.H4(id='info_mes',children='',style={'color':'#8d8d8d'}),
                            html.H6(id='info_fase',children=''),
                        ],className='three columns'),
                        
                        html.Div([
                            html.H6(id='info_pista',children=''),
                            html.H6(id='info_via',children=''),
                            html.H6(id='info_solo',children=''),
                        ],className='three columns'),
                        html.Div([
                            html.H6(children='Causa:',style={'color':'#494949'}),
                            html.H6(id='info_causa',children='',style={'color':'#8d8d8d'}),
                            html.H6(children='Tipo:',style={'color':'#494949'}),
                            html.H6(id='info_tipo',children='',style={'color':'#8d8d8d'}),
                        ],className='three columns'),
                        
                    ]),
                    html.Div(style={'margin-top':'10px','height': '40px', 'width': '100%','background-color': '#ffffff','border-bottom': '2px solid #aaaaaa'},children=[
                        
                        html.Div([
                            html.H6(children='',style={'color':'#8d8d8d'}),
                        ],className='seven columns'),
                        html.Div([
                            html.Img(src='data:image/png;base64,{}'.format(iconp_base64))
                        ],className='one columns'),
                        html.Div(children=[
                            html.H6(id='info_pessoas',children='',style={'color':'#8d8d8d'}),
                        ],className='one columns'),
                        
                        html.Div(children=[
                            html.Img(src='data:image/png;base64,{}'.format(iconv_base64))

                        ],className='one columns'),
                        html.Div([
                            html.H6(id='info_veiculos',children='',style={'color':'#8d8d8d'}),
                        ],className='one columns'),
                    ]),

                    html.H4('Modelo'),
                    dcc.Dropdown(
                        id= 'modelo',
                        options=[
                            {'label': 'Logistic Regression', 'value': 1},
                            {'label': 'Random Forest', 'value': 2},
                        ],
                        value=1
                    ), 
                    html.Br(),
                    dbc.Button( 
                    id='submeter',
                    n_clicks=0,
                    children='Submeter',
                    color='primary',
                    block=True
                    ),
                    html.Br(),
                    html.H1(id='result',children='',style={'textAlign': 'center'})
                ], className="eight columns")
                
            ]),
            html.Br(),
            html.Br()
        ], className="row"),

        html.Div([
            html.Br(),
            html.Br(),
            html.Div(style={'border-top': '2px solid #aaaaaa'},children=[
                html.Br(),
                html.H1("Mapa de Ocorrências", style={'text-align': 'center'}),

                dcc.Dropdown(
                    id='tipo',
                    options=[
                        {"label": "Acidentes", "value": "acidentes"},
                        {"label": "Mortos", "value": "mortos"},
                        {"label": "Feridos", "value": "feridos"},
                        {"label": "Ilesos", "value": "ilesos"},
                        ],
                    value="acidentes",
                    style={'width': "40%"}),
                
                dcc.Dropdown(
                    id='anos',
                    options=[
                        {"label": "2007", "value": 2007},
                        {"label": "2008", "value": 2008},
                        {"label": "2009", "value": 2009},
                        {"label": "2010", "value": 2010},
                        {"label": "2011", "value": 2011},
                        {"label": "2012", "value": 2012},
                        {"label": "2013", "value": 2013},
                        {"label": "2014", "value": 2014},
                        {"label": "2015", "value": 2015},
                        {"label": "2016", "value": 2016},
                        {"label": "2017", "value": 2017},
                        {"label": "2018", "value": 2018},
                        {"label": "2019", "value": 2019},
                        {"label": "2020", "value": 2020}
                    ],
                    value=2020,
                    style={'width': "30%"}),

                html.H4(id='message', children=[], style={'text-align': 'left'}),
                html.Br(),
                html.Div([
                    dcc.Graph(id='map-container', figure={}, style={'text-align': 'center'})
                ], style={'margin': 'auto','position':'relative'})
            ]),
            html.Br(),
            html.Br()
        ], className="row"),

        html.Div(style={'border-top': '2px solid #aaaaaa'},children=[
            html.Br(),
            html.Br(),
            html.Div(children=[
                html.H1(
                    children='Ocorrências',
                    style={
                        'textAlign': 'center',
                        'color': 'black'
                    }
                ),

                html.Div(children='Ocorrências por tipo e causa de acidentes', style={
                    'textAlign': 'center',
                    'color': 'black'
                }),

                html.Div([
                    html.Label('Tipo de Dado'),
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[
                            {'label': 'Tipo de Acidente', 'value': 'tipo_acidente'},
                            {'label': 'Causa de Acidente', 'value': 'causa_acidente'}            
                        ],
                        value='tipo_acidente'
                    )       
                ], style={'width': '48%'}),    

                dcc.Graph(
                    id='graph-with-slider',
                    style={'margin':'auto'}        
                ),
                
                dcc.Slider(
                    id='year-slider',
                    min=df_causa_acidente['ano'].min(),
                    max=df_causa_acidente['ano'].max(),
                    value=df_causa_acidente['ano'].min(),
                    marks={str(year): str(year) for year in df_causa_acidente['ano'].unique()},
                    step=None
                )
            ]),
            html.Br(),
            html.Br()
        ], className="row"),

        html.Div(style={'border-top': '2px solid #aaaaaa'},children=[
            html.Br(),
            html.Br(),
            html.Div([
                html.H1(
                    children='Estado Clínico por UF',
                    style={
                        'textAlign': 'center',
                        'color': 'black'
                    }
                ),

                html.Div(children='Quantidade de Vítimas por Estado Clínico em cada Federação', style={
                    'textAlign': 'center',
                    'color': 'black'
                }),

                html.Div([
                    html.Label('Estado_Clínico'),
                    dcc.Dropdown(
                        id='xaxis-column2',
                        options=[{'label': 'Mortos', 'value': 'mortos'},
                        {
                            'label': 'Feridos Graves', 'value': 'feridos_graves'
                        },
                        {
                            'label': 'Feridos Leves', 'value': 'feridos_leves'
                        },
                        {
                            'label': 'Ilesos', 'value': 'ilesos'
                        }],
                        value='mortos'
                    )
                ],style={'width': '48%', 'display': 'inline-block'}),

                dcc.Graph(id='indicator-graphic',),

                dcc.Slider(
                    id='year--slider',
                    min=df_pessoa['ano'].min(),
                    max=df_pessoa['ano'].max(),
                    value=df_pessoa['ano'].max(),
                    marks={str(year): str(year) for year in df_pessoa['ano'].unique()},
                    step=None
                )
            ]),
            html.Br(),
            html.Br()
        ], className="row"),
        html.Div(style={'border-top': '2px solid #aaaaaa'},children=[
            html.Br(),
            html.Br(),
            html.Div([
                html.H1(
                    children='Estado Clínico por mês',
                    style={
                        'textAlign': 'center',
                        'color': 'black'
                    }
                ),
                html.Div([
                    html.Label('Estado_Clínico'),
                    dcc.Dropdown(
                        id='xaxiss-column',
                        options=[{'label': 'Mortos', 'value': 'mortos'},
                        {
                            'label': 'Feridos Graves', 'value': 'feridos_graves'
                        },
                        {
                            'label': 'Feridos Leves', 'value': 'feridos_leves'
                        },
                        {
                            'label': 'Ilesos', 'value': 'ilesos'
                        }],
                        value='mortos'
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),

                dcc.Graph(id='indicador-graphic'),

                dcc.Slider(
                    id='ano--slider',
                    min=dfano['ano'].min(),
                    max=dfano['ano'].max(),
                    value=dfano['ano'].max(),
                    marks={str(year): str(year) for year in dfano['ano'].unique()},
                    step=None
                )
            ]),
            html.Br(),
            html.Br(),
        ], className="row")
    ])
])

# CALLBACKS
@app.callback(
    Output('result','children'),
    [Input('submeter', 'n_clicks')],
    [State('dia_semana','value'),State('causa_acidente','value'),State('tipo_acidente','value'),
    State('fase_dia','value'),State('condicao_meteorologica','value'),State('tipo_pista','value'),
    State('tracado_via','value'), State('solo','value'), State('pessoas','value'), State('veiculos','value'),
    State('mes','value'),State('modelo','value')]
)
def update_predicao(n_clicks,dia_semana_value,causa_acidente_value,tipo_acidente_value,fase_dia_value,condicao_meteorologica_value,tipo_pista_value,tracado_via_value, solo_value,pessoas_value,veiculos_value,mes_value,modelo_value):
    
    # ESCOLHA DO MODELO DE CLASSIFICAÇÃO
    if modelo_value==1:
        # LR
        teste = [dia_semana_value,causa_acidente_value,tipo_acidente_value,fase_dia_value,condicao_meteorologica_value,tipo_pista_value,tracado_via_value, solo_value,pessoas_value,veiculos_value,mes_value]
        print(teste)
        parameter_list=['dia_semana','causa_acidente','tipo_acidente','fase_dia','condicao_meteorologica','tipo_pista','tracado_via','uso_solo','pessoas','veiculos','mes']
        input_variables=pd.DataFrame([teste],columns=parameter_list,dtype=int)
        prediction = lr_clf1.predict(input_variables)
        print(prediction)

    if modelo_value ==2:
        # RF
        teste = [dia_semana_value,causa_acidente_value,tipo_acidente_value,condicao_meteorologica_value, solo_value,pessoas_value,veiculos_value,mes_value]
        print(teste)
        parameter_list=['dia_semana','causa_acidente','tipo_acidente','condicao_meteorologica','uso_solo','pessoas','veiculos','mes']
        input_variables=pd.DataFrame([teste],columns=parameter_list,dtype=int)
        prediction = rf_clf1.predict(input_variables)
        print(prediction)

    # RESULTADO
    if (prediction==[1]) :

        test = 'img/acidentec1.png'
        test_base64 = base64.b64encode(open(test, 'rb').read()).decode('ascii')

        return html.Div([
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(test_base64))
        ],  className="eight columns",
        )

    if (prediction==[2]) :

        test = 'img/acidentec2.png'
        test_base64 = base64.b64encode(open(test, 'rb').read()).decode('ascii')

        return html.Div([
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(test_base64))
        ],  className="eight columns",
        )   
    
    if (prediction==[3]):

        test = 'img/acidentec3.png'
        test_base64 = base64.b64encode(open(test, 'rb').read()).decode('ascii')

        return html.Div([
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(test_base64))
        ],  className="eight columns",
        ) 

@app.callback(
    Output('info_dia','children'),
    [Input('submeter','n_clicks')],
    [State('dia_semana','value')]
)
def update_dia_semana(n_clicks,dia_semana_value):
    dias = ['DOM','SEG','TER','QUA','QUI','SEX','SÁB']
    return dias[dia_semana_value-1]

@app.callback(
    Output('info_causa','children'),
    [Input('submeter','n_clicks')],
    [State('causa_acidente','value')]
)
def update_causa(n_clicks,causa_acidente_value):
    causa = ['Falta de atenção', 'Outras', 'Animais na pista', 'Defeito mecânico em veículo', 'Não guardar distância de segurança', 'Velocidade incompatível', 'Desobediência à sinalização', 'Ingestão de álcool', 'Defeito na via', 'Dormindo', 'Ultrapassagem indevida', 'Fenômenos da natureza', 'Avarias e/ou desgaste excessivo no pneu', 'Falta de atenção à condução', 'Desobediência às normas de trânsito pelo condutor', 'Restrição de visibilidade', 'Falta de atenção do pedestre', 'Condutor dormindo', 'Pista escorregadia', 'Sinalização da via insuficiente ou inadequada', 'Mal súbito', 'Carga excessiva e/ou mal acondicionada', 'Objeto estático sobre o leito carroçável', 'Deficiência de iluminação/sinalização do veículo', 'Ingestão de substâncias psicoativas', 'Agressão externa', 'Desobediência às normas de trânsito pelo pedestre', 'Ingestão de álcool e/ou substâncias psicoativas pelo pedestre']
    return causa[causa_acidente_value-1]

@app.callback(
    Output('info_tipo','children'),
    [Input('submeter','n_clicks')],
    [State('tipo_acidente','value')]
)
def update_tipo(n_clicks,tipo_acidente_value):
    tipo = ['Colisão frontal', 'Saída de pista', 'Atropelamento de animal', 'Capotamento', 'Colisão lateral', 'Atropelamento de pessoa', 'Colisão traseira', 'Colisão transversal', 'Tombamento', 'Colisão com objeto fixo', 'Danos eventuais', 'Queda de veículo', 'Derramamento de carga', 'Colisão com bicicleta', 'Colisão com objeto móvel', 'Incêndio', 'Queda de ocupante de veículo', 'Saída de leito carroçável', 'Colisão com objeto estático', 'Atropelamento de pedestre', 'Colisão com objeto em movimento', 'Engavetamento']
    return tipo[tipo_acidente_value-1]

@app.callback(
    Output('info_fase','children'),
    [Input('submeter','n_clicks')],
    [State('fase_dia','value')]
)
def update_fase(n_clicks,fase_dia_value):
    fase = ['Pleno Dia','Plena Noite','Amanhecer','Anoitecer']
    return html.H5(id='info_fase',children='('+fase[fase_dia_value-1]+')',style={'color':'#8d8d8d'})

@app.callback(
    Output('info_met','children'),
    [Input('submeter','n_clicks')],
    [State('condicao_meteorologica','value')]
)
def update_condicao_met(n_clicks,condicao_meteorologica_value):
    condicao = ['ceu claro', 'chuva', 'nublado', 'sol', 'neblina', 'vento', 'granizo', 'neve', 'chuvisco']
    met = condicao[condicao_meteorologica_value-1]

    tempo = 'img/'+met+'.png'
    tempo_base64 = base64.b64encode(open(tempo, 'rb').read()).decode('ascii')

    return html.Div([
            html.Img(src='data:image/png;base64,{}'.format(tempo_base64))
        ],
        ) 

@app.callback(
    Output('info_pista','children'),
    [Input('submeter','n_clicks')],
    [State('tipo_pista','value')]
)
def update_tipo_pista(n_clicks,tipo_pista_value):
    pista = ['Dupla','Simples','Múltipla']
    return html.H6(id='info_pista',children='Pista: '+pista[tipo_pista_value-1],style={'color':'#8d8d8d'}), 

@app.callback(
    Output('info_via','children'),
    [Input('submeter','n_clicks')],
    [State('tracado_via','value')]
)
def update_via(n_clicks,tracado_via_value):
    tracado = ['Reta', 'Curva', 'Cruzamento', 'Interseção de vias', 'Rotatória', 'Desvio temporário', 'Viaduto', 'Ponte', 'Retorno regulamentado', 'Túnel']
    return html.H6(id='info_via',children='Via: '+tracado[tracado_via_value-1],style={'color':'#8d8d8d'})

@app.callback(
    Output('info_solo','children'),
    [Input('submeter','n_clicks')],
    [State('solo','value')]
)
def update_solo(n_clicks,solo_value):
    solos = ['Rural','Urbano','Indefinido']
    return html.H6(id='info_solo',children='Zona: '+solos[solo_value-1],style={'color':'#8d8d8d'})

@app.callback(
    Output('info_pessoas','children'),
    [Input('submeter','n_clicks')],
    [State('pessoas','value')]
)
def update_pessoas(n_clicks,pessoas_value):
    return html.H6(id='info_pessoas',children=pessoas_value,style={'color':'#8d8d8d'}) 

@app.callback(
    Output('info_veiculos','children'),
    [Input('submeter','n_clicks')],
    [State('veiculos','value')]
)
def update_veiculos(n_clicks,veiculos_value):
    return html.H6(id='info_veiculos',children=veiculos_value,style={'color':'#8d8d8d'})

@app.callback(
    Output('info_mes','children'),
    [Input('submeter','n_clicks')],
    [State('mes','value')]
)
def update_mes(n_clicks,mes_value):
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    return meses[mes_value-1]

################################################################################################################################

# Callbacks
@app.callback(
    [
        Output(component_id='message', component_property='children'),
        Output(component_id='map-container', component_property='figure'),
        Input(component_id='anos', component_property='value'),
        Input(component_id='tipo', component_property='value')
    ]
)
def update_map(ano, tipo):
    
    container = [f"Mapa com número de {tipo} em: {ano}"]

    # Arquivo geojson com o shape do Brasil
    url = 'https://raw.githubusercontent.com/samuelamico/Mapas_Brasil/master/Mapas/Estados.geojson'
    with urlopen(url) as response:
        br = json.load(response)

    
    if tipo == 'acidentes':
        # Filtrando os dados com base no intervalo de entrada
        df_ano_uf = df[df['ano'] == ano]

        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.acidentes,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'acidentes'],
                        width=1000)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de acidentes",
                                                lenmode="pixels", len=200))


    df_ano_uf = df_pessoa[df_pessoa['ano'] == ano]

    if tipo == 'mortos':
        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.mortos,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'mortos'],
                        width=1000)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de mortes",
                                                lenmode="pixels", len=200))
    if tipo == 'mortos':
        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.mortos,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'mortos'],
                        width=1000)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de mortes",
                                                lenmode="pixels", len=200))


    if tipo == 'feridos':
        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.feridos,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'feridos'],
                        width=1000)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de feridos",
                                                lenmode="pixels", len=200))
           
    if tipo == 'ilesos':
        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.ilesos,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'ilesos'],
                        width=1000)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de ilesos",
                                                lenmode="pixels", len=200))


    return container, fig

################################################################################################################################
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
    Input('xaxis-column', 'value')])
    
def update_figure(selected_year, xaxis_value):
    if xaxis_value == 'causa_acidente':
        filtered_causa_df = df_causa_acidente[df_causa_acidente.ano == selected_year]
        # Faz uma contagem da quantidade de acidentes por tipo de acidente        

        fig = px.bar(filtered_causa_df, x="causa_acidente", y="Qtd Acidentes")
        fig.update_traces(marker_color='rgb(16, 141, 228)')

        fig.update_layout(transition_duration=500)

        return fig
    elif xaxis_value == 'tipo_acidente':
        filtered_tipo_df = df_tipo_acidente[df_tipo_acidente.ano == selected_year]
        # Faz uma contagem da quantidade de acidentes por tipo de acidente        


        fig = px.bar(filtered_tipo_df, x="tipo_acidente", y="Qtd Acidentes")
        fig.update_traces(marker_color='rgb(16, 141, 228)')

        fig.update_layout(transition_duration=500)

        return fig

####################################################################################################################################

#Faz com que atualize automaticamente após as mudanças
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column2', 'value'),
     Input('year--slider', 'value')])

def update_graph(xaxis_column,year_value):
    dff = df_pessoa[df_pessoa['ano'] == year_value]
    dff = dff.set_index('uf')
    dff = dff.sort_values(by=xaxis_column, ascending=False)
    #print(dff.info())
    #Gráfico de colunas
    fig = px.bar(dff ,x=dff.index, y=xaxis_column)
    fig.update_traces(marker_color='rgb(16, 141, 228)')
    

    fig.update_layout(transition_duration=500)
    return fig

######################################################################################################################################

#Faz com que atualize automaticamente após as mudanças
@app.callback(
    Output('indicador-graphic', 'figure'),
    [Input('xaxiss-column', 'value'),
     Input('ano--slider', 'value')])
def update_graph(xaxis_column,year_value):
    dff = dfano[dfano['ano'] == year_value]
  
    #Gráfico de colunas
    fig = px.bar(dff,x=dff['mes'],y=xaxis_column)
    fig.update_traces(marker_color='rgb(16, 141, 228)')

    fig.update_layout(transition_duration=500)
    return fig


######################################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=True)