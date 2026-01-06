import sympy
import re
import vector2D

quantities_baseUnits = {
    "Position Vector": ["m"], # Chapter 2
    "Position Magnitude": ["m"],
    "Position Direction": ["Degrees", "Radians"],
    "Position X Component": ["m"],
    "Position Y Component": ["m"],
    "Displacement Vector": ["m"],
    "Displacement Magnitude": ["m"],
    "Displacement Direction": ["Degrees", "Radians"],
    "Displacement X Component": ["m"],
    "Displacement Y Component": ["m"],
    "Distance": ["m"],
    "Time": ["s", "min", "h"],
    "Velocity Vector": ["m/s", "km/h", "m/min"],
    "Velocity Magnitude": ["m/s", "km/h", "m/min"],
    "Velocity Direction": ["Degrees", "Radians"],
    "Velocity X Component": ["m/s", "km/h", "m/min"],
    "Velocity Y Component": ["m/s", "km/h", "m/min"],
    "Speed": ["m/s", "km/h", "m/min"],
    "Acceleration Vector": ["m/s²"],
    "Acceleration Magnitude": ["m/s²"],
    "Acceleration Direction": ["Degrees", "Radians"],
    "Acceleration X Component": ["m/s²"],
    "Acceleration Y Component": ["m/s²"],
    "Horizontal Range": ["m"],
    # "Force Vector": ["N"], # Chapter 3
    # "Force Magnitude": ["N"],
    # "Force Direction": ["Degrees", "Radians"],
    # "Force X Component": ["N"],
    # "Force Y Component": ["N"],
    # "Mass": ["g"],
    # "Weight": ["N"],
    # "Normal Force": ["N"],
    # "Static Friction Coefficient": [""],
    # "Torque": ["N⋅m"], # Chapter 4
    # "Work": ["J"],
    # "Power": ["W"],
    # "Kinetic Energy": ["J"],
    # "Potential Energy": ["J"],
    # "Gravitational Potential Energy": ["J"],
    # "Elastic Potential Energy": ["J"],
    # "Mechanical Energy": ["J"],
    # "Linear Momentum": ["kg⋅m/s"],
    # "Impulse": ["kg⋅m/s"],
    # "Internal Energy": ["J"], # Chapter 5
    # "Heat Energy": ["J"],
    # "Pressure": ["N/m²"],
    # "Length": ["m"],
    # "Area": ["m²"],
    # "Volume": ["m³", "L"],
    # "Engine Efficiency": [""],
    # "Supplied Energy": ["J"],
    # "Anglular Displacement": ["Degrees", "Radians"], # Chapter 6
    # "Radius": ["m"],
    # "Angular Velocity": ["Degrees/s", "Radians/s"],
    # "Angular Acceleration": ["Degrees/s²", "Radians/s²"],
    # "Rotational Inertia": ["kg⋅m²"],
    # "Angular Momentum": ["kg⋅m²/s"],
    # "Frequency": ["1/s"],
    # "Period": ["s"],
    # "Spring Constant": ["N/m"],
    # "Number of Vibrations": [""],
    # "Wave Amplitude": ["m"],
    # "Linear Mass Density": ["kg/m"],
    # "Wave Length": ["m"],
    # "Density": ["g/m³", "g/L"],
    # "Young's Modulus": ["N/m²"],
    # "Liquid Elastic Coefficient": ["N/m²"],
    # "Number of Antinodes": [""],
    # "Sound Intensity": ["W/m²"],
    # "Sound Intensity Level": ["dB"],
    # "Electric Current": ["A"],
    # "Charge": ["C"],
    # "Number of Electrons": ["e"],
    # "Number of Electrons Per Unit Volume": ["e/m³", "e/L"],
    # "Resistance": ["Ω"],
    # "Voltage": ["V"],
    # "Resistivity": ["Ω⋅m"],
    # "Conductivity": ["1/Ω⋅m"],
    # "Temperature Coefficient of Resistivity": ["1/°C"],
    # "Electromotive Force": ["V"],
    # "Internal Resistance": ["Ω"],
    # "Electric Power": ["W"],
    # Chapter 10:
    # "Magnetic Flux": ["Wb", "Mx", "T⋅m²"],
    # "Magnetic Flux Density": ["T", "Wb/m²", "Mx/m²"],
    # "Number of Turns": [""],
    # "Number of Turns Per Unit Length": ["1/m"],
}

