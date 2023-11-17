import numpy as np
a = np.array([1, 2, 3])
y = np.delete(a, [0, 1], axis=1)
print(y)