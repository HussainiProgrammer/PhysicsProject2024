from types import ModuleType
import sympy
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.axes
from mpl_toolkits import mplot3d
import vector3D

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
plt.rcParams["mathtext.default"] = "regular"

hsv_map = plt.get_cmap("hsv")

class Vector2D:
    def __init__(self, *args, c="c", unit=""): # c is the coorinates system and "c" means the cartesian coordinate system and anything else would mean the polar coordinate system
        if c == "c":
            x, y = args

            self.x = sympy.sympify(x)
            self.y = sympy.sympify(y)

            self.magnitude = sympy.sympify(sympy.sqrt(sympy.Pow(self.x, 2) + sympy.Pow(self.y, 2)))

            self.theta_radians = sympy.atan2(self.y, self.x)
            self.theta_degrees = sympy.deg(self.theta_radians)

            self.displayedValues = ["X Component", "Y Component"]

        else:
            magnitude, theta = args

            self.magnitude = sympy.sympify(magnitude)

            if "r" in c:
                self.theta_radians = sympy.sympify(theta)
                self.theta_degrees = sympy.deg(self.theta_radians)

                self.displayedValues = ["Magnitude", "Radians"]

            else:
                self.theta_degrees = sympy.sympify(theta)
                self.theta_radians = sympy.rad(self.theta_degrees)

                self.displayedValues = ["Magnitude", "Degrees"]

            self.x = self.magnitude*sympy.cos(self.theta_radians)
            self.y = self.magnitude*sympy.sin(self.theta_radians)

        self.unit = unit

    def cartesian_coordinates(self) -> str:
        if self.magnitude == 0: return "\\overrightarrow{0}"
        return f"\\left({sympy.latex(self.x)} {self.getUnit()}, {sympy.latex(self.y)} {self.getUnit()}\\right)"
    
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
                    else: axes.append(sympy.latex(self.y) + " " + self.getUnit() + " \\hat{j}")

            else:
                if len(axes) > 0:
                    if self.y == 1: axes.append("+\\hat{j}")
                    elif self.y == -1: axes.append("-\\hat{j}")
                    else:
                        if self.y < 0: axes.append(sympy.latex(self.y) + " \\hat{j}")
                        else: axes.append("+" + sympy.latex(self.y) + " \\hat{j}")

                else:
                    if self.y == 1: axes.append("\\hat{j}")
                    elif self.y == -1: axes.append("-\\hat{j}")
                    else: axes.append(sympy.latex(self.y) + " \\hat{j}")

        return "\\left(" + "".join(axes) + "\\right)"

    def polar_coordinates(self, measure="Degrees") -> str:
        if self.magnitude == 0: return "\\overrightarrow{0}"
        if measure == "Degrees": return f"\\left({sympy.latex(self.magnitude)} {self.unit}, {sympy.latex(self.theta_degrees)}\\degree\\right)"
        else: return f"\\left({sympy.latex(self.magnitude)} {self.unit}, {sympy.latex(self.theta_radians)} rad \\right)"

    def getLabel(self): return self.unit_vectors()
    
    def getUnit(self): return re.sub("(.+)/(.+)", "\\\\frac{\\1}{\\2}", self.unit)

    def graph(self, i=None):
        if i: plt.figure(i)

        if self.magnitude == 0: plt.plot(0,0, marker=".", markersize=20, linestyle="None", color="blue", label="$" + self.getLabel() + "$")
        else: plt.arrow(0, 0, float(sympy.N(self.x)), float(sympy.N(self.y)), width=0.006*self.magnitude, head_width=0.06*self.magnitude, head_length=0.06*self.magnitude, fc="blue", ec="blue", label="$ " + self.getLabel() + " $")
        
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")

        plt.grid()
        plt.axis("equal")
        plt.legend(fontsize=18)
        plt.show()

    def draw_on_graph(self, origin: tuple=(0,0), p: ModuleType|matplotlib.axes._axes.Axes=plt):
        if self.magnitude == 0:
            circle = plt.Circle(origin, 0.055, label="$ " + self.getLabel() + " $")
            p.add_patch(circle)
            return circle
        
        return p.arrow(origin[0], origin[1], float(sympy.N(self.x)), float(sympy.N(self.y)), width=0.006*self.magnitude, head_width=0.06*self.magnitude, head_length=0.06*self.magnitude, label="$ " + self.getLabel() + " $")

    def __neg__(self) -> "Vector2D": return -1*self

    def __pos__(self) -> "Vector2D": return self

    def __add__(self, addend: "Vector2D") -> "Vector2D": return Vector2D(self.x + addend.x, self.y + addend.y)

    def __sub__(self, subtrahend: "Vector2D") -> "Vector2D": return Vector2D(self.x - subtrahend.x, self.y - subtrahend.y)

    def __mul__(self, multiplier: int|float|sympy.Basic) -> "Vector2D": return Vector2D(multiplier*self.x, multiplier*self.y)

    def __rmul__(self, multiplicand: int|float|sympy.Basic) -> "Vector2D": return Vector2D(multiplicand*self.x, multiplicand*self.y)

    def __truediv__(self, divisor) -> "Vector2D": return Vector2D(self.x/divisor, self.y/divisor)

    def scalar_product(self, multiplier: "Vector2D"): return self.x*multiplier.x + self.y*multiplier.y

    def vector_product(self, multiplier: "Vector2D") -> vector3D.Vector3D: return vector3D.Vector3D(0, 0, self.x*multiplier.y - multiplier.x*self.y)

    def __eq__(self, other: "Vector2D") -> bool: return self.x == other.x and self.y == other.y # and self.unit == other.unit

    def __str__(self): return f"({self.x}{self.unit}, {self.y}{self.unit})"

    def toVector3D(self) -> vector3D.Vector3D:
        vector = vector3D.Vector3D(self.x, self.y, 0, unit=self.unit)
        vector.getLabel = self.getLabel

        return vector

