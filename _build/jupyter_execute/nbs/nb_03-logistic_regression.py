# Regressão Logística

## Resumo dos resultados dessa etapa

Os dados são transformados e codificados para adequação com os algorítimos de apredizagem computacional utilizados em seguida.

## Breve explicação e referências sobre o método

## Detalhamento da etapa

### Imports

import joblib
import numpy as np


from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

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

lreg = LogisticRegression(solver='saga')

lreg_params = {
    'max_iter':np.arange(50, 450, 50),
    'fit_intercept':[True, False],
    'random_state':[42]
}

lreg_gs = GridSearchCV(lreg, lreg_params, verbose=1)

lreg_gs.fit(scaled_X, scaled_y.ravel())

## Modelo

lreg_model = lreg_gs.best_estimator_

lreg_model.get_params()

## Performance

lreg_model.score(scaled_X, scaled_y)

print(classification_report(
    scaled_y,
    lreg_model.predict(scaled_X),
    target_names=categories
))

joblib.dump(lreg_model, paths['lreg_model'])

