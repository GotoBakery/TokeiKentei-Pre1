import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import japanize_matplotlib

# Directory setup
OUTPUT_DIR = "/workspaces/TokeiKentei-Pre1/notes/assets/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Style settings
plt.style.use('ggplot')
plt.rcParams['font.family'] = 'IPAexGothic' # Fallback, japanize-matplotlib handles this usually

def save_plot(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
    plt.close()
    print(f"Saved {filename}")

def plot_bernoulli():
    p = 0.3
    x = [0, 1]
    y = [1-p, p]
    plt.figure(figsize=(6, 4))
    plt.bar(x, y, color='skyblue', edgecolor='black', width=0.5)
    plt.xticks([0, 1], ['失敗 (0)', '成功 (1)'])
    plt.title(f'ベルヌーイ分布 (p={p})')
    plt.ylabel('確率')
    save_plot('bernoulli.png')

def plot_binomial():
    n, p = 10, 0.5
    x = np.arange(0, n+1)
    y = stats.binom.pmf(x, n, p)
    plt.figure(figsize=(6, 4))
    plt.bar(x, y, color='skyblue', edgecolor='black')
    plt.title(f'二項分布 (n={n}, p={p})')
    plt.xlabel('成功回数')
    plt.ylabel('確率')
    save_plot('binomial.png')

def plot_poisson():
    lam = 3
    x = np.arange(0, 15)
    y = stats.poisson.pmf(x, lam)
    plt.figure(figsize=(6, 4))
    plt.bar(x, y, color='lightgreen', edgecolor='black')
    plt.title(f'ポアソン分布 ($\lambda$={lam})')
    plt.xlabel('発生回数')
    plt.ylabel('確率')
    save_plot('poisson.png')

def plot_geometric():
    p = 0.3
    x = np.arange(0, 15) # Failures before first success
    y = stats.geom.pmf(x+1, p) # scipy defines geom by trials, so shift? No, wait. 
    # Notes say: X = failures before success. 
    # scipy.stats.geom is number of trials to get first success (supported on {1, 2, ...})
    # PMF(k) = (1-p)^{k-1} p.
    # Note def: P(X=x) = (1-p)^x p for x=0, 1, ...
    # So if Y ~ geom(p), Y \in {1, 2..}, then X = Y - 1.
    # P(Y-1 = x) = P(Y = x+1) = (1-p)^{x+1-1} p = (1-p)^x p. Correct.
    y = stats.geom.pmf(x+1, p)
    
    plt.figure(figsize=(6, 4))
    plt.bar(x, y, color='salmon', edgecolor='black')
    plt.title(f'幾何分布 (p={p}) \n (初めて成功するまでの失敗回数)')
    plt.xlabel('失敗回数')
    plt.ylabel('確率')
    save_plot('geometric.png')

def plot_nbinom():
    r, p = 3, 0.5
    x = np.arange(0, 15)
    # Notes: failures X until r successes. 
    # scipy.stats.nbinom(n, p) is failures. n is number of successes (r).
    # PMF(k) = choose(k+n-1, n-1) p^n (1-p)^k.
    # Note def: choose(x+r-1, x) p^r (1-p)^x. 
    # Same since choose(n, k) = choose(n, n-k). choose(x+r-1, x) = choose(x+r-1, r-1).
    y = stats.nbinom.pmf(x, r, p)
    
    plt.figure(figsize=(6, 4))
    plt.bar(x, y, color='orange', edgecolor='black')
    plt.title(f'負の二項分布 (r={r}, p={p})')
    plt.xlabel('失敗回数')
    plt.ylabel('確率')
    save_plot('nbinom.png')

def plot_continuous_uniform():
    a, b = 2, 5
    x = np.linspace(a-1, b+1, 100)
    y = stats.uniform.pdf(x, loc=a, scale=b-a)
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, color='blue')
    plt.fill_between(x, y, alpha=0.3, color='blue')
    plt.title(f'連続一様分布 U({a}, {b})')
    save_plot('continuous_uniform.png')

def plot_normal():
    mu, sigma = 0, 1
    x = np.linspace(-4, 4, 100)
    y = stats.norm.pdf(x, mu, sigma)
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, color='red')
    plt.fill_between(x, y, alpha=0.3, color='red')
    plt.title(f'正規分布 N({mu}, {sigma}^2)')
    save_plot('normal.png')

def plot_exponential():
    lam = 1.0 # lambda
    # scipy exponential scale = 1/lambda
    x = np.linspace(0, 5, 100)
    y = stats.expon.pdf(x, scale=1/lam)
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, color='green')
    plt.fill_between(x, y, alpha=0.3, color='green')
    plt.title(f'指数分布 Exp({lam})')
    save_plot('exponential.png')

