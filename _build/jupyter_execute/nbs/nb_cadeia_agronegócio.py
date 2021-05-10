# Mensurando toda a cadeia do Agronegócios

Fonte: As bases de dados utilizadas neste capítulo estão disponíveis no [repositório do CEPEA ESALQ/USP](https://www.cepea.esalq.usp.br/br/pib-do-agronegocio-brasileiro.aspx)

## Carregando bibliotecas

# carregamento e manipulação de dados
import pandas as pd
import numpy as np

# utils
from datetime import datetime

# graphs
import altair as alt

# formatando numeros em tabelas
pd.set_option('display.float_format', lambda x: '%.2f' % x)

## Carregando Dados

agronegócio=(
    pd.read_excel(
        "https://www.cepea.esalq.usp.br/upload/kceditor/files/Planilha_PIB_Cepea_Portugues_Site_2020.xlsx",
        sheet_name='PIB',
        skiprows=7,
        skipfooter=2)
    [['Unnamed: 0', '(A) Insumos', '(B) Agropecuária ', '(C) Indústria','(D) Serviços']]
)

agronegócio=(
    agronegócio.rename(
        columns={
            'Unnamed: 0':'Data',
            '(A) Insumos':'Insumos Agrícolas',
            '(B) Agropecuária ':'Agropecuária',
            '(C) Indústria':'Agro Indústria',
            '(D) Serviços':'Agro Serviços'})
)
agronegócio.info()

agronegócio['Data']=agronegócio.Data.apply(lambda row:datetime(row,1,1))
agronegócio.head()

agronegócio_variação=(
    pd.read_excel(
        "https://www.cepea.esalq.usp.br/upload/kceditor/files/Planilha_PIB_Cepea_Portugues_Site_2020.xlsx",
        sheet_name='VARIAÇÃO',
        skiprows=7,
        skipfooter=2)
    [['Unnamed: 0', '(A) Insumos', '(B) Agropecuária ', '(C) Indústria','(D) Serviços']]
).rename(
    columns={
        'Unnamed: 0':'Data',
        '(A) Insumos':'Insumos_Agrícolas',
        '(B) Agropecuária ':'Agropecuária',
        '(C) Indústria':'Agroindústria',
        '(D) Serviços':'Agrosserviços'}
)
agronegócio_variação.info()

agronegócio_variação['Data']=agronegócio_variação.Data.apply(lambda row:datetime(row,1,1))
agronegócio_variação.tail()

vermelho, azul = "#ae1325", "#1a1e76"

def highlight_breakpoint(campo, breakpoint=0, colors=(vermelho,azul)):
    return alt.condition(f"datum.{campo} <= {breakpoint}", alt.value(vermelho), alt.value(azul))

fig = (
    alt.Chart(
        agronegócio_variação,
        title='Variação anual Insumos Agrícolas',
        width=800,
        height=400
    ).mark_bar().encode(
        x=alt.X('year(Data):T', title="Período"),
        y=alt.Y('Insumos_Agrícolas:Q', title="Variação Percentual"),
        color=highlight_breakpoint("Insumos_Agrícolas"),
        tooltip=['year(Data):T', 'Insumos_Agrícolas:Q']
    )
)
fig

fig = (
    alt.Chart(
        agronegócio_variação,
        title='Variação anual Agro Indústria',
        width=800,
        height=400
    ).mark_bar().encode(
        x=alt.X('year(Data):T', title="Período"),
        y=alt.Y('Agroindústria:Q', title="Variação Percentual"),
        color=highlight_breakpoint("Agroindústria"),
        tooltip=['year(Data):T', 'Agroindústria:Q']
    )
)
fig

fig = (
    alt.Chart(
        agronegócio_variação,
        title='Variação anual Agro Pecuária',
        width=800,
        height=400
    ).mark_bar().encode(
        x=alt.X('year(Data):T', title="Período"),
        y=alt.Y('Agropecuária:Q', title="Variação Percentual"),
        color=highlight_breakpoint("Agropecuária"),
        tooltip=['year(Data):T', 'Agrospecuária:Q']
    )
)
fig

fig = (
    alt.Chart(
        agronegócio_variação,
        title='Variação anual Agro Serviços',
        width=800,
        height=400
    ).mark_bar().encode(
        x=alt.X('year(Data):T', title="Período"),
        y=alt.Y('Agrosserviços:Q', title="Variação Percentual"),
        color=highlight_breakpoint("Agrosserviços"),
        tooltip=['year(Data):T', 'Agrosserviços:Q']
    )
)
fig

