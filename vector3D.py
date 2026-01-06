from types import ModuleType
import sympy
import numpy as np
import re
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
plt.rcParams["mathtext.default"] = "regular"

hsv_map = plt.get_cmap("hsv")

class Vector3D:
    def __init__(self, *args, unit=""): # c is the coorinates system and "c" means the cartesian coordinate system and anything else would mean the polar coordinate system (the spherical coordinate system is not implemented)
        self.x = sympy.sympify(args[0])
        self.y = sympy.sympify(args[1])
        self.z = sympy.sympify(args[2])

        self.magnitude = sympy.sympify(sympy.sqrt(sympy.Pow(self.x, 2) + sympy.Pow(self.y, 2) + sympy.Pow(self.z, 2)))

        self.unit = unit

    def cartesian_coordinates(self) -> str:
        if self.magnitude == 0: return "\\overrightarrow{0}"
        return f"\\left({sympy.latex(self.x)} {self.getUnit()} , {sympy.latex(self.y)} {self.getUnit()} \\right)" if self.z == 0 else f"\\left({sympy.latex(self.x)} {self.getUnit()} , {sympy.latex(self.y)} {self.getUnit()} , {sympy.latex(self.z)} {self.getUnit()} \\right)"
    
    def unit_vectors(self) -> str:
        if self.magnitude == 0: return "\\overrightarrow{0}"

        axes = []

        if self.x != 0:
            if self.unit:
                if self.x == 1: axes.append("1 " + self.getUnit() + " \\hat{i}")
                elif self.x == -1: axes.append("-1 " + self.getUnit() + " \\hat{i}")
                else: axes.append(sympy.latex(self.x) + " " + self.getUnit() + " \\hat{i}")

            else:
                if self.x == 1: axes.append("\\hat{i}")
                elif self.x == -1: axes.append("-\\hat{i}")
                else: axes.append(sympy.latex(self.x) + "\\hat{i}")
                
        if self.y != 0:
            if self.unit:
                if len(axes) > 0:
                    if self.y == 1: axes.append("+1 " + self.getUnit() + " \\hat{j}")
                    elif self.y == -1: axes.append("-1 " + self.getUnit() + " \\hat{j}")
                    else:
                        if self.y < 0: axes.append(sympy.latex(self.y) + " " + self.getUnit() + " \\hat{j}")
                        else: axes.append("+" + sympy.latex(self.y) + " " + self.getUnit() + " \\hat{j}")

                else:
                    if self.y == 1: axes.append("1 " + self.getUnit() + " \\hat{j}")
                    elif self.y == -1: axes.append("-1 " + self.getUnit() + " \\hat{j}")
                    else: axes.append(sympy.latex(self.y) + " " + self.getUnit() + " \\hat")

            else:
                if len(axes) > 0:
                    if self.y == 1: axes.append("+\\hat{j}")
                    elif self.y == -1: axes.append("-\\hat{j}")
                    else:
                        if self.y < 0: axes.append(sympy.latex(self.y) + "\\hat{j}")
                        else: axes.append("+" + sympy.latex(self.y) + "\\hat{j}")

                else:
                    if self.y == 1: axes.append("\\hat{j}")
                    elif self.y == -1: axes.append("-\\hat{j}")
                    else: axes.append(sympy.latex(self.y) + "\\hat")

        if self.z != 0:
            if self.unit:
                if len(axes) > 0:
                    if self.z == 1: axes.append("+1 " + self.getUnit() + " \\hat{k}")
                    elif self.z == -1: axes.append("-1 " + self.getUnit() + " \\hat{k}")
                    else:
                        if self.z < 0: axes.append(sympy.latex(self.z) + " " + self.getUnit() + " \\hat{k}")
                        else: axes.append("+" + sympy.latex(self.z) + " " + self.getUnit() + " \\hat{k}")

                else:
                    if self.z == 1: axes.append("1 " + self.getUnit() + " \\hat{k}")
                    elif self.z == -1: axes.append("-1 " + self.getUnit() + " \\hat{k}")
                    else: axes.append(sympy.latex(self.z) + " " + self.getUnit() + " \\hat{k}")

            else:
                if len(axes) > 0:
                    if self.z == 1: axes.append("+\\hat{k}")
                    elif self.z == -1: axes.append("-\\hat{k}")
                    else:
                        if self.z < 0: axes.append(sympy.latex(self.z) + "\\hat{k}")
                        else: axes.append("+" + sympy.latex(self.z) + "\\hat{k}")

                else:
                    if self.z == 1: axes.append("\\hat{k}")
                    elif self.z == -1: axes.append("-\\hat{k}")
                    else: axes.append(sympy.latex(self.z) + "\\hat{k}")

        return "\\left( " + "".join(axes) + " \\right)"

    def getLabel(self): return self.unit_vectors()
    
    def getUnit(self): return re.sub("(.+)/(.+)", "\\\\frac{\\1}{\\2}", self.unit)

    def graph(self):
        ax: mplot3d.axes3d.Axes3D = plt.axes(projection="3d")

        if self.magnitude == 0: ax.plot((0), (0), (0), color="blue", label="$ " + self.getLabel() + " $", linestyle="None", marker=".", markersize=5)

        else:
            ax.plot((0, float(sympy.N(self.x))), (0, float(sympy.N(self.y))), (0, float(sympy.N(self.z))), linestyle="None")
            ax.quiver((0), (0), (0), (self.x), (self.y), (self.z), arrow_length_ratio=0.1, label="$ " + self.getLabel() + " $")

        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Z Axis")

        plt.axis("equal")
        plt.legend(fontsize=18)
        plt.show()

    def draw_on_graph(self, axes: mplot3d.axes3d.Axes3D|ModuleType, origin=(0,0,0), color="blue"):
        if self.magnitude == 0: return axes.plot(origin[0], origin[1], origin[2], color=color, label="$ " + self.getLabel() + " $", linestyle="None", marker=".", markersize=5)

        else:
            axes.plot((origin[0], origin[0] + float(sympy.N(self.x))), (origin[1], origin[1] + float(sympy.N(self.y))), (origin[2], origin[2] + float(sympy.N(self.z))), linestyle="None")
            return axes.quiver((origin[0]), (origin[1]), (origin[2]), (float(sympy.N(self.x))), (float(sympy.N(self.y))), (float(sympy.N(self.z))), color=color, arrow_length_ratio=0.1, label="$ " + self.getLabel() + " $")

    def __neg__(self) -> "Vector3D": return -1*self

    def __pos__(self) -> "Vector3D": return self

    def __add__(self, addend: "Vector3D") -> "Vector3D": return Vector3D(self.x + addend.x, self.y + addend.y, self.z + addend.z)

    def __sub__(self, subtrahend: "Vector3D") -> "Vector3D": return Vector3D(self.x - subtrahend.x, self.y - subtrahend.y, self.z - subtrahend.z)

    def __mul___(self, multiplier) -> "Vector3D": return Vector3D(multiplier*self.x, multiplier*self.y, multiplier*self.z)

    def __rmul__(self, multiplicand) -> "Vector3D": return Vector3D(multiplicand*self.x, multiplicand*self.y, multiplicand*self.z)

    def __truediv__(self, divisor) -> "Vector3D": return Vector3D(self.x/divisor, self.y/divisor, self.z/divisor)

    def scalar_product(self, multiplier: "Vector3D"): return self.x*multiplier.x + self.y*multiplier.y + self.z*multiplier.z

    def vector_product(self, multiplier: "Vector3D") -> "Vector3D": return Vector3D(self.y*multiplier.z - multiplier.y*self.z, self.z*multiplier.x - multiplier.z*self.x, self.x*multiplier.y - multiplier.x*self.y)

    def __eq__(self, other: "Vector3D") -> bool: return self.x == other.x and self.y == other.y and self.z == other.z # and self.unit == other.unit

    def __str__(self) -> str: return f"({self.x}{self.unit}, {self.y}{self.unit}, {self.z}{self.unit})"

