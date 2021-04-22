# Rede Neural

## Resumo dos resultados dessa etapa

Uma rede neural simples foi ajustada aos modelos.

A escolha do formato simples foi motivada pelo numero relativamente baixo de observações para esse tipo de modelo.

O modelo atingiu uma acurácia média de 82%.

## Breve explicação e referências sobre o método

## Detalhamento da etapa

### Imports

import requests
from io import BytesIO
import joblib
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier

from ann_visualizer.visualize import ann_viz

from sklearn.metrics import classification_report

import lime
import lime.lime_tabular

import eli5
import shap
shap.initjs()

def load_remote_joblib(url):
    """função utilizada para carregar joblib de fonte remota
    ESSA FUNCAO É PERIGOSA
    a função joblib.load pode executar código arbitrário durante sua execuççao
    não utilize essa parte do código se você não tiver certeza do que está fazendo
    """
    content = requests.get(url).content
    return joblib.load(BytesIO(content))
    

x_scaler = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/x_scaler.joblib")
scaled_X = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/scaled_X.joblib")

y_scaler = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/y_scaler.joblib")
scaled_y = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/scaled_y.joblib")

categories = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/categories.joblib")

### Tunning

O número de observações é baixo para esse tipo de modelo.

Mantivemos o desenho da rede simples para diminuir a complexidade e testamos essa configuração.

## Definição da Rede

def baseline_model():
    model = Sequential()
    model.add(Dense(10,
                    input_dim=39,
                    kernel_initializer='normal',
                    activation='relu'))
    model.add(Dense(1, activation='sigmoid', kernel_initializer='normal'))
    
    model.compile(
        loss='BinaryCrossentropy',
        metrics=['accuracy'],
        optimizer='adam'
    )
    
    return model

baseline_model().summary()

## Treinamento Rede

nn_model = KerasClassifier(baseline_model,
                           epochs=100,
                           batch_size=3,
                           verbose=0)

nn_model.fit(scaled_X, scaled_y)

#ann_viz(baseline_model(), filename='rede_2_categs.gv', title='Rede Neural - 2 categorias')

## Performance

prediction = nn_model.predict(scaled_X)

print(
    classification_report(
        scaled_y,
        prediction, 
        target_names=categories
    )
)

nn_model.model.save(paths['nn_estimator')

