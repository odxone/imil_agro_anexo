# Floresta Aleatória

## Resumo dos resultados dessa etapa

Os dados são transformados e codificados para adequação com os algorítimos de apredizagem computacional utilizados em seguida.

## Breve explicação e referências sobre o método

## Detalhamento da etapa

### Imports

import joblib
import numpy as np


from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

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

O número de parâmetros para tunar aqui é bem maior do que os anteriores

Usando RandomSearchCV para busca de hiperparâmetros

max_depth = [int(x) for x in np.arange(1, 11)]
max_features = ['auto', 'sqrt']
min_samples_leaf = [int(2**x) for x in np.arange(0, 4)]
min_samples_slit = [int(2**x) for x in np.arange(4, 8)]
n_estimators = [int(x) * 100 for x in np.arange(1, 8)]

param_grid ={
    'max_depth':max_depth,
    'max_features':max_features,
    'min_samples_leaf':min_samples_leaf,
    'min_samples_split':min_samples_slit,
    'n_estimators':n_estimators,
}

rfr = RandomForestClassifier()

rfr_rs = RandomizedSearchCV(
    estimator=rfr,
    param_distributions=param_grid,
    n_iter=30,
    cv=3,
    random_state=42
)

rfr_rs.fit(scaled_X, scaled_y.ravel())

## Modelo

rf_model = rfr_rs.best_estimator_

rf_model.get_params()

## Performance

print(classification_report(
    scaled_y,
    rf_model.predict(scaled_X),
    target_names=categories
))

joblib.dump(rf_model, paths['rf_model'])

