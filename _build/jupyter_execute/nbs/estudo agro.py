<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Bibliotecas" data-toc-modified-id="Bibliotecas-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Bibliotecas</a></span></li><li><span><a href="#Cenário-Econômico" data-toc-modified-id="Cenário-Econômico-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Cenário Econômico</a></span></li><li><span><a href="#Valor-adicionado-por-setor" data-toc-modified-id="Valor-adicionado-por-setor-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Valor adicionado por setor</a></span></li><li><span><a href="#Agropecuária-em-Valores" data-toc-modified-id="Agropecuária-em-Valores-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Agropecuária em Valores</a></span></li><li><span><a href="#Mensurando-toda-a-cadeia-do-Agronegócios" data-toc-modified-id="Mensurando-toda-a-cadeia-do-Agronegócios-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Mensurando toda a cadeia do Agronegócios</a></span></li><li><span><a href="#Produtividade-Agropecuária" data-toc-modified-id="Produtividade-Agropecuária-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Produtividade Agropecuária</a></span></li></ul></div>

## Bibliotecas

import pandas as pd

**Séries do Banco Central do Brasil**

import sgs

**Pacotes de visualização**

import seaborn as sns
import cufflinks as cf
import plotly.express as px
import itertools
from itertools import product
from plotly.offline import iplot
import plotly.graph_objs as go
from scipy import stats
import plotly.offline as py
import plotly.offline as py
import plotly.graph_objs as go
import plotly

plotly.offline.init_notebook_mode(connected=True)
cf.go_offline()

**Geo**

import geopandas as gpd
from libpysal.weights.contiguity import Queen
import libpysal
from libpysal import examples
import pygeoda
import matplotlib
import matplotlib.pyplot as plt
import geopandas as gpd
%matplotlib inline
from splot.libpysal import plot_spatial_weights

## Cenário Econômico

- Foram utilizadas 

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

## Valor adicionado por setor

series_VA = [22105,22106,22107,22110]
labels_VA = ['PIB_Agropecuária','PIB_Indústria','PIB_serviços','Consumo_das_famílias']
data_inicial ='01-01-1996'
data_final = '01-01-2021'
Valor_adicionado_por_setor = sgs.dataframe(series_VA, start= data_inicial, end=data_final)
Valor_adicionado_por_setor = Valor_adicionado_por_setor.rename(columns={s:l for s, l in zip(series_VA, labels_VA)})

Valor_adicionado_por_setor.head()

Valor_adicionado_por_setor.iplot(title= 'PIB Trimestral por Setor- Dados dessazonalizados')

shape=gpd.read_file('C:/Users/agend/Desktop/Estudo_virtual/mun_agro.shp')
shape.head(2)

fig, ax = plt.subplots(figsize=(12,12), subplot_kw={'aspect':'equal'})
shape.plot(column='V2', scheme='Quantiles', k=7,cmap='OrRd',legend=True, ax=ax),ax.set_title("Área média por município(Agropecuária)", fontdict={'fontsize':25}),ax.set_xlabel(' ', fontdict={'fontsize':20}),ax.set_facecolor('lightgrey'),ax.spines['bottom'].set_linewidth(5.5)
fig.tight_layout()

regioes=pd.read_csv("C:/Users/agend/Desktop/Estudo Agro/bases/regioes_agro.csv", sep = ";", encoding='latin-1')
mapa=pd.merge(shape,regioes,on=['OBJECTID'],how='left')
mapa.head()

fig = px.box(mapa, x=mapa['Estado'], y=mapa['V2'], color=mapa['Região'],title="Área Média(ha) por município")
fig.show()



## Agropecuária em Valores

## Mensurando toda a cadeia do Agronegócios

## Produtividade Agropecuária

