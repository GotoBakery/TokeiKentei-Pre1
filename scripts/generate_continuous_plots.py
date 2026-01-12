import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy.stats import uniform, norm, expon, gamma, beta, chi2, t, f
import os

# Output directory
output_dir = "/workspaces/TokeiKentei-Pre1/notes/images"
os.makedirs(output_dir, exist_ok=True)

def plot_pdf(x, y, title, filename):
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, color='skyblue', linewidth=2)
    plt.fill_between(x, y, color='skyblue', alpha=0.3)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

# 1. Continuous Uniform Distribution
x = np.linspace(-1, 6, 1000)
y = uniform.pdf(x, loc=0, scale=5) # 0 to 5
plot_pdf(x, y, "連続一様分布 U(0, 5)", "continuous_uniform.png")

# 2. Normal Distribution
x = np.linspace(-4, 4, 1000)
y = norm.pdf(x)
plot_pdf(x, y, "標準正規分布 N(0, 1)", "normal.png")

# 3. Exponential Distribution
x = np.linspace(0, 5, 1000)
y = expon.pdf(x, scale=1) # lambda=1 -> scale=1/lambda = 1
plot_pdf(x, y, "指数分布 Exp(1)", "exponential.png")

# 4. Gamma Distribution
x = np.linspace(0, 10, 1000)
y = gamma.pdf(x, a=2, scale=2) # shape=2, scale=2
plot_pdf(x, y, "ガンマ分布 Ga(2, 2)", "gamma.png")

# 5. Beta Distribution
x = np.linspace(0, 1, 1000)
y = beta.pdf(x, 2, 5)
plot_pdf(x, y, "ベータ分布 Be(2, 5)", "beta.png")

# 6. Chi-squared Distribution
x = np.linspace(0, 10, 1000)
y = chi2.pdf(x, df=3)
plot_pdf(x, y, "カイ二乗分布 (df=3)", "chi2.png")

# 7. t Distribution
x = np.linspace(-4, 4, 1000)
y = t.pdf(x, df=2)
plot_pdf(x, y, "t分布 (df=2)", "t_dist.png")

# 8. F Distribution
x = np.linspace(0, 5, 1000)
y = f.pdf(x, dfn=5, dfd=2)
plot_pdf(x, y, "F分布 (df1=5, df2=2)", "f_dist.png")

print("Generated continuous plots in", output_dir)
