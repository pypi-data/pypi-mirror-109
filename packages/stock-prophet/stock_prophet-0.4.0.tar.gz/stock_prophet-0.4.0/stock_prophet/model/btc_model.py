import os
import time
import pickle
import prophet
import yfinance as yf


def _get_history():
    return yf.Ticker('BTC-USD') \
             .history(period='1w', interval='1h')

def _prepare_df(data):
    data.index = data.index.tz_convert(time.tzname[0])
    data.index = data.index.tz_localize(None)

    return data.reset_index() \
               .rename(columns={'index': 'ds', 'Close': 'y'}) \
               .loc[:, ['ds', 'y']]

def train_model(filepath='models/btc_model.pkl'):
    df = _prepare_df(_get_history())
    model = prophet.Prophet()
    model.fit(df)

    with open(filepath, 'wb') as file:
        pickle.dump(model, file)

def read_model(filepath='models/btc_model.pkl'):
    return pickle.load(open(filepath, 'rb'))

def get_preidction(n_steps, plot_filepath='static/plot.png'):
    model = read_model()
    forecast = model.predict(model.make_future_dataframe(periods=n_steps, freq=3600))
    model.plot(forecast.iloc[-144:]).savefig(plot_filepath)

    return forecast.iloc[-n_steps:][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