i = Vector2D(1,0)
j = Vector2D(0,1)

zero_vector = Vector2D(0,0)

def Vector2D_sum(vectors: list[Vector2D]):
    originX = 0
    originY = 0

    figure = plt.figure()
    ax = figure.add_subplot(111)

    colors = hsv_map(np.linspace(0, 0.8, len(vectors)+1))
    # np.random.shuffle(colors)

    finalVector = zero_vector

    arrows = []

    for i, vector in enumerate(vectors):
        arrow = vector.draw_on_graph(origin=(originX, originY), p=ax)
        arrow.set_color(colors[i])
        arrow.set_alpha(0.5)

        originX += vector.x
        originY += vector.y

        finalVector += vector
        arrows.append(arrow)

    finalArrow = finalVector.draw_on_graph(p=ax)
    finalArrow.set_color(colors[len(vectors)])
    finalArrow.set_alpha(0.8)

    return finalVector, figure, ax, arrows, finalArrow

def VectorProduct(a: Vector2D, b: Vector2D):
    figure = plt.figure()
    ax: mplot3d.axes3d.Axes3D = figure.add_subplot(111, projection="3d")

    r = a.vector_product(b)

    a_quiver = a.toVector3D().draw_on_graph(axes=ax, color="red")
    b_quiver = b.toVector3D().draw_on_graph(axes=ax, color="blue")
    r_quiver = r.draw_on_graph(axes=ax, color="green")

    return figure, ax, r, a_quiver, b_quiver, r_quiver

def input_to_Vector2D(text: str) -> Vector2D:
    if text == "0": return zero_vector

    if "i" in text or "j" in text:
        xExpr = "([^j]*)i"
        yExpr = "([^i]*)j"

        i_coefficient = re.findall(xExpr, text)
        j_coefficient = re.findall(yExpr, text)

        if i_coefficient: x = sympy.sympify(i_coefficient[0])
        else: x = 0

        if j_coefficient: y = sympy.sympify(j_coefficient[0])
        else: y = 0

        return Vector2D(x, y)
    
    if "deg" in text:
        match = re.match(r"\((.*),(.*)deg\)", text)
        v = Vector2D(*match.groups(), c="pd")
        v.getLabel = lambda v=v: v.polar_coordinates(measure="Degrees")
        return v

    elif "rad" in text:
        match = re.match(r"\((.*),(.*)rad\)", text)
        v = Vector2D(*match.groups(), c="pr")
        v.getLabel = lambda v=v: v.polar_coordinates(measure="Radians")
        return v

    else:
        match = re.match(r"\((.*),(.*)\)", text)
        return Vector2D(*match.groups())

if __name__ == "__main__":
    t = "$ \\vec{\\tau}\\pi 𝜏$"

    figure = plt.figure()
    ax = figure.add_subplot(111)

    zero_vector.draw_on_graph(p=ax).set_color("red")
    input_to_Vector2D("(1, 2*pi-pi/4 rad)").draw_on_graph(p=ax).set_color("blue")
    input_to_Vector2D("(-1, 1)").draw_on_graph(p=ax).set_color("green")


    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")

    plt.legend()
    plt.axis("equal")
    plt.show()

    vector3D.zero_vector.graph()