def plot_gamma():
    # Ga(a, b), a: shape, b: scale
    a, b = 2, 2
    # scipy gamma(a, scale=size). Note def: scale b is 1/beta commonly, here it says b is scale parameter.
    # Notes: f(x) = 1/(Gamma(a)b^a) x^{a-1} e^{-x/b}.
    # Scipy gamma.pdf(x, a, scale=1) is 1/Gamma(a) x^{a-1} e^{-x}.
    # With scale=b: 1/(Gamma(a)b) (x/b)^{a-1} e^{-x/b} * (1/b)? No.
    # Scipy docs: pdf(x, a, loc, scale) = gamma.pdf(y, a) / scale with y = (x-loc)/scale
    # = (1/scale) * (y^{a-1} e^{-y} / Gamma(a))
    # = (1/b) * ((x/b)^{a-1} e^{-x/b} / Gamma(a))
    # = (1/b) * (x^{a-1} / b^{a-1} * e^{-x/b} / Gamma(a))
    # = x^{a-1} / (b^a Gamma(a)) * e^{-x/b}. Matches notes!
    x = np.linspace(0, 15, 100)
    y = stats.gamma.pdf(x, a, scale=b)
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, color='purple')
    plt.fill_between(x, y, alpha=0.3, color='purple')
    plt.title(f'ガンマ分布 Ga({a}, {b})')
    save_plot('gamma.png')

def plot_beta():
    a, b = 2, 5
    x = np.linspace(0, 1, 100)
    y = stats.beta.pdf(x, a, b)
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, color='orange')
    plt.fill_between(x, y, alpha=0.3, color='orange')
    plt.title(f'ベータ分布 Be({a}, {b})')
    save_plot('beta.png')

def plot_chi2():
    df_list = [1, 3, 5]
    x = np.linspace(0, 10, 100)
    plt.figure(figsize=(6, 4))
    for df in df_list:
        y = stats.chi2.pdf(x, df)
        plt.plot(x, y, label=f'df={df}')
    plt.title('カイ二乗分布')
    plt.legend()
    save_plot('chi2.png')

def plot_t_dist():
    df_list = [1, 5, 30]
    x = np.linspace(-4, 4, 1000)
    plt.figure(figsize=(6, 4))
    plt.plot(x, stats.norm.pdf(x), label='Normal', linestyle='--', color='black', alpha=0.5)
    for df in df_list:
        y = stats.t.pdf(x, df)
        plt.plot(x, y, label=f't(df={df})')
    plt.title('t分布')
    plt.legend()
    save_plot('t_dist.png')

def plot_f_dist():
    df_pairs = [(10, 10), (10, 20), (50, 50)]
    x = np.linspace(0.01, 3, 100)
    plt.figure(figsize=(6, 4))
    for d1, d2 in df_pairs:
        y = stats.f.pdf(x, d1, d2)
        plt.plot(x, y, label=f'F({d1}, {d2})')
    plt.title('F分布')
    plt.legend()
    save_plot('f_dist.png')

