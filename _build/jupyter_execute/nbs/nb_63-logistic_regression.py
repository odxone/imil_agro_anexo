# Regressão Logística

## Resumo dos resultados dessa etapa

O modelo de regressão logística foi ajustado aos dados.

Após refinamento dos hiperparâmetros, a acurácia média atingida por esse modelo foi de 73%.

## Breve explicação e referências sobre o método

Em inglês:
* A [página do Scikit Learn sobre regressões logísticas](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression) é uma excelente fonte para compreender o método.

## Detalhamento da etapa

### Imports

import requests
from io import BytesIO
import joblib
import numpy as np

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report

from random import choice, seed

import lime
import lime.lime_tabular

import eli5
import shap
shap.initjs()

def load_remote_joblib(url):
    """função utilizada para carregar joblib de fonte remota
    ESSAfeature_namesCAO É PERIGOSA
    a função joblib.load pode executar código arbitrário durante sua execuççao
    não utilize essa parte do código se você não tiver certeza do que está fazendo
    """
    content = requests.get(url).content
    return joblib.load(BytesIO(content))
    

x_scaler = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/x_scaler.joblib")
scaled_X = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/scaled_X.joblib")

y_scaler = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/y_scaler.joblib")
scaled_y = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/scaled_y.joblib")

feature_names = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/features.joblib")
categories = load_remote_joblib("https://github.com/feliciov/agro_online/raw/main/nbs/data_gini/categories.joblib")

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

joblib.dump(lreg_model, 'data_gini/lreg_model.joblib')

## Interpretabilidade

Sorteio de uma observação para ser utilizada nos algorítimos de interpretabilidade

seed(42)

random_obs_idx = choice(range(len(scaled_X)))

random_obs = scaled_X[random_obs_idx]

### ELI5

eli5.show_weights(lreg_model, feature_names=feature_names)

eli5.explain_prediction_sklearn(lreg_model, random_obs,feature_names=feature_names)

### LIME

explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=scaled_X,
    feature_names=feature_names,
    class_names=categories,
    mode='classification'
)

lime_exp_rl = explainer.explain_instance(
    random_obs,
    lreg_model.predict_proba,
)

lime_exp_rl.show_in_notebook()

### SHAP

shap_rl_expainer = shap.KernelExplainer(
    lreg_model.predict_proba,
    shap.sample(scaled_X, random_state=42)
)

shap_rl_values = shap_rl_expainer.shap_values(shap.sample(scaled_X, random_state=42))

shap.force_plot(
    shap_rl_expainer.expected_value[0],
    shap_rl_values[0],
    feature_names=feature_names
)

shap.decision_plot(
    shap_rl_expainer.expected_value[0],
    shap_rl_values[0],
    feature_names=feature_names
)

shap.summary_plot(
    shap_rl_values[0],
    features=shap.sample(scaled_X, random_state=42),
    feature_names=feature_names
)

