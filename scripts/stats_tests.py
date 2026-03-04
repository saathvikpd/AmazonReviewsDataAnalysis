import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests

def compute_corr(time, num_reviews, helpful_votes, max_lag = 50, category = "All_Beauty"):
    
    df = pd.DataFrame({
        "reviews": num_reviews,
        "helpful": helpful_votes
    })
    
    results = {}
    
    for lag in range(0, max_lag):
        df[f"helpful_lag{lag}"] = df["helpful"].shift(lag)
        results[-lag] = df["reviews"].corr(df[f"helpful_lag{lag}"])
    
    corr_data = results.items()
    corr_data = sorted(results.items(), key = lambda x: x[0])

    plt.figure()
    ax = plt.plot(list(map(lambda x: x[0], corr_data)), list(map(lambda x: x[1], corr_data)))
    plt.xlabel("Time Lag")
    plt.ylabel("Correlation")
    plt.title(f"Corr b/w num reviews & lagged helpful votes, Category: '{category}")
    plt.savefig(f"plots/corr_plot_{category}.png")

    peak_lag = -max(corr_data, key = lambda x: x[1])[0]

    return ax, peak_lag


def compute_OLS(time, num_reviews, helpful_votes, lag = 1):

    df = pd.DataFrame({
        "reviews": num_reviews,
        "helpful": helpful_votes
    })

    df[f"reviews_lag{lag}"] = df["reviews"].shift(lag)
    df[f"helpful_lag{lag}"] = df["helpful"].shift(lag)
    
    df = df.dropna()
        
    X = df[[f"reviews_lag{lag}", f"helpful_lag{lag}"]]
    X = sm.add_constant(X)

    model = sm.OLS(df["reviews"], X).fit()

    return model

def compute_granger(time, num_reviews, helpful_votes, num_lag = 1, category = "All_Beauty"):

    df = pd.DataFrame({
        "reviews": num_reviews,
        "helpful": helpful_votes
    })


    data = df[["reviews", "helpful"]]
    
    results = grangercausalitytests(data, maxlag = num_lag)

    p_values = []

    for lag in range(1, num_lag + 1):
        p_val = results[lag][0]['ssr_ftest'][1]
        p_values.append(p_val)

    lags = np.arange(1, num_lag + 1)

    plt.figure()
    plt.plot(lags, p_values, marker='o')
    plt.axhline(0.05, linestyle='--')
    plt.xlabel("Lag")
    plt.ylabel("Granger causality p-val")
    plt.title(f"Granger causality p-vals vs lag, Category: '{category}")
    plt.savefig(f"plots/granger_{category}.png")

    return results


def run_tests(time, num_reviews, helpful_votes, category = "All_Beauty"):

    print("Generating correlation plot...")

    plot, peak_lag = compute_corr(time, num_reviews, helpful_votes, category = category)

    print(f"Correlation peaks at lag = {peak_lag}")

    print("Computing OLS...")

    model = compute_OLS(time, num_reviews, helpful_votes, lag = peak_lag)

    print(model.summary())

    print("Running Granger Causality test...")

    test_results = compute_granger(time, num_reviews, helpful_votes, num_lag = peak_lag, category = category)
    