def plot_distribution_relations():
    # Professional SVG Layout for Discrete Distributions
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Nodes Position
    nodes_data = {
        'Bernoulli': (0.5, 0.9, 'ベルヌーイ分布\nBin(1, p)'),
        'Binomial': (0.5, 0.65, '二項分布\nBin(n, p)'),
        'Geometric': (0.1, 0.65, '幾何分布\nGeo(p)'),
        'HyperGeom': (0.9, 0.65, '超幾何分布\nHG(N, M, n)'),
        'Poisson': (0.5, 0.3, 'ポアソン分布\nPo(λ)'),
        'NegBinom': (0.1, 0.3, '負の二項分布\nNB(r, p)'),
    }
    
    import matplotlib.patches as mpatches
    import math
    
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Store patch objects to link arrows
    node_patches = {}

    def draw_box(name, x, y, label):
        t = ax.text(x, y, label, ha='center', va='center', fontsize=16, fontweight='bold', zorder=10)
        t.set_bbox(dict(boxstyle="round,pad=1.0,rounding_size=0.2", fc="white", ec="#7f8c8d", linewidth=2, alpha=1.0))
        # Force a draw (or at least get the patch structure) - usually set_bbox creates it
        # We access the patch from the text object
        node_patches[name] = t.get_bbox_patch()

    for name, (x, y, label) in nodes_data.items():
        draw_box(name, x, y, label)
        
    # Arrows
    arrows = [
        ('Bernoulli', 'Binomial', 'n回試行\n(独立和)', '#2980b9', 0.0), # Blue (Sum)
        ('Bernoulli', 'Geometric', '初めて成功', '#34495e', -0.3),
        ('Binomial', 'Poisson', 'n→∞, p→0\n(極限)', '#c0392b', 0.0),
        ('HyperGeom', 'Binomial', 'N→∞\n(近似)', '#c0392b', 0.0),
        ('Geometric', 'NegBinom', 'r回成功\n(独立和)', '#2980b9', 0.0),
    ]
    
    for start, end, label, color, rad in arrows:
        # Use patchA/patchB to stop arrow at the boundary of the box
        # shrinkA/shrinkB adds a little gap
        
        # Calculate label position
        sx, sy, _ = nodes_data[start]
        ex, ey, _ = nodes_data[end]
        
        # Draw Arrow
        # Note: when using patchA/patchB, xy and xytext are ignored for positioning!
        # The spacing is handled by connectionstyle and shrink
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.8,head_length=1.5", 
                                    connectionstyle=f"arc3,rad={rad}", 
                                    color=color, linewidth=3,
                                    patchA=node_patches[start],
                                    patchB=node_patches[end],
                                    shrinkA=0, shrinkB=0),
                    zorder=1)
        
        # Manual Label Positioning
        # Since we use patchA/patchB, the arrow follows the shortest path between patches (modified by arc)
        # Getting the exact midpoint of that path is tricky without the renderer.
        # We will use the center-to-center arc calculation but be conservative.
        
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        dx, dy = ex - sx, ey - sy
        dist = math.sqrt(dx*dx + dy*dy)
        
        if rad != 0 and dist > 0:
            shift = rad * dist * 0.5
            nx, ny = dy/dist, -dx/dist # Right Normal
            mx += nx * shift
            my += ny * shift
            
        # Draw Label
        ax.text(mx, my, label, ha='center', va='center', fontsize=14, color=color, fontweight='bold',
                bbox=dict(fc='white', ec=color, boxstyle="square,pad=0.4", alpha=1.0, linewidth=1.5), zorder=5)

    # Legend
    legend_elements = [
        mpatches.Patch(color='#c0392b', label='極限・近似 (Limit/Approx)'),
        mpatches.Patch(color='#2980b9', label='和・特殊化 (Sum/Special Case)'),
        mpatches.Patch(color='#34495e', label='基本的な導出 (Basic Derivation)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=12, frameon=True, framealpha=1.0, edgecolor='#bdc3c7')

    plt.title('離散型分布の体系', fontsize=24, y=0.98)
    save_plot('distribution_relations.svg')

def plot_continuous_relations():
    # Professional SVG Layout for Continuous Distributions
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.axis('off')
    import math
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    nodes_data = {
        'Normal': (0.2, 0.9, '正規分布\nN(μ, σ^2)'),
        'StdNormal': (0.2, 0.65, '標準正規分布\nN(0, 1)'),
        't': (0.2, 0.3, 't分布\nt(k)'),
        
        'Chi2': (0.55, 0.65, 'カイ二乗分布\nχ^2(k)'),
        'F': (0.55, 0.3, 'F分布\nF(m, n)'),
        
        'Gamma': (0.85, 0.65, 'ガンマ分布\nGa(a, b)'),
        'Exp': (0.85, 0.3, '指数分布\nExp(λ)'),
    }
    
    node_patches = {}
    
    for name, (x, y, label) in nodes_data.items():
        t = ax.text(x, y, label, ha='center', va='center', fontsize=16, fontweight='bold', zorder=10)
        t.set_bbox(dict(boxstyle="round,pad=1.0,rounding_size=0.2", fc="white", ec="#7f8c8d", linewidth=2, alpha=1.0))
        node_patches[name] = t.get_bbox_patch()
        
    # Arrows
    arrows = [
        ('Normal', 'StdNormal', '標準化', '#34495e', 0.0),
        ('StdNormal', 'Chi2', '二乗和', '#2980b9', 0.0), # Blue (Sum of squares)
        ('Gamma', 'Exp', 'a=1\n(特殊ケース)', '#2980b9', 0.0),
        ('Gamma', 'Chi2', 'a=k/2, b=2', '#2980b9', 0.0), # Straight Left
        ('StdNormal', 't', '分子: Z', '#f39c12', 0.0), # Orange (Construction)
        ('Chi2', 't', '分母: \u221A(Y/k)', '#f39c12', 0.15),
        ('Chi2', 'F', '定義: 比', '#f39c12', 0.0),
    ]
    
    for start, end, label, color, rad in arrows:
        sx, sy, _ = nodes_data[start]
        ex, ey, _ = nodes_data[end]
        
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.8,head_length=1.5", 
                                    connectionstyle=f"arc3,rad={rad}", 
                                    color=color, linewidth=3,
                                    patchA=node_patches[start],
                                    patchB=node_patches[end],
                                    shrinkA=0, shrinkB=0),
                    zorder=1)
        
        # Label placement
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        dx, dy = ex - sx, ey - sy
        dist = math.sqrt(dx*dx + dy*dy)
        
        if rad != 0 and dist > 0:
            shift = rad * dist * 0.5
            nx, ny = dy/dist, -dx/dist # Right Normal to match arc3 curvature direction
            mx += nx * shift
            my += ny * shift

        if label:
            ax.text(mx, my, label, ha='center', va='center', fontsize=14, color=color, fontweight='bold',
                    bbox=dict(fc='white', ec=color, boxstyle="square,pad=0.4", alpha=1.0, linewidth=1.5), zorder=5)
    
    # Legend
    import matplotlib.patches as mpatches
    legend_elements = [
        mpatches.Patch(color='#34495e', label='標準的な導出 (Standard Derivation)'),
        mpatches.Patch(color='#2980b9', label='特殊ケース (Special Case)'),
        mpatches.Patch(color='#f39c12', label='定義による構成 (Construction)'),
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=12, frameon=True, framealpha=1.0, edgecolor='#bdc3c7')
    
    plt.title('連続型分布の体系', fontsize=24, y=0.98)
    save_plot('continuous_distribution_relations.svg')

