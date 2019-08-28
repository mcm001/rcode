import numpy as np
import math

def vectorFrom(magnitude: float, direction: float):
    x = math.cos(direction / 180 * math.pi) * magnitude
    y = math.sin(direction / 180 * math.pi) * magnitude
    
    return np.array([x, y])

def vectorOf(coordinates: list):
    return np.array(coordinates)

def columnVectorOf(coordinates: list):
    array = []
    for coordinate in coordinates:
        array += [[coordinate]]
    
    return np.array(array)

# v1 = np.array([[9],[1],[-5]])

v1 = columnVectorOf([9, 1, -5])
v2 = columnVectorOf([-7, 2, 0])

a = 3
b = 2.5

print(a * v1 + b * v2 )



# print(np.linalg.norm(C))

# # tan theta is Cy / Cx, so 
# # theta is atan(Cy / Cx)
# angle = math.atan(C[1] / C[0]) / math.pi * 180 
# print(angle)
