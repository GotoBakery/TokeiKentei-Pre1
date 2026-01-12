import matplotlib.pyplot as plt
import matplotlib.patches as patches
import japanize_matplotlib
import os

output_dir = "/workspaces/TokeiKentei-Pre1/notes/images"
os.makedirs(output_dir, exist_ok=True)

def draw_box(ax, x, y, text, color='skyblue', width=3.5, height=1.2):
    rect = patches.FancyBboxPatch((x - width/2, y - height/2), width, height,
                                  boxstyle="round,pad=0.1",
                                  linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold')
    return (x, y)

def draw_arrow(ax, start, end, label="", color='black', style='->', linestyle='-'):
    # Simple straight arrow
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle=style, color=color, lw=1.5, shrinkB=5, linestyle=linestyle))

    
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y, label, ha='center', va='bottom', fontsize=9, 
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.9))

plt.figure(figsize=(8, 6))
ax = plt.gca()
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 9)
ax.axis('off')

# Nodes
# Nodes
# Layout: Y-shape
# Top Left: AS, Top Right: Mean
# Middle: Prob
# Bottom: Dist

as_conv = draw_box(ax, 2.5, 8, "概収束\n(Almost Sure)\n$P(\\lim X_n = X) = 1$", color='#ffcccc')
mean_conv = draw_box(ax, 7.5, 8, "平均収束\n(Mean Square)\n$E[|X_n - X|^2] \\to 0$", color='#ccffcc')
prob_conv = draw_box(ax, 5, 5, "確率収束\n(In Probability)\n$X_n \\to^P X$", color='#ccccff')
dist_conv = draw_box(ax, 5, 2, "分布収束\n(In Distribution)\n$X_n \\to^d X$", color='#ffffcc')


# Edges (Implications)
# AS -> Prob (Diagonal down-right)
draw_arrow(ax, (2.5, 7.4), (4.0, 5.6), label="ならば")

# Mean -> Prob (Diagonal down-left)
draw_arrow(ax, (7.5, 7.4), (6.0, 5.6), label="ならば")

# Prob -> Dist (Vertical down)
draw_arrow(ax, (5.0, 4.4), (5.0, 2.6), label="ならば")

# Partial converse (Prob -> Dist -> Constant)
# Only if target is constant c
draw_arrow(ax, (6.0, 2.6), (6.0, 4.4), label="定数への収束なら\n逆も成立", style='->', color='gray', linestyle='--')




plt.title("確率変数の収束概念の関係性", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "convergence_relations.png"))
print("Generated convergence diagram.")
