# Classificação Ridge

## Resumo dos resultados dessa etapa

O modelo Ridge foi ajustado aos dados.

Após o refinamento dos hiperparâmetros, a acurácia média atingida pelo modelo ridge foi de 73%.

## Breve explicação e referências sobre o método

## Detalhamento da etapa

### Imports

import requests
from io import BytesIO
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

joblib.dump(ridge_model, 'data_gini/ridge_model.joblib')

## ELI5



## LIME



## SHAP



