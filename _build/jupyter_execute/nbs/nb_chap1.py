# Cenário Econômico

Fonte: SGS Banco Central do Brasil

Nestes dois primeiros Capítulos foram plotadas informações macro econômicas sobre a perspectiva do setor agropecuário. Para analisar o cenário econômico foram utilizadas séries do IBGE do repositório SGS do Banco Central do Brasil, obtidos através de API.

## Carregando bibliotecas

#dados
import sgs

#manipulacao de dados
import pandas as pd

#graphs
import plotly.graph_objs as go
import plotly.offline as py
import cufflinks as cf

py.init_notebook_mode(connected=True)
cf.go_offline()

series = [7326]
labels = ['PIB_variação_real_ano']
data_inicial ='31-12-1962'
data_final = '31-12-2020'
PIB_variação= sgs.dataframe(series, start= data_inicial, end=data_final)
PIB_variação= PIB_variação.rename(columns={s:l for s, l in zip(series, labels)})

cores = []
for x in PIB_variação['PIB_variação_real_ano']:
    if x < 0:
        cores.append('red')
    else:
        cores.append('blue')

data = [go.Bar(x=PIB_variação.index,
               y=PIB_variação['PIB_variação_real_ano'],
               marker = {'color': cores,
                         'line': {'color': '#333',
                                  'width': 2}
                        },
               opacity= 0.9
              )
       ]
configuracoes_layout = go.Layout(title='Variação real anual do PIB',
                                 yaxis={'title':'Variação percentual'},
                                 xaxis={'title':'Período'})
fig = go.Figure(data=data, layout=configuracoes_layout)
py.iplot(fig)

series = [4380]
labels = ['PIB_valores']
data_inicial ='31-12-1990'
data_final = '31-12-2020'
PIB_valores = sgs.dataframe(series, start= data_inicial, end=data_final)
PIB_valores = PIB_valores.rename(columns={s:l for s, l in zip(series, labels)})

PIB_valores['PIB_valores']=PIB_valores['PIB_valores']/100000
PIB_valores.iplot(kind='bar', color='Darkblue', title='PIB Mensal em valores correntes em trilhões de reais')

series = [7327,7329,7328]
labels = ['PIB_agro','PIB_serviços','PIB_indústria']
data_inicial ='01-01-2015'
data_final = '31-12-2020'
PIB_setor = sgs.dataframe(series, start= data_inicial, end=data_final)
PIB_setor= PIB_setor.rename(columns={s:l for s, l in zip(series, labels)})

PIB_setor.head()

cores = []
for x in PIB_setor['PIB_agro']:
    if x < 0:
        cores.append('red')
    else:
        cores.append('blue')

data = [go.Bar(x=PIB_setor.index,
               y=PIB_setor['PIB_agro'],
               marker = {'color': cores,
                         'line': {'color': '#333',
                                  'width': 2}
                        },
               opacity= 0.9
              )
       ]
configuracoes_layout = go.Layout(title='Variação anual do PIB da Agropecuária',
                                 yaxis={'title':'Variação percentual'},
                                 xaxis={'title':'Período'})
fig = go.Figure(data=data, layout=configuracoes_layout)
py.iplot(fig)

cores = []
for x in PIB_setor['PIB_serviços']:
    if x < 0:
        cores.append('red')
    else:
        cores.append('blue')

data = [go.Bar(x=PIB_setor.index,
               y=PIB_setor['PIB_serviços'],
               marker = {'color': cores,
                         'line': {'color': '#333',
                                  'width': 2}
                        },
               opacity= 0.9
              )
       ]
configuracoes_layout = go.Layout(title='Variação anual do PIB da Serviços',
                                 yaxis={'title':'Variação percentual'},
                                 xaxis={'title':'Período'})
fig = go.Figure(data=data, layout=configuracoes_layout)
py.iplot(fig)

cores = []
for x in PIB_setor['PIB_indústria']:
    if x < 0:
        cores.append('red')
    else:
        cores.append('blue')

data = [go.Bar(x=PIB_setor.index,
               y=PIB_setor['PIB_indústria'],
               marker = {'color': cores,
                         'line': {'color': '#333',
                                  'width': 2}
                        },
               opacity= 0.9
              )
       ]
configuracoes_layout = go.Layout(title='Variação anual do PIB da Indústria',
                                 yaxis={'title':'Variação percentual'},
                                 xaxis={'title':'Período'})
fig = go.Figure(data=data, layout=configuracoes_layout)
py.iplot(fig)