def plot_hypothesis_testing():
    # Visualizing Rejection Region (Two-tailed)
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x)
    
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, color='black')
    
    # Fill rejection regions
    crit = 1.96
    plt.fill_between(x, y, where=(x >= crit), color='red', alpha=0.5, label='棄却域 (2.5%)')
    plt.fill_between(x, y, where=(x <= -crit), color='red', alpha=0.5)
    
    plt.title('両側検定の棄却域 (α=0.05)')
    plt.legend()
    save_plot('hypothesis_testing.png')

def plot_goodness_of_fit():
    # Observed vs Expected
    categories = ['A', 'B', 'C', 'D', 'E']
    expected = [20, 20, 20, 20, 20]
    observed = [22, 18, 25, 15, 20]
    
    x = np.arange(len(categories))
    width = 0.35
    
    plt.figure(figsize=(6, 4))
    plt.bar(x - width/2, observed, width, label='観測度数', color='skyblue')
    plt.bar(x + width/2, expected, width, label='期待度数', color='lightgray', alpha=0.7)
    
    plt.xticks(x, categories)
    plt.title('適合度検定 (観測 vs 期待)')
    plt.legend()
    save_plot('goodness_of_fit.png')

def plot_regression_3d():
    # Conceptual 3D plot
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(figsize=(8, 6)) # Increased figure size
    ax = fig.add_subplot(111, projection='3d')
    
    # Generate data
    np.random.seed(42)
    x1 = np.random.rand(20) * 10
    x2 = np.random.rand(20) * 10
    y = 2 * x1 + 3 * x2 + 5 + np.random.randn(20) * 2
    
    ax.scatter(x1, x2, y, c='blue', marker='o')
    
    # Plane
    X1, X2 = np.meshgrid(np.linspace(0, 10, 10), np.linspace(0, 10, 10))
    Y = 2 * X1 + 3 * X2 + 5
    ax.plot_surface(X1, X2, Y, alpha=0.3, color='orange')
    
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Y')
    plt.title('重回帰分析のイメージ')
    
    # Adjust margins to prevent cutoff
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1) # Full bleed? No, might cut labels.
    # Default is tight_layout in save_plot which might be aggressive for 3d.
    # Let's try explicit layout adjustment or view init
    ax.view_init(elev=20, azim=45)
    
    # Save manually with extra padding
    plt.savefig(os.path.join(OUTPUT_DIR, 'regression_3d.png'), dpi=150, bbox_inches='tight', pad_inches=0.5)
    plt.close()
    print("Saved regression_3d.png")

def plot_residual_plot():
    # Fitted vs Residuals
    np.random.seed(42)
    fitted = np.linspace(10, 50, 50)
    # Homoscedastic
    residuals = np.random.randn(50) * 2
    
    plt.figure(figsize=(6, 4))
    plt.scatter(fitted, residuals, color='blue', alpha=0.7)
    plt.axhline(0, color='black', linestyle='--')
    plt.xlabel('予測値 (Fitted Values)')
    plt.ylabel('残差 (Residuals)')
    plt.title('残差プロット (等分散の例)')
    save_plot('residual_plot.png')

def plot_regularization_path():
    # Schematic of Ridge/Lasso path
    lambdas = np.logspace(-2, 2, 100)
    # Fake coefficients
    beta1 = 1 / (1 + lambdas)          # Ridge-like
    beta2 = np.maximum(0, 1 - lambdas) # Lasso-like (hits zero)
    
    plt.figure(figsize=(6, 4))
    plt.plot(np.log10(lambdas), beta1, label='Ridge的 (漸近して0)', linestyle='--')
    plt.plot(np.log10(lambdas), beta2, label='Lasso的 (0になる)', linewidth=2)
    
    plt.xlabel('正則化パラメータ (log λ)')
    plt.ylabel('係数の大きさ')
    plt.title('正則化パス (イメージ)')
    plt.legend()
    save_plot('regularization_path.png')

