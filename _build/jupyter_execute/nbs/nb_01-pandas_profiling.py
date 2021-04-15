# Pré-Processamento - Análise das variáveis

## Resumo do alcance dessa etapa

Importados e tratados, os dados agora deve ser analisados. A análise e exploração estão descritos nessa etapa e guiam os próximos passos.

## Detalhamento da etapa

### Imports

import pandas as pd

from pandas_profiling import ProfileReport

import yaml

with open('../_local_paths.yml') as f:
    paths = yaml.load(f, Loader=yaml.FullLoader)

X = pd.read_pickle(paths['X'])

report = ProfileReport(X, minimal=True)
report

A análise apontou não apontou características graves nos dados (como alta correlação entre features). Prosseguimos para o próximo passo.