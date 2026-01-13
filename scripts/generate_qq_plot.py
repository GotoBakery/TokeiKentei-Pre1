
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

# Ensure directory exists
output_dir = "/workspaces/TokeiKentei-Pre1/notes/assets/images"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "qq_plot.png")

# Generate synthetic data (ideally normal)
np.random.seed(42)
data = np.random.normal(loc=0, scale=1, size=100)

# Create Q-Q plot
plt.figure(figsize=(6, 6))
stats.probplot(data, dist="norm", plot=plt)
plt.title("Normal Q-Q Plot")
plt.xlabel("Theoretical Quantiles")
plt.ylabel("Sample Quantiles")
plt.grid(True, linestyle='--', alpha=0.6)

# Save the plot
plt.savefig(output_path, bbox_inches='tight', dpi=100)
plt.close()

print(f"Generated Q-Q plot at: {output_path}")