quantitiy_symbol = {
    "Position Vector": "\\vec{x}",
    "Position Magnitude": "x",
    "Position Direction": "\\theta",
    "Position X Component": "x_{x}",
    "Position Y Component": "x_{y}",
    "Displacement Vector": "\\vec{\\Delta x}",
    "Displacement Magnitude": "\\Delta x",
    "Displacement Direction": "\\theta",
    "Displacement X Component": "\\Delta x_{x}",
    "Displacement Y Component": "\\Delta x_{y}",
    "Distance": "d",
    "Time": "t",
    "Velocity Vector": "\\vec{v}",
    "Velocity Magnitude": "v",
    "Velocity Direction": "\\theta",
    "Velocity X Component": "v_{x}",
    "Velocity Y Component": "v_{y}",
    "Speed": "v_{s}",
    "Acceleration Vector": "\\vec{a}",
    "Acceleration Magnitude": "a",
    "Acceleration Direction": "\\theta",
    "Acceleration X Component": "a_{x}",
    "Acceleration Y Component": "a_{y}",
    "Horizontal Range": "R",
    # To Be Continued...
}

prefixes_exponents = {
    "":    0,
    "k":   3,
    "d":  -1,
    "c":  -2,
    "m":  -3,
    "µ":  -6,
    "n":  -9,
    # "p": -12,
    # "f": -15,
    # "a": -18,
    # "z": -21,
    # "y": -24,
    # "da":  1,
    # "h":   2,
    # "M":   6,
    # "G":   9,
    # "T":  12,
    # "P":  15,
    # "E":  18,
    # "Z":  21,
    # "Y":  24,
}

base_unit_conversion = {
    "Degrees-Radians": lambda x: sympy.rad(x),
    "Radians-Degrees": lambda x: sympy.deg(x),
    "Degrees-Revolutions": lambda x: x/360,
    "Revolutions-Degrees": lambda x: x*360,
    "Revolutions-Radians": lambda x: x*2*sympy.pi,
    "Radians-Revolutions": lambda x: x/(2*sympy.pi),
    "s-min": lambda x: x/60,
    "min-s": lambda x: x*60,
    "s-h": lambda x: x/3600,
    "h-s": lambda x: x*3600,
    "min-h": lambda x: x/60,
    "h-min": lambda x: x*60,
    "m³-L": lambda x: x*sympy.N("1e+3"),
    "L-m³": lambda x: x*sympy.N("1e-3"),
    # * -->
    "m/s-km/h": lambda x: x*sympy.Rational(5, 18),
    "km/h-m/s": lambda x: x*sympy.Rational(18, 5),
    # ** -->
    "Wb-Mx": lambda x: x*sympy.N("1e+8"),
    "Mx-Wb": lambda x: x*sympy.N("1e-8"),
    "Wb-T⋅m²": lambda x: x,
    "T⋅m²-Wb": lambda x: x,
    "T⋅m²-Mx": lambda x: x*sympy.N("1e+8"),
    "Mx-T⋅m²": lambda x: x*sympy.N("1e-8"),
    "Wb/m²-Mx/m²": lambda x: x*sympy.N("1e+8"),
    "Mx/m²-Wb/m²": lambda x: x*sympy.N("1e-8"),
    "Wb/m²-T": lambda x: x,
    "T-Wb/m²": lambda x: x,
    "T-Mx/m²": lambda x: x*sympy.N("1e+8"),
    "Mx/m²-T": lambda x: x*sympy.N("1e-8"),
    # <-- **
    # <-- *
}

quantities = list(quantities_baseUnits.keys())

prefixes = list(prefixes_exponents.keys())

baseUnits = []
for baseUnitList in quantities_baseUnits.values(): baseUnits.extend(baseUnitList)
baseUnits = sorted(list(set(baseUnits)))

no_prefixes = [
    "Degrees", "Radians", "min", "h", "dB", "e",
    "m/s", "km/h", "m/min", "m/s²", "N⋅m", "kg⋅m/s", "N/m²", "Degrees/s", "Radians/s", "Degrees/s²", "Radians/s²", "kg⋅m²", "kg⋅m²/s", "1/s", "N/m", "kg/m", "g/m³", "g/L", "N/m²", "W/m²", "e/m³", "e/L", "Ω⋅m", "1/Ω⋅m", "1/°C", "Wb", "Mx", "T⋅m²", "T", "Wb/m²", "Mx/m²", "1/m",
]

exceptions = ["ks", "cC"] # kilosecond, centicoulomb

quantities_units = {}

for quantity, base_units in quantities_baseUnits.items():
    units = []
    for baseUnit in base_units:
        if baseUnit:
            if baseUnit in no_prefixes:
                units.append(baseUnit)

            else:
                for prefix in prefixes:
                    if prefix+baseUnit not in exceptions:
                        units.append(prefix+baseUnit)

    quantities_units[quantity] = units

def input_to_value(*args):
    if "Vector" in args[1]: return vector2D.input_to_Vector2D(args[0])
    else: return sympy.sympify(args[0])

