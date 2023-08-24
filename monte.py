import numpy as np

def monte_carlo_option_price(r, S, K, T, volatility, option_type="c", sims=10000):
    """
    """

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

# Test
r = 0.05
S = 100
K = 100
T = 1
volatility = 0.2
sims = 10000
call_price = monte_carlo_option_price(r, S, K, T, volatility, "c", sims)
put_price = monte_carlo_option_price(r, S, K, T, volatility, "p", sims)
print(f"Call Option Price: {call_price}")
print(f"Put Option Price: {put_price}")