i = Vector3D(1,0,0)
j = Vector3D(0,1,0)
k = Vector3D(0,0,1)

zero_vector = Vector3D(0,0,0)

def Vector3D_sum(vectors: list[Vector3D]):
    originX = 0
    originY = 0
    originZ = 0

    figure = plt.figure()
    ax = figure.add_subplot(111, projection="3d")

    colors = hsv_map(np.linspace(0, 0.8, len(vectors)+1))
    # np.random.shuffle(colors)

    finalVector = zero_vector

    quivers = []

    for i, vector in enumerate(vectors):
        quiver = vector.draw_on_graph(ax, (originX, originY, originZ))
        quiver.set_color(colors[i])
        quiver.set_alpha(0.6)

        originX += vector.x
        originY += vector.y
        originZ += vector.z

        finalVector += vector
        quivers.append(quiver)

    finalQuiver = finalVector.draw_on_graph(ax)
    finalQuiver.set_color(colors[len(vectors)])
    finalQuiver.set_alpha(0.6)

    return finalVector, figure, ax, finalQuiver, quivers

def input_to_Vector3D(text: str) -> Vector3D: return Vector3D(*re.match("((.*),(.*),(.*))", text).groups())

if __name__ == "__main__":
    figure = plt.figure()
    ax = figure.add_subplot(111, projection="3d")

    a = (i+j+k)
    b = (i-j+k)

    a.draw_on_graph(ax, color="red")
    b.draw_on_graph(ax, color="blue")

    a.vector_product(b).draw_on_graph(ax, color="green")

    plt.axis("equal")
    plt.legend(fontsize=16)
    plt.show()

    figure = plt.figure()
    ax = figure.add_subplot(111, projection="3d")

    a = 2*i
    b = j
    
    a.draw_on_graph(ax, color="red")
    b.draw_on_graph(ax, color="blue")

    a.vector_product(b).draw_on_graph(ax, color="green")

    plt.axis("equal")
    plt.legend(fontsize=16)
    plt.show()
    
    # A = i+k
    # B = j+k
    # C = A.vector_product(B)

    # A.label = "$\\overrightarrow{A} = " + A.cartesian_coordinates() + "$"
    # B.label = "$\\overrightarrow{B} = " + B.cartesian_coordinates() + "$"
    # C.label = "$\\overrightarrow{C} = \\overrightarrow{A} \\times \\overrightarrow{B} = " + C.cartesian_coordinates() + "$"

    # ax: mplot3d.axes3d.Axes3D = plt.axes(projection="3d")

    # A_quiver = A.draw_on_graph(ax)
    # B_quiver = B.draw_on_graph(ax)
    # C_quiver = C.draw_on_graph(ax)

    # A_quiver.set_color("red")
    # B_quiver.set_color("yellow")
    # C_quiver.set_color("green")

    # ax.plot(0,0,0, linestyle="None", color="purple", marker=".", markersize=10, label="Origin (0,0,0)")

    # ax.set_xlabel("X Axis")
    # ax.set_ylabel("Y Axis")
    # ax.set_zlabel("Z Axis")

    # plt.axis("equal")
    # plt.legend(fontsize=12)
    # plt.show()

    # Vector3D_sum([i,j,k, 2*i, 2*j, 2*k, 0.5*(i+j), 0.5*k])
    # Vector3D_sum([A,B,C])

    # ax.set_xlabel("X Axis")
    # ax.set_ylabel("Y Axis")
    # ax.set_zlabel("Z Axis")
    
    # plt.axis("equal")
    # plt.legend(fontsize=12)
    # plt.show()