def getExponent(unit: str):
    if "²" in unit: return 2
    elif "³" in unit: return 3
    else: return 1

def analyzeUnit(unit):
    match = re.match(rf"^({"|".join(sorted(prefixes, key=lambda x: -len(x)))})?({"|".join(baseUnits)})$", unit)

    if match:
        prefix, baseUnit = match.groups()
        return (prefix or "", baseUnit)
    
    else:
        return ("", unit)
    
def getNewValue(value, p1: str, u1: str, p2: str, u2: str):
    different_p = p1 != p2
    different_u = u1 != u2

    if different_p or different_u: value = value*sympy.N(f"1e{prefixes_exponents[p1]*getExponent(u1)}")
    if different_u: value = base_unit_conversion[f"{u1}-{u2}"](value)
    if different_p or different_u: value = value*sympy.N(f"1e{-prefixes_exponents[p2]*getExponent(u2)}")

    return value

def analyzeCompositeUnits(baseUnit):
    if "/" in baseUnit:
        numerator, denominator = baseUnit.split("/")

        numerator = tuple([unit for unit in numerator.replace("1", "").split("⋅") if unit])
        denominator = tuple(denominator.split("⋅"))

    else:
        numerator = tuple([unit for unit in baseUnit.split("⋅") if unit])
        denominator = tuple()

    return (numerator, denominator)

def new_getNewUnit(value, u1, u2):
    numerator1, denominator1 = analyzeCompositeUnits(u1)
    numerator2, denominator2 = analyzeCompositeUnits(u2)

    if len(numerator1) == len(numerator2) and len(denominator1) == len(denominator2):
        for numUnit1, numUnit2 in zip(numerator1, numerator2):
            p1, bu1 = analyzeUnit(numUnit1)
            p2, bu2 = analyzeUnit(numUnit2)

            different_p = p1 != p2
            different_bu = bu1 != bu2

            if different_p or different_bu: value = value*sympy.N(f"1e{prefixes_exponents[p1]*getExponent(bu1)}")
            if different_bu: value = base_unit_conversion[f"{bu1}-{bu2}"](value)
            if different_p or different_bu: value = value*sympy.N(f"1e{-prefixes_exponents[p2]*getExponent(bu2)}")

        denominator = 1
        for denUnit1, denUnit2 in zip(denominator1, denominator2):
            p1, bu1 = analyzeUnit(denUnit1)
            p2, bu2 = analyzeUnit(denUnit2)

            different_p = p1 != p2
            different_bu = bu1 != bu2

            if different_p or different_bu: denominator = denominator*sympy.N(f"1e{prefixes_exponents[p1]*getExponent(bu1)}")
            if different_bu: denominator = base_unit_conversion[f"{bu1}-{bu2}"](denominator)
            if different_p or different_bu: denominator = denominator*sympy.N(f"1e{-prefixes_exponents[p2]*getExponent(bu2)}")

        value = value/denominator

    else:
        pass

    return value

class Value:
    def __init__(self, quantity: str, value, unit: str, objects: list, prefix: str="", baseUnit: str=""):
        self.value: int|float|sympy.Basic|vector2D.Vector2D = value
        self.quantity = quantity
        self.unit = unit
        self.objects = objects

        if not prefix and not baseUnit: self.prefix, self.baseUnit = analyzeUnit(unit)
        else: self.prefix, self.baseUnit = prefix, baseUnit

        if type(self.value) == vector2D.Vector2D: value.unit = unit

    def change_unit(self, newUnit: str):
        if self.unit != newUnit:
            newPrefix, newBaseUnit = analyzeUnit(newUnit)
            self.value = getNewValue(self.value, self.prefix, self.baseUnit, newPrefix, newBaseUnit)
            self.unit, self.prefix, self.baseUnit = newUnit, newPrefix, newBaseUnit

            if type(self.value) == vector2D.Vector2D: self.value.unit = self.unit

    def in_another_unit(self, newUnit: str):
        if self.unit != newUnit:
            newPrefix, newBaseUnit = analyzeUnit(newUnit)
            if type(self.value) == vector2D.Vector2D: self.value.unit = self.unit
            return Value(self.quantity, getNewValue(self.value, self.prefix, self.baseUnit, newPrefix, newBaseUnit), newUnit, self.objects, prefix=newPrefix, baseUnit=newBaseUnit)
        
        return self
        
    def latex(self):
        if type(self.value) == vector2D.Vector2D: return self.value.getLabel()
        else: return sympy.latex(self.value) + " " + re.sub("(.+)/(.+)", "\\\\frac{\\1}{\\2}", self.unit)

