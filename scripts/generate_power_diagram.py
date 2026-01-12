
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy.stats import norm

def plot_power_concept():
    # Parameters
    p0 = 0.5
    p1 = 0.65
    n = 100
    alpha = 0.05
    
    # Standard deviations
    sigma0 = np.sqrt(p0 * (1 - p0) / n)
    sigma1 = np.sqrt(p1 * (1 - p1) / n)
    
    # Critical value (one-sided)
    z_crit = norm.ppf(1 - alpha)
    x_crit = p0 + z_crit * sigma0
    
    # X range
    x = np.linspace(0.35, 0.8, 1000)
    
    # Distributions
    y0 = norm.pdf(x, p0, sigma0)
    y1 = norm.pdf(x, p1, sigma1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot H0 distribution
    ax.plot(x, y0, label='帰無仮説 $H_0$ ($p=p_0$)', color='blue')
    ax.fill_between(x, y0, where=(x >= x_crit), color='blue', alpha=0.3, label='有意水準 $\\alpha$ (第一種の過誤)')
    
    # Plot H1 distribution
    ax.plot(x, y1, label='対立仮説 $H_1$ ($p=p_1$)', color='red')
    ax.fill_between(x, y1, where=(x >= x_crit), color='red', alpha=0.3, label='検出力 $1-\\beta$')
    ax.fill_between(x, y1, where=(x < x_crit), color='orange', alpha=0.3, label='$\\beta$ (第二種の過誤)')
    
    # Critical value line
    ax.axvline(x=x_crit, color='black', linestyle='--', label=f'棄却限界値 $x_c$')
    
    # Annotations
    ax.annotate(f'棄却限界値\n$p_0 + 1.96\\sigma_0$', xy=(x_crit, max(y0)/2), xytext=(x_crit+0.05, max(y0)/2),
                arrowprops=dict(facecolor='black', shrink=0.05))
    
    ax.set_title('検出力とサンプルサイズの概念図')
    ax.set_xlabel('標本比率 $\\hat{p}$')
    ax.set_ylabel('確率密度')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('/workspaces/TokeiKentei-Pre1/notes/images/power_sample_size.png')
    plt.close()

if __name__ == "__main__":
    plot_power_concept()
