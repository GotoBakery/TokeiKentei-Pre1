
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy.stats import skewnorm, norm, laplace, cosine, t

def create_skewness_plot():
    x = np.linspace(-4, 4, 1000)
    
    # Negative Skew
    y_neg = skewnorm.pdf(x, -5)
    # Symmetric (Normal)
    y_sym = norm.pdf(x)
    # Positive Skew
    y_pos = skewnorm.pdf(x, 5)

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.plot(x, y_neg, label='負の歪度', color='blue')
    plt.title('負の歪度 (左に裾が長い)')
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    plt.yticks([])
    
    plt.subplot(1, 3, 2)
    plt.plot(x, y_sym, label='対称', color='green')
    plt.title('対称 (正規分布)')
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    plt.yticks([])

    plt.subplot(1, 3, 3)
    plt.plot(x, y_pos, label='正の歪度', color='red')
    plt.title('正の歪度 (右に裾が長い)')
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    plt.yticks([])

    plt.tight_layout()
    plt.savefig('notes/images/skewness.png')
    plt.close()

def create_kurtosis_plot():
    x = np.linspace(-4, 4, 1000)

    # Leptokurtic (High Kurtosis)
    y_lepto = t.pdf(x, df=2)
    
    # Mesokurtic (Normal Kurtosis)
    y_meso = norm.pdf(x)
    
    # Platykurtic (Low Kurtosis)
    y_platy = cosine.pdf(x)

    plt.figure(figsize=(10, 6))
    
    plt.plot(x, y_lepto, label='急尖 (尖度が大きい)', color='red', linestyle='-')
    plt.plot(x, y_meso, label='正規 (尖度=3)', color='green', linestyle='--')
    plt.plot(x, y_platy, label='緩尖 (尖度が小さい)', color='blue', linestyle='-.')
    
    plt.title('尖度の比較')
    plt.legend()
    plt.yticks([])
    plt.axvline(x=0, color='gray', linestyle=':', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('notes/images/kurtosis.png')
    plt.close()

if __name__ == "__main__":
    create_skewness_plot()
    create_kurtosis_plot()
