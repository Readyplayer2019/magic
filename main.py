import numpy as np
import math

def norm_cdf(x):
    """Compute the CDF of the standard normal distribution."""
    return 0.5 * (1 + math.erf(x / np.sqrt(2)))

def black_scholes(r, S, K, T, volatility, option_type="c"):
    """
    Calculate Black-Scholes price of a European call or put option.
    """
    if not (option_type == "c" or option_type == "p"):
        print("Option type must be either 'c' for Call or 'p' for Put!")
        exit()

    d1 = (np.log(S / K) + (r + volatility ** 2 / 2) * T) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    if option_type == "c":
        option_price = S * norm_cdf(d1) - K * np.exp(-r * T) * norm_cdf(d2)
    else:
        option_price = K * np.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

    return option_price

if __name__ == "__main__":
    r = float(input("Enter risk-free rate: "))
    S = float(input("Enter stock price: "))
    K = float(input("Enter strike price: "))
    T = float(input("Enter time to maturity in years: "))
    volatility = float(input("Enter volatility: "))

    call_price = black_scholes(r, S, K, T, volatility, option_type="c")
    put_price = black_scholes(r, S, K, T, volatility, option_type="p")

    print(f"Call option price: {call_price:.2f}")
    print(f"Put option price: {put_price:.2f}")
