# Floresta Aleatória

## Resumo dos resultados dessa etapa

Foi ajustado um modelo do tipo Floresta Aleatória aos dados.

Após exploração aleatória dos hiperparâmetros, a acurácia média atingida pelo modelo foi de 75%.

## Breve explicação e referências sobre o método

## Detalhamento da etapa

### Imports

import requests
from io import BytesIO
import joblib
import numpy as np

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import classification_report

from random import seed, choice

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
    

x_scaler = load_remote_joblib("https://github.com/odxone/imil_agro_anexo/raw/main/nbs/data_gini/x_scaler.joblib")
scaled_X = load_remote_joblib("https://github.com/odxone/imil_agro_anexo/raw/main/nbs/data_gini/scaled_X.joblib")

y_scaler = load_remote_joblib("https://github.com/odxone/imil_agro_anexo/raw/main/nbs/data_gini/y_scaler.joblib")
scaled_y = load_remote_joblib("https://github.com/odxone/imil_agro_anexo/raw/main/nbs/data_gini/scaled_y.joblib")

feature_names = load_remote_joblib("https://github.com/odxone/imil_agro_anexo/raw/main/nbs/data_gini/features.joblib")
categories = load_remote_joblib("https://github.com/odxone/imil_agro_anexo/raw/main/nbs/data_gini/categories.joblib")

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

joblib.dump(rf_model, 'data_gini/rf_model.joblib')

## Interpretabilidade

Sorteio de uma observação para ser utilizada nos algorítimos de interpretabilidade

seed(42)

random_obs_idx = choice(range(len(scaled_X)))

random_obs = scaled_X[random_obs_idx]

### ELI5

eli5.show_weights(rf_model, feature_names=feature_names)

eli5.explain_prediction_sklearn(rf_model, random_obs,feature_names=feature_names)

### LIME

explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=scaled_X,
    feature_names=feature_names,
    class_names=categories,
    mode='classification'
)

lime_exp_rl = explainer.explain_instance(
    random_obs,
    rf_model.predict_proba,
)

lime_exp_rl.show_in_notebook()

### SHAP

shap_rl_expainer = shap.KernelExplainer(
    rf_model.predict_proba,
    shap.sample(scaled_X, random_state=42)
)

shap_rl_values = shap_rl_expainer.shap_values(shap.sample(scaled_X, random_state=42))

O código abaixo gera um gráfico bastante interessante, porém pesado, e foi omitido para melhorar a navegação nesse anexo.

```python
shap.force_plot(
    shap_rl_expainer.expected_value[0],
    shap_rl_values[0],
    feature_names=feature_names
)
```

Com pequenas modificações, o mesmo método também pode ser utilizado para os outros modelos.

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