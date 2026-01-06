import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
plt.rcParams["mathtext.default"] = "regular"
plt.rcParams["mathtext.fontset"] = "stix"

figure = plt.figure()
ax: mplot3d.axes3d.Axes3D= figure.add_subplot(111, projection="3d")

t = np.linspace(0, 25, 100)
x = -0.31*t**2 + 7.2*t + 28
y = 0.22*t**2 - 9.1*t + 30

ax.plot3D(x,y,t)

ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Time")
ax.axis("equal")

ax.view_init(90, -90)

plt.show()