def plot_time_series_example():
    t = np.arange(100)
    # Trend + Seasonality + Noise
    trend = 0.1 * t
    season = 2 * np.sin(2 * np.pi * t / 12)
    noise = np.random.randn(100)
    y = trend + season + noise
    
    plt.figure(figsize=(8, 4))
    plt.plot(t, y)
    plt.title('時系列データの例 (トレンド + 季節性)')
    plt.xlabel('時間')
    save_plot('time_series_example.png')

def plot_acf_pacf_schematic():
    # Schematic plots for AR(1) and MA(1) identification
    lags = np.arange(11)
    
    # AR(1) case: phi=0.7
    acf_ar = 0.7 ** lags
    pacf_ar = np.zeros(11); pacf_ar[0]=1; pacf_ar[1]=0.7
    
    # MA(1) case: theta=0.7
    # ACF(1) = theta/(1+theta^2) ... simplified schematic: Cutoff at 1
    acf_ma = np.zeros(11); acf_ma[0]=1; acf_ma[1]=0.5 # Schematic
    pacf_ma = 0.5 * (0.6 ** lags) # Decaying schematic
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    
    # AR(1) Row
    axes[0, 0].bar(lags, acf_ar, color='blue')
    axes[0, 0].set_title('AR(1)のACF (減衰)')
    axes[0, 1].bar(lags, pacf_ar, color='red')
    axes[0, 1].set_title('AR(1)のPACF (切断)')
    
    # MA(1) Row
    axes[1, 0].bar(lags, acf_ma, color='blue')
    axes[1, 0].set_title('MA(1)のACF (切断)')
    axes[1, 1].bar(lags, pacf_ma, color='red')
    axes[1, 1].set_title('MA(1)のPACF (減衰)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'acf_pacf_schematic.png'), dpi=150)
    plt.close()
    print("Saved acf_pacf_schematic.png")

def plot_rank_sum_schematic():
    # Visualization of Wilcoxon Rank Sum Test Process
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Data
    # Group A: [10, 30, 50] (Blue)
    # Group B: [20, 40] (Red)
    # Sorted: 10(A), 20(B), 30(A), 40(B), 50(A)
    # Ranks:   1,     2,     3,     4,     5
    
    # arrow properties
    arrow_props = dict(arrowstyle="->", color="gray", linewidth=2)
    
    # 1. Raw Data Display
    ax.text(0.1, 0.9, "1. データ観測 (Raw Data)", fontsize=16, fontweight='bold')
    
    # Group A Box
    ax.text(0.1, 0.8, "群 A", fontsize=14, color='#2980b9', fontweight='bold')
    ax.text(0.1, 0.75, "10, 30, 50", fontsize=14, bbox=dict(fc='#ecf0f1', ec='#2980b9'))
    
    # Group B Box
    ax.text(0.3, 0.8, "群 B", fontsize=14, color='#c0392b', fontweight='bold')
    ax.text(0.3, 0.75, "20, 40", fontsize=14, bbox=dict(fc='#ecf0f1', ec='#c0392b'))
    
    # Arrow down
    ax.annotate("", xy=(0.2, 0.65), xytext=(0.2, 0.72), arrowprops=arrow_props)
    
    # 2. Sorting & Pooling
    ax.text(0.1, 0.6, "2. 混合してソート (Sort)", fontsize=16, fontweight='bold')
    
    sorted_data = [
        (10, 'A', '#2980b9'),
        (20, 'B', '#c0392b'),
        (30, 'A', '#2980b9'),
        (40, 'B', '#c0392b'),
        (50, 'A', '#2980b9')
    ]
    
    import matplotlib.patches as mpatches
    start_x = 0.1
    gap = 0.15
    y_vals = 0.5
    
    for i, (val, group, col) in enumerate(sorted_data):
        # Draw value box
        rect = mpatches.FancyBboxPatch((start_x + i*gap, y_vals), 0.1, 0.08, 
                                     boxstyle="round,pad=0.02", fc='white', ec=col, linewidth=2)
        ax.add_patch(rect)
        ax.text(start_x + i*gap + 0.05, y_vals + 0.04, str(val), 
                ha='center', va='center', fontsize=14, color=col, fontweight='bold')
        
    # Arrow down
    ax.annotate("", xy=(0.2, 0.4), xytext=(0.2, 0.48), arrowprops=arrow_props)

    # 3. Ranking
    ax.text(0.1, 0.35, "3. 順位付け (Ranking)", fontsize=16, fontweight='bold')
    
    y_ranks = 0.25
    for i, (val, group, col) in enumerate(sorted_data):
        rank = i + 1
        # Draw rank circle
        circle = mpatches.Circle((start_x + i*gap + 0.05, y_ranks), 0.04, fc=col, alpha=0.2)
        ax.add_patch(circle)
        ax.text(start_x + i*gap + 0.05, y_ranks, str(rank), 
                ha='center', va='center', fontsize=16, fontweight='bold', color=col)
        
        # Connect value to rank
        ax.plot([start_x + i*gap + 0.05, start_x + i*gap + 0.05], [y_vals, y_ranks+0.05], 
                color='gray', linestyle=':', alpha=0.5)

    # Arrow to calculation
    ax.annotate("", xy=(0.8, 0.25), xytext=(0.8, 0.33), arrowprops=arrow_props)
    
    # 4. Calculation
    ax.text(0.6, 0.2, "4. 順位和の計算 (Calculate)", fontsize=16, fontweight='bold')
    
    # Sum A
    ax.text(0.6, 0.1, "群 A の順位和 $W_A$:", fontsize=14, color='#2980b9')
    ax.text(0.85, 0.1, "1 + 3 + 5 = 9", fontsize=16, fontweight='bold', color='#2980b9')
    
    # Sum B (Optional context)
    ax.text(0.6, 0.05, "(参考) 群 B:", fontsize=12, color='#c0392b')
    ax.text(0.85, 0.05, "2 + 4 = 6", fontsize=12, color='#c0392b')

    plt.title('ウィルコクソンの順位和検定の仕組み', fontsize=20)
    save_plot('rank_sum_test_schematic.png')

def plot_markov_chain_transition():
    import math
    import matplotlib.patches as mpatches
    
    # 3-State Markov Chain Diagram (Sunny, Cloudy, Rainy)
    # Use SVG for perfect text rendering
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # States positions (Triangle)
    states = {
        '晴\n(Sunny)': (0.5, 0.75),   # Moved down from 0.85 to avoid title overlap
        '曇\n(Cloudy)': (0.2, 0.3),   # Moved down slightly or kept similar
        '雨\n(Rainy)': (0.8, 0.3)
    }
    
    # Store patches for precise arrow start/end
    node_patches = {}
    radius = 0.08
    
    # Draw Nodes
    for label, (x, y) in states.items():
        # Use simple circle patch, but we need to pass it to annotation if we want patchA/patchB support
        # However, circle patch support in annotate is sometimes tricky with boundaries.
        # Let's use Drawing Area based patches or just shrinking.
        
        # Draw visible circle
        circle = mpatches.Circle((x, y), radius, fc='white', ec='black', linewidth=2, zorder=10)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=16, fontweight='bold', zorder=11)
        
        # Virtual patch for arrow calculation (slightly larger to stop arrow at edge)
        # Using simple coordinate calculation is often more robust for simple shapes than Patch logic in loose matplotlib versions
        pass
        
    # Draw Arrows (Transitions)
    transitions = [
        ('晴\n(Sunny)', '曇\n(Cloudy)', '0.3', 0.1),
        ('曇\n(Cloudy)', '晴\n(Sunny)', '0.4', 0.1),
        ('曇\n(Cloudy)', '雨\n(Rainy)', '0.4', 0.1),
        ('雨\n(Rainy)', '曇\n(Cloudy)', '0.5', 0.1),
        ('雨\n(Rainy)', '晴\n(Sunny)', '0.2', 0.1),
    ]
    
    # Self transitions: (State, Prob, LabelPosOffset)
    self_trans = [
        ('晴\n(Sunny)', '0.6', (0.0, 0.15), 1.5),   # Top
        ('曇\n(Cloudy)', '0.2', (-0.12, -0.1), 3.5), # Bottom-Left
        ('雨\n(Rainy)', '0.3', (0.12, -0.1), 5.5)   # Bottom-Right
    ]
    
    # Helper to get point on circle edge
    def get_edge_point(c_x, c_y, r, angle_rad):
        return c_x + r * math.cos(angle_rad), c_y + r * math.sin(angle_rad)

    for start, end, prob, rad in transitions:
        sx, sy = states[start]
        ex, ey = states[end]
        
        # Angle from start to end
        angle = math.atan2(ey-sy, ex-sx)
        
        # For arc3, rad determines curvature.
        # We manually calculate start/end points on the circle to look good
        # Perpendicular shift not needed if we rely on connectionstyle arc
        
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.8,head_length=1.5", 
                                    connectionstyle=f"arc3,rad={rad}", 
                                    color='#34495e', linewidth=2,
                                    shrinkA=30, shrinkB=30), zorder=1)
        
        # Label Manual Placement (Midpoint + Normal shift)
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        dx, dy = ex - sx, ey - sy
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Shift amount depends on rad and direction
        # Simple heuristic: move perpendicular to chord
        nx, ny = -dy, dx
        shift_mag = rad * dist * 0.6 # Tuning parameter
        
        lx = mx + (nx/dist) * shift_mag
        ly = my + (ny/dist) * shift_mag
        
        ax.text(lx, ly, prob, fontsize=14, color='blue', fontweight='bold', 
                bbox=dict(fc='white', ec='none', alpha=0.8, pad=0.1), ha='center', va='center', zorder=5)

    # Self loops using FancyArrowPatch or Annotate with loop
    for state, prob, (off_x, off_y), angle_base_rad in self_trans:
         cx, cy = states[state]
         
         # Explicitly set start/end angles and direction for each state
         if state.startswith('晴'): # Top: Curve Above
             theta_start = math.pi / 2 + 0.6  # Left side of top
             theta_end = math.pi / 2 - 0.6    # Right side of top
             rad_val = -2.0 # Curvature
             lx, ly = cx, cy + 0.2
         elif state.startswith('曇'): # Bottom Left: Curve Left-Down
             theta_start = math.pi * 1.25 + 0.6
             theta_end = math.pi * 1.25 - 0.6
             rad_val = -2.0
             lx, ly = cx - 0.15, cy - 0.1
         else: # Bottom Right: Curve Right-Down
             theta_start = math.pi * 1.75 + 0.6
             theta_end = math.pi * 1.75 - 0.6
             rad_val = -2.0
             lx, ly = cx + 0.15, cy - 0.1

         x1, y1 = get_edge_point(cx, cy, radius, theta_start)
         x2, y2 = get_edge_point(cx, cy, radius, theta_end)
         
         ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.8,head_length=1.5", 
                                    connectionstyle=f"arc3,rad={rad_val}", 
                                    color='#34495e', linewidth=2), zorder=1)
         
         ax.text(lx, ly, prob, fontsize=14, color='blue', fontweight='bold', ha='center', va='center')

    plt.title('マルコフ連鎖の状態遷移図 (例: 天気)', fontsize=24, y=0.98)
    # Save as SVG for safety
    save_plot('markov_chain_transition.svg')

