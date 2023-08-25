from flask import Flask, render_template, request, jsonify
import numpy as np
import math

app = Flask(__name__)
sims = 10000
""""
def heston_simulation(ia, iv, mu, p, theta, sigma, r, T, dt):
    N = int(T / dt)
    s = np.zeros(N + 1)
    v = np.zeros(N + 1)
    s[0] = ia
    v[0] = iv
    for t in range(1, N + 1):
        dW1 = np.sqrt(dt) * np.random.normal()
        dW2 = r * dW1 + np.sqrt(1 - r ** 2) * np.sqrt(dt) * np.random.normal()

        v[t] = v[t - 1] + p * (theta - max(v[t - 1], 0)) * dt + sigma * np.sqrt(max(v[t - 1], 0)) * dW2
        v[t] = max(v[t], 0)
        s[t] = s[t - 1] * np.exp((mu - 0.5 * v[t]) * dt + np.sqrt(v[t]) * dW1)
    return s, np.sqrt(v)
"""
import numpy as np


def heston_simulation(ia, iv, mu, p, theta, sigma, r, T, dt):
    if not -1 <= r <= 1:
        raise ValueError("Correlation coefficient 'r' must be between -1 and 1.")

    # Number of steps
    N = int(T / dt)
    # Initialize stock and volatility paths
    s = np.zeros(N + 1)
    v = np.zeros(N + 1)
    # Initial values
    s[0] = ia
    v[0] = iv

    for t in range(1, N + 1):
        # Generate correlated Brownian motions
        dW1 = np.sqrt(dt) * np.random.normal()
        dW2 = r * dW1 + np.sqrt(1 - r ** 2) * np.sqrt(dt) * np.random.normal()

        # Update volatility path
        v[t] = v[t - 1] + p * (theta - max(v[t - 1], 0)) * dt + sigma * np.sqrt(max(v[t - 1], 0)) * dW2
        v[t] = max(v[t], 0)  # Ensure volatility is non-negative

        if v[t] > 1e-8:  # Check if the volatility is close to zero
            s[t] = s[t - 1] * np.exp((mu - 0.5 * v[t]) * dt + np.sqrt(v[t]) * dW1)
        else:
            s[t] = s[t - 1]  # No change if volatility is almost zero

    return s, np.sqrt(v)


def monte_carlo_option_price(r, S, K, T, volatility, option_type="c", sims=10000):
    dt = 1.0
    discount_factor = np.exp(-r * T)
    payoffs = []

    for _ in range(sims):
        st = S
        for _ in range(int(T)):
            z = np.random.standard_normal()
            st *= np.exp((r - 0.5 * volatility ** 2) * dt + volatility * np.sqrt(dt) * z)
        if option_type == "c":
            payoffs.append(max(0, st - K))
        else:
            payoffs.append(max(0, K - st))
    return discount_factor * np.mean(payoffs)


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / np.sqrt(2)))


""""
def get_price(r, S, K, T, volatility, option_type="c", model="black-scholes"):
    match model:
        case "black-scholes":
            return black_scholes(r, S, K, T, volatility, option_type)
        case "monte-carlo":
            return monte_carlo_option_price(r, S, K, T, volatility, option_type)
"""


def get_price(r, S, K, T, volatility, option_type="c", model="black-scholes"):
    if model == "black-scholes":
        return black_scholes(r, S, K, T, volatility, option_type)
    elif model == "heston":
        ia = S
        iv = volatility ** 2  # Assuming you pass annualized volatility
        mu = r
        k = 0.3  # mean-reversion speed
        theta = 0.04  # long-term variance
        sigma = 0.1  # vol of vol
        dt = 0.01  # time step
        payoffs = []
        for _ in range(sims):
            st, _ = heston_simulation(ia, iv, mu, k, theta, sigma, r, T, dt)
            if option_type == "c":
                payoffs.append(max(0, st[-1] - K))
            else:
                payoffs.append(max(0, K - st[-1]))

        discount_factor = np.exp(-r * T)
        return discount_factor * np.mean(payoffs)
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


@app.route('/heston')
def heston():
    return render_template('heston.html')


@app.route('/api/option')
def api():
    rate = float(request.args.get('rate')) / 100
    stock = float(request.args.get('stock'))
    strike = float(request.args.get('strike'))
    maturity = float(request.args.get('maturity'))
    volatility = float(request.args.get('volatility')) / 100

    model = request.args.get('model')

    years = list(range(1, int(maturity) + 1))
    call_prices = [get_price(rate, stock, strike, year, volatility, "c", model) for year in years]
    put_prices = [get_price(rate, stock, strike, year, volatility, "p", model) for year in years]

    print(call_prices, put_prices)

    return jsonify({"call_prices": call_prices, "put_prices": put_prices})


@app.route("/api/heston")
def heston_api():
    initial_asset = float(request.args.get('initial_asset'))
    initial_variance = float(request.args.get('initial_variance')) / 100
    rate_of_return = float(request.args.get('Rate_of_return'))
    theta = float(request.args.get('theta'))
    reversion = float(request.args.get('k')) / 100
    dt = float(request.args.get('dt'))
    sigma = float(request.args.get('sigma')) / 100
    simulation_time = float(request.args.get("simulation_time"))
    correlation_with_asset = float(request.args.get('correlation_with_asset')) / 100

    s, v = heston_simulation(initial_asset, initial_variance, rate_of_return, reversion, theta, sigma,
                             correlation_with_asset, simulation_time, dt)
    output = jsonify({"asset_price": list(s), "stochastic_volatility": list(v)})
    print({"asset_price": list(s), "stochastic_volatility": list(v)})
    return output


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
