import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import bernoulli
from scipy.stats import binom
import sys

#https://stackoverflow.com/questions/24788200/calculate-the-cumulative-distribution-function-cdf-in-python
def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def plot_ecdf(a):
    x, y = ecdf(a)
    x = np.insert(x, 0, x[0])
    y = np.insert(y, 0, 0.)
    plt.plot(x, y, drawstyle='steps-post')
    plt.show()

def plot_binom(n, p):
    cdf = binom.cdf([x for x in range(256)], n, p)
    # Plot CDF
    #plt.subplot(1, 2, 2)
    plt.step([x for x in range(256)], cdf, where='post')
    plt.title(f'Binomial CDF (n={n}, p={p})')
    plt.xlabel('Number of successes')
    plt.ylabel('Cumulative Probability')
    plt.xticks(np.arange(0, 256, 16))
    #plt.xticks(x)
    plt.ylim(0, 1.1)
    plt.show()

def test_monte_carlo():
    #vals = np.asarray([], dtype=int)
    vals = np.random.randint(0, 256, 100000)
    x_values = [x for x in range(256)]
    unique, counts = np.unique(vals, return_counts=True)
    plt.bar(x_values,counts)
    plt.show()

    plot_ecdf(vals)

def test_bernoulli():
    # Parameters for the Bernoulli distribution
    p = 0.5  # Probability of success

    # Values for the Bernoulli random variable (0 and 1)
    #x = np.array([0, 1])
    x = [x for x in range(256)]

    # PMF and CDF
    pmf = bernoulli.pmf(x, p)
    cdf = bernoulli.cdf(x, p)

    # Plot PMF
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.stem(x, pmf, use_line_collection=True)
    plt.title('Bernoulli PMF')
    plt.xlabel('x')
    plt.ylabel('Probability')
    plt.xticks([0, 1])
    plt.ylim(0, 1.1)

    # Plot CDF
    plt.subplot(1, 2, 2)
    plt.step(x, cdf, where='post')
    plt.title('Bernoulli CDF')
    plt.xlabel('x')
    plt.ylabel('Cumulative Probability')
    plt.xticks([0, 1])
    plt.ylim(0, 1.1)

    plt.tight_layout()
    plt.show()


def test_binomial():
    # Parameters for the Binomial distribution
    n = 100  # Number of trials
    p = 0.5  # Probability of success in each trial

    # Values for the Binomial random variable (from 0 to n)
    #x = np.arange(0, n + 1)

    # PMF and CDF
    pmf = binom.pmf(x, n, p)
    cdf = binom.cdf(x, n, p)

    # Plot PMF
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.stem(x, pmf, use_line_collection=True)
    plt.title(f'Binomial PMF (n={n}, p={p})')
    plt.xlabel('Number of successes')
    plt.ylabel('Probability')
    plt.xticks(np.arange(0, 256, 16))
    plt.ylim(0, 1.1)

    # Plot CDF
    plt.subplot(1, 2, 2)
    plt.step(x, cdf, where='post')
    plt.title(f'Binomial CDF (n={n}, p={p})')
    plt.xlabel('Number of successes')
    plt.ylabel('Cumulative Probability')
    plt.xticks(np.arange(0, 256, 16))
    #plt.xticks(x)
    plt.ylim(0, 1.1)

    plt.tight_layout()
    plt.show()

def main():
    args = sys.argv[1:]
    n = int(args[0])
    #p = float(args[1])
    t = int(args[1]) # threshold, below 256
    p = t/256
    plot_binom(n, p)

if __name__ == "__main__":
    main()

