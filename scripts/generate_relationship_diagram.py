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

def draw_arrow(ax, start, end, label=""):
    # Calculate offset for arrow start/end to avoid overlap with box
    # Simple approximation: shorten arrow by 1.5 units
    
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # Adjust start and end points
    # This is rough; for strict boxes we'd intersect. 
    # But since boxes are uniform, we can just start/end at fixed distance from center
    # Box width 3.5 -> half is 1.75. Height 1.0 -> half is 0.5.
    
    # Determine direction
    if abs(dx) > abs(dy): # Horizontal
        offset_x = 1.8 if dx > 0 else -1.8
        offset_y = 0
    else: # Vertical
        offset_x = 0
        offset_y = 0.6 if dy > 0 else -0.6
        
    ax.annotate("", xy=(end[0]-offset_x, end[1]-offset_y), xytext=(start[0]+offset_x, start[1]+offset_y),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    
    # Label position
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2 + 0.2
    if label:
        ax.text(mid_x, mid_y, label, ha='center', va='bottom', fontsize=9, color='darkblue',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

plt.figure(figsize=(10, 8))
ax = plt.gca()
ax.set_xlim(-2, 12)
ax.set_ylim(-4, 4)
ax.axis('off')

# Nodes
bern = draw_box(ax, 0, 0, "ベルヌーイ分布\nBin(1, p)")
binom = draw_box(ax, 5, 0, "二項分布\nBin(n, p)")
poisson = draw_box(ax, 10, 0, "ポアソン分布\nPo(λ)")
hyper = draw_box(ax, 5, 3, "超幾何分布\nHG(N, M, n)")
geom = draw_box(ax, 0, -3, "幾何分布\nGeo(p)")
nbinom = draw_box(ax, 5, -3, "負の二項分布\nNB(r, p)")

# Edges
draw_arrow(ax, bern, binom, "n回試行 (独立和)")
draw_arrow(ax, binom, poisson, "n→∞, np→λ (少数の法則)")
draw_arrow(ax, hyper, binom, "N→∞ (非復元→復元)")
draw_arrow(ax, bern, geom, "初めて成功するまで")
draw_arrow(ax, geom, nbinom, "r回成功するまで (独立和)")
# draw_arrow(ax, binom, nbinom, "試行回数固定 vs 成功回数固定") # Optional, might clutter

plt.title("離散型確率分布の関係性", fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "distribution_relations.png"))
print("Generated relationship diagram.")
