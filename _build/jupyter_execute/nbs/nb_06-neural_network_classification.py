# Rede Neural

## Resumo dos resultados dessa etapa

Os dados são transformados e codificados para adequação com os algorítimos de apredizagem computacional utilizados em seguida.

## Breve explicação e referências sobre o método

## Detalhamento da etapa

### Imports

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

import yaml

with open('/mnt/d/Clientes/ODX/agro/online_book/_local_paths.yml') as f:
    paths = yaml.load(f, Loader=yaml.FullLoader)

x_scaler = joblib.load(paths['x_scaler'])
scaled_X = joblib.load(paths['scaled_X'])

y_scaler = joblib.load(paths['y_scaler'])
scaled_y = joblib.load(paths['scaled_y'])

categories = joblib.load(paths['categories'])

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

nn_model.model.save(paths['nn_estimator'])

