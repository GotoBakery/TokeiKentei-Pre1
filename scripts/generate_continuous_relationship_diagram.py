import matplotlib.pyplot as plt
import matplotlib.patches as patches
import japanize_matplotlib
import os

output_dir = "/workspaces/TokeiKentei-Pre1/notes/images"
os.makedirs(output_dir, exist_ok=True)

def draw_box(ax, x, y, text, color='skyblue'):
    width = 3.5
    height = 1.0
    rect = patches.FancyBboxPatch((x - width/2, y - height/2), width, height,
                                  boxstyle="round,pad=0.1",
                                  linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=12, fontweight='bold')
    return (x, y)

def draw_arrow(ax, start, end, label="", curve=0):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # Adjust for box size (approximate)
    if abs(dx) > abs(dy):
        s_x = start[0] + (1.75 if dx > 0 else -1.75)
        s_y = start[1]
        e_x = end[0] - (1.75 if dx > 0 else -1.75)
        e_y = end[1]
    else:
        s_x = start[0]
        s_y = start[1] + (0.5 if dy > 0 else -0.5)
        e_x = end[0]
        e_y = end[1] - (0.5 if dy > 0 else -0.5)

    style = f"test" # Placeholder to check logic path
    # ax.annotate uses arrowprops={'arrowstyle': '->', 'connectionstyle': 'arc3,rad=0.2'} etc.
    
    arrow_args = dict(arrowstyle="->", color="black", lw=1.5)
    if curve != 0:
        arrow_args['connectionstyle'] = f"arc3,rad={curve}"

    ax.annotate("", xy=(e_x, e_y), xytext=(s_x, s_y),
                arrowprops=arrow_args)

    
    # Label placement (approximate middle)
    mid_x = (s_x + e_x) / 2
    mid_y = (s_y + e_y) / 2
    if curve != 0:
        mid_x += 0.5 # Shift label for curved arrows
    
    if label:
        ax.text(mid_x, mid_y + 0.2, label, ha='center', va='bottom', fontsize=9, color='darkblue',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

plt.figure(figsize=(10, 10))
ax = plt.gca()
ax.set_xlim(-2, 12)
ax.set_ylim(-6, 6)
ax.axis('off')

# Nodes
norm_std = draw_box(ax, 5, 4, "標準正規分布\nZ ~ N(0, 1)")
norm_gen = draw_box(ax, 0, 4, "一般正規分布\nN(μ, σ²)")
chi2 = draw_box(ax, 5, 0, "カイ二乗分布\nχ²(n)", color='#ffcc99')
t_dist = draw_box(ax, 10, 0, "t分布\nt(n)", color='#ccffcc')
f_dist = draw_box(ax, 5, -4, "F分布\n$F(n_1, n_2)$", color='#ffffcc')
gamma_box = draw_box(ax, 0, 0, "ガンマ分布\nGa(a, b)")
exp_box = draw_box(ax, 0, -2, "指数分布\nExp(λ)")

# Edges
draw_arrow(ax, norm_gen, norm_std, "標準化\n(X-μ)/σ")
draw_arrow(ax, norm_std, chi2, "二乗和 ΣZ²")
draw_arrow(ax, norm_std, t_dist, "", curve=0.3)
draw_arrow(ax, chi2, t_dist, "Z / √(Y/n)")
draw_arrow(ax, chi2, f_dist, "比 $(X/n_1)/(Y/n_2)$")
draw_arrow(ax, gamma_box, chi2, "a=n/2, b=2")
draw_arrow(ax, gamma_box, exp_box, "a=1")
draw_arrow(ax, t_dist, f_dist, "T² ~ F(1, n)", curve=-0.3)
draw_arrow(ax, t_dist, norm_std, "n→∞", curve=-0.3)


plt.title("連続型確率分布と標本分布の関係性", fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "continuous_distribution_relations.png"))
print("Generated continuous relationship diagram.")