def collectValues(givenValues: list[Value], desiredValues: list[list[str, str, list]], exceptions: list[str]=[]) -> tuple[list[Value], str, int, list[Value]]:
    foundValues: list[Value] = []
    additional_sol = ""
    steps = 0
    newValues: list[Value] = []

    # Experimental:
    # variable_number = 1

    for quantity, unit, objects in desiredValues:
        value = findValue(quantity, objects, givenValues+newValues)

        if (value is None) and ((find_value := eval(quantity.replace(" ", "_"))(givenValues+newValues, unit, objects, exceptions)) is not None):
            additional_sol += find_value[0] + "$\n\n$"
            value = find_value[1]
            steps += 1 + find_value[2]

            newValues.append(value)
            newValues.extend(find_value[3])

        # Experimental:
        # elif value is None: value = Value(quantity, sympy.Symbol(f"{quantitiy_symbol[quantity]}{variable_number}"), unit, objects)
        # variable_number += 1

        if type(value) == Value and value.unit != unit: additional_sol += quantitiy_symbol[quantity] + " = " + value.latex() + " = " + (value:=value.in_another_unit(unit)).latex() + "$\n\n$"

        foundValues.append(value)

    return (foundValues, additional_sol, steps, newValues)

def findValue(quantity: str, objects: list, givenValues: list[Value]):
    for value in givenValues:
        if (value.quantity == quantity) and (value.objects == objects):
            return value

def getSolution(givenValues: list[list[str]], requiredValues: list[list[str]]) -> tuple[str, list[vector2D.Vector2D, vector2D.vector3D.Vector3D]]:
    for index, g in enumerate(givenValues):
        g = g[:]
        g[1] = input_to_value(g[1], g[0])
        g[3] = [obj.strip() for obj in g[3].split(",")]
        givenValues[index] = Value(*g)

    for index, r in enumerate(requiredValues):
        requiredValues[index] = {"quantity": r[0], "unit": r[1], f"objects": [obj.strip() for obj in r[2].split(",")]}

    listOfSolutions = []
    vectors = []

    for value in requiredValues:
        requiredFunction: function = eval(value["quantity"].replace(" ", "_"))
        solution = requiredFunction(givenValues, value["unit"], value["objects"])
        if solution is None:
            listOfSolutions.append("\\text{Sorry, we couldn't find the " + value["quantity"] + " of " + ", ".join(value["objects"]) + ".}")

        else:
            listOfSolutions.append(solution[0])
            givenValues.append(solution[1])
            if type(solution[1].value) == vector2D.Vector2D or type(solution[1].value) == vector2D.vector3D.Vector3D: vectors.append(solution[1].value)

    return "$\n\n$".join(listOfSolutions), vectors

