# Ranking Mundial - EXP e IMP Agro

Fonte: [FAO - ONU](http://www.fao.org/faostat/en/#data/TP)

## Importação de bibliotecas

# download dados
import requests
from io import BytesIO
from zipfile import ZipFile

# manipulacao
import pandas as pd
import numpy as np

# graphs
import altair as alt


## Download dados

#aprox 61 MB
data_path = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Trade_Crops_Livestock_E_All_Data.zip"
download = requests.get(data_path).content

# descompactando
zipfile = ZipFile(BytesIO(download))
zipfile.filelist

O arquivo baixado é composto por 3 outros arquivos. Escolhemos trabalhar com o segundo.

df = pd.read_csv(zipfile.open(zipfile.filelist[1]), encoding='latin1')

print(df.shape)
df.head()

## Filtro e preparação dos dados

Apesar de listar dados desde 1961, esses dados estão presentes em poucos os casos.

Vamos focar o restante da análise somente no dado mais recente (2019)

df = df[['Area Code', 'Area', 'Item Code', 'Item', 'Element Code', 'Element',
       'Unit', 'Y2019']]

Os dados compreendem não só países mas também grupos de países definidos por critérios geográficos ou econômicos.

Para essa análise, removemos os grupos e prosseguimos somente com os países.

exclude_areas = [
    'World',
    # continentes e subcontinentes
    'Oceania', 'Oceania (excluding intra-trade)',
    'Australia and New Zealand', 'Australia and New Zealand (excluding intra-trade)',
    #
    'Europe', 'Europe (excluding intra-trade)',
    'Eastern Europe', 'Eastern Europe (excluding intra-trade)',
    'Northern Europe', 'Northern Europe (excluding intra-trade)',
    'Western Europe', 'Western Europe (excluding intra-trade)',
    'Southern Europe', 'Southern Europe (excluding intra-trade)',
    'Belgium-Luxembourg',
    #
    'Asia', 'Asia (excluding intra-trade)',
    'Central Asia', 'Central Asia (excluding intra-trade)',
    'Eastern Asia', 'Eastern Asia (excluding intra-trade)', 
    'Western Asia', 'Western Asia (excluding intra-trade)',
    'Southern Asia', 'Southern Asia (excluding intra-trade)',
    'South-eastern Asia', 'South-Eastern Asia (excluding intra-trade)',
    'USSR',
    'China (excluding intra-trade)',
    'China, Hong Kong SAR',
    'China, Macao SAR',
    'China, Taiwan Province of',
    'China, mainland',
    'Melanesia', 'Melanesia (excluding intra-trade)',
    'Micronesia', 'Micronesia (excluding intra-trade)', 
    'Polynesia', 'Polynesia (excluding intra-trade)',
    #
    'Americas', 'Americas (excluding intra-trade)'
    'Northern America', 'Northern America (excluding intra-trade)', 
    'Central America', 'Central America (excluding intra-trade)',
    'South America', 'South America (excluding intra-trade)',
    'Caribbean', 'Caribbean (excluding intra-trade)',
    #
    'Africa', 'Eastern Africa',
    'Africa (excluding intra-trade)',
    'Northern Africa', 'Northern Africa (excluding intra-trade)', 
    'Middle Africa', 'Middle Africa (excluding intra-trade)',
    'Eastern Africa (excluding intra-trade)', 
    'Western Africa', 'Western Africa (excluding intra-trade)',
    'Southern Africa', 'Southern Africa (excluding intra-trade)',
    'Sudan (former)',  
    # classificacoes e grupos economicos
    'Least Developed Countries', 'Least Developed Countries (excluding intra-trade)',
    'Low Income Food Deficit Countries', 'Low Income Food Deficit Countries (excluding intra-trade)',
    'Net Food Importing Developing Countries', 'Net Food Importing Developing Countries (excluding intra-trade)',
    'Small Island Developing States', 'Small Island Developing States (excluding intra-trade)',
    'European Union (12) (excluding intra-trade)',
    'European Union (15) (excluding intra-trade)',
    'European Union (25) (excluding intra-trade)',
    'European Union (27)', 'European Union (27) (excluding intra-trade)',
    'European Union (28)', 'European Union (28) (excluding intra-trade)',
    'Land Locked Developing Countries', 'Land Locked Developing Countries (excluding intra-trade)',
]

# exclui os grupos e os não disponíveis
df = df[~df['Area'].isin(exclude_areas)].dropna()

Ainda uma outra separação é necessária.

Os items foram listados individualmente e agregados. Abaixo, separamos esses dois tipos.

group_products = [
    'Agricultural Products', 'Food Excluding Fish', 'Cereals and Preparations',
    'Cereal preparations', 'Cereals', 'Fats and Oils (excluding Butter)',
    'Animal Fats and Oils (excl. Butter)', 'Vegetable Oil and Fat',
    'Meat and Meat Preparations', 'Bovine Meat', 'Poultry Meat',
    'Pigmeat', 'Other Meat', 'Sugar and Honey', 'Fruit and Vegetables',
    'Fruit', 'Vegetables', 'Pulses', 'Roots and Tubers', 'Nuts',
    'Sugar Crops Primary', 'Dairy Products and Eggs', 'Dairy Products',
    'Eggs', 'Beverages', 'Alcoholic Beverages', 'Non-alcoholic Beverages',
    'Other food', 'Oilseeds', 'Other food nes', 'Non-food',
    'Fodder and Feeding Stuff', 'Non-edible Crude Materials',
    'Natural Rubber', 'Textile Fibres', 'Hides and skins',
    'Crude Materials nes', 'Non-edible Fats and Oils', 'Tobacco',
    'Total Merchandise Trade',
]

# separação
df_produtos = df[~df['Item'].isin(group_products)]
df_agregados = df[df['Item'].isin(group_products)]

df_produtos.head()

def separa_tipos(dataf):
    exp_value = dataf[dataf['Element'] == "Export Value"]
    exp_qtd = dataf[dataf['Element'] == "Export Quantity"]
    imp_value = dataf[dataf['Element'] == "Import Value"]
    imp_qtd = dataf[dataf['Element'] == "Import Quantity"]
    return exp_value, exp_qtd, imp_value, imp_qtd

exp_value_prod, exp_qtd_prod, imp_value_prod, imp_qtd_prod = separa_tipos(df_produtos)
exp_value_grupo, exp_qtd_grupo, imp_value_grupo, imp_qtd_grupo = separa_tipos(df_agregados)

## Criação dos Rankings

def adiciona_ranking(dados):
    dados = dados.assign(
        rank = dados
        .groupby("Item")["Y2019"]
        .rank("dense", ascending=False)
    )
    return dados

#
exp_value_prod = adiciona_ranking(exp_value_prod)
exp_qtd_prod = adiciona_ranking(exp_qtd_prod)
imp_value_prod = adiciona_ranking(imp_value_prod)
imp_qtd_prod = adiciona_ranking(imp_qtd_prod)
#
exp_value_grupo = adiciona_ranking(exp_value_grupo)
exp_qtd_grupo = adiciona_ranking(exp_qtd_grupo)
imp_value_grupo = adiciona_ranking(imp_value_grupo)
imp_qtd_grupo = adiciona_ranking(imp_qtd_grupo)

## Produtos em que o país está no Top 5

def produtos_top_n_pais(dados, n, pais):
    topn = dados[dados["rank"] <= n]
    return topn[(topn['Area'] == pais) &
                (topn['Y2019'] != 0)]

### Exportação em Valores

top5_exp_value_prod = produtos_top_n_pais(exp_value_prod, 5, "Brazil")
top5_exp_value_prod

### Exportação em Quantidade

top5_exp_qtd_prod = produtos_top_n_pais(exp_qtd_prod, 5, "Brazil")
top5_exp_qtd_prod

### Importação em Valores

top5_imp_value_prod = produtos_top_n_pais(imp_value_prod, 5, "Brazil")
top5_imp_value_prod

### Importação em Quantidade

top5_imp_qtd_prod = produtos_top_n_pais(imp_qtd_prod, 5, "Brazil")
top5_imp_qtd_prod