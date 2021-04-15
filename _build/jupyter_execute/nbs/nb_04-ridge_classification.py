# Classificação Ridge

## Resumo dos resultados dessa etapa

Os dados são transformados e codificados para adequação com os algorítimos de apredizagem computacional utilizados em seguida.

## Breve explicação e referências sobre o método

## Detalhamento da etapa

### Imports

import joblib
import numpy as np


from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import RidgeClassifier

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

ridge = RidgeClassifier(random_state=42)

ridge_params = {
    'alpha':np.arange(0.1, 10.1, 0.1),
    'fit_intercept':[True, False],
    'tol': [1/10**(i) for i in np.arange(3, 6)]
}

ridge_gs = GridSearchCV(ridge, ridge_params, n_jobs=-1, cv=4)

ridge_gs.fit(scaled_X, scaled_y.ravel())

## Modelo

ridge_model = ridge_gs.best_estimator_

ridge_model.get_params()

## Performance

print(
    classification_report(
        scaled_y,
        ridge_model.predict(scaled_X),
        target_names=categories
    ))

joblib.dump(ridge_model, paths['ridge_model'])

