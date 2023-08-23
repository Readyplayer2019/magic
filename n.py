from flask import Flask, render_template, request
import numpy as np
import math
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / np.sqrt(2)))

def get_price(r, S, K, T, volatility, option_type="c", model="black-scholes"):
    if model == "black-scholes":
        return black_scholes(r, S, K, T, volatility, option_type)
    else:
        return

def black_scholes(r, S, K, T, volatility, option_type="c"):
    if not (option_type == "c" or option_type == "p"):
        return "Option type must be either 'c' for Call or 'p' for Put!"

    d1 = (np.log(S / K) + (r + volatility ** 2 / 2) * T) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    if option_type == "c":
        option_price = S * norm_cdf(d1) - K * np.exp(-r * T) * norm_cdf(d2)
    else:
        option_price = K * np.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

    return option_price


@app.route('/', methods=['GET', 'POST'])

def index():
    plot_div = None

    if request.method == 'POST':
        r = float(request.form['r'])
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])  # You might not need T here if you are changing it
        volatility = float(request.form['volatility'])
        # model = request.form['model']

        # Generate prices for a range of years
        years = list(range(int(T), int(T) + 10))
        call_prices = [get_price(r, S, K, year, volatility, "c") for year in years]
        put_prices = [get_price(r, S, K, year, volatility, "p") for year in years]

        # Create the plot
        trace1 = go.Scatter(x=years, y=call_prices, mode="lines+markers", name="Call Option Price")
        trace2 = go.Scatter(x=years, y=put_prices, mode="lines+markers", name="Put Option Price")
        layout = go.Layout(title="Option Prices over the Years", xaxis=dict(title="Year"), yaxis=dict(title="Price"))
        figure = go.Figure(data=[trace1, trace2], layout=layout)
        plot_div = plotly.offline.plot(figure, output_type='div')

    return render_template('index.html', plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
