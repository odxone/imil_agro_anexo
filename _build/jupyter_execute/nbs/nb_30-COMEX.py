# Balança Comercial

Fonte: [SECINT e SEPEC](https://www.gov.br/produtividade-e-comercio-exterior/pt-br/assuntos/comercio-exterior/estatisticas/base-de-dados-bruta)

Os dados descritos nessa fonte são extensos. O código utilizado para resumir os dados está descrito no final desse documento e os resultados dessa agregação, que são utilizados no documento, estão disponiveis [aqui](https://github.com/feliciov/agro_online/tree/main/nbs/data_comex).

## Carregamento das bibliotecas

# download e manipulacao dos dados
import pandas as pd
import requests

# graficos
import altair as alt

# utilitarios
from datetime import datetime
from functools import reduce
from io import BytesIO

## Carregamento dos dados

df_exp = pd.read_pickle("https://github.com/feliciov/agro_online/raw/main/nbs/data_comex/grouped_exp.pkl.xz")
df_imp = pd.read_pickle("https://github.com/feliciov/agro_online/raw/main/nbs/data_comex/grouped_imp.pkl.xz")

caminho_tabelas_conversao = "https://balanca.economia.gov.br/balanca/bd/tabelas/TABELAS_AUXILIARES.xlsx"

# download das tabelas de conversões. verify=False porque o certificado de segurança 
# do www.gov.br está comunmente off e sem isso o download falha
excel_conversao = requests.get(caminho_tabelas_conversao, verify=False).content

df_vias = pd.read_excel(BytesIO(excel_conversao), sheet_name='15')

## Exportação

### por Categoria ISIC

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

### Agro por Bloco Destino

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

### Agro por Vias de Escoamento

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

### por Unidade da Federação

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

### AGRO por Unidade da Federação

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

### Agro por Categoria CUCI

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

## Importação

### por Categoria ISIC

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

### Agro por Bloco de Origem

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

### por Unidade da Federação

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

### Agro por Unidade da Federação

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

### Agro por Categoria CUCI

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

## Código para Download e tratamento das bases extensas

```python
caminho_tabelas_conversao = "https://balanca.economia.gov.br/balanca/bd/tabelas/TABELAS_AUXILIARES.xlsx"

# download das tabelas de conversões. verify=False porque o certificado de segurança 
# do www.gov.br está comunmente off e sem isso o download falha
excel_conversao = requests.get(caminho_tabelas_conversao, verify=False).content

df_conversao_ncm_isic = pd.read_excel(BytesIO(excel_conversao), sheet_name="4")[['CO_NCM', 'NO_ISIC_SECAO']]
df_conversao_ncm_cuci = pd.read_excel(BytesIO(excel_conversao), sheet_name="17")[['CO_NCM', 'NO_CUCI_GRUPO']]
df_vias = pd.read_excel(BytesIO(excel_conversao), sheet_name='15')

# a lista dos países/bloco precisa de intervenção
df_conversao_blocos = pd.read_excel(BytesIO(excel_conversao), sheet_name="12")[['CO_PAIS', 'NO_BLOCO']]

df_conversao_blocos = df_conversao_blocos[df_conversao_blocos.NO_BLOCO.isin(
    ['África', 'América Central e Caribe', 'América do Norte',
       'América do Sul', 'Ásia (Exclusive Oriente Médio)',
       'Europa', 'Oceania', 'Oriente Médio']
)]

# efetivamente, essas linhas removem os países em duplicidade, listados uma segunda vez nos grupos economicos
# 'Associação de Nações do Sudeste Asiático - ASEAN'
# 'Mercado Comum do Sul - Mercosul'
# 'União Europeia - UE'
```

As bases originais são relativamente extensas (~350 e ~450Mb). O código abaixo foi escrito para reduzir a necessidade de memória durante sua execução. Assume-se que o usuário carregou as bases de dados e modificou os caminhos para refletir o local em seu computador.

Caso a máquina onde o código será executado tenha capacidade, é possível ler e executar as uniões em um só passo. Nesse caso, fica a cargo do usuário realizar as modificações.

```python
caminho_dados_exportacao = "CAMINHO_NO_SEU_COMPUTADOR.csv"
caminho_dados_importacao = "OUTRO_CAMINHO.csv"

# exportacao
partials = []

for chunk in pd.read_csv(
    caminho_dados_exportacao,
    sep=';',
    chunksize=300_000 # numero de linhas para calcular em cada passo
):
    df_chunk = chunk.merge(df_conversao_ncm_isic, on="CO_NCM", how='left')
    df_chunk = df_chunk.merge(df_conversao_ncm_cuci, on="CO_NCM", how='left')
    df_chunk = df_chunk.merge(df_grupo_pais, on='CO_PAIS', how='left')
    df_chunk = df_chunk.fillna('Grupo não Identificado').groupby(
        ['CO_ANO', 'CO_MES', 'SG_UF_NCM', 'NO_BLOCO', 'CO_VIA', 'NO_ISIC_SECAO', 'NO_CUCI_GRUPO'])['VL_FOB'].sum()
    
    partials.append(df_chunk)

df_exp = reduce(lambda l, r: pd.concat([l, r]), [p.reset_index() for p in partials])
# outro groupby para resolver possiveis problemas nas bordas dos chunks
df_exp = (
    df_exp.groupby(
        ['CO_ANO', 'CO_MES', 'SG_UF_NCM', 'NO_BLOCO', 'CO_VIA', 'NO_ISIC_SECAO', 'NO_CUCI_GRUPO']
        )['VL_FOB'].sum()
        .reset_index()
        )


# importacao
partials = []

for chunk in pd.read_csv(
    caminho_dados_importacao,
    sep=';',
    chunksize=300_000 # numero de linhas para calcular em cada passo
):
    df_chunk = chunk.merge(df_conversao_ncm_isic, on="CO_NCM", how='left')
    df_chunk = df_chunk.merge(df_conversao_ncm_cuci, on="CO_NCM", how='left')
    df_chunk = df_chunk.merge(df_grupo_pais, on='CO_PAIS', how='left')
    df_chunk = df_chunk.fillna('Grupo não Identificado').groupby(
        ['CO_ANO', 'CO_MES', 'SG_UF_NCM', 'NO_BLOCO', 'CO_VIA', 'NO_ISIC_SECAO', 'NO_CUCI_GRUPO'])['VL_FOB'].sum()
    
    partials.append(df_chunk)

df_imp = reduce(lambda l, r: pd.concat([l, r]), [p.reset_index() for p in partials])
# outro groupby para resolver possiveis problemas nas bordas dos chunks
df_imp = (
    df_imp.groupby(
        ['CO_ANO', 'CO_MES', 'SG_UF_NCM', 'NO_BLOCO', 'CO_VIA', 'NO_ISIC_SECAO', 'NO_CUCI_GRUPO']
        )['VL_FOB'].sum()
        .reset_index()
        )

del partials
```

