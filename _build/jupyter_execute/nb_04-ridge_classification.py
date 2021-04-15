# Classificação Ridge

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

# editar metadata
# tags ['remove-cell']

x_scaler = joblib.load('/mnt/d/Clientes/ODX/agro/agro_book/data/x_scaler.joblib')
scaled_X = joblib.load('/mnt/d/Clientes/ODX/agro/agro_book/data/scaled_X.joblib')

y_scaler = joblib.load('/mnt/d/Clientes/ODX/agro/agro_book/data/y_scaler.joblib')
scaled1_y = joblib.load('/mnt/d/Clientes/ODX/agro/agro_book/data/scaled_X.joblib')

categories = joblib.load('/mnt/d/Clientes/ODX/agro/agro_book/data/categories.joblib')

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

