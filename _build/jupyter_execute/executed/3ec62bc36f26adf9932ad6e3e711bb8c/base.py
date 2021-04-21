import pandas as pd
import numpy as np
import geopandas as gpd

import yaml

with open('_local_paths.yml') as f:
    paths = yaml.load(f, Loader=yaml.FullLoader)

GINI_DATA_PATH = paths['GINI_DATA_PATH']
CENSO_AGRO_DATA_PATH = paths['CENSO_AGRO_DATA_PATH']

y = pd.read_excel(GINI_DATA_PATH)
df = gpd.read_file(CENSO_AGRO_DATA_PATH)

from zipfile import ZipFile
from io import BytesIO

zf =ZipFile('/mnt/c/Users/felic/Downloads/Bases Censo-1.zip')

teste = pd.read_excel(
    BytesIO(zf.read('Atlas 2013_municipal, estadual e Brasil.xlsx')),
    sheet_name='MUN 91-00-10', usecols=['ANO', 'Codmun7', 'Município', 'GINI']
)

df.head()

df.info()

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

teste.head()

print(y.shape)
y.head()

y.info()

y.gini = pd.to_numeric(y.gini, errors='coerce')

# valor de corte
y.gini.quantile(q=.5)

y.gini = np.select(
    [y['gini'] <= y['gini'].quantile(q=.5)],
    ['gini_baixo'], default='gini_alto'
)

df = df.merge(y, left_on='GEO', right_on='COD_MUN')

df.shape

df.dropna().shape #inefetivo, o merge foi do tipo 'inner_join', não haviam NAs resultantes

municipios = df['MUNICIPIO']
X = df.drop(columns=[
    'COD_UF', 'NOME_UF', 'COD_MUN', 'NOM_MUN', 'AREAMED', 'GEO', 'MUNICIPIO'
])

# editar metadata
# tags ['remove-input']

municipios.to_pickle(paths['municipios'])
X.to_pickle(paths['X'])

