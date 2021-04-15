# Pré-Processamento - Análise das variáveis

## Resumo do alcance dessa etapa

Importados e tratados, os dados agora deve ser analisados. A análise e exploração estão descritos nessa etapa e guiam os próximos passos.

## Detalhamento da etapa

### Imports

import pandas as pd

from pandas_profiling import ProfileReport

# editar metadata
# tags ['remove-input']
X = pd.read_pickle('/mnt/d/Clientes/ODX/agro/agro_book/data/X.pkl.xz')

report = ProfileReport(X, minimal=True)
report

A análise apontou ...

