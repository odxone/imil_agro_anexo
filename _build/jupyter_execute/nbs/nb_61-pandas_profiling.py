# Pré-Processamento - Análise das variáveis

## Resumo do alcance dessa etapa

Importados e tratados, os dados agora deve ser analisados. A análise e exploração estão descritos nessa etapa e guiam os próximos passos.

## Detalhamento da etapa

### Imports

import pandas as pd

from pandas_profiling import ProfileReport

X = pd.read_pickle('data_gini/X.pkl.xz')

report = ProfileReport(X, minimal=True)
report

A análise não apontou características graves nos dados (como alta correlação entre features).

O índice foi apontado como 100% de valores únicos, mas ele será removido para modelagem.

Prosseguimos para o próximo passo.

