# dados
import sgs

# manipulacao basica dos dados
import pandas as pd
import numpy as np

# analise de series temporais
from statsmodels.stats import api as stats
from statsmodels.tsa import api as tsa

series = [22105, 22106, 22107, 22110]
labels = ['Agropecuária', 'Indústria', 'Serviços', 'Famílias']

data_inicial = '01-01-1996'
data_final = '01-01-2021'

dataf = sgs.dataframe(series, start= data_inicial, end=data_final)

dataf = dataf.rename(columns={s:l for s, l in zip(series, labels)})

dataf.head()

acf = tsa.graphics.plot_acf(dataf['Agropecuária'])
tsa.adfuller(dataf['Agropecuária'])

acf = tsa.graphics.plot_acf(dataf['Indústria'])
tsa.adfuller(dataf['Indústria'])

acf = tsa.graphics.plot_acf(dataf['Serviços'])
tsa.adfuller(dataf['Serviços'])

acf = tsa.graphics.plot_acf(dataf['Famílias'])
tsa.adfuller(dataf['Famílias'])

# diferenciação 1
df = dataf.diff(1)[1:]

acf = tsa.graphics.plot_acf(df['Agropecuária'])
tsa.adfuller(df['Agropecuária'])

acf = tsa.graphics.plot_acf(df['Indústria'])
tsa.adfuller(df['Indústria'])

acf = tsa.graphics.plot_acf(df['Serviços'])
tsa.adfuller(df['Serviços'])

acf = tsa.graphics.plot_acf(df['Famílias'])
tsa.adfuller(df['Famílias'])

model = tsa.VAR(df, dates=df.index, freq='QS-OCT')
fit = model.fit(maxlags=16)

model.select_order(10).summary()

fit = model.fit(maxlags=2)

fit.summary()

fig = fit.plot_acorr(resid=True)

stats.acorr_ljungbox(fit.resid['Agropecuária'], return_df=True, lags=np.arange(1, 13))

irf = fit.irf(8) # numero de lags arbitrariamente escolhido
irf_plot = irf.plot()

irf_plot = irf.plot(orth=True) # IRF Ortogonalizada

cum_responses = irf.plot_cum_effects() # IRF efeitos cumulativos

cum_responses = irf.plot_cum_effects(orth=True) # IRF ortogonalizada efeitos cumulativos