"""
====================================
scatterstats customization
====================================

In this example, we'll how to customize the appearance of the scatterstats plot using keyword arguments.

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import inferplot

x = np.random.normal(loc=5, scale=10, size=200)
y = x + np.random.normal(loc=0, scale=5, size=200)
data = pd.DataFrame({"x": x, "y": y})

inferplot.scatterstats("x", "y", data)
plt.show()