def plot_markov_chain_convergence():
    # Convergence to Stationary Distribution
    steps = 20
    
    # Transition Matrix P
    # Sunny, Cloudy, Rainy
    P = np.array([
        [0.6, 0.3, 0.1],
        [0.4, 0.2, 0.4],
        [0.2, 0.5, 0.3]
    ])
    
    # Initial Distribution (Given it's sunny today)
    pi = np.array([1.0, 0.0, 0.0])
    
    history = np.zeros((steps, 3))
    history[0] = pi
    
    for i in range(1, steps):
        pi = np.dot(pi, P)
        history[i] = pi
        
    plt.figure(figsize=(10, 6))
    plt.plot(history[:, 0], label='晴 (Sunny)', marker='o')
    plt.plot(history[:, 1], label='曇 (Cloudy)', marker='s')
    plt.plot(history[:, 2], label='雨 (Rainy)', marker='^')
    
    plt.title('定常分布への収束 (初期状態: 晴)', fontsize=16)
    plt.xlabel('ステップ数 ($n$)', fontsize=12)
    plt.ylabel('状態確率 $\pi_n$', fontsize=12)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True, alpha=0.3)
    save_plot('markov_chain_convergence.png')

def plot_pca_illustration():
    # PCA: Maximize Variance
    np.random.seed(42)
    # Generate correlated data
    mean = [0, 0]
    cov = [[2, 1.5], [1.5, 2]]  # High correlation
    X = np.random.multivariate_normal(mean, cov, 200)
    
    # Calculate PCA manually for plotting arrows
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    pca.fit(X)
    
    # Components (direction vectors)
    v1 = pca.components_[0] * np.sqrt(pca.explained_variance_[0]) * 2
    v2 = pca.components_[1] * np.sqrt(pca.explained_variance_[1]) * 2
    
    plt.figure(figsize=(8, 8))
    plt.scatter(X[:, 0], X[:, 1], alpha=0.6, label='データ点')
    
    # Draw Mean
    plt.plot(pca.mean_[0], pca.mean_[1], 'kx')
    
    # Draw Vectors
    plt.arrow(pca.mean_[0], pca.mean_[1], v1[0], v1[1], color='#c0392b', width=0.05, head_width=0.2, label='第1主成分 (PC1)')
    plt.arrow(pca.mean_[0], pca.mean_[1], v2[0], v2[1], color='#2980b9', width=0.05, head_width=0.2, label='第2主成分 (PC2)')
    
    plt.axis('equal')
    plt.title('主成分分析による分散最大化方向の探索', fontsize=16)
    plt.xlabel('$x_1$', fontsize=12)
    plt.ylabel('$x_2$', fontsize=12)
    plt.grid(True, alpha=0.3)
    # Creating custom legend manually since arrow isn't automatically added nicely
    import matplotlib.patches as mpatches
    red_patch = mpatches.Patch(color='#c0392b', label='第1主成分 (分散最大)')
    blue_patch = mpatches.Patch(color='#2980b9', label='第2主成分 (直交方向)')
    plt.legend(handles=[red_patch, blue_patch])
    
    save_plot('pca_illustration.png')

