from flask import Flask, render_template, request

app = Flask(__name__)

import numpy as np
import math


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / np.sqrt(2)))


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
    if request.method == 'POST':
        r = float(request.form['r'])
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])
        volatility = float(request.form['volatility'])

        call_price = black_scholes(r, S, K, T, volatility, option_type="c")
        put_price = black_scholes(r, S, K, T, volatility, option_type="p")

        return render_template('index.html', call_price=call_price, put_price=put_price)

    return render_template('index.html')

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World 1234!</p>"

if __name__ == '__main__':
    app.run(debug=True)


