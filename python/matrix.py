import numpy as np

import math

A = np.array([0, -8])
B = np.array([math.cos(60 / 180 * math.pi) * 15, math.sin(60 / 180 * math.pi) * 15])


C = B - A

print(C)

print(np.linalg.norm(C))

# tan theta is Cy / Cx, so 
# theta is atan(Cy / Cx)
angle = math.atan(C[1] / C[0]) / math.pi * 180 
print(angle)