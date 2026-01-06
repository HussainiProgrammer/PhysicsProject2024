import sympy
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

quantity_vectorEquations = {
    "Position Magnitude": ["tan(theta)=r_y/r_x", "r_x=rcos(theta)", "r_y=rsin(theta)"],
    "Position Direction": ["tan(theta)=r_y/r_x", "r_x=rcos(theta)", "r_y=rsin(theta)"],
    "Position X Component": ["tan(theta)=r_y/r_x", "r_x=rcos(theta)", "r_y=rsin(theta)"],
    "Position Y Component": ["tan(theta)=r_y/r_x", "r_x=rcos(theta)", "r_y=rsin(theta)"],
    "Displacement Magnitude": ["tan(theta)=dr_y/dr_x", "dr_x=drcos(theta)", "dr_y=drsin(theta)"],
    "Displacement Direction": ["tan(theta)=dr_y/dr_x", "dr_x=drcos(theta)", "dr_y=drsin(theta)"],
    "Displacement X Component": ["tan(theta)=dr_y/dr_x", "dr_y=drsin(theta)", "dr_x=drcos(theta)"],
    "Displacement Y Component": ["tan(theta)=dr_y/dr_x", "dr_x=drcos(theta)", "dr_y=drsin(theta)"],
    "Velocity Magnitude": ["tan(theta)=v_y/v_x", "v_x=vcos(theta)", "v_y=vsin(theta)"],
    "Velocity Direction": ["tan(theta)=v_y/v_x", "v_x=vcos(theta)", "v_y=vsin(theta)"],
    "Velocity X Component": ["tan(theta)=v_y/v_x", "v_x=vcos(theta)", "v_y=vsin(theta)"],
    "Velocity Y Component": ["tan(theta)=v_y/v_x", "v_x=vcos(theta)", "v_y=vsin(theta)"],
    "Acceleration Magnitude": ["tan(theta)=a_y/a_x", "a_x=acos(theta)", "a_y=asin(theta)"],
    "Acceleration Direction": ["tan(theta)=a_y/a_x", "a_x=acos(theta)", "a_y=asin(theta)"],
    "Acceleration X Component": ["tan(theta)=a_y/a_x", "a_x=acos(theta)", "a_y=asin(theta)"],
    "Acceleration Y Component": ["tan(theta)=a_y/a_x", "a_x=acos(theta)", "a_y=asin(theta)"],
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
    "da":  1,
    "h":   2,
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

def new_getNewValue(value, u1, u2):
    numerator1, denominator1 = analyzeCompositeUnits(u1)
    numerator2, denominator2 = analyzeCompositeUnits(u2)

    denominator = 1
    if len(numerator1) == len(numerator2) and len(denominator1) == len(denominator2):
        for numUnit1, numUnit2 in zip(numerator1, numerator2):
            p1, bu1 = analyzeUnit(numUnit1)
            p2, bu2 = analyzeUnit(numUnit2)

            different_p = p1 != p2
            different_bu = bu1 != bu2

            if different_p or different_bu: value = value*sympy.N(f"1e{prefixes_exponents[p1]*getExponent(bu1)}")
            if different_bu: value = base_unit_conversion[f"{bu1}-{bu2}"](value)
            if different_p or different_bu: value = value*sympy.N(f"1e{-prefixes_exponents[p2]*getExponent(bu2)}")

        for denUnit1, denUnit2 in zip(denominator1, denominator2):
            p1, bu1 = analyzeUnit(denUnit1)
            p2, bu2 = analyzeUnit(denUnit2)

            different_p = p1 != p2
            different_bu = bu1 != bu2

            if different_p or different_bu: denominator = denominator*sympy.N(f"1e{prefixes_exponents[p1]*getExponent(bu1)}")
            if different_bu: denominator = base_unit_conversion[f"{bu1}-{bu2}"](denominator)
            if different_p or different_bu: denominator = denominator*sympy.N(f"1e{-prefixes_exponents[p2]*getExponent(bu2)}")

    else: pass
        # convert the original value to base composite units (which I choose for every quantity)
        # convert that to the new unit which is different in composition using the dictionary I will set up
        # there you go!

    return value/denominator

def replaceListItem(currentList: list, currentValue, newValue) -> list:
    newList = []

    for item in currentList:
        if item == currentValue:
            if newValue: newList.append(newValue)

        else: newList.append(item)

    return newList

def removeListItem(currentList: list, removedItem) -> list:
    newList = currentList.copy()
    newList.remove(removedItem)
    return newList

def removeAll(currentList: list, removedValue) -> list:
    newList = []

    for item in currentList:
        if item != removedValue:
            newList.append(item)

    return newList

def removeVectorExceptions(exceptions: list, quantity):
    result = exceptions.copy()
    for obj in quantity_vectorEquations[quantity]: result = removeAll(result, obj)

    return result

def evaluateNumber(number: sympy.Basic): return sympy.N(number, 8)

class Value:
    def __init__(self, quantity: str, value, unit: str, objects: list): #, prefix: str="", baseUnit: str=""):
        self.value: int|float|sympy.Basic = value
        self.quantity = quantity
        self.unit = unit
        self.objects = objects

    def change_unit(self, newUnit: str):
        if self.unit != newUnit:
            self.value = new_getNewValue(self.value, self.unit, newUnit)
            self.unit = newUnit

    def in_another_unit(self, newUnit: str):
        if self.unit != newUnit: return Value(self.quantity, new_getNewValue(self.value, self.unit, newUnit), newUnit, self.objects)
        return self
        
    def latex(self, evaluate: bool=True): 
        if "Direction" in self.quantity:
            if self.unit == "Degrees":
                result = sympy.latex(evaluateNumber(self.value)) + " \\degree"
            
            else:
                value_display: sympy.Basic = sympy.nsimplify(self.value)

                if value_display.has(sympy.asin, sympy.acos, sympy.atan, sympy.atan2):result = sympy.latex(evaluateNumber(self.value)) + " $ $rad"
                else: result = sympy.latex(sympy.nsimplify(self.value)) + " $ $rad"

            return result            
        else:    
            display_value = evaluateNumber(self.value) if evaluate else self.value
            
            return sympy.latex(display_value) + " " + re.sub("(.+)/(.+)", "\\\\frac{\\1}{\\2}", self.unit)
        
    def __repr__(self):
        return f"{self.quantity}, {self.value}, {self.unit}, {self.objects}"

def collectValues(givenValues: list[Value], desiredValues: list[list[str, str, list]], exceptions: list[str]=[]) -> tuple[list[Value], str, int, list[Value]]:
    foundValues: list[Value] = []
    additional_sol = ""
    steps = 0
    newValues: list[Value] = []

    # Experiment:
    # variable_number = 1

    for quantity, unit, objects in desiredValues:
        value = findValue(quantity, objects, givenValues+newValues)

        if (value is None) and ((find_value := eval(quantity.replace(" ", "_"))(givenValues+newValues, unit, objects, exceptions)) is not None):
            additional_sol += find_value[0] + "$\n\n$"
            value = find_value[1]
            steps += 1 + find_value[2]

            newValues.append(value)
            newValues.extend(find_value[3])

        # Experiment:
        # elif value is None: value = Value(quantity, sympy.Symbol(f"{quantitiy_symbol[quantity]}{variable_number}"), unit, objects)
        # variable_number += 1

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
        g[1] = sympy.sympify(g[1])
        g[3] = [obj.strip() for obj in g[3].split(",")]
        givenValues[index] = Value(*g)

    for index, r in enumerate(requiredValues):
        requiredValues[index] = {"quantity": r[0], "unit": r[1], f"objects": [obj.strip() for obj in r[2].split(",")]}

    listOfSolutions = []

    for value in requiredValues:
        requiredFunction: function = eval(value["quantity"].replace(" ", "_"))
        solution = requiredFunction(givenValues, value["unit"], value["objects"])
        if solution is None:
            listOfSolutions.append("\\text{Sorry, we couldn't find the " + value["quantity"] + " of " + ", ".join(value["objects"]) + ".}")

        else:
            listOfSolutions.append(solution[0])
            givenValues.append(solution[1])

    return re.sub("\\.0(\\D)", "\\1", "$\n\n$".join(listOfSolutions))

def Position_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "position components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects], ["Position Y Component", unit, objects]], exceptions=exceptions+["position components"])

        if x_component and y_component:
            result = Value("Position Magnitude", sympy.sqrt(sympy.Pow(x_component.value, 2) + sympy.Pow(y_component.value, 2)), x_component.unit, objects)

            sol += "r = \\sqrt{r_{x}^{2} + r_{y}^{2}} $\n$ r = \\sqrt{\\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2}} $\n$ r = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "r_x=rcos(theta)" not in exceptions:
        (x_component, direction), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects], ["Position Direction", "Degrees", objects]], exceptions=exceptions+["r_x=rcos(theta)"])

        if x_component and direction:
            radians = sympy.rad(direction.value)

            result = Value("Position Magnitude", x_component.value/sympy.cos(radians), unit, objects)

            sol += "r_{x} = r cos\\theta $\n$ " + x_component.latex() + " = r \\times cos\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + x_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.cos(radians))) + "} = r $\n$" + result.latex() + " = r"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "r_y=rsin(theta)" not in exceptions:
        (y_component, direction), sol, steps, newValues = collectValues(values, [["Position Y Component", unit, objects], ["Position Direction", "Degrees", objects]], exceptions=exceptions+["r_y=rsin(theta)"])

        if y_component and direction:
            radians = sympy.rad(direction.value)

            result = Value("Position Magnitude", y_component.value/sympy.sin(radians), unit, objects)

            sol += "r_{y} = r sin\\theta $\n$ " + y_component.latex() + " = r \\times sin\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + y_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.sin(radians))) + "} = r $\n$" + result.latex() + " = r"
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
            radians = sympy.atan2(y_component.value, x_component.value)
            degrees = sympy.deg(radians)

            result = Value("Position Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{r_{y}}{r_{x}} $\n$ tan\\left( \\theta \\right) = \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "r_x=rcos(theta)" not in exceptions:
        (x_component, magnitude), sol, steps, newValues = collectValues(values, [["Position X Component", "m", objects], ["Position Magnitude", "m", objects]], exceptions=exceptions+["r_x=rcos(theta)"])

        if x_component and magnitude:
            radians = sympy.acos(x_component.value/magnitude.value)
            degrees = sympy.deg(radians)

            result = Value("Position Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "r_{x} = r cos\\left( \\theta \\right) $\n$ " + x_component.latex() + " = " + magnitude.latex() + " \\times cos\\left( \\theta \\right) $\n$ \\frac{" + x_component.latex() + "}{" + magnitude.latex() + "} = cos\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "r_y=rsin(theta)" not in exceptions:
        (y_component, magnitude), sol, steps, newValues = collectValues(values, [["Position Y Component", "m", objects], ["Position Magnitude", "m", objects]], exceptions=exceptions+["r_y=rsin(theta)"])

        if y_component and magnitude:
            radians = sympy.asin(y_component.value/magnitude.value)
            degrees = sympy.deg(radians)

            result = Value("Position Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "r_{y} = r sin\\left( \\theta \\right) $\n$ " + y_component.latex() + " = " + magnitude.latex() + " \\times sin\\left( \\theta \\right) $\n$ \\frac{" + y_component.latex() + "}{" + magnitude.latex() + "} = sin\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
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

    if "r_x=rcos(theta)" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Position Magnitude", unit, objects], ["Position Direction", "Degrees", objects]], exceptions=exceptions+["r_x=rcos(theta)"])

        if magnitude and direction:
            radians = sympy.rad(direction.value)
            result = Value("Position X Component", magnitude.value*sympy.cos(radians), unit, objects)

            sol += "r_{x} = r cos\\left( \\theta \\right) $\n$ r_{x} = " + magnitude.latex() + " \\times cos\\left( " + direction.latex() + " \\right) $\n$ r_{x} = " + magnitude.latex() + " \\times " + sympy.latex(evaluateNumber(sympy.cos(radians))) + " $\n$ r_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=r_y/r_x" not in exceptions:
        (direction, y_component), sol, steps, newValues = collectValues(values, [["Position Direction", "Degrees", objects], ["Position Y Component", unit, objects]], exceptions=exceptions+["tan(theta)=r_y/r_x"])

        if direction and y_component:
            radians = sympy.rad(direction.value)
            result = Value("Position X Component", y_component.value/sympy.tan(radians), unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{r_{y}}{r_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{" + y_component.latex() + "}{r_{x}} $\n$ r_{x} = \\frac{" + y_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.tan(radians))) + "} $\n$ r_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "x_displacement" not in exceptions:
        if "Final" in objects:
            (displacement, initial_position), sol, steps, newValues = collectValues(values, [["Displacement X Component", unit, removeListItem(objects, "Final")], ["Position X Component", unit, replaceListItem(objects, "Final", "Initial")]], exceptions=removeVectorExceptions(exceptions, "Position X Component")+["x_displacement"])
            if displacement and initial_position:
                result = Value("Position X Component", displacement.value + initial_position.value, unit, objects)

                sol += "\\Delta r_{x} = r_{xf} - r_{xi} $\n$ " + displacement.latex() + " = r_{xf} - \\left(" + initial_position.latex() + "\\right) $\n$ " + displacement.latex() + " + \\left(" + initial_position.latex() + "\\right) = r_{xf} $\n$" + result.latex() + " = r_{xf}"
                steps += 1

                solutions.append((sol, result, steps, newValues))

        elif "Initial" in objects:
            (displacement, final_position), sol, steps, newValues = collectValues(values, [["Displacement X Component", unit, removeListItem(objects, "Initial")], ["Position X Component", unit, replaceListItem(objects, "Initial", "Final")]], exceptions=removeVectorExceptions(exceptions, "Position X Component")+["x_displacement"])

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

    if "r_y=rsin(theta)" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Position Magnitude", unit, objects], ["Position Direction", "Degrees", objects]], exceptions=exceptions+["r_y=rsin(theta)"])

        if magnitude and direction:
            radians = sympy.rad(direction.value)
            result = Value("Position X Component", magnitude.value*sympy.sin(radians), unit, objects)

            sol += "r_{y} = r sin\\left( \\theta \\right) $\n$ r_{y} = " + magnitude.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ r_{y} = " + magnitude.latex() + " \\times " + sympy.latex(evaluateNumber(sympy.sin(radians))) + " $\n$ r_{y} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=r_y/r_x" not in exceptions:
        (direction, x_component), sol, steps, newValues = collectValues(values, [["Position Direction", "Degrees", objects], ["Position X Component", unit, objects]], exceptions=exceptions+["tan(theta)=r_y/r_x"])

        if direction and x_component:
            radians = sympy.rad(direction.value)
            result = Value("Position Y Component", x_component.value*sympy.tan(radians), unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{r_{y}}{r_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{r_{y}{" + x_component.latex() + "}} $\n$ " + sympy.latex(sympy.tan(radians)) + " \\times " + x_component.latex() + " = r_{y} $\n$" + result.latex() + " = r_{y}"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "y_displacement" not in exceptions:
        if "Final" in objects:
            (displacement, initial_position), sol, steps, newValues = collectValues(values, [["Displacement Y Component", unit, removeListItem(objects, "Final")], ["Position Y Component", unit, replaceListItem(objects, "Final", "Initial")]], exceptions=removeVectorExceptions(exceptions, "Position Y Component")+["y_displacement"])

            if displacement and initial_position:
                result = Value("Position Y Component", displacement.value + initial_position.value, unit, objects)

                sol += "\\Delta r_{y} = r_{yf} - r_{yi} $\n$ " + displacement.latex() + " = r_{yf} - \\left(" + initial_position.latex() + "\\right) $\n$ " + displacement.latex() + " + \\left(" + initial_position.latex() + "\\right) = r_{yf} $\n$" + result.latex() + " = r_{yf}"
                steps += 1

                solutions.append((sol, result, steps, newValues))

        elif "Initial" in objects:
            (displacement, final_position), sol, steps, newValues = collectValues(values, [["Displacement Y Component", unit, removeListItem(objects, "Initial")], ["Position Y Component", unit, replaceListItem(objects, "Initial", "Final")]], exceptions=removeVectorExceptions(exceptions, "Position Y Component")+["y_displacement"])

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

    if "displacement components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Displacement X Component", unit, objects], ["Displacement Y Component", unit, objects]],exceptions=exceptions+["displacement components"])

        if x_component and y_component:
            result = Value("Displacement Magnitude", sympy.sqrt(sympy.Pow(x_component.value, 2) + sympy.Pow(y_component.value, 2)), x_component.unit, objects)

            sol += "\\Delta r = \\sqrt{\\Delta r_{x}^{2} + \\Delta r_{y}^{2}} $\n$ r = \\sqrt{\\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2}} $\n$ r = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "dr_x=drcos(theta)" not in exceptions:
        (x_component, direction), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects], ["Position Direction", "Degrees", objects]], exceptions=exceptions+["dr_x=drcos(theta)"])

        if x_component and direction:
            radians = sympy.rad(direction.value)

            result = Value("Displacement Magnitude", x_component.value/sympy.cos(radians), unit, objects)

            sol += "\\Delta r_{x} = \\Delta r cos\\theta $\n$ " + x_component.latex() + " = \\Delta r \\times cos\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + x_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.cos(radians))) + "} = \\Delta r $\n$" + result.latex() + " = \\Delta r"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "dr_y=drsin(theta)" not in exceptions:
        (y_component, direction), sol, steps, newValues = collectValues(values, [["Displacement Y Component", unit, objects], ["Displacement Direction", "Degrees", objects]], exceptions=exceptions+["dr_y=drsin(theta)"])

        if y_component and direction:
            radians = sympy.rad(direction.value)

            result = Value("Displacement Magnitude", y_component.value/sympy.sin(radians), unit, objects)

            sol += "\\Delta r_{y} = \\Delta r sin\\theta $\n$ " + y_component.latex() + " = \\Delta r \\times sin\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + y_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.sin(radians))) + "} = \\Delta r $\n$" + result.latex() + " = \\Delta r"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Displacement_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "tan(theta)=dr_y/dr_x" not in exceptions:
        (y_component, x_component), sol, steps, newValues = collectValues(values, [["Displacement Y Component", "m", objects], ["Displacement X Component", "m", objects]], exceptions=exceptions+["tan(theta)=dr_y/dr_x"])

        if y_component and x_component:
            radians = sympy.atan2(y_component.value, x_component.value)
            degrees = sympy.deg(radians)

            result = Value("Displacement Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{\\Delta r_{y}}{\\Delta r_{x}} $\n$ tan\\left( \\theta \\right) = \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "dr_x=drcos(theta)" not in exceptions:
        (x_component, magnitude), sol, steps, newValues = collectValues(values, [["Displacement X Component", "m", objects], ["Displacement Magnitude", "m", objects]], exceptions=exceptions+["dr_x=drcos(theta)"])

        if x_component and magnitude:
            radians = sympy.acos(x_component.value/magnitude.value)
            degrees = sympy.deg(radians)

            result = Value("Displacement Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "\\Delta r_{x} = \\Delta r cos\\left( \\theta \\right) $\n$ " + x_component.latex() + " = " + magnitude.latex() + " \\times cos\\left( \\theta \\right) $\n$ \\frac{" + x_component.latex() + "}{" + magnitude.latex() + "} = cos\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "dr_y=drsin(theta)" not in exceptions:
        (y_component, magnitude), sol, steps, newValues = collectValues(values, [["Displacement Y Component", "m", objects], ["Displacement Magnitude", "m", objects]], exceptions=exceptions+["dr_y=drsin(theta)"])

        if y_component and magnitude:
            radians = sympy.asin(y_component.value/magnitude.value)
            degrees = sympy.deg(radians)

            result = Value("Displacement Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "\\Delta r_{y} = \\Delta r sin\\left( \\theta \\right) $\n$ " + y_component.latex() + " = " + magnitude.latex() + " \\times sin\\left( \\theta \\right) $\n$ \\frac{" + y_component.latex() + "}{" + magnitude.latex() + "} = sin\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Displacement_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "dr_x=drcos(theta)" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Displacement Magnitude", unit, objects], ["Displacement Direction", "Degrees", objects]], exceptions=exceptions+["dr_x=drcos(theta)"])

        if magnitude and direction:
            radians = sympy.rad(direction.value)
            result = Value("Position X Component", magnitude.value*sympy.cos(radians), unit, objects)

            sol += "\\Delta r_{x} = \\Delta r cos\\left( \\theta \\right) $\n$ \\Delta r_{x} = " + magnitude.latex() + " \\times cos\\left( " + direction.latex() + " \\right) $\n$ \\Delta r_{x} = " + magnitude.latex() + " \\times " + sympy.latex(evaluateNumber(sympy.cos(radians))) + " $\n$ \\Delta r_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=dr_y/dr_x" not in exceptions:
        (direction, y_component), sol, steps, newValues = collectValues(values, [["Displacement Direction", "Degrees", objects], ["Displacement Y Component", unit, objects]], exceptions=removeVectorExceptions(exceptions, "Displacement X Component")+["tan(theta)=dr_y/dr_x"])

        if direction and y_component:
            radians = sympy.rad(direction.value)
            result = Value("Displacement X Component", y_component.value/sympy.tan(radians), unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{\\Delta r_{y}}{\\Delta r_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{" + y_component.latex() + "}{\\Delta r_{x}} $\n$ \\Delta r_{x} = \\frac{" + y_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.tan(radians))) + "} $\n$ \\Delta r_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "x_displacement" not in exceptions:
        (final_position, initial_position), sol, steps, newValues = collectValues(values, [["Position X Component", unit, objects+["Final"]], ["Position X Component", unit, objects+["Initial"]]], exceptions=removeVectorExceptions(exceptions, "Displacement X Component")+["x_displacement"])

        if final_position and initial_position:
            result = Value("Displacement X Component", final_position.value - initial_position.value, unit, objects)

            sol += "\\Delta r_{x} = r_{xf} - r_{xi} $\n$ \\Delta r_{x} = " + final_position.latex() + " - \\left(" + initial_position.latex() + "\\right) $\n$ \\Delta r_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "x_average_velocity" not in exceptions:
        (velocity, time), sol, steps, newValues = collectValues(values, [["Velocity X Component", unit+"/s", objects+["Average"]], ["Time", "s", objects]], exceptions=removeVectorExceptions(exceptions, "Displacement X Component")+["x_average_velocity"])

        if velocity and time:
            result = Value("Displacement X Component", velocity.value*time.value, unit, objects)

            sol += "v_{avg_{x}} = \\frac{\\Delta r_{x}}{\\Delta t} $\n$ " + velocity.latex() + " = \\frac{\\Delta r_{x}}{" + time.latex() + "} $\n$ " + velocity.latex() + " \\times " + time.latex() + " = \\Delta r_{x} $\n$ " + result.latex() + " = \\Delta r_{x}"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "x:dr=v_i*t+1/2at^2" not in exceptions:
        (velocity, time, acceleration), sol, steps, newValues = collectValues(values, [["Velocity X Component", "m/s", objects+["Initial"]], ["Time", "s", objects], ["Acceleration X Component", "m/s²", objects]], exceptions=removeVectorExceptions(exceptions, "Displacement X Component")+["x:dr=v_i*t+1/2at^2"])

        if velocity and time and acceleration:
            result = Value("Displacement X Component", velocity.value*time.value + acceleration.value*sympy.Pow(time.value, 2)/2, "m", objects)

            sol += "\\Delta r_{x} = v_{ix}\\Delta t + \\frac{1}{2}a_{x}\\Delta t^{2} $\n$ \\Delta r_{x} = " + velocity.latex() + "\\times " + time.latex() + " + \\frac{1}{2} \\times " + acceleration.latex() + " \\times \\left(" + time.latex() + "\\right)^{2}$\n$ \\Delta r_{x} = " + result.latex()
            steps += 1

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$ \\Delta r_{x} = " + result.latex()

            solutions.append((sol, result, steps, newValues))

    if "x:v_f^2 = v_i^2 + 2adr" not in exceptions:
        (final_velocity, initial_velocity, acceleration), sol, steps, newValues = collectValues(values, [["Velocity X Component", "m/s", objects+["Final"]], ["Velocity X Component", "m/s", objects+["Initial"]], ["Acceleration X Component", "m/s²", objects]], exceptions=removeVectorExceptions(exceptions, "Displacement X Component")+["x:v_f^2 = v_i^2 + 2adr"])

        if final_velocity and initial_velocity and acceleration:
            result = Value("Displacement X Component", (sympy.Pow(final_velocity.value, 2) - sympy.Pow(initial_velocity.value, 2))/(2*acceleration.value), "m", objects)

            sol += "v_{fx}^{2} = v_{ix}^{2} + 2a_{x}\\Delta r_{x} $\n$ \\left( " + final_velocity.latex() + " \\right)^{2} = \\left( " + initial_velocity.latex() + " \\right)^{2} + 2 \\times " + acceleration.latex() + " \\times \\Delta r_{x} $\n$ " + sympy.latex(evaluateNumber(sympy.Pow(final_velocity.value, 2))) + "\\frac{m^{2}}{s^{2}} - " + sympy.latex(evaluateNumber(sympy.Pow(initial_velocity.value, 2))) + "\\frac{m^{2}}{s^{2}} = " + sympy.latex(evaluateNumber(2 * acceleration.value)) + "\\frac{m}{s^{2}} \\times \\Delta r_{x} $\n$ \\frac{" + sympy.latex(evaluateNumber(sympy.Pow(final_velocity.value, 2) - sympy.Pow(initial_velocity.value, 2))) + "\\frac{m^{2}}{s^{2}}}{" + sympy.latex(evaluateNumber(2 * acceleration.value)) + " \\frac{m}{s^{2}}} = \\Delta r_{x} $\n$ " + result.latex() + " = \\Delta r_{x}"
            steps += 1

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.latex() + " = \\Delta r_{x}"

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Displacement_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "dr_y=drsin(theta)":
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Displacement Magnitude", unit, objects], ["Displacement Direction", "Degrees", objects]], exceptions=exceptions+["dr_y=drsin(theta)"])

        if magnitude and direction:
            radians = sympy.rad(direction.value)
            result = Value("Displacement Y Component", magnitude.value*sympy.sin(radians))

            sol += "\\Delta r_{y} = \\Delta r sin\\left( \\theta \\right) $\n$ \\Delta r_{y} = " + magnitude.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ \\Delta r_{y} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=dr_y/dr_x" not in exceptions:
        (direction, x_component), sol, steps, newValues = collectValues(values, [["Displacement Direction", "Degrees", objects], ["Displacement Y Component", unit, objects]], exceptions=exceptions+["tan(theta)=dr_y/dr_x"])

        if direction and x_component:
            radians = sympy.rad(direction.value)
            result = Value("Displacement Y Component", x_component.value*sympy.tan(radians), objects)

            sol += "tan\\left( \\theta \\right) = \\frac{\\Delta r_{y}}{\\Delta r_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{\\Delta r_{y}{" + x_component.latex() + "}} $\n$ " + sympy.latex(sympy.tan(radians)) + " \\times " + x_component.latex() + " = \\Delta r_{y} $\n$" + result.latex() + " = \\Delta r_{y}"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "y_displacement" not in exceptions:
        (final_position, initial_position), sol, steps, newValues = collectValues(values, [["Position Y Component", unit, objects+["Final"]], ["Position Y Component", unit, objects+["Initial"]]], exceptions=removeVectorExceptions(exceptions, "Displacement Y Component")+["y_displacement"])

        if final_position and initial_position:
            result = Value("Displacement Y Component", final_position.value - initial_position.value, unit, objects)

            sol += "\\Delta r_{y} = r_{yf} - r_{yi} $\n$ \\Delta r_{y} = " + final_position.latex() + " - \\left(" + initial_position.latex() + "\\right) $\n$ \\Delta r_{y} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "y_average_velocity" not in exceptions:
        (velocity, time), sol, steps, newValues = collectValues(values, [["Velocity Y Component", "m/s", objects+["Average"]], ["Time", "s", objects]], exceptions=removeVectorExceptions(exceptions, "Displacement Y Component")+["y_average_velocity"])

        if velocity and time:
            result = Value("Displacement Y Component", velocity.value*time.value, "m", objects)

            sol += "v_{avg_{y}} = \\frac{\\Delta r_{y}}{\\Delta t} $\n$ " + velocity.latex() + " = \\frac{\\Delta r_{y}}{" + time.latex() + "} $\n$ " + velocity.latex() + " \\times " + time.latex() + " = \\Delta r_{y} $\n$ " + result.latex() + " = \\Delta r_{y}"
            steps += 1

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$ \\Delta r_{y} = " + result.latex()

            solutions.append((sol, result, steps, newValues))

    if "y:dr=v_i*t+1/2at^2" not in exceptions:
        (velocity, time, acceleration), sol, steps, newValues = collectValues(values, [["Velocity Y Component", "m/s", objects+["Initial"]], ["Time", "s", objects], ["Acceleration Y Component", "m/s²", objects]], exceptions=removeVectorExceptions(exceptions, "Displacement Y Component")+["y:dr=v_i*t+1/2at^2"])

        if velocity and time and acceleration:
            result = Value("Displacement Y Component", velocity.value*time.value + acceleration.value*sympy.Pow(time.value, 2)/2, "m", objects)

            sol += "\\Delta r_{y} = v_{iy}\\Delta t + \\frac{1}{2}a_{y}\\Delta t^{2} $\n$ \\Delta r_{y} = " + velocity.latex() + "\\times " + time.latex() + " + \\frac{1}{2} \\times " + acceleration.latex() + " \\times \\left(" + time.latex() + "\\right)^{2}$\n$ \\Delta r_{y} = " + result.latex()
            steps += 1

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$ \\Delta r_{y} = " + result.latex()

            solutions.append((sol, result, steps, newValues))

    if "y:v_f^2 = v_i^2 + 2adr" not in exceptions:
        (final_velocity, initial_velocity, acceleration), sol, steps, newValues = collectValues(values, [["Velocity Y Component", "m/s", objects+["Final"]], ["Velocity Y Component", "m/s", objects+["Initial"]], ["Acceleration Y Component", "m/s²", objects]], exceptions=removeVectorExceptions(exceptions, "Displacement Y Component")+["y:v_f^2 = v_i^2 + 2adr"])

        if final_velocity and initial_velocity and acceleration:
            result = Value("Displacement Y Component", (sympy.Pow(final_velocity.value, 2) - sympy.Pow(initial_velocity.value, 2))/(2*acceleration.value), "m", objects)

            sol += "v_{fy}^{2} = v_{iy}^{2} + 2a_{y}\\Delta r_{y} $\n$ \\left( " + final_velocity.latex() + " \\right)^{2} = \\left( " + initial_velocity.latex() + " \\right)^{2} + 2 \\times " + acceleration.latex() + " \\times \\Delta r_{y} $\n$ " + sympy.latex(evaluateNumber(sympy.Pow(final_velocity.value, 2))) + "\\frac{m^{2}}{s^{2}} - " + sympy.latex(evaluateNumber(sympy.Pow(initial_velocity.value, 2))) + "\\frac{m^{2}}{s^{2}} = " + sympy.latex(evaluateNumber(2 * acceleration.value)) + "\\frac{m}{s^{2}} \\times \\Delta r_{y} $\n$ \\frac{" + sympy.latex(evaluateNumber(sympy.Pow(final_velocity.value, 2) - sympy.Pow(initial_velocity.value, 2))) + "\\frac{m^{2}}{s^{2}}}{" + sympy.latex(evaluateNumber(2 * acceleration.value)) + " \\frac{m}{s^{2}}} = \\Delta r_{y} $\n$ " + result.latex() + " = \\Delta r_{y}"
            steps += 1

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.latex() + " = \\Delta r_{y}"

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Distance(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    # if "average speed" not in exceptions:
    #     (speed, time), sol, steps, newValues = collectValues(values, [["Speed", "m/s", objects+["Average"]], ["Time", "s", objects]], exceptions=exceptions+["average speed"])

    #     if speed and time:
    #         result = Value("Distance", speed.value*time.value, "m", objects)
            
    #         sol += "v_{s,avg} = \\frac{d}{\\Delta t} $\n$ " + speed.latex() + " = \\frac{d}{" + time.latex() + "} $\n$ " + speed.latex() + " \\times " + time.latex() + " = d $\n$ " + result.latex() + " = d"
    #         steps += 1

    #         if result.unit != unit:
    #             result.change_unit(unit)
    #             sol += "$\n$ " + result.latex() + " = d"

    #         solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Time(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    # if "average speed" not in exceptions:
    #     (speed, distance), sol, steps, newValues = collectValues(values, [["Speed", "m/s", objects+["Average"]], ["Distance", "m", objects]], exceptions=exceptions)

    #     if speed and distance:
    #         result = Value("Time", distance.value/speed.value, "s", objects)

    #         sol += "v_{s, avg} = \\frac{d}{\\Delta t} $\n$ " + speed.latex() + " = \\frac{" + distance.latex() + "}{\\Delta t} $\n$ \\Delta t = \\frac{" + distance.latex() + "}{" + speed.latex() + "} $\n$"
    #         steps += 1

    #         if result.unit != unit:
    #             result.change_unit(unit)
    #             sol += "$\n$ \\Delta t = " + result.latex()

    #         solutions.append((sol, result, steps, newValues))

    # if "x_average_velocity" not in exceptions:
    #     (velocity, displacement), sol, steps, newValues = collectValues(values, [["Velocity X Component", "m/s", objects+["Average"]], ["Displacement X Component", "m", objects]], exceptions=exceptions+["x_average_velocity"])

    #     if velocity and displacement:
    #         result = Value("Time", displacement.value/velocity.value, "s", objects)

    #         sol += "v_{avg, x} = \\frac{\\Delta r_{x}}{\\Delta t} $\n$" + velocity.latex() + " = \\frac{" + displacement.latex() + "}{\\Delta t} $\n$ \\Delta t = \\frac{" + displacement.latex() + "}{" + velocity.latex() + "} $\n$ \\Delta t = " + result.latex()
    #         steps += 1

    #         if result.unit != unit:
    #             result.change_unit(unit)
    #             sol += "$\n$ \\Delta t = " + result.latex()

    #         solutions.append((sol, result, steps, newValues))

    # if "y_average_velocity" not in exceptions:
    #     (velocity, displacement), sol, steps, newValues = collectValues(values, [["Velocity Y Component", "m/s", objects+["Average"]], ["Displacement Y Component", "m", objects]], exceptions=exceptions+["y_average_velocity"])

    #     if velocity and displacement:
    #         result = Value("Time", displacement.value/velocity.value, "s", objects)

    #         sol += "v_{avg, y} = \\frac{\\Delta r_{y}}{\\Delta t} $\n$" + velocity.latex() + " = \\frac{" + displacement.latex() + "}{\\Delta t} $\n$ \\Delta t = \\frac{" + displacement.latex() + "}{" + velocity.latex() + "} $\n$ \\Delta t = " + result.latex()
    #         steps += 1

    #         if result.unit != unit:
    #             result.change_unit(unit)
    #             sol += "$\n$ \\Delta t = " + result.latex()

    #         solutions.append((sol, result, steps, newValues))

    # if "x_acceleration" not in exceptions:
    #     (acceleration, final_velocity, initial_velocity), sol, steps, newValues = collectValues(values, [["Velocity X Component", "m/s", objects+["Final"]], ["Velocity X Component", "m/s", objects+["Initial"]], ["Acceleration X Component", "m/s²", objects]], exceptions=exceptions+["x_acceleration"])

    #     if acceleration and final_velocity and initial_velocity:
    #         result = Value("Time", (final_velocity.value - initial_velocity.value)/acceleration.value, "s", objects)

    #         sol += "v_{fx} = v_{ix} + a_{x}\\Delta t $\n$ " + final_velocity.latex() + " = " + initial_velocity.latex() + " + " + acceleration.latex() + " \\times \\Delta t $\n$ " + final_velocity.latex() + " - " + initial_velocity.latex() + " = " + acceleration.latex() + " \\times \\Delta t $\n$ \\frac{" + sympy.latex(evaluateNumber(final_velocity.value - initial_velocity.value)) + " \\frac{m}{s}}{" + acceleration.latex() + "} $\n$ \\Delta t = " + result.latex()
    #         steps += 1

    #         if result.unit != unit:
    #             result.change_unit(unit)
    #             sol += "$\n$ \\Delta t = " + result.latex()

    #         solutions.append((sol, result, steps, newValues))

    # if "y_acceleration" not in exceptions:
    #     (final_velocity, initial_velocity, acceleration), sol, steps, newValues = collectValues(values, [["Velocity Y Component", "m/s", objects+["Final"]], ["Velocity Y Component", "m/s", objects+["Initial"]], ["Acceleration Y Component", "m/s²", objects]], exceptions=exceptions+["y_acceleration"])

    #     if acceleration and final_velocity and initial_velocity:
    #         result = Value("Time", (final_velocity.value - initial_velocity.value)/acceleration.value, "s", objects)

    #         sol += "v_{fy} = v_{iy} + a_{y}\\Delta t $\n$ " + final_velocity.latex() + " = " + initial_velocity.latex() + " + " + acceleration.latex() + " \\times \\Delta t $\n$ " + final_velocity.latex() + " - " + initial_velocity.latex() + " = " + acceleration.latex() + " \\times \\Delta t $\n$ \\frac{" + sympy.latex(evaluateNumber(final_velocity.value - initial_velocity.value)) + " \\frac{m}{s}}{" + acceleration.latex() + "} $\n$ \\Delta t = " + result.latex()
    #         steps += 1

    #         if result.unit != unit:
    #             result.change_unit(unit)
    #             sol += "$\n$ \\Delta t = " + result.latex()

    #         solutions.append((sol, result, steps, newValues))

    # if "@:dr=v_i*t+1/2a*t^2" not in exceptions:
    #     (displacement, initial_velocity, acceleration), sol, steps, newValues = collectValues(values, [["Displacement @ Component", "m", objects], ["Velocity @ Component", "m/s", objects+["Initial"]], ["Acceleration @ Component", "m/s²", objects]], exceptions+["@:dr=v_It+1/2at^2"])

    #     if displacement and initial_velocity and acceleration:
    #         if initial_velocity.value == 0:
    #             pass

    #         elif acceleration.value == 0:
    #             pass

    #         else:
    #             t = sympy.Symbol("\\Delta t", real=True, positive=True)
    #             equation = sympy.Eq(displacement.value, initial_velocity.value*t + sympy.Rational(1,2) * acceleration.value * sympy.Pow(t, 2))
    #             solution_set = sympy.solve(equation)

    #             if solution_set:
    #                 result = Value("Time", solution_set[0], "s", objects)

    #                 sol += ""
    #                 steps += 1

    #                 solutions.append((sol, result, steps, newValues))

    # if "@:dr=v_i*t+1/2a*t^2" not in exceptions:
    #     (displacement, initial_velocity, acceleration), sol, steps, newValues = collectValues(values, [["Displacement @ Component", "m", objects], ["Velocity @ Component", "m/s", objects+["Initial"]], ["Acceleration @ Component", "m/s²", objects]], exceptions+["@:dr=v_It+1/2at^2"])

    #     if displacement and initial_velocity and acceleration:
    #         if initial_velocity.value == 0:
    #             pass

    #         elif acceleration.value == 0:
    #             pass

    #         else:
    #             t = sympy.Symbol("\\Delta t", real=True, positive=True)
    #             equation = sympy.Eq(displacement.value, initial_velocity.value*t + sympy.Rational(1,2) * acceleration.value * sympy.Pow(t, 2))
    #             ss = sympy.solve(equation)

    #             if ss:
    #                 result = Value("Time", ss[0], "s", objects)

    #                 sol += ""
    #                 steps += 1

    #                 solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "velocity components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Velocity X Component", unit, objects], ["Velocity Y Component", unit, objects]], exceptions=exceptions+["velocity components"])

        if x_component and y_component:
            result = Value("Velocity Magnitude", sympy.sqrt(sympy.Pow(x_component.value, 2) + sympy.Pow(y_component.value, 2)), x_component.unit, objects)

            sol += "v = \\sqrt{v_{x}^{2} + v_{y}^{2}} $\n$ v = \\sqrt{\\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2}} $\n$ v = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "v_x=vcos(theta)" not in exceptions:
        (x_component, direction), sol, steps, newValues = collectValues(values, [["Velocity X Component", unit, objects], ["Velocity Direction", "Degrees", objects]], exceptions=exceptions+["v_x=vcos(theta)"])

        if x_component and direction:
            radians = sympy.rad(direction.value)

            result = Value("Velocity Magnitude", x_component.value/sympy.cos(radians), unit, objects)

            sol += "v_{x} = v cos\\theta $\n$ " + x_component.latex() + " = v \\times cos\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + x_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.cos(radians))) + "} = v $\n$" + result.latex() + " = v"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "v_y=vsin(theta)" not in exceptions:
        (y_component, direction), sol, steps, newValues = collectValues(values, [["Velocity Y Component", unit, objects], ["Velocity Direction", "Degrees", objects]], exceptions=exceptions+["v_y=vsin(theta)"])

        if y_component and direction:
            radians = sympy.rad(direction.value)

            result = Value("Velocity Magnitude", y_component.value/sympy.sin(radians), unit, objects)

            sol += "v_{y} = v sin\\theta $\n$ " + y_component.latex() + " = v \\times sin\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + y_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.sin(radians))) + "} = v $\n$" + result.latex() + " = v"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "tan(theta)=v_y/v_x" not in exceptions:
        (y_component, x_component), sol, steps, newValues = collectValues(values, [["Velocity Y Component", unit, objects], ["Velocity X Component", unit, objects]], exceptions=exceptions+["tan(theta)=v_y/v_x"])

        if y_component and x_component:
            radians = sympy.atan2(y_component.value, x_component.value)
            degrees = sympy.deg(radians)

            result = Value("Velocity Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{v_{y}}{v_{x}} $\n$ tan\\left( \\theta \\right) = \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "v_x=vcos(theta)" not in exceptions:
        (x_component, magnitude), sol, steps, newValues = collectValues(values, [["Velocity X Component", unit, objects], ["Velocity Magnitude", unit, objects]], exceptions=exceptions+["v_x=vcos(theta)"])

        if x_component and magnitude:
            radians = sympy.acos(x_component.value/magnitude.value)
            degrees = sympy.deg(radians)

            result = Value("Velocity Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "v_{x} = v cos\\left( \\theta \\right) $\n$ " + x_component.latex() + " = " + magnitude.latex() + " \\times cos\\left( \\theta \\right) $\n$ \\frac{" + x_component.latex() + "}{" + magnitude.latex() + "} = cos\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "v_y=vsin(theta)" not in exceptions:
        (y_component, magnitude), sol, steps, newValues = collectValues(values, [["Velocity Y Component", unit, objects], ["Velocity Magnitude", unit, objects]], exceptions=exceptions+["v_y=vsin(theta)"])

        if y_component and magnitude:
            radians = sympy.asin(y_component.value/magnitude.value)
            degrees = sympy.deg(radians)

            result = Value("Velocity Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "v_{y} = v sin\\left( \\theta \\right) $\n$ " + y_component.latex() + " = " + magnitude.latex() + " \\times sin\\left( \\theta \\right) $\n$ \\frac{" + y_component.latex() + "}{" + magnitude.latex() + "} = sin\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "v_x=vcos(theta)" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Velocity Magnitude", unit, objects], ["Velocity Direction", "Degrees", objects]], exceptions=exceptions+["v_x=vcos(theta)"])

        if magnitude and direction:
            radians = sympy.rad(direction.value)
            result = Value("Velocity X Component", magnitude.value*sympy.cos(radians), unit, objects)

            sol += "v_{x} = v cos\\left( \\theta \\right) $\n$ v_{x} = " + magnitude.latex() + " \\times cos\\left( " + direction.latex() + " \\right) $\n$ v_{x} = " + magnitude.latex() + " \\times " + sympy.latex(evaluateNumber(sympy.cos(radians))) + " $\n$ v_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=v_y/v_x" not in exceptions:
        (direction, y_component), sol, steps, newValues = collectValues(values, [["Velocity Direction", "Degrees", objects], ["Velocity Y Component", unit, objects]], exceptions=exceptions+["tan(theta)=v_y/v_x"])

        if direction and y_component:
            radians = sympy.rad(direction.value)
            result = Value("Velocity X Component", y_component.value/sympy.tan(radians), unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{v_{y}}{v_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{" + y_component.latex() + "}{v_{x}} $\n$ v_{x} = \\frac{" + y_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.tan(radians))) + "} $\n$ v_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Velocity_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "v_y=vsin(theta)" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Velocity Magnitude", unit, objects], ["Velocity Direction", "Degrees", objects]], exceptions=exceptions+["v_y=vsin(theta)"])

        if magnitude and direction:
            radians = sympy.rad(direction.value)
            result = Value("Velocity X Component", magnitude.value*sympy.sin(radians), unit, objects)

            sol += "v_{y} = v sin\\left( \\theta \\right) $\n$ v_{y} = " + magnitude.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ v_{y} = " + magnitude.latex() + " \\times " + sympy.latex(evaluateNumber(sympy.sin(radians))) + " $\n$ v_{y} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=v_y/v_x" not in exceptions:
        (direction, x_component), sol, steps, newValues = collectValues(values, [["Velocity Direction", "Degrees", objects], ["Velocity X Component", unit, objects]], exceptions=exceptions+["tan(theta)=v_y/v_x"])

        if direction and x_component:
            radians = sympy.rad(direction.value)
            result = Value("Velocity Y Component", x_component.value*sympy.tan(radians), unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{v_{y}}{v_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{v_{y}{" + x_component.latex() + "}} $\n$ " + sympy.latex(sympy.tan(radians)) + " \\times " + x_component.latex() + " = v_{y} $\n$" + result.latex() + " = v_{y}"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Speed(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    # if "average speed" not in exceptions and "Average" in objects:
    #     (distance, time), sol, steps, newValues = collectValues(values, [["Distance", unit.split("/")[0], objects], ["Time", unit.split("/")[1], objects]], exceptions=exceptions)

    #     if distance and time:
    #         result = Value("Distance", distance.value/time.value, unit, objects)
            
    #         sol += "v_{s,avg} = \\frac{d}{\\Delta t} $\n$ v_{s, avg} = \\frac{" + distance.latex() + "}{" + time.latex() + "} $\n$ v_{s, avg} = " + result.latex()
    #         steps += 1

    #         solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_Magnitude(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "acceleration components" not in exceptions:
        (x_component, y_component), sol, steps, newValues = collectValues(values, [["Acceleration X Component", unit, objects], ["Acceleration Y Component", unit, objects]], exceptions=exceptions+["acceleration components"])

        if x_component and y_component:
            result = Value("Acceleration Magnitude", sympy.sqrt(sympy.Pow(x_component.value, 2) + sympy.Pow(y_component.value, 2)), x_component.unit, objects)

            sol += "a = \\sqrt{a_{x}^{2} + a_{y}^{2}} $\n$ a = \\sqrt{\\left( " + x_component.latex() + " \\right)^{2} + \\left( " + y_component.latex() + " \\right)^{2}} $\n$ a = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "a_x=acos(theta)" not in exceptions:
        (x_component, direction), sol, steps, newValues = collectValues(values, [["Acceleration X Component", unit, objects], ["Acceleration Direction", "Degrees", objects]], exceptions=exceptions+["a_x=acos(theta)"])

        if x_component and direction:
            radians = sympy.rad(direction.value)

            result = Value("Acceleration Magnitude", x_component.value/sympy.cos(radians), unit, objects)

            sol += "a_{x} = a cos\\theta $\n$ " + x_component.latex() + " = a \\times cos\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + x_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.cos(radians))) + "} = a $\n$" + result.latex() + " = a"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "a_y=asin(theta)" not in exceptions:
        (y_component, direction), sol, steps, newValues = collectValues(values, [["Acceleration Y Component", unit, objects], ["Acceleration Direction", "Degrees", objects]], exceptions=exceptions+["a_y=asin(theta)"])

        if y_component and direction:
            radians = sympy.rad(direction.value)

            result = Value("Acceleration Magnitude", y_component.value/sympy.sin(radians), unit, objects)

            sol += "a_{y} = a sin\\theta $\n$ " + y_component.latex() + " = a \\times sin\\left( " + direction.latex() + " \\right) $\n$ \\frac{" + y_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.sin(radians))) + "} = a $\n$" + result.latex() + " = a"
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_Direction(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "tan(theta)=a_y/a_x" not in exceptions:
        (y_component, x_component), sol, steps, newValues = collectValues(values, [["Acceleration Y Component", unit, objects], ["Acceleration X Component", unit, objects]], exceptions=exceptions+["tan(theta)=a_y/a_x"])

        if y_component and x_component:
            radians = sympy.atan2(y_component.value, x_component.value)
            degrees = sympy.deg(radians)

            result = Value("Acceleration Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{a_{y}}{a_{x}} $\n$ tan\\left( \\theta \\right) = \\frac{" + y_component.latex() + "}{" + x_component.latex() + "} $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "a_x=acos(theta)" not in exceptions:
        (x_component, magnitude), sol, steps, newValues = collectValues(values, [["Acceleration X Component", unit, objects], ["Acceleration Magnitude", unit, objects]], exceptions=exceptions+["a_x=acos(theta)"])

        if x_component and magnitude:
            radians = sympy.acos(x_component.value/magnitude.value)
            degrees = sympy.deg(radians)

            result = Value("Acceleration Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "a_{x} = a cos\\left( \\theta \\right) $\n$ " + x_component.latex() + " = " + magnitude.latex() + " \\times cos\\left( \\theta \\right) $\n$ \\frac{" + x_component.latex() + "}{" + magnitude.latex() + "} = cos\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "a_y=asin(theta)" not in exceptions:
        (y_component, magnitude), sol, steps, newValues = collectValues(values, [["Acceleration Y Component", unit, objects], ["Acceleration Magnitude", unit, objects]], exceptions=exceptions+["a_y=asin(theta)"])

        if y_component and magnitude:
            radians = sympy.asin(y_component.value/magnitude.value)
            degrees = sympy.deg(radians)

            result = Value("Acceleration Direction", degrees if unit == "Degrees" else radians, unit, objects)

            sol += "a_{y} = a sin\\left( \\theta \\right) $\n$ " + y_component.latex() + " = " + magnitude.latex() + " \\times sin\\left( \\theta \\right) $\n$ \\frac{" + y_component.latex() + "}{" + magnitude.latex() + "} = sin\\left( \\theta \\right) $\n$ \\therefore \\theta = " + result.latex()
            steps += 1

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_X_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "a_x=acos(theta)" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Acceleration Magnitude", unit, objects], ["Acceleration Direction", "Degrees", objects]], exceptions=exceptions+["a_x=acos(theta)"])

        if magnitude and direction:
            radians = sympy.rad(direction.value)
            result = Value("Acceleration X Component", magnitude.value*sympy.cos(radians), unit, objects)

            sol += "a_{x} = a cos\\left( \\theta \\right) $\n$ a_{x} = " + magnitude.latex() + " \\times cos\\left( " + direction.latex() + " \\right) $\n$ a_{x} = " + magnitude.latex() + " \\times " + sympy.latex(evaluateNumber(sympy.cos(radians))) + " $\n$ a_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=a_y/a_x" not in exceptions:
        (direction, y_component), sol, steps, newValues = collectValues(values, [["Acceleration Direction", "Degrees", objects], ["Acceleration Y Component", unit, objects]], exceptions=exceptions+["tan(theta)=a_y/a_x"])

        if direction and y_component:
            radians = sympy.rad(direction.value)
            result = Value("Acceleration X Component", y_component.value/sympy.tan(radians), unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{a_{y}}{a_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{" + y_component.latex() + "}{a_{x}} $\n$ a_{x} = \\frac{" + y_component.latex() + "}{" + sympy.latex(evaluateNumber(sympy.tan(radians))) + "} $\n$ a_{x} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0]

    else:
        return min(solutions, key=lambda x: x[2])

def Acceleration_Y_Component(values: list[Value], unit: str, objects: list[str], exceptions: list[str]=[]) -> tuple[str, Value, int, list[Value]]:
    solutions = []

    if "a_y=asin(theta)" not in exceptions:
        (magnitude, direction), sol, steps, newValues = collectValues(values, [["Acceleration Magnitude", unit, objects], ["Acceleration Direction", "Degrees", objects]], exceptions=exceptions+["a_y=asin(theta)"])

        if magnitude and direction:
            radians = sympy.rad(direction.value)
            result = Value("Acceleration X Component", magnitude.value*sympy.sin(radians), unit, objects)

            sol += "a_{y} = a sin\\left( \\theta \\right) $\n$ a_{y} = " + magnitude.latex() + " \\times sin\\left( " + direction.latex() + " \\right) $\n$ a_{y} = " + magnitude.latex() + " \\times " + sympy.latex(evaluateNumber(sympy.sin(radians))) + " $\n$ a_{y} = " + result.latex()
            steps += 1

            solutions.append((sol, result, steps, newValues))

    if "tan(theta)=a_y/a_x" not in exceptions:
        (direction, x_component), sol, steps, newValues = collectValues(values, [["Acceleration Direction", "Degrees", objects], ["Acceleration X Component", unit, objects]], exceptions=exceptions+["tan(theta)=a_y/a_x"])

        if direction and x_component:
            radians = sympy.rad(direction.value)
            result = Value("Acceleration Y Component", x_component.value*sympy.tan(radians), unit, objects)

            sol += "tan\\left( \\theta \\right) = \\frac{a_{y}}{a_{x}} $\n$ tan\\left( " + direction.latex() + " \\right) = \\frac{a_{y}{" + x_component.latex() + "}} $\n$ " + sympy.latex(sympy.tan(radians)) + " \\times " + x_component.latex() + " = a_{y} $\n$" + result.latex() + " = a_{y}"
            steps += 1

            solutions.append((sol, result, steps, newValues))

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
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
    plt.rcParams["mathtext.default"] = "regular"
    plt.rcParams["mathtext.fontset"] = "stix"

    problems = [
        # [
        #     [['Position X Component', '-25', 'm', 'Box'], ['Position Direction', '2*pi/3', 'Radians', 'Box']],
        #     [['Position Magnitude', 'm', 'Box'], ['Position Y Component', 'm', 'Box']]
        # ],
        # [
        #     [['Position X Component', '3', 'm', 'Ball'], ['Position Y Component', '4', 'm', 'Ball']],
        #     [['Position Magnitude', 'm', 'Ball'], ['Position Direction', 'Degrees', 'Ball']]
        # ],
        # [
        #     [['Position X Component', '3', 'm', 'Ball'], ['Position Magnitude', '5', 'm', 'Ball']],
        #     [['Position Direction', 'Degrees', 'Ball'], ['Position Y Component', 'm', 'Ball']]
        # ],
        # [
        #     [['Position Y Component', '4', 'm', 'Ball'], ['Position Magnitude', '5', 'm', 'Ball']],
        #     [['Position Direction', 'Degrees', 'Ball'], ['Position X Component', 'm', 'Ball']]
        # ],
        # [
        #     [['Position Y Component', '3', 'm', 'Ball'], ['Position Direction', '30', 'Degrees', 'Ball']],
        #     [['Position Magnitude', 'm', 'Ball'], ['Position X Component', 'm', 'Ball']]
        # ],
        # [
        #     [['Position Magnitude', '5', 'm', 'Ball, Final'], ['Position Direction', 'deg(atan2(4,3))', 'Degrees', 'Ball, Final'], ['Displacement X Component', '16', "m", "Ball"], ["Displacement Y Component", '0', 'm', "Ball"]],
        #     [['Position Magnitude', 'm', 'Ball, Initial']]
        # ],
        # [
        #     [["Position X Component", 5, "m", "Ball, Initial"], ["Position X Component", 10, "m", "Ball, Final"]],
        #     [["Displacement X Component", "m", "Ball"]]
        # ],
        # [
        #     [["Velocity X Component", 5, "m/s", "Ball, Average"], ["Time", 10, "s", "Ball"]],
        #     [["Displacement X Component", "m", "Ball"]]
        # ],
        [
            [["Velocity X Component", 5, "m/s", "Ball, Initial"], ["Time", 10, "s", "Ball"], ["Acceleration X Component", 2, "m/s²", "Ball"]],
            [["Displacement X Component", "m", "Ball"]]
        ],
        # [
        #     [["Velocity X Component", 5, "m/s", "Ball, Initial"], ["Velocity X Component", -20, "m/s", "Ball, Final"], ["Acceleration X Component", 2, "m/s²", "Ball"]],
        #     [["Displacement X Component", "nm", "Ball"]]
        # ],
        # [
        #     [["Position Y Component", 5, "m", "Ball, Initial"], ["Position Y Component", 10, "m", "Ball, Final"]],
        #     [["Displacement Y Component", "m", "Ball"]]
        # ],
        # [
        #     [["Velocity X Component", 5, "m/s", "Ball, Average"], ["Time", 10, "s", "Ball"]],
        #     [["Displacement X Component", "m", "Ball"]]
        # ],
        # [
        #     [["Velocity Y Component", 5, "m/s", "Ball, Average"], ["Time", 10, "s", "Ball"]],
        #     [["Displacement Y Component", "m", "Ball"]]
        # ],
        # [
        #     [["Velocity Y Component", 5, "m/s", "Ball, Initial"], ["Time", 10, "s", "Ball"], ["Acceleration Y Component", 2, "m/s²", "Ball"]],
        #     [["Displacement Y Component", "m", "Ball"]]
        # ],
        # [
        #     [["Velocity Y Component", 5, "m/s", "Ball, Initial"], ["Velocity Y Component", -20, "m/s", "Ball, Final"], ["Acceleration Y Component", 2, "m/s²", "Ball"]],
        #     [["Displacement Y Component", "m", "Ball"]]
        # ],
    ]

    for g, r in problems:
        print("start")
        text = "$ " + getSolution(g, r) +" $"
        plt.text(0, 0, text).set_fontsize(25)
        plt.show()
