import math
import re

quantities_baseUnits = {
    "Position Magnitude": ["m"], # Chapter 2
    "Position Direction": ["Degrees", "Radians"],
    "Position X Component": ["m"],
    "Position Y Component": ["m"],
    "Displacement Magnitude": ["m"],
    "Displacement Direction": ["Degrees", "Radians"],
    "Displacement X Component": ["m"],
    "Displacement Y Component": ["m"],
    "Distance": ["m"],
    "Time": ["s", "min", "h"],
    "Velocity Magnitude": ["m/s", "km/h", "m/min"],
    "Velocity Direction": ["Degrees", "Radians"],
    "Velocity X Component": ["m/s", "km/h", "m/min"],
    "Velocity Y Component": ["m/s", "km/h", "m/min"],
    "Speed": ["m/s", "km/h", "m/min"],
    "Acceleration Magnitude": ["m/s²"],
    "Acceleration Direction": ["Degrees", "Radians"],
    "Acceleration X Component": ["m/s²"],
    "Acceleration Y Component": ["m/s²"],
    "Horizontal Range": ["m"],
    # "Force Magnitude": ["N"], # Chapter 3
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
    # "Temperature": ["°C", "K"]
    # "Temperature Coefficient of Resistivity": ["1/°C", "1/K"],
    # "Electromotive Force": ["V"],
    # "Internal Resistance": ["Ω"],
    # "Electric Power": ["W"],
    # Chapter 10:
    # "Magnetic Flux": ["Wb", "Mx"s],
    # "Magnetic Flux Density": ["Wb/m²", "Mx/m²"],
    # "Number of Turns": [""],
    # "Number of Turns Per Unit Length": ["1/m"],
}

