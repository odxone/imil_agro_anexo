# Pré-Processamento - Leitura e Limpeza

## Resumo do alcance dessa etapa

Os dados são importados de diferentes fontes e unidos em uma única base.
A cada variável é dado um nome informativo, a base é limpada de inconsitências e ausências e, por fim, a desigualdade (medida como um índice Gini) é classificada em duas categorias: alto e baixo.

Fontes dados:

[Censo Agro 2017 Mapa Interativo - IBGE](https://mapasinterativos.ibge.gov.br/agrocompara/)

[Datasus - Min Saúde](http://tabnet.datasus.gov.br/cgi/ibge/censo/cnv/ginibr.def)

O mapa Interativo não disponibiliza o link para download direto. Subimos o [arquivo](https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/mun_agro.zip) (baixado no dia XX/XX/XXXX) em nosso repositório.

## Detalhamento da etapa

### Imports

import pandas as pd
import numpy as np

# carregamento de dados armazenado em shapefile
import geopandas as gpd

### Leitura e Limpesa das bases de dados

df = gpd.read_file("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/mun_agro.zip")

y = pd.read_csv(
    "http://tabnet.datasus.gov.br/cgi/ibge/censo/bases/ginibr.csv",
    encoding='latin1',
    decimal=',',
    sep=";",
    skiprows=2,
    skipfooter=2,
    engine="python",
)

df.head()

df.info()

O arquivo utilizado veio com as variáveis nomeadas de maneira pouco informativa.

Com auxílio do [dicionário de dados](https://mapasinterativos.ibge.gov.br/agrocompara/dados/def_indicadores.pdf), mudamos os rótulos para que sejam mais informativos.

dict_rename = {
    'V1' :'Estabelecimento Agropecuário (N)',
    'V2' :'Área média (ha)',
    'V3' : 'Pessoal Ocupado / Estabelecimento (Pessoa)',
    'V4' :'Área lavoura/ Adubadeira (ha)',
    'V5' :'Área lavoura/ Colheitadeira(ha)',
    'V6' :'Área lavoura/ Semeadeira(ha)',
    'V7' :'Área lavoura/ Trator(ha)',
    'V8' :'Atividade-Lavoura Temporária (%)',
    'V9' :'Atividade-Lavoura Permanente(%)',
    'V10' :'Atividade-Pecuária(%)',
    'V11' :'Atividade-Horticultura&Floricultura(%)',
    'V12' :'Atividade-Sementes&Mudas(%)',
    'V13' :'Atividade-Produção Florestal(%)',
    'V14' :'Atividade-Pesca(%)',
    'V15' :'Atividade-Aquicultura(%)',
    'V16' :'Uso das terras-Lavoura(%)',
    'V17' :'Uso das terras-Pastagem (%)',
    'V18' :'Aves-Corte (%)',
    'V19' :'Aves-Ovos(%)',
    'V20' :'Bovinos-Corte (%)',
    'V21' :'Bovinos-Leite(%)',
    'V22' :'Rendimento-Arroz (kg/ha)',
    'V23' :'Rendimento-Cana (kg/ha)',
    'V24' :'Rendimento-Mandioca (kg/ha)',
    'V25' :'Rendimento-Milho (kg/ha)',
    'V26' :'Rendimento-Soja (kg/ha)',
    'V27' :'Rendimento-Trigo(kg/ha)',
    'V28' :'Rendimento-Cacau(kg/ha)',
    'V29' :'Rendimento-Café(kg/ha)',
    'V30':'Rendimento-Laranja(kg/ha)',
    'V31':'Rendimento-Uva(kg/ha)',
    'V32':'Carga de Bovinos (n/ha)',
    'V33':'Cisterna (%)',
    'V34':'Utilização de Agrotóxicos (%)',
    'V35':'Despesa com Agrotóxicos (%)',
    'V36':'Uso de irrigação (%)',
    'V37':'Assistência Técnica (%)',
    'V38':'Agricultura familiar (%)',
    'V39':'Produtor com escolaridade até Ensino Fundamental(%)',
}

df = df.rename(columns=dict_rename)

Nem todas as variáveis são informativas para essa análise (como as coordenadas dos shapes, por exemplo).
Abaixo, selecionamos as que não foram julgadas relevantes.

variaveis_relevantes = [
    'GEO', 'MUNICIPIO', 'Estabelecimento Agropecuário (N)',
    'Área média (ha)', 'Pessoal Ocupado / Estabelecimento (Pessoa)',
    'Área lavoura/ Adubadeira (ha)', 'Área lavoura/ Colheitadeira(ha)',
    'Área lavoura/ Semeadeira(ha)', 'Área lavoura/ Trator(ha)',
    'Atividade-Lavoura Temporária (%)', 'Atividade-Lavoura Permanente(%)',
    'Atividade-Pecuária(%)', 'Atividade-Horticultura&Floricultura(%)',
    'Atividade-Sementes&Mudas(%)', 'Atividade-Produção Florestal(%)',
    'Atividade-Pesca(%)', 'Atividade-Aquicultura(%)',
    'Uso das terras-Lavoura(%)', 'Uso das terras-Pastagem (%)',
    'Aves-Corte (%)', 'Aves-Ovos(%)', 'Bovinos-Corte (%)',
    'Bovinos-Leite(%)', 'Rendimento-Arroz (kg/ha)',
    'Rendimento-Cana (kg/ha)', 'Rendimento-Mandioca (kg/ha)',
    'Rendimento-Milho (kg/ha)', 'Rendimento-Soja (kg/ha)',
    'Rendimento-Trigo(kg/ha)', 'Rendimento-Cacau(kg/ha)',
    'Rendimento-Café(kg/ha)', 'Rendimento-Laranja(kg/ha)',
    'Rendimento-Uva(kg/ha)', 'Carga de Bovinos (n/ha)',
    'Cisterna (%)', 'Utilização de Agrotóxicos (%)',
    'Despesa com Agrotóxicos (%)', 'Uso de irrigação (%)',
    'Assistência Técnica (%)', 'Agricultura familiar (%)',
    'Produtor com escolaridade até Ensino Fundamental(%)',
    ]

df = df[variaveis_relevantes]

A base do Datasus utilizou o código IBGE sem o dígito verificador. Criando coluna com essa informação para usar de chave na união entre as bases.

df['COD_MUN'] = df.GEO.astype(int).astype(str).str[:-1]

Com os dados do censo agropecuário melhor formatados, seguimos para processamento dos dados da FONTE

Primeira etapa é separar o código do município do nome.

y[['COD_MUN', 'NOME_MUN']] = y['Município'].str.split(' ', n=1, expand=True)

print(y.shape)
y.head()

y.info()

y = y[['COD_MUN', '2010']].rename(columns={
    '2010':'gini'
})

### Criação das categorias

Gini foi binarizado em 'gini_alto' e 'gini_baixo', critério de corte no 50 percentil

# valor de corte
y.gini.quantile(q=.5)

y.gini = np.select(
    [y['gini'] <= y['gini'].quantile(q=.5)],
    ['gini_baixo'], default='gini_alto'
)

### Merge

df = df.merge(y, on='COD_MUN')

df.shape

df.dropna().shape #inefetivo, o merge foi do tipo 'inner_join', não haviam NAs resultantes

Em seguida, separamos os labels dos municípios e as variáveis de interesse.

df.head()

municipios = df['MUNICIPIO']
X = df.drop(columns=[
    'COD_MUN', 'GEO', 'MUNICIPIO'
])

df[X.duplicated()]

Os 5 municípios não tem dados do censo agro e serão removidos

municipios= municipios[~X.duplicated()]
X = X[~X.duplicated()]

A próxima etapa é escalar e codificar as features conforme necessário.

# editar metadata
# tags ['remove-input']

municipios.to_pickle('data_gini/municipios.pkl.xz')
X.to_pickle('data_gini/X.pkl.xz')