def plot_clustering_example():
    # 2 Subplots: Dendrogram and K-Means
    fig = plt.figure(figsize=(16, 6))
    
    # 1. Dendrogram (Hierarchical)
    ax1 = fig.add_subplot(121)
    from scipy.cluster.hierarchy import dendrogram, linkage
    np.random.seed(42)
    X = np.random.rand(15, 2)
    Z = linkage(X, 'ward')
    dendrogram(Z, ax=ax1)
    ax1.set_title('階層的クラスタリング (デンドログラム)', fontsize=14)
    ax1.set_xlabel('サンプルインデックス')
    ax1.set_ylabel('距離')
    
    # 2. K-means (Non-hierarchical)
    ax2 = fig.add_subplot(122)
    # Generate 3 clusters
    mean1 = [2, 2]; cov1 = [[0.2, 0], [0, 0.2]]
    mean2 = [8, 3]; cov2 = [[0.5, 0], [0, 0.5]]
    mean3 = [5, 8]; cov3 = [[0.3, 0], [0, 0.3]]
    X1 = np.random.multivariate_normal(mean1, cov1, 50)
    X2 = np.random.multivariate_normal(mean2, cov2, 50)
    X3 = np.random.multivariate_normal(mean3, cov3, 50)
    
    ax2.scatter(X1[:, 0], X1[:, 1], c='#e74c3c', alpha=0.7, label='Cluster 1')
    ax2.scatter(X2[:, 0], X2[:, 1], c='#3498db', alpha=0.7, label='Cluster 2')
    ax2.scatter(X3[:, 0], X3[:, 1], c='#2ecc71', alpha=0.7, label='Cluster 3')
    
    # Centroids
    ax2.scatter([2, 8, 5], [2, 3, 8], c='black', s=200, marker='X', label='Centroids')
    
    ax2.set_title('非階層的クラスタリング (K-means法)', fontsize=14)
    ax2.set_xlabel('Variable 1')
    ax2.set_ylabel('Variable 2')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_plot('clustering_example.png')