def Position_Vector(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "displacement" not in exceptions and len(objects) >= 1:
        sol = ""
        steps = 0

        if "Final" ==  objects[0]:
            (displacement, initial_position), additional_solution, additional_steps, newValues = collectValues(values, [["Displacement Vector", unit, objects[1:]], ["Position Vector", unit, ["Initial"]+objects[1:]]], exceptions=exceptions+["displacement"])

            if displacement and initial_position:
                steps += 1

                result = Value("Position Vector", displacement.value + initial_position.value, displacement.unit, objects)
                sol += "\\vec{\\Delta x} = \\vec{x_{f}} - \\vec{x_{i}}$\n$" + displacement.latex() + " = \\vec{x_{f}} - " + initial_position.latex() + "$\n$" + displacement.latex() + " + " + initial_position.latex() + " = \\vec{x_{f}}$\n$" + result.latex() + " = " + "\\vec{x_{f}}"

                solutions.append((additional_solution+sol, result, steps+additional_steps, newValues))

        else:
            (displacement, final_position), additional_solution, additional_steps, newValues = collectValues(values, [["Displacement Vector", unit, objects[1:]], ["Position Vector", unit, ["Final"]+objects[1:]]], exceptions=exceptions+["displacement"])

            if displacement and final_position:
                steps += 1

                result = Value("Position Vector", final_position.value - displacement.value, displacement.unit, objects)
                sol += "\\vec{\\Delta x} = \\vec{x_{f}} - \\vec{x_{i}}$\n$" + displacement.latex() + " = " + final_position.latex() + " - \\vec{x_{i}}$\n$\\vec{x_{i}} = " + final_position.latex() + " - " + displacement.latex() + "$\n$\\vec{x_{i}} = " + result.latex()

                solutions.append((additional_solution+sol, result, steps+additional_steps, newValues))

    if "position components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects], ["Position Y Component", unit, objects]], exceptions+["position components"])

        if x_component and y_component:
            vector = vector2D.Vector2D(x_component.value, y_component.value, unit=unit)

            if "Polar Coordinates" in objects:
                vector.getLabel = lambda v=vector: v.polar_coordinates()

                magnitude = Value("Position Magnitude", vector.magnitude, unit, objects)
                direction = Value("Position Direction", vector.theta_degrees, "Degrees", objects)

                vector.displayedValues += ["Magnitude", "Degrees"]

                result = Value("Position Vector", vector, unit, objects)

                newValues.append(magnitude)
                newValues.append(direction)

                sol += "x = \\sqrt{x_{x}^{2} + x_{y}^{2}} $\n$ x = \\sqrt{ \\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2} } $\n$ x = " + magnitude.latex() + " $\n\n$ \\theta = tan^{-1}\\left( \\frac{x_{y}}{x_{x}} \\right) $\n$ \\theta = tan^{-1}\\left( \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} \\right) $\n$ \\theta = " + direction.latex() + " $\n\n$ \\vec{x} = \\left( " + magnitude.latex() + " , " + direction.latex() + " \\right)"
                steps += 1

                solutions.append((sol, result, steps, newValues))

            else:
                result = Value("Position Vector", vector, unit, objects)
                sol += "\\vec{x} = x_{x} \\hat{i} + x_{y} \\hat{j} $\n$ \\vec{x} = " + x_component.latex() + " \\hat{i} + " + y_component.latex() + " \\hat{j} $\n$ \\vec{x} = " + result.latex()
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if "position polar" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Position Magnitude", unit, objects], ["Position Direction", "Degrees", objects]], exceptions+["position polar"])

        if magnitude and direction:
            vector = vector2D.Vector2D(magnitude.value, direction.value, c="pd", unit=unit)

            if "Rectangular Coordinates":
                x_component = Value("Position X Component", vector.x, unit, objects)
                y_component = Value("Position Y Component", vector.y, unit, objects)

                vector.displayedValues += ["X Component", "Y Component"]

                result = Value("Position Vector", vector, unit, objects)

                newValues.append(x_component)
                newValues.append(y_component)

                sol += "x_{x} = x \\ cos\\theta $\n$ x_{x} = " + magnitude.latex() + " \\cdot cos\\left( " + direction.latex() + " \\right) $\n$ x_{x} = " + x_component.latex() + " $\n$ x_{y} = x sin\\theta $\n$ x_{y} = " + y_component.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ x_{y} = " + y_component.latex() + " $\n\n$ \\vec{x} = " + vector.unit_vectors()

                steps += 1

                solutions.append((sol, result, steps, newValues))

            else:
                vector.getLabel = lambda v=vector: v.polar_coordinates()
                result = Value("Position Vector", vector, unit, objects)
                sol += "\\vec{x} = \\left( " + magnitude.latex() + ", " + direction.latex() + " \\right)"
                steps += 1

                solutions.append((sol, result, steps, newValues))
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Position_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    vector = findValue("Position Vector", objects, values)
    if vector and "Magnitude" in vector.value.displayedValues:
        result = Value("Position Magnitude", vector.value.magnitude, vector.unit, objects)
        sol = "x = " + result.latex()

        if result.unit != unit:
            result.change_unit(unit)
            sol += "$\n$ x = " + result.latex()

        steps = 0

        return (sol, result, steps, [])
    
    if "position components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects], ["Position Y Component", unit, objects]], exceptions+["position components"])

        if x_component and y_component:
            result = Value("Position Magnitude", sympy.sqrt(sympy.Pow(x_component.value, 2) + sympy.Pow(y_component.value, 2)), x_component.unit, objects)

            sol += "x = \\sqrt{x_{x}^{2} + x_{y}^{2}} $\n$ x = \\sqrt{\\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2}} $\n$ x = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "x_x=xcos(theta)" not in exceptions:
        (x_component, direction), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects], ["Position Direction", "Degrees", objects]], exceptions+["x_x=xcos(theta)"])

        if x_component and direction:
            result = Value("Position Magnitude", x_component.value/sympy.cos(sympy.rad(direction.value)), unit, objects)

            sol += "x_{x} = x cos\\theta $\n$ " + x_component.latex() + " = x \\times cos\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + x_component.latex() + "}{" + sympy.latex(sympy.cos(direction.value)) + "} = x $\n$" + result.latex() + " = x"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "x_y=xsin(theta)" not in exceptions:
        (y_component, direction), sol, steps, newValues = collectValues(values, [["Position Y Component", unit, objects], ["Position Direction", "Degrees", objects]], exceptions+["x_y=xsin(theta)"])

        if y_component and direction:
            result = Value("Position Magnitude", y_component.value/sympy.sin(sympy.rad(direction.value)), unit, objects)

            sol += "x_{y} = x sin\\theta $\n$ " + y_component.latex() + " = x \\times sin\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + y_component.latex() + "}{" + sympy.latex(sympy.sin(direction.value)) + "} = x $\n$" + result.latex() + " = x"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Position_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Position_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Position_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Displacement_Vector(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "displacement" not in exceptions:
        (initial_position, final_position), sol, steps, newValues = collectValues(values, [["Position Vector", unit, ["Initial"]+objects], ["Position Vector", unit, ["Final"]+objects]], exceptions+["displacement"])

        if initial_position and final_position:
            result = Value("Displacement Vector", final_position.value - initial_position.value, unit, objects)

            sol += "\\vec{\\Delta x} = \\vec{x_{f}} - \\vec{x_{i}} $\n$ \\vec{\\Delta x} = " + final_position.latex() + " - " + initial_position.latex() + " $\n$ \\vec{\\Delta x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "velocity" not in exceptions:
        (velocity, time), sol, steps, newValues = collectValues(values, [["Velocity Vector", "m/s", objects], ["Time", "s", objects]], exceptions+["velocity"])
        if velocity and time:
            result = Value("Displacement Vector", velocity.value*time.value, "m", objects)

            sol += "\\vec{v} = \\frac{\\vec{\\Delta x}}{t} $\n$ " + velocity.latex() + " = \\frac{\\vec{\\Delta x}}{" + time.latex() + "} $\n$ " + velocity.latex() + " \\times " + time.latex() + " = \\vec{\\Delta x} $\n$" + result.latex() + " = \\vec{\\Delta x}"
            steps += 1

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$ " + result.latex() + " = \\vec{\\detla x}"

            solutions.append((sol, result, steps, newValues))

    if "displacement components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Displacement X Component", unit, objects], ["Displacement Y Component", unit, objects]], exceptions+["displacement components"])

        if x_component and y_component:
            vector = vector2D.Vector2D(x_component.value, y_component.value, unit=unit)

            if "Polar Coordinates" in objects:
                vector.getLabel = lambda v=vector: v.polar_coordinates()

                magnitude = Value("Displacement Magnitude", vector.magnitude, unit, objects)
                direction = Value("Displacement Direction", vector.theta_degrees, "Degrees", objects)

                vector.displayedValues += ["Magnitude", "Degrees"]

                result = Value("Displacement Vector", vector, unit, objects)

                newValues.append(magnitude)
                newValues.append(direction)

                sol += "\\Delta x = \\sqrt{\\Delta x_{x}^{2} + \\Delta x_{y}^{2}} $\n$ \\Delta x = \\sqrt{ \\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2} } $\n$ \\Delta x = " + magnitude.latex() + " $\n\n$ \\theta = tan^{-1}\\left( \\frac{\\Delta x_{y}}{\\Delta x_{x}} \\right) $\n$ \\theta = tan^{-1}\\left( \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} \\right) $\n$ \\theta = " + direction.latex() + " $\n\n$ \\vec{\\Delta x} = \\left( " + magnitude.latex() + " , " + direction.latex() + " \\right)"
                steps += 1

                solutions.append((sol, result, steps, newValues))

            else:
                result = Value("Displacement Vector", vector, unit, objects)
                sol += "\\vec{\\Delta x} = \\Delta x_{x} \\hat{i} + \\Delta x_{y} \\hat{j} $\n$ \\vec{\\Delta x} = " + x_component.latex() + " \\hat{i} + " + y_component.latex() + " \\hat{j} $\n$ \\vec{v} = " + result.latex()
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if "displacement polar" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Displacement Magnitude", unit, objects], ["Displacement Direction", "Degrees", objects]], exceptions+["displacement polar"])

        if magnitude and direction:
            vector = vector2D.Vector2D(magnitude.value, direction.value, c="pd", unit=unit)

            if "Rectangular Coordinates":
                x_component = Value("Displacement X Component", vector.x, unit, objects)
                y_component = Value("Displacement Y Component", vector.y, unit, objects)

                vector.displayedValues += ["X Component", "Y Component"]

                result = Value("Displacement Vector", vector, unit, objects)

                newValues.append(x_component)
                newValues.append(y_component)

                sol += "\\Delta x_{x} = \\Delta x \\ cos\\theta $\n$ \\Delta x_{x} = " + magnitude.latex() + " \\cdot cos\\left( " + direction.latex() + " \\right) $\n$ \\Delta x_{x} = " + x_component.latex() + " $\n$ \\Delta x_{y} = x sin\\theta $\n$ \\Delta x_{y} = " + y_component.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ \\Delta x_{y} = " + y_component.latex() + " $\n\n$ \\vec{\\Delta x} = " + vector.unit_vectors()

                steps += 1

                solutions.append((sol, result, steps, newValues))

            else:
                vector.getLabel = lambda v=vector: v.polar_coordinates()
                result = Value("Displacement Vector", vector, unit, objects)
                sol += "\\vec{\\Delta x} = \\left( " + magnitude.latex() + ", " + direction.latex() + " \\right)"
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Displacement_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Displacement_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Displacement_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Displacement_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Distance(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Time(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Velocity_Vector(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "velocity components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Velocity X Component", unit, objects], ["Velocity Y Component", unit, objects]], exceptions+["velocity components"])

        if x_component and y_component:
            vector = vector2D.Vector2D(x_component.value, y_component.value, unit=unit)

            if "Polar Coordinates" in objects:
                vector.getLabel = lambda v=vector: v.polar_coordinates()

                magnitude = Value("Velocity Magnitude", vector.magnitude, unit, objects)
                direction = Value("Velocity Direction", vector.theta_degrees, "Degrees", objects)

                vector.displayedValues += ["Magnitude", "Degrees"]

                result = Value("Velocity Vector", vector, unit, objects)

                newValues.append(magnitude)
                newValues.append(direction)

                sol += "v = \\sqrt{v_{x}^{2} + v_{y}^{2}} $\n$ v = \\sqrt{ \\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2} } $\n$ v = " + magnitude.latex() + " $\n\n$ \\theta = tan^{-1}\\left( \\frac{v_{y}}{v_{x}} \\right) $\n$ \\theta = tan^{-1}\\left( \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} \\right) $\n$ \\theta = " + direction.latex() + " $\n\n$ \\vec{v} = \\left( " + magnitude.latex() + " , " + direction.latex() + " \\right)"
                steps += 1

                solutions.append((sol, result, steps, newValues))

            else:
                result = Value("Velocity Vector", vector, unit, objects)
                sol += "\\vec{v} = v_{x} \\hat{i} + v_{y} \\hat{j} $\n$ \\vec{v} = " + x_component.latex() + " \\hat{i} + " + y_component.latex() + " \\hat{j} $\n$ \\vec{v} = " + result.latex()
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if "velocity polar" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Velocity Magnitude", unit, objects], ["Velocity Direction", "Degrees", objects]], exceptions+["velocity polar"])

        if magnitude and direction:
            vector = vector2D.Vector2D(magnitude.value, direction.value, c="pd", unit=unit)

            if "Rectangular Coordinates":
                x_component = Value("Velocity X Component", vector.x, unit, objects)
                y_component = Value("Velocity Y Component", vector.y, unit, objects)

                vector.displayedValues += ["X Component", "Y Component"]

                result = Value("Velocity Vector", vector, unit, objects)

                newValues.append(x_component)
                newValues.append(y_component)

                sol += "v_{x} = v \\ cos\\theta $\n$ v_{x} = " + magnitude.latex() + " \\cdot cos\\left( " + direction.latex() + " \\right) $\n$ v_{x} = " + x_component.latex() + " $\n$ v_{y} = v sin\\theta $\n$ v_{y} = " + y_component.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ v_{y} = " + y_component.latex() + " $\n\n$ \\vec{v} = " + vector.unit_vectors()

                steps += 1

                solutions.append((sol, result, steps, newValues))

            else:
                vector.getLabel = lambda v=vector: v.polar_coordinates()
                result = Value("Velocity Vector", vector, unit, objects)
                sol += "\\vec{v} = \\left( " + magnitude.latex() + ", " + direction.latex() + " \\right)"
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if "average velocity" not in exceptions:
        (displacement_vector, time), sol, steps, newValues = collectValues(values, [["Displacement Vector", "m", objects], ["Time", "s", objects]], exceptions=exceptions+["average velocity"])

        if displacement_vector and time:
            result = Value("Velocity", displacement_vector.value/time.value, "m/s", objects)
            sol += "\\vec{v} = \\frac{\\vec{\\Delta x}}{t} $\n$ \\vec{v} = \\frac{" + displacement_vector.latex() + "}{" + time.latex() + "} $\n$ \\vec{v} = " + result.latex()
            steps += 1

            if result.unit != unit:
                result.change_unit(unit)
                sol += " $\n$ \\vec{v} = " + result.latex()

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Velocity_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Velocity_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Velocity_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Speed(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Acceleration_Vector(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "velocity components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Velocity X Component", unit, objects], ["Velocity Y Component", unit, objects]], exceptions+["velocity components"])

        if x_component and y_component:
            vector = vector2D.Vector2D(x_component.value, y_component.value, unit=unit)

            if "Polar Coordinates" in objects:
                vector.getLabel = lambda v=vector: v.polar_coordinates()

                magnitude = Value("Velocity Magnitude", vector.magnitude, unit, objects)
                direction = Value("Velocity Direction", vector.theta_degrees, "Degrees", objects)

                vector.displayedValues += ["Magnitude", "Degrees"]

                result = Value("Velocity Vector", vector, unit, objects)

                newValues.append(magnitude)
                newValues.append(direction)

                sol += "v = \\sqrt{v_{x}^{2} + v_{y}^{2}} $\n$ v = \\sqrt{ \\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2} } $\n$ v = " + magnitude.latex() + " $\n\n$ \\theta = tan^{-1}\\left( \\frac{v_{y}}{v_{x}} \\right) $\n$ \\theta = tan^{-1}\\left( \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} \\right) $\n$ \\theta = " + direction.latex() + " $\n\n$ \\vec{v} = \\left( " + magnitude.latex() + " , " + direction.latex() + " \\right)"
                steps += 1

                solutions.append((sol, result, steps, newValues))

            else:
                result = Value("Velocity Vector", vector, unit, objects)
                sol += "\\vec{v} = v_{x} \\hat{i} + v_{y} \\hat{j} $\n$ \\vec{v} = " + x_component.latex() + " \\hat{i} + " + y_component.latex() + " \\hat{j} $\n$ \\vec{v} = " + result.latex()
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if "velocity polar" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Velocity Magnitude", unit, objects], ["Velocity Direction", "Degrees", objects]], exceptions+["velocity polar"])

        if magnitude and direction:
            vector = vector2D.Vector2D(magnitude.value, direction.value, c="pd", unit=unit)

            if "Rectangular Coordinates":
                x_component = Value("Velocity X Component", vector.x, unit, objects)
                y_component = Value("Velocity Y Component", vector.y, unit, objects)

                vector.displayedValues += ["X Component", "Y Component"]

                result = Value("Velocity Vector", vector, unit, objects)

                newValues.append(x_component)
                newValues.append(y_component)

                sol += "v_{x} = v \\ cos\\theta $\n$ v_{x} = " + magnitude.latex() + " \\cdot cos\\left( " + direction.latex() + " \\right) $\n$ v_{x} = " + x_component.latex() + " $\n$ v_{y} = v sin\\theta $\n$ v_{y} = " + y_component.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ v_{y} = " + y_component.latex() + " $\n\n$ \\vec{v} = " + vector.unit_vectors()

                steps += 1

                solutions.append((sol, result, steps, newValues))

            else:
                vector.getLabel = lambda v=vector: v.polar_coordinates()
                result = Value("Velocity Vector", vector, unit, objects)
                sol += "\\vec{v} = \\left( " + magnitude.latex() + ", " + direction.latex() + " \\right)"
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Acceleration_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Acceleration_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Acceleration_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

