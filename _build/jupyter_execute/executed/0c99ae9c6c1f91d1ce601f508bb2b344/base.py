# download e manipulacao dos dados
import pandas as pd
import requests

# graficos
import altair as alt

# utilitarios
from datetime import datetime
from functools import reduce
from io import BytesIO

df_exp = pd.read_pickle("https://github.com/feliciov/agro_online/raw/main/nbs/data_comex/grouped_exp.pkl.xz")
df_imp = pd.read_pickle("https://github.com/feliciov/agro_online/raw/main/nbs/data_comex/grouped_imp.pkl.xz")

caminho_tabelas_conversao = "https://balanca.economia.gov.br/balanca/bd/tabelas/TABELAS_AUXILIARES.xlsx"

# download das tabelas de conversões. verify=False porque o certificado de segurança 
# do www.gov.br está comunmente off e sem isso o download falha
excel_conversao = requests.get(caminho_tabelas_conversao, verify=False).content

df_vias = pd.read_excel(BytesIO(excel_conversao), sheet_name='15')

fig = (
    alt.Chart(
        df_exp[df_exp['CO_ANO'] != 2021]
        .groupby(['CO_ANO', 'NO_ISIC_SECAO'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line(point=True)
    .encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('NO_ISIC_SECAO:N', title="Categoria ISIC"),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'NO_ISIC_SECAO:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_exp[(df_exp['CO_ANO'] != 2021) &
               (df_exp['NO_ISIC_SECAO'] == "Agropecuária")]
        .groupby(['CO_ANO', 'NO_BLOCO'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line().encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('NO_BLOCO', title='Bloco de Países'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'NO_BLOCO:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_exp[(df_exp['CO_ANO'] != 2021) &
               (df_exp['NO_ISIC_SECAO'] == "Agropecuária")]
        .merge(df_vias, on='CO_VIA')
        .groupby(['CO_ANO', 'NO_VIA'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line().encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('NO_VIA', title='Via de escoamento'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'NO_VIA:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_exp[(df_exp['CO_ANO'] != 2021)]
        .merge(df_vias, on='CO_VIA')
        .groupby(['CO_ANO', 'SG_UF_NCM'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line().encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('SG_UF_NCM', title='Estado Origem'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'SG_UF_NCM:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_exp[(df_exp['CO_ANO'] != 2021) &
               (df_exp['NO_ISIC_SECAO'] == "Agropecuária")]
        .merge(df_vias, on='CO_VIA')
        .groupby(['CO_ANO', 'SG_UF_NCM'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line().encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('SG_UF_NCM', title='Estado Origem'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'SG_UF_NCM:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_exp[(df_exp['CO_ANO'] != 2021) &
               (df_exp['NO_ISIC_SECAO'] == "Agropecuária")]
        .merge(df_vias, on='CO_VIA')
        .groupby(['CO_ANO', 'NO_CUCI_GRUPO'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line().encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('NO_CUCI_GRUPO', title='Categoria CUCI'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'NO_CUCI_GRUPO:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_imp[df_imp['CO_ANO'] != 2021]
        .groupby(['CO_ANO', 'NO_ISIC_SECAO'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line(point=True)
    .encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('NO_ISIC_SECAO:N', title="Categoria ISIC"),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'NO_ISIC_SECAO:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_imp[(df_imp['CO_ANO'] != 2021) &
               (df_imp['NO_ISIC_SECAO'] == "Agropecuária")]
        .groupby(['CO_ANO', 'NO_BLOCO'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line().encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('NO_BLOCO', title='Bloco de Países'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'NO_BLOCO:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_imp[(df_imp['CO_ANO'] != 2021)]
        .merge(df_vias, on='CO_VIA')
        .groupby(['CO_ANO', 'SG_UF_NCM'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line().encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('SG_UF_NCM', title='Estado Origem'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'SG_UF_NCM:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_imp[(df_imp['CO_ANO'] != 2021) &
               (df_imp['NO_ISIC_SECAO'] == "Agropecuária")]
        .merge(df_vias, on='CO_VIA')
        .groupby(['CO_ANO', 'SG_UF_NCM'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line(point=True).encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('SG_UF_NCM', title='UF Destino'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'SG_UF_NCM:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

fig = (
    alt.Chart(
        df_imp[(df_imp['CO_ANO'] != 2021) &
               (df_imp['NO_ISIC_SECAO'] == "Agropecuária")]
        .merge(df_vias, on='CO_VIA')
        .groupby(['CO_ANO', 'NO_CUCI_GRUPO'])['VL_FOB'].sum()
        .reset_index()
    ).mark_line().encode(
        alt.X('CO_ANO:N', title='Ano'),
        alt.Y('FOB:Q', title='milhões de US$'),
        alt.Color('NO_CUCI_GRUPO', title='Categoria CUCI'),
        alt.Tooltip(['CO_ANO:N', 'FOB:Q', 'NO_CUCI_GRUPO:N'])
    ).transform_calculate(FOB='datum.VL_FOB/1000000')
)
fig

