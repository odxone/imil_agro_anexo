# Análise dos empregos formais

O BACEN disponibiliza séries trimestrais dessasonalizadas do CAGED no [Sistema Gerador de Séries Temporais](https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries)(SGST).

Os dados utilizados nessa análise foram coletados via API do SGST, utilizando a biblioteca `sgs`.

## Importando bibliotecas

# manipulação de dados
import pandas as pd
import numpy as np

# acesso a api do SGST
import sgs

# gráficos
import altair as alt

## Download dos dados

A janela máxima de dados solicitada está descrita abaixo. No caso em que as séries não estão disponíveis por todo o período, os dados parciais foram utilizados

start_date = "01/01/1960"
end_date = "01/01/2021"

# numero das séries de interesse
codigos_novo_caged_dessasonalizados = [
    28784, 28785, 28786, 28787,
    28788, 28789, 28790, 28791,
    28792, 28793, 28794, 28795,
    28796, 28797, 28798, 28799,
    28800, 28801, 28802, 28803,
    28804,
]

emprego_dessaz = sgs.dataframe(codigos_novo_caged_dessasonalizados, start_date, end_date)

## Transformações pré-análise

As séries são retornadas nomeadas com os seus respectivos códigos. Abaixo, renomeamos para nomes mais informativos.

rename_dict = {
    'index':'Trimestre',
    28763 :'Total',
    28764 :'Agropecuária',
    28765 :'Indústrias extrativas',
    28766 :'Indústrias de transformação',
    28767 :'SIUP',
    28768 :'Eletricidade e gás',
    28769 :'Água, esgoto e gestão de resíduos',
    28770 :'Construção',
    28771 :'Comércio',
    28772 :'Serviços',
    28773 :'Transporte, armazenamento e correio',
    28774 :'Alojamento e alimentação',
    28775 :'Informação e comunicação',
    28776 :'Atividades financeiras e seguros',
    28777 :'Atividades imobiliárias',
    28778 :'Atividades profissionais, científicas e técnicas ',
    28779 :'Atividades administrativas e serviços complementares',
    28780 :'Administração pública, defesa e seguridade social',
    28781 :'Educação',
    28782 :'Saúde e serviços sociais',
    28783 :'Outras atividades de serviços',
    28784 :'Total',
    28785 :'Agropecuária',
    28786 :'Indústrias extrativas',
    28787 :'Indústrias de transformação',
    28788 :'SIUP',
    28789 :'Eletricidade e gás',
    28790 :'Água, esgoto e gestão de resíduos',
    28791 :'Construção',
    28792 :'Comércio',
    28793 :'Serviços',
    28794 :'Transporte, armazenamento e correio',
    28795 :'Alojamento e alimentação',
    28796 :'Informação e comunicação',
    28797 :'Atividades financeiras e seguros',
    28798 :'Atividades imobiliárias',
    28799 :'Atividades profissionais, científicas e técnicas ',
    28800 :'Atividades administrativas e serviços complementares',
    28801 :'Administração pública, defesa e seguridade social',
    28802 :'Educação',
    28803 :'Saúde e serviços sociais',
    28804 :'Outras atividades de serviços',
}

emprego_dessaz = emprego_dessaz.reset_index().rename(columns=rename_dict)

emprego_dessaz = emprego_dessaz.set_index('Trimestre')

Em seguida, calculamos a série da variação percentual entre períodos e transformamos ambas séries para o formato esperado pela biblioteca gráfica.

emprego_dessaz_melted = (
    emprego_dessaz.drop(columns=['Total'])
    .reset_index()
    .melt(id_vars='Trimestre', var_name='Setor', value_name='Empregos'))

delta_emprego_dessaz_melted = (
    emprego_dessaz.drop(columns=['Total'])
    .pct_change()[1:]
    .reset_index()
    .melt(id_vars='Trimestre', var_name='Setor', value_name='Empregos'))

## Gráficos
Estoque de emprego formal por setor

sel = alt.selection(type='single', init={'Setor':'Agropecuária'}, bind='legend')

alt.Chart(
    emprego_dessaz_melted[emprego_dessaz_melted.Trimestre >= '2001-01-01']
).mark_line(point=False).encode(
    x = alt.X("Trimestre:T"),
    y = alt.Y("Empregos:Q", title='Empregos formais'),
    color = 'Setor:N',
    opacity=alt.condition(sel, alt.OpacityValue(1), alt.OpacityValue(0.4)),
    tooltip=alt.Tooltip(['Trimestre:T', 'Empregos:Q', 'Setor:N'])
).add_selection(
    sel
)

Variação percentual do emprego formal por setor

sel = alt.selection(type='single', init={'Setor':'Agropecuária'}, bind='legend')

alt.Chart(
    delta_emprego_dessaz_melted[delta_emprego_dessaz_melted['Trimestre'] >= '2001-01-01']
).mark_line(point=False).encode(
    x = alt.X("Trimestre:T"),
    y = alt.Y("Empregos:Q", title='Variação Empregos'),
    color = 'Setor:N',
    opacity=alt.condition(sel, alt.OpacityValue(1), alt.OpacityValue(0.1)),
    tooltip=alt.Tooltip(['Trimestre:T', 'Empregos:Q', 'Setor:N'])
).add_selection(
    sel
)

## Matriz de correlação
entre as variações do emprego formal por setor

df = (emprego_dessaz.drop(columns=['Total'])
    .pct_change()[1:]
    .reset_index()
)

print(df[df['Trimestre'].dt.year >= 2001].dropna().Trimestre.min())

df = (
    df[df['Trimestre'].dt.year >= 2001]
    .dropna()
    .drop(columns='Trimestre')
    .corr()
)

df = df.reset_index().melt(id_vars="index")

fig = alt.Chart(
    df,
    title="Variação percentual do emprego formal por setor (dessazonalizado)"
).mark_rect().encode(
    x=alt.X('index:N', title=''),
    y=alt.Y('variable:N', title=''),
    color=alt.Color('value:Q', title='Correlação', scale=alt.Scale(domain=(-.25, 1))),
    tooltip=alt.Tooltip(['index:N', 'variable:N', 'value:Q'])
)
fig