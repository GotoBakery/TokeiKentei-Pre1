import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy.stats import binom, poisson, geom, nbinom
import os

# Output directory
output_dir = "/workspaces/TokeiKentei-Pre1/notes/images"
os.makedirs(output_dir, exist_ok=True)

def plot_pmf(x, pmf, title, filename):
    plt.figure(figsize=(6, 4))
    plt.bar(x, pmf, color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel("k")
    plt.ylabel("P(X=k)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

# 1. Bernoulli Distribution
x = [0, 1]
pmf = binom.pmf(x, 1, 0.6) # Using binom with n=1 is Bernoulli
plt.figure(figsize=(4, 4))
plt.bar(x, pmf, color='skyblue', edgecolor='black', width=0.4)
plt.xticks([0, 1])
plt.title("ベルヌーイ分布 (p=0.6)")
plt.savefig(os.path.join(output_dir, "bernoulli.png"))
plt.close()

# 2. Binomial Distribution
x = np.arange(0, 16)
pmf = binom.pmf(x, 15, 0.4)
plot_pmf(x, pmf, "二項分布 (n=15, p=0.4)", "binomial.png")

# 3. Poisson Distribution
x = np.arange(0, 16)
pmf = poisson.pmf(x, 4)
plot_pmf(x, pmf, "ポアソン分布 (lambda=4)", "poisson.png")

# 4. Geometric Distribution
x = np.arange(1, 11)
pmf = geom.pmf(x, 0.3)
plot_pmf(x, pmf, "幾何分布 (p=0.3)", "geometric.png")

# 5. Negative Binomial Distribution
x = np.arange(0, 21)
pmf = nbinom.pmf(x, 5, 0.4) # x is number of failures
plot_pmf(x, pmf, "負の二項分布 (r=5, p=0.4)", "nbinom.png")

print("Generated plots in", output_dir)
