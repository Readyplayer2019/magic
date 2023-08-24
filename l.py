from flask import Flask, render_template, request
import numpy as np
import math
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / np.sqrt(2)))

def black_scholes(r, S, K, T, volatility, option_type="c"):
    # ... (Same as above)

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_div = None
    call_price = None
    put_price = None

    if request.method == 'POST':
        r = float(request.form['r'])
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])
        volatility = float(request.form['volatility'])

        call_price = black_scholes(r, S, K, T, volatility, option_type="c")
        put_price = black_scholes(r, S, K, T, volatility, option_type="p")

        # Let's assume you want option prices for the next 10 years
        years = list(range(1, 11))
        call_prices = [black_scholes(r, S, K, year, volatility, option_type="c") for year in years]
        put_prices = [black_scholes(r, S, K, year, volatility, option_type="p") for year in years]

        # Create the plot
        trace1 = go.Scatter(x=years, y=call_prices, mode="lines+markers", name="Call Option Price")
        trace2 = go.Scatter(x=years, y=put_prices, mode="lines+markers", name="Put Option Price")
        layout = go.Layout(title="Option Prices over the Years", xaxis=dict(title="Year"), yaxis=dict(title="Price"))
        figure = go.Figure(data=[trace1, trace2], layout=layout)
        plot_div = plotly.offline.plot(figure, output_type='div')

    return render_template('index.html', plot_div=plot_div, call_price=call_price, put_price=put_price)

if __name__ == '__main__':
    app.run(debug=True)
