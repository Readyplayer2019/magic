""""
from flask import Flask, render_template, request
import numpy as np
import math
import plotly
import plotly.graph_objs as go
import json
import pandas
app = Flask(__name__)

import numpy as np

"""""
""""""

"""
def heston_simulation(ia, iv, mu, k, theta, sigma, r, T, dt):
    N = int(T / dt)
    s = np.zeros(N + 1)
    v = np.zeros(N + 1)
    s[0] = ia
    v[0] = iv
    for t in range(1, N + 1):
        dW1 = np.sqrt(dt) * np.random.normal()
        dW2 = np.sqrt(dt) * np.random.normal()

        # brainium motion ?
        dW2 = r* dW1 + np.sqrt(1 - r ** 2) * dW2

        v[t] = v[t - 1] + k * (theta - max(v[t - 1], 0)) * dt + sigma * np.sqrt(max(v[t - 1], 0)) * dW2
        v[t] = max(v[t], 0)

        #  stochastic volatility
        s[t] = s[t - 1] * np.exp((mu - 0.5 * v[t]) * dt + np.sqrt(v[t]) * dW1)

    return s, np.sqrt(v)


# Parameters for the simulation
ia = 100
iv = 0.04
mu = 0.05
k = 2
theta = 0.04
sigma = 0.2
r = -0.5
T = 1
dt = 0.001

s, v = heston_simulation(ia, iv, mu, k, theta, sigma, r, T, dt)


#GBM: / mean reversion models
 #   hester model:/standard deviation returss
 #create me a hester model in python which finds the volatility and uses brainium motion
def monte_carlo_option_price(r, S, K, T, volatility, option_type="c", sims=10000):
    


    dt = 1.0  # time increment, assuming each step is one year
    discount_factor = np.exp(-r * T)
    payoffs = []

    for _ in range(sims):
        st = S
        for _ in range(int(T)):
            z = np.random.standard_normal()
            st *= np.exp((r - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * z)
        if option_type == "c":
            payoffs.append(max(0, st - K))
        else:
            payoffs.append(max(0, K - st))

    option_price = discount_factor * np.mean(payoffs)
    return option_price

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / np.sqrt(2)))

def get_price(r, S, K, T, volatility, option_type="c", model="black-scholes"):
    if model == "black-scholes":
        return black_scholes(r, S, K, T, volatility, option_type)
    else:
        return monte_carlo_option_price(r, S, K, T, volatility, option_type)

def black_scholes(r, S, K, T, volatility, option_type="c"):
    if not (option_type == "c" or option_type == "p"):
        raise "Option type must be either 'c' for Call or 'p' for Put!"

    d1 = (np.log(S / K) + (r + volatility ** 2 / 2) * T) / (volatility * np.sqrt(T))
    d2 = d1 - (volatility * np.sqrt(T))

    if option_type == "c":
        option_price = S * norm_cdf(d1) - K * np.exp(-r * T) * norm_cdf(d2)
    else:
        option_price = K * np.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

    return float(option_price)

plot_div = None

@app.route('/')
def index():
    return render_template('index.html', plot_div=plot_div)


@app.route('/api')
def api():
    r = float(request.args.get('r'))
    S = float(request.args.get('S'))
    K = float(request.args.get('K'))
    T = float(request.args.get('T'))  # You might not need T here if you are changing it
    volatility = float(request.args.get('volatility'))
    model = request.args.get('model')

    # Generate prices for a range of years
    years = list(range(1, int(T)+1))
    call_prices = [get_price(r, S, K, year, volatility, "c", model) for year in years]
    put_prices = [get_price(r, S, K, year, volatility, "p", model) for year in years]

    # Create the plot
    # trace1 = go.Scatter(x=years, y=call_prices, mode="lines+markers", name="Call Option Price")
    # trace2 = go.Scatter(x=years, y=put_prices, mode="lines+markers", name="Put Option Price")
    # layout = go.Layout(title="Option Prices over the Years", xaxis=dict(title="Year"), yaxis=dict(title="Price"))
    # figure = go.Figure(data=[trace1, trace2], layout=layout)
    # plot_div = plotly.offline.plot(figure, output_type='div')

    return [call_prices, put_prices]

if __name__ == '__main__':
    app.run(debug=True)

"""
""""
"""
from flask import Flask, render_template, request, jsonify
import numpy as np
import math

app = Flask(__name__)

def heston_simulation(ia, iv, mu, k, theta, sigma, r, T, dt):
    N = int(T / dt)
    s = np.zeros(N + 1)
    v = np.zeros(N + 1)
    s[0] = ia
    v[0] = iv
    for t in range(1, N + 1):
        dW1 = np.sqrt(dt) * np.random.normal()
        dW2 = r * dW1 + np.sqrt(1 - r ** 2) * np.sqrt(dt) * np.random.normal()

        v[t] = v[t - 1] + k * (theta - max(v[t - 1], 0)) * dt + sigma * np.sqrt(max(v[t - 1], 0)) * dW2
        v[t] = max(v[t], 0)
        s[t] = s[t - 1] * np.exp((mu - 0.5 * v[t]) * dt + np.sqrt(v[t]) * dW1)
    return s, np.sqrt(v)

def monte_carlo_option_price(r, S, K, T, volatility, option_type="c", sims=10000):
    dt = 1.0
    discount_factor = np.exp(-r * T)
    payoffs = []

    for _ in range(sims):
        st = S
        for _ in range(int(T)):
            z = np.random.standard_normal()
            st *= np.exp((r - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * z)
        if option_type == "c":
            payoffs.append(max(0, st - K))
        else:
            payoffs.append(max(0, K - st))
    return discount_factor * np.mean(payoffs)

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / np.sqrt(2)))

def get_price(r, S, K, T, volatility, option_type="c", model="black-scholes"):
    if model == "black-scholes":
        return black_scholes(r, S, K, T, volatility, option_type)
    else:
        return monte_carlo_option_price(r, S, K, T, volatility, option_type)

def black_scholes(r, S, K, T, volatility, option_type="c"):
    d1 = (np.log(S / K) + (r + volatility ** 2 / 2) * T) / (volatility * np.sqrt(T))
    d2 = d1 - (volatility * np.sqrt(T))

    if option_type == "c":
        return S * norm_cdf(d1) - K * np.exp(-r * T) * norm_cdf(d2)
    else:
        return K * np.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    r = float(request.args.get('r'))
    S = float(request.args.get('S'))
    K = float(request.args.get('K'))
    T = float(request.args.get('T'))
    volatility = float(request.args.get('volatility'))
    model = request.args.get('model')

    years = list(range(1, int(T) + 1))
    call_prices = [get_price(r, S, K, year, volatility, "c", model) for year in years]
    put_prices = [get_price(r, S, K, year, volatility, "p", model) for year in years]

    return jsonify({"call_prices": call_prices, "put_prices": put_prices})

if __name__ == '__main__':
    app.run(debug=True)