def plot_continuity_correction():
    # Binomial(10, 0.5) vs Normal Approx
    n, p = 10, 0.5
    k = 3 # P(X <= 3)
    
    x = np.arange(0, n + 1)
    prob = stats.binom.pmf(x, n, p)
    
    mu = n * p
    sigma = np.sqrt(n * p * (1 - p))
    
    x_norm = np.linspace(-1, n + 1, 200)
    y_norm = stats.norm.pdf(x_norm, mu, sigma)
    
    plt.figure(figsize=(10, 6))
    
    # Bar plot for Binomial
    plt.bar(x, prob, width=1.0, edgecolor='black', alpha=0.3, label='二項分布 (離散)', color='skyblue')
    
    # Highlight P(X <= k) area in discrete
    plt.bar(x[:k+1], prob[:k+1], width=1.0, edgecolor='black', alpha=0.6, color='dodgerblue', label=f'P(X <= {k})')
    
    # Normal Curve
    plt.plot(x_norm, y_norm, 'r-', linewidth=2, label='正規近似 (連続)')
    
    # Highlight correction area
    x_fill = np.linspace(-1, k + 0.5, 100)
    y_fill = stats.norm.pdf(x_fill, mu, sigma)
    plt.fill_between(x_fill, y_fill, 0, color='red', alpha=0.2, label=f'補正あり積分範囲 (x <= {k}+0.5)')
    
    # Annotation for +0.5
    plt.axvline(x=k + 0.5, color='green', linestyle='--', linewidth=2)
    plt.text(k + 0.6, 0.05, '+0.5補正\n(3.5まで積分)', color='green', fontweight='bold', ha='left')

    plt.title(f'連続修正のイメージ: B({n}, {p}) を N({mu}, {sigma:.2f}) で近似', fontsize=16)
    plt.xlabel('x')
    plt.ylabel('確率密度 / 確率')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    save_plot('continuity_correction.png')

# Run all
if __name__ == "__main__":
    plot_bernoulli()
    plot_binomial()
    plot_poisson()
    plot_geometric()
    plot_nbinom()
    plot_continuous_uniform()
    plot_normal()
    plot_exponential()
    plot_gamma()
    plot_beta()
    plot_chi2()
    plot_t_dist()
    plot_f_dist()
    plot_distribution_relations()
    plot_continuous_relations()
    
    # Batch 2 Functions
    plot_hypothesis_testing()
    plot_goodness_of_fit()
    plot_regression_3d()
    plot_residual_plot()
    plot_regularization_path()
    plot_time_series_example()
    plot_acf_pacf_schematic()
    plot_rank_sum_schematic()
    
    # Batch 3 Functions
    plot_markov_chain_transition()
    plot_markov_chain_convergence()
    
    # Batch 4 Functions (Ch22, Ch24)
    plot_pca_illustration()
    plot_clustering_example()
    plot_continuity_correction()
    
    print("All images generated.")