def Horizontal_Range(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    pass

if __name__ == "__main__":
    # import matplotlib.pyplot as plt

    # v = [Value("Displacement Vector", vector2D.Vector2D(5, 5), "m", []), Value("Position Vector", vector2D.Vector2D(24,2), "m", ["Initial"])]
    # s = Position_Vector(v, "m", ["Final"])
    # t = s[0]

    # v = [Value("Position X Component", 4, "m", []), Value("Position Y Component", 3, "m", [])]
    # s = Position_Magnitude(v, "m", [])
    # t = s[0]

    # plt.text(0,0, "$" + t + "$", fontsize=24)
    # plt.show()

    # r = new_getNewUnit(sympy.sympify(1), "nm/ks", "km/ns")

    # plt.text(0,0, "$" + sympy.latex(r) + "$", fontsize=24)
    # plt.show()

    # import matplotlib.pyplot as plt

    # a, b, c, d, e, f = vector2D.VectorProduct(vector2D.i, vector2D.j)

    # plt.axis("equal")
    # plt.legend(fontsize=16)
    # plt.show()

    # vector2D.Vector2D_sum([vector2D.i, vector2D.j, 2*vector2D.j, 2*vector2D.i, vector2D.i, vector2D.j, vector2D.i, vector2D.j, vector2D.i, vector2D.j, ])[0]

    # plt.axis("equal")
    # plt.legend(fontsize=16)
    # plt.show()

    # vector3D.Vector3D_sum([vector3D.i, vector3D.i, vector3D.j, vector3D.j, vector3D.k, vector3D.k, vector3D.k, vector3D.i, vector3D.j])

    # plt.axis("equal")
    # plt.legend(fontsize=16)
    # plt.show()

    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
    plt.rcParams["mathtext.default"] = "regular"
    plt.rcParams["mathtext.fontset"] = "stix"

    plt.text(0,0, "$ \\mathit{" + quantitiy_symbol["Acceleration Vector"] + " \\cdot \\vec{b}} $", fontsize=20)
    plt.show()