# Pré-Processamento - Padronização e Codificação

## Resumo do alcance dessa etapa

Os dados são transformados e codificados para adequação com os algorítimos de apredizagem computacional utilizados em seguida.

## Detalhamento da etapa

### Imports

import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

import joblib

X = pd.read_pickle("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/X.pkl.xz")

y = X['gini']
X = X.drop(columns=['gini'])

## Padronização

Foi escolhida a padronização de todas as variáveis a valores entre 0 e 1.

x_scaler = MinMaxScaler()
scaled_X = x_scaler.fit_transform(X)

### Codificação

A variável alvo, o índice gini, é codificado de forma binária a seguir.

O formato foi escolhido porque ele se adapta a todos os algorítimos escolhidos.

Os rótulos das categorias foram mantidos para utilização nos métodos que os pedem.

y_scaler = OneHotEncoder(sparse=False, drop='first')
scaled_y = y_scaler.fit_transform([[i] for i in y.values])

categories = y_scaler.categories_[0].tolist()

Em seguida, prosseguimos para as modelagens.

joblib.dump(x_scaler, 'data_gini/x_scaler.joblib')
joblib.dump(scaled_X, 'data_gini/scaled_X.joblib')

joblib.dump(y_scaler, 'data_gini/y_scaler.joblib')
joblib.dump(scaled_y, 'data_gini/scaled_y.joblib')

joblib.dump(categories, 'data_gini/categories.joblib')