quantitiy_symbol = {
    "Position Magnitude": "r",
    "Position Direction": "\\theta",
    "Position X Component": "r_{x}",
    "Position Y Component": "r_{y}",
    "Displacement Magnitude": "\\Delta x",
    "Displacement Direction": "\\theta",
    "Displacement X Component": "\\Delta r_{x}",
    "Displacement Y Component": "\\Delta r_{y}",
    "Distance": "d",
    "Time": "t",
    "Velocity Magnitude": "v",
    "Velocity Direction": "\\theta",
    "Velocity X Component": "v_{x}",
    "Velocity Y Component": "v_{y}",
    "Speed": "v_{s}",
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
    "Degrees-Radians": lambda x: math.radians(x),
    "Radians-Degrees": lambda x: math.degrees(x),
    "Degrees-Revolutions": lambda x: x/360,
    "Revolutions-Degrees": lambda x: x*360,
    "Revolutions-Radians": lambda x: x*2*math.pi,
    "Radians-Revolutions": lambda x: x/(2*math.pi),
    "s-min": lambda x: x/60,
    "min-s": lambda x: x*60,
    "s-h": lambda x: x/3600,
    "h-s": lambda x: x*3600,
    "min-h": lambda x: x/60,
    "h-min": lambda x: x*60,
    "m³-L": lambda x: x*1e+3,
    "L-m³": lambda x: x*1e-3,
    # * -->
    "m/s-km/h": lambda x: x*5/18,
    "km/h-m/s": lambda x: x*18/5,
    # ** -->
    "Wb-Mx": lambda x: x*1e+8,
    "Mx-Wb": lambda x: x*1e-8,
    "Wb-T⋅m²": lambda x: x,
    "T⋅m²-Wb": lambda x: x,
    "T⋅m²-Mx": lambda x: x*1e+8,
    "Mx-T⋅m²": lambda x: x*1e-8,
    "Wb/m²-Mx/m²": lambda x: x*1e+8,
    "Mx/m²-Wb/m²": lambda x: x*1e-8,
    "Wb/m²-T": lambda x: x,
    "T-Wb/m²": lambda x: x,
    "T-Mx/m²": lambda x: x*1e+8,
    "Mx/m²-T": lambda x: x*1e-8,
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

    if different_p or different_u: value = value*eval(f"1e{prefixes_exponents[p1]*getExponent(u1)}")
    if different_u: value = base_unit_conversion[f"{u1}-{u2}"](value)
    if different_p or different_u: value = value*eval(f"1e{-prefixes_exponents[p2]*getExponent(u2)}")

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

def new_getNewValue(value, u1, u2):
    numerator1, denominator1 = analyzeCompositeUnits(u1)
    numerator2, denominator2 = analyzeCompositeUnits(u2)

    for numUnit1, numUnit2 in zip(numerator1, numerator2):
        p1, bu1 = analyzeUnit(numUnit1)
        p2, bu2 = analyzeUnit(numUnit2)

        different_p = p1 != p2
        different_bu = bu1 != bu2

        if different_p or different_bu: value = value*eval(f"1e{prefixes_exponents[p1]*getExponent(bu1)}")
        if different_bu: value = base_unit_conversion[f"{bu1}-{bu2}"](value)
        if different_p or different_bu: value = value*eval(f"1e{-prefixes_exponents[p2]*getExponent(bu2)}")

    denominator = 1
    for denUnit1, denUnit2 in zip(denominator1, denominator2):
        p1, bu1 = analyzeUnit(denUnit1)
        p2, bu2 = analyzeUnit(denUnit2)

        different_p = p1 != p2
        different_bu = bu1 != bu2

        if different_p or different_bu: denominator = denominator*eval(f"1e{prefixes_exponents[p1]*getExponent(bu1)}")
        if different_bu: denominator = base_unit_conversion[f"{bu1}-{bu2}"](denominator)
        if different_p or different_bu: denominator = denominator*eval(f"1e{-prefixes_exponents[p2]*getExponent(bu2)}")

    return value/denominator

def replaceListItem(currentList: list, currentValue, newValue) -> list:
    newList = []

    for item in currentList:
        if item == currentValue:
            if newValue: newList.append(newValue)

        else: newList.append(item)

    return newList

class Value:
    def __init__(self, quantity: str, value, unit: str, objects: list): #, prefix: str="", baseUnit: str=""):
        self.value: int|float = value
        self.quantity = quantity
        self.unit = unit
        self.objects = objects

        # if not prefix and not baseUnit: self.prefix, self.baseUnit = analyzeUnit(unit)
        # else: self.prefix, self.baseUnit = prefix, baseUnit

    # def change_unit(self, newUnit: str):
    #     if self.unit != newUnit:
    #         newPrefix, newBaseUnit = analyzeUnit(newUnit)
    #         self.value = getNewValue(self.value, self.prefix, self.baseUnit, newPrefix, newBaseUnit)
    #         self.unit, self.prefix, self.baseUnit = newUnit, newPrefix, newBaseUnit

    # def in_another_unit(self, newUnit: str):
    #     if self.unit != newUnit:
    #         newPrefix, newBaseUnit = analyzeUnit(newUnit)
    #         return Value(self.quantity, getNewValue(self.value, self.prefix, self.baseUnit, newPrefix, newBaseUnit), newUnit, self.objects, prefix=newPrefix, baseUnit=newBaseUnit)
        
    #     return self

    def change_unit(self, newUnit: str):
        if self.unit != newUnit:
            self.value = new_getNewValue(self.value, self.unit, newUnit)
            self.unit = newUnit

    def in_another_unit(self, newUnit: str):
        if self.unit != newUnit: return Value(self.quantity, new_getNewValue(self.value, self.unit, newUnit), newUnit, self.objects)
        return self
        
    def latex(self): return str(self.value) + " " + re.sub("(.+)/(.+)", "\\\\frac{\\1}{\\2}", self.unit)

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

        if type(value) == Value and value.unit != unit: additional_sol += quantitiy_symbol[quantity] + " = " + value.latex() + " = " + (value:=value.in_another_unit(unit)).latex() + "$\n\n$"

        foundValues.append(value)

    return (foundValues, additional_sol, steps, newValues)

def findValue(quantity: str, objects: list, givenValues: list[Value]):
    for value in givenValues:
        if (value.quantity == quantity) and (value.objects == objects):
            return value

def getSolution(givenValues: list[list[str]], requiredValues: list[list[str]]) -> tuple[str, list]:
    for index, g in enumerate(givenValues):
        g = g[:]
        g[1] = eval(g[1])
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
            #if type(solution[1].value) == vector2D.Vector2D or type(solution[1].value) == vector2D.vector3D.Vector3D: vectors.append(solution[1].value)

    return "$\n\n$".join(listOfSolutions), vectors

def Position_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "position components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects], ["Position Y Component", unit, objects]], exceptions+["position components"])

        if x_component and y_component:
            result = Value("Position Magnitude", math.sqrt(math.pow(x_component.value, 2) + math.pow(y_component.value, 2)), x_component.unit, objects)

            sol += "r = \\sqrt{x^{2} + y^{2}} $\n$ r = \\sqrt{\\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2}} $\n$ r = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "r_x=rcos(theta)" not in exceptions:
        (x_component, direction), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects], ["Position Direction", "Degrees", objects]], exceptions+["r_x=rcos(theta)"])

        if x_component and direction:
            radians = math.radians(direction.value)

            result = Value("Position Magnitude", x_component.value/math.cos(radians), unit, objects)

            sol += "r_{x} = r cos\\theta $\n$ " + x_component.latex() + " = r \\times cos\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + x_component.latex() + "}{cos\\left( " + direction.latex() + " \\degree \\right)} = r $\n$" + result.latex() + " = r"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "r_y=rsin(theta)" not in exceptions:
        (y_component, direction), sol, steps, newValues = collectValues(values, [["Position Y Component", unit, objects], ["Position Direction", "Degrees", objects]], exceptions+["r_y=rsin(theta)"])

        if y_component and direction:
            result = Value("Position Magnitude", y_component.value/math.sin(math.radians(direction.value)), unit, objects)

            sol += "y = r sin\\theta $\n$ " + y_component.latex() + " = r \\times sin\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + y_component.latex() + "}{" + str(math.sin(direction.value)) + "} = r $\n$" + result.latex() + " = r"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Position_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "tan(theta)=r_y/r_x" not in exceptions:
        (y_component, x_component), sol, steps, newValues = collectValues(values, [["Position Y Component", "m", objects], ["Position X Component", "m", objects]], exceptions=exceptions+["tan(theta)=r_y/r_x"])

        if y_component and x_component:
            radians = math.atan2(y_component.value, x_component.value)
            degrees = math.degrees(radians)

            result_value = degrees if unit == "Degrees" else radians

            result = Value("Position Direction", result_value, unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{r_{y}}{r_{x}} $\n$ tan\\left( \\theta \\right) = \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "r_x=rcos(theta)" not in exceptions:
        (x_component, magnitude), sol, steps, newValues = collectValues(values, [["Position X Component", "m", objects], ["Position Magnitude", "m", objects]], exceptions=exceptions+["r_x=rcos(theta)"])

        if x_component and magnitude:
            radians = math.acos(x_component.value/magnitude.value)
            degrees = math.degrees(radians)

            result_value = degrees if unit == "Degrees" else radians

            result = Value("Position Direction", result_value, unit, objects)

            sol += "r_{x} = r cos\\left( \\theta \\right) $\n$ " + x_component.latex() + " = " + magnitude.latex() + " \\times cos\\left( \\theta \\right) $\n$ \\frac{" + x_component.latex() + "}{" + magnitude.latex() + "} = cos\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "r_y=rsin(theta)" not in exceptions:
        (y_component, magnitude), sol, steps, newValues = collectValues(values, [["Position Y Component", "m", objects], ["Position Magnitude", "m", objects]], exceptions=exceptions+["r_y=rsin(theta)"])

        if x_component and magnitude:
            radians = math.asin(y_component.value/magnitude.value)
            degrees = math.degrees(radians)

            result_value = degrees if unit == "Degrees" else radians

            result = Value("Position Direction", result_value, unit, objects)

            sol += "y = r sin\\left( \\theta \\right) $\n$ " + y_component.latex() + " = " + magnitude.latex() + " \\times sin\\left( \\theta \\right) $\n$ \\frac{" + y_component.latex() + "}{" + magnitude.latex() + "} = sin\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Position_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "r_x=rcos(theta)":
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Position Magnitude", unit, objects], ["Position Direction", "Degrees", objects]], exceptions=exceptions+["r_x=rcos(theta)"])

        if magnitude and direction:
            radians = math.radians(direction.value)
            result = Value("Position X Component", magnitude.value*math.cos(radians))

            sol += "r_{x} = r cos\\left( \\theta \\right) $\n$ r_{x} = " + magnitude.latex() + " \\times cos\\left( " + direction.latex() + " \\degree \\right) $\n$ r_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=r_y/r_x" not in exceptions:
        (direction, y_component), sol, steps, newValues = collectValues(values, [["Position Direction", "Degrees", objects], ["Position Y Component", unit]])

        if direction and y_component:
            radians = math.radians(direction.value)
            result = Value("Position X Component", y_component.value/math.tan(radians), objects)

            sol += "tan\\left( \\theta \\right) = \\frac{r_{y}}{r_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{" + y_component.latex() + "}{r_{x}} $\n$ r_{x} = \\frac{" + y_component.latex() + "}{" + str(math.tan(radians)) + "} $\n$ r_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "displacement" not in exceptions:
        if "Final" in objects:
            (displacement, initial_position), sol, steps, newValues = collectValues(values, [["Displacement X Component", unit, objects], ["Position X Component", unit, replaceListItem(objects, "Final", "Initial")]], exceptions=exceptions+["displacement"])

            if displacement and initial_position:
                result = Value("Position X Component", displacement.value + initial_position.value, unit, objects)

                sol += "\\Delta r_{x} = r_{xf} - r_{xi} $\n$ " + displacement.latex() + " = r_{xf} - \\left(" + initial_position.latex() + "\\right $\n$ " + displacement.latex() + " + \\left(" + initial_position.latex() + "\\right) = r_{xf} $\n$" + result.latex() + " = r_{xf}"
                steps += 1

                solutions.append((sol, result, steps, newValues))

        elif "Initial" in objects:
            (displacement, final_position), sol, steps, newValues = collectValues(values, [["Displacement X Component", unit, objects], ["Position X Component", unit, replaceListItem(objects, "Initial", "Final")]], exceptions=exceptions+["displacement"])

            if displacement and final_position:
                result = Value("Position X Component", displacement.value + final_position.value, unit, objects)

                sol += "\\Delta r_{x} = r_{xf} - r_{xi} $\n$ " + displacement.latex() + " = " + final_position.latex() + " - r_{xi} $\n$ r_{xi} = " + final_position.latex() + " - \\left(" + displacement.latex() + "\\right) $\n$ r_{xi} = " + result.latex()
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Position_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "r_y=rsin(theta)":
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Position Magnitude", unit, objects], ["Position Direction", "Degrees", objects]], exceptions=exceptions+["r_y=rsin(theta)"])

        if magnitude and direction:
            radians = math.radians(direction.value)
            result = Value("Position X Component", magnitude.value*math.sin(radians))

            sol += "r_{y} = r sin\\left( \\theta \\right) $\n$ r_{y} = " + magnitude.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ r_{y} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=r_y/r_x" not in exceptions:
        (direction, x_component), sol, steps, newValues = collectValues(values, [["Position Direction", "Degrees", objects], ["Position X Component", unit]])

        if direction and x_component:
            radians = math.radians(direction.value)
            result = Value("Position Y Component", x_component.value*math.tan(radians), objects)

            sol += "tan\\left( \\theta \\right) = \\frac{r_{y}}{r_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{r_{y}{" + x_component.latex() + "}} $\n$ " + str(math.tan(radians)) + " \\times " + x_component.latex() + " = r_{y} $\n$" + result.latex() + " = r_{y}"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "displacement" not in exceptions:
        if "Final" in objects:
            (displacement, initial_position), sol, steps, newValues = collectValues(values, [["Displacement Y Component", unit, objects], ["Position Y Component", unit, replaceListItem(objects, "Final", "Initial")]], exceptions=exceptions+["displacement"])

            if displacement and initial_position:
                result = Value("Position Y Component", displacement.value + initial_position.value, unit, objects)

                sol += "\\Delta r_{y} = r_{yf} - r_{yi} $\n$ " + displacement.latex() + " = r_{yf} - \\left(" + initial_position.latex() + "\\right $\n$ " + displacement.latex() + " + \\left(" + initial_position.latex() + "\\right) = r_{yf} $\n$" + result.latex() + " = r_{yf}"
                steps += 1

                solutions.append((sol, result, steps, newValues))

        elif "Initial" in objects:
            (displacement, final_position), sol, steps, newValues = collectValues(values, [["Displacement Y Component", unit, objects], ["Position Y Component", unit, replaceListItem(objects, "Initial", "Final")]], exceptions=exceptions+["displacement"])

            if displacement and final_position:
                result = Value("Position X Component", displacement.value + final_position.value, unit, objects)

                sol += "\\Delta r_{y} = r_{yf} - r_{yi} $\n$ " + displacement.latex() + " = " + final_position.latex() + " - r_{yi} $\n$ r_{yi} = " + final_position.latex() + " - \\left(" + displacement.latex() + "\\right) $\n$ r_{yi} = " + result.latex()
                steps += 1

                solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Displacement_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Displacement_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Displacement_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Displacement_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Distance(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Time(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Speed(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Horizontal_Range(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []



    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

if __name__ == "__main__":
    pass