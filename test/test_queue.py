import numpy as np
import sys
sys.path.append("/home/nick/Queue/src")
from queue import production

times = np.random.exponential(30, size=1000).astype(int).tolist()
stations = 5

line = production(times, stations)
print(f"Total Time: {line.total_time}")
