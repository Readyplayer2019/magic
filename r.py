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
    # ... (rest of the black_scholes function)

black_scholes()

@app.route('/', methods=['GET', 'POST'])
def index():
    # ... (rest of the index function)
