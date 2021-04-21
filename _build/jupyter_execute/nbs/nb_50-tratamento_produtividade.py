# Produtividade na Agricultura

Os dados utilizados nessa análise vieram da [tabela 6588, do Levantamento Sistemático da Produção Agrícula](https://sidra.ibge.gov.br/tabela/6588) do IBGE.


## Carregamento de bibliotecas

#download e manipulacao dos dados
import pandas as pd
import numpy as np

#graficos
import altair as alt

#painel interativo
import panel as pn

#utilidades
from datetime import datetime

pn.extension('vega')

## Carregamento e tratamento dos dados

# caminho utilizado para download dos dados utilizando a API do IBGE
path_lspa = 'https://sidra.ibge.gov.br/geratabela?format=us.csv&name=tabela6588.csv&terr=N&rank=-&query=t/6588/n1/all/v/all/p/first%20173/c48/all/l/,,p%2Bv%2Bc48%2Bt'

lspa = pd.read_csv(
    path_lspa,
    skiprows=1,
    skipfooter=18,
    engine='python',
    na_values=["...", "-"],
    parse_dates=['Mês'],
    dtype={
        'Variável': str,
        'Produto das lavouras': str,
        'Área': str,
        'Valor': np.float64,
    }
)

lspa.head()

lspa.info()

Alguns dos dados precisam ser convertidos e transformados para formatos mais úteis.

Abaixo, fazemos essas transformações.

lspa = lspa.rename(columns={'Unnamed: 3':"Unidade Territorial", 'Unnamed: 4':"Valor"
})

FULL_MONTHS = {'janeiro': 1,  'fevereiro': 2, 'março': 3,    'abril': 4,
               'maio': 5,     'junho': 6,     'julho': 7,     'agosto': 8,
               'setembro': 9, 'outubro': 10,  'novembro': 11, 'dezembro': 12}

lspa['Mês'] = lspa['Mês'].str.split(' ').apply(lambda row: datetime(int(row[1]), FULL_MONTHS[row[0]], 1))

lspa['Unidade Territorial'].unique()

Só solicitamos os dados a nível Nacional, a coluna não agrega nenhuma informação e será dropada

lspa = lspa.drop(columns=['Unidade Territorial'])

Os produtos listados abaixo tiveram uma quebra significativa de metologia no meio do período.

Os dados relativos a esses produtos são descartados.

produtos_dropados = [
    '2 Abacaxi', '3 Alho', '13 Cebola',
    '14 Coco-da-baía', '16 Guaraná', '19 Maçã',
    '20 Malva', '22 Pimenta-do-reino', '23 Sisal ou agave', 'Total'
]

lspa = lspa[~lspa['Produto das lavouras'].isin(produtos_dropados)]

## Preparação dos Gráficos

def plot_producao(df, produto):
    dataf = df[
        (df['Variável'] == 'Produção (Toneladas)') &
        (df['Produto das lavouras'] == produto)
    ]

    return alt.Chart(dataf).mark_line().encode(
        x=alt.X("Mês:T", title='Período'),
        y=alt.Y('Valor:Q', title='Toneladas'),
        tooltip=alt.Tooltip(["Mês:T", 'Valor:Q'])
    ).properties(
        title=f"{produto} - Produção"
    )

def plot_areas(df, produto):
    dataf = df[
        (df['Variável'].isin(['Área plantada (Hectares)', 'Área colhida (Hectares)'])) &
        (df['Produto das lavouras'] == produto)
    ]

    return alt.Chart(dataf).mark_line().encode(
        x=alt.X("Mês:T", title='Período'),
        y=alt.Y("Valor:Q", title='Hectares'),
        color=alt.Color("Variável:N"),
        tooltip=alt.Tooltip(["Mês:T", "Valor:Q", "Variável:N"])
    ).properties(
        title=f"{produto} - Áreas"
    )

def plot_rendimento(df, produto):
    dataf = df[
        (df['Variável'] == 'Rendimento médio (Quilogramas por Hectare)') &
        (df['Produto das lavouras'] == produto)
    ]

    return alt.Chart(dataf).mark_line().encode(
        x=alt.X("Mês:T", title="Período"),
        y=alt.Y("Valor:Q", title="Kg/hectare"),
        tooltip=alt.Tooltip(["Mês:T", "Valor:Q"])
    ).properties(
        title=f"{produto} - Rendimento médio"
    )


def plot_produto(df, produto):
    graph_prod = plot_producao(df, produto)
    graph_areas = plot_areas(df, produto)
    graph_rendimento = plot_rendimento(df, produto)
    
    return alt.hconcat(graph_prod, graph_areas, graph_rendimento)

## Gráficos

lspa['Produto das lavouras'].unique()
# lista de opções de produtos na base carregada

plot_produto(lspa, '11 Cana-de-açúcar')

plot_produto(lspa, '1.15 Soja')

plot_produto(lspa, '1.4 Arroz')

## Preparação do painel interativo

O código a seguir foi escrito para execução em um kernel ativo. Sem esse kernel (que é o caso de quem está visualizando esse notebook no GitHub Pages) o painel não funciona.

def plot_grafico_produto(tipo_grafico, Produto, dados=lspa):
    tipos = {
        'producao': plot_producao,
        'areas': plot_areas,
        'rendimento': plot_rendimento,
    }
    
    return tipos[tipo_grafico](dados, Produto)

lspa.head()

panel = pn.interact(
    plot_grafico_produto,
    tipo_grafico=pn.widgets.Select(
        options={
            "Produção":'producao', 
            "Áreas Plantada/Colhida":'areas', 
            "Rendimento médio por Hectare":'rendimento',},
        name="Tipo de Gráfico"
    ),
    Produto=lspa['Produto das lavouras'].unique().tolist()
)

## Painel Interativo

pn.Row(panel[0], panel[1])

