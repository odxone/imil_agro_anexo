# Cenário Econômico

Fonte: SGS Banco Central do Brasil

Nestes dois primeiros Capítulos foram plotadas informações macro econômicas sobre a perspectiva do setor agropecuário. Para analisar o cenário econômico foram utilizadas séries do IBGE do repositório SGS do Banco Central do Brasil, obtidos através de API.

## Carregando bibliotecas

#dados
import sgs

#manipulacao de dados
import pandas as pd

#graphs
import altair as alt

series = [7326]
labels = ['PIB_variação_real_ano']
data_inicial ='31-12-1962'
data_final = '31-12-2020'
PIB_variação= sgs.dataframe(series, start= data_inicial, end=data_final)
PIB_variação= PIB_variação.rename(columns={s:l for s, l in zip(series, labels)})

vermelho, azul = "#ae1325", "#1a1e76"

def highlight_breakpoint(campo, breakpoint=0, colors=(vermelho,azul)):
    return alt.condition(f"datum.{campo} <= {breakpoint}", alt.value(vermelho), alt.value(azul))

fig = (
    alt.Chart(
        PIB_variação.reset_index(),
        title='Variação real anual do PIB',
        width=800,
        height=400)
    .mark_bar(width=10)
    .encode(
        x = alt.X('index:T', title='Período'),
        y = alt.Y('PIB_variação_real_ano:Q', title='Variação percentual'),
        color=highlight_breakpoint("PIB_variação_real_ano"),
        tooltip=alt.Tooltip(['index:T', 'PIB_variação_real_ano:Q'])
    )
)
fig

series = [4380]
labels = ['PIB_valores']
data_inicial ='31-12-1990'
data_final = '31-12-2020'
PIB_valores = sgs.dataframe(series, start= data_inicial, end=data_final)
PIB_valores = PIB_valores.rename(columns={s:l for s, l in zip(series, labels)})

fig = (
    alt.Chart(
        PIB_valores.reset_index(),
        title="PIB mensal em valores correntes",
        width=800,
        height=400,
    ).mark_area().encode(
        x=alt.X('index:T', title="Período"),
        y=alt.Y('PIB_valores:Q', title="Trilhões de R$"),
    ).configure_mark(color=azul)
)
fig

series = [7327,7329,7328]
labels = ['PIB_agro','PIB_serviços','PIB_indústria']
data_inicial ='01-01-2015'
data_final = '31-12-2020'
PIB_setor = sgs.dataframe(series, start= data_inicial, end=data_final)
PIB_setor= PIB_setor.rename(columns={s:l for s, l in zip(series, labels)})

PIB_setor.head()

fig = (
    alt.Chart(
        PIB_setor['PIB_agro'].reset_index(),
        title='Variação anual do PIB da Agropecuária',
        width=800,
        height=400)
    .mark_bar(width=90)
    .encode(
        x = alt.X('year(index):T', title='Período'),
        y = alt.Y('PIB_agro:Q', title='Variação percentual'),
        color=highlight_breakpoint("PIB_agro"),
        tooltip=alt.Tooltip(['year(index):T', 'PIB_agro:Q'])
    )
)
fig

fig = (
    alt.Chart(
        PIB_setor['PIB_serviços'].reset_index(),
        title='Variação anual do PIB de Serviços',
        width=800,
        height=400)
    .mark_bar(width=90)
    .encode(
        x = alt.X('year(index):T', title='Período'),
        y = alt.Y('PIB_serviços:Q', title='Variação percentual'),
        color=highlight_breakpoint("PIB_serviços"),
        tooltip=alt.Tooltip(['year(index):T', 'PIB_serviços:Q'])
    )
)
fig

fig = (
    alt.Chart(
        PIB_setor['PIB_indústria'].reset_index(),
        title='Variação anual do PIB da Indústria',
        width=800,
        height=400)
    .mark_bar(width=90)
    .encode(
        x = alt.X('year(index):T', title='Período'),
        y = alt.Y('PIB_indústria:Q', title='Variação percentual'),
        color=highlight_breakpoint("PIB_indústria"),
        tooltip=alt.Tooltip(['year(index):T', 'PIB_indústria:Q'])
    )
)
fig