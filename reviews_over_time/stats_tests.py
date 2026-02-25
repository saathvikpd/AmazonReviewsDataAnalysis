import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests

def compute_corr(time, num_reviews, helpful_votes, max_lag = 50):
    
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

    plt.figure(0)
    ax = plt.plot(list(map(lambda x: x[0], corr_data)), list(map(lambda x: x[1], corr_data)))
    plt.xlabel("Time Lag")
    plt.ylabel("Correlation")
    plt.title("Correlation between num reviews & lagged helpful votes")
    plt.savefig("plots/corr_plot.png")

    return ax


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

def compute_granger(time, num_reviews, helpful_votes, num_lag = 1):

    df = pd.DataFrame({
        "reviews": num_reviews,
        "helpful": helpful_votes
    })


    data = df[["reviews", "helpful"]]
    
    test_results = grangercausalitytests(data, maxlag = num_lag)

    return test_results


def run_tests(time, num_reviews, helpful_votes):

    print("Generating correlation plot...")

    compute_corr(time, num_reviews, helpful_votes)

    print("Computing OLS...")

    model = compute_OLS(time, num_reviews, helpful_votes)

    print(model.summary())

    print("Running Granger Causality test...")

    test_results = compute_granger(time, num_reviews, helpful_votes)
    