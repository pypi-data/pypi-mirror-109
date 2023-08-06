import os
import time
import pickle
import prophet
import yfinance as yf


def _get_history():
    return yf.Ticker('BTC-USD') \
             .history(period='1w', interval='1h')

def _prepare_df(data):
    print(data.index.name)
    data.index = data.index.tz_convert(time.tzname[0])
    data.index = data.index.tz_localize(None)
    print(data)
    return data.reset_index() \
               .rename(columns={'index': 'ds', 'Close': 'y'}) \
               .loc[:, ['ds', 'y']]

def train_model():
    df = _prepare_df(_get_history())
    model = prophet.Prophet()
    model.fit(df)

    with open('models/btc_model.pkl', 'wb') as file:
        pickle.dump(model, file)

def read_model():
    return pickle.load(open('models/btc_model.pkl', 'rb'))

def get_preidction(n_steps):
    model = read_model()
    forecast = model.predict(model.make_future_dataframe(periods=n_steps))
    model.plot(forecast.iloc[-72:]).savefig('static/plot.png')

    return forecast.iloc[-n_steps:][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

