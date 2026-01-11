import sympy
import re

pi = sympy.pi

quantites = ["Force", "Elasticity Constant", "Change in Length", "Stress", "Area", "Longitudinal Strain", "Length", "Young Modulus"]

quantites_units = {
    "Force": ["N"],
    "Elasticity Constant": ["N/m"],
    "Change in Length": ["m", "cm", "mm"],
    "Stress": ["N/m²"],
    "Area": ["m²", "cm²", "mm²"],
    "Longitudinal Strain": [], # Add "None" for the menu options in the UI
    "Length": ["m", "cm", "mm"],
    "Young Modulus": ["N/m²"],
}

unit_conversion = {
    "m-cm": lambda x: x*100,
    "m-mm": lambda x: x*1000,
    "cm-m": lambda x: x*0.01,
    "cm-mm": lambda x: x*10,
    "mm-m": lambda x: x*0.001,
    "mm-cm": lambda x: x*0.1,
    "m²-cm²": lambda x: x*10000,
    "m²-mm²": lambda x: x*1000000,
    "cm²-m²": lambda x: x*0.0001,
    "cm²-mm²": lambda x: x*100,
    "mm²-m²": lambda x: x*0.000001,
    "mm²-cm²": lambda x: x*0.01,
}

def toInt(number):
    if number == int(number): number = int(number)
    return number

class Value:
    def __init__(self, quantity: str, value, unit: str, objects: list):
        self.value = sympy.N(value)
        self.quantity = quantity
        self.unit = unit
        self.objects = objects

    def change_unit(self, newUnit: str):
        if self.unit != newUnit:
            self.value = sympy.nsimplify(unit_conversion[f'{self.unit}-{newUnit}'](self.value))
            self.unit = newUnit

    def in_another_unit(self, newUnit: str):
        if self.unit != newUnit:
            return Value(self.quantity, sympy.nsimplify(unit_conversion[f'{self.unit}-{newUnit}'](self.value), ), unit=newUnit, objects=self.objects)
        
    def latex(self):
        return sympy.latex(self.value) + " " + re.sub("(.+)/(.+)", "\\\\frac{\\1}{\\2}", self.unit)
    
def findValue(quantity: str, objects: list, values: list[Value]):
    for value in values:
        if (type(value) == Value) and (value.quantity == quantity) and (value.objects == objects):
            return value

def getSolution(givenValues: list[Value], requiredValues: list[dict]):
    for index, g in enumerate(givenValues):
        g[3] = [obj.strip() for obj in g[3].split(",")]

        givenValues[index] = Value(*g)

    for index, r in enumerate(requiredValues):
        r[2] = [obj.strip() for obj in r[2].split(",")]

        requiredValues[index] = {"quantity": r[0], "unit": r[1], "objects": r[2]}

    if givenValues and requiredValues:
        listOfSolutions = []

        for value in requiredValues:
            requiredFunction: function = eval(value["quantity"].replace(" ", "_"))
            solution = requiredFunction(givenValues, value["objects"], value["unit"]) if len(quantites_units[value["quantity"]]) > 1 else requiredFunction(givenValues, value["objects"])

            if solution is None:
                listOfSolutions.append(f"Sorry, we couldn't find the " + value["quantity"] + " of " + ", ".join(value["objects"]) + ".}")

            else:
                listOfSolutions.append(solution[0])
                givenValues.append(solution[1])

        return re.sub(r'(\d)\.0(?=\D)', r'\1', "$\n\n$".join(listOfSolutions))
    
def Force(values: list[Value], objects: list, exceptions: list[str]=[]):
    solutions = []

    if "F=kΔL" not in exceptions:
        sol = ""
        steps = 0

        const = findValue("Elasticity Constant", objects, values)
        change = findValue("Change in Length", objects, values)

        if (change is None) and (find_change := Change_in_Length(values, objects, "m", exceptions+["F=kΔL"])):
            steps += 1; sol += find_change[0] + "$\n\n$"
            change = find_change[1]

        if const and change:
            if change.unit != "m":
                sol += "\\Delta L$ $=$ $" + change.latex() + "$ $=$ $" + (change := change.in_another_unit("m")).latex() + "$\n\n$"

            steps += 1

            result = Value("Change in Length", sympy.nsimplify(const.value*change.value), "N", objects)
            sol += "F$ $=$ $k \\Delta L$\n$F$ $=$ $" + const.latex() + " \\times " + change.latex() + "$\n$F$ $=$ $" + result.latex()

            solutions.append((sol, result, steps))
    
    if "stress" not in exceptions:
        sol = ""
        steps = 0

        stress = findValue("Stress", objects, values)

        if (stress is None) and (find_stress := Stress(values, objects, exceptions+["stress"])):
            steps += 1; sol += find_stress[0] + "$\n\n$"
            stress = find_stress[1]
    
        area = findValue("Area", objects, values)

        if (area is None) and (find_area := Area(values, objects, "m²", exceptions+["stress"])):
            steps += 1; sol += find_area[0] + "$\n\n$"
            area = find_area[1]
    
        if stress and area:
            if area.unit != "m²":
                sol += "A$ $=$ $" + area.latex() + "$ $=$ $" + (area := area.in_another_unit("m²")).latex() + "$\n\n$"

            steps += 1

            result = Value("Force", sympy.nsimplify(stress.value * area.value), "N", objects)
            sol += "Stress$ $=$ $\\frac{F}{A}$\n$" + stress.latex() + "$ $=$ $\\frac{F}{" + area.latex() + "}$\n$" + stress.latex() + " \\times " + area.latex() + "$ $=$ $F$\n$" + result.latex() + "$ $=$ $F"

            solutions.append((sol, result, steps))
    
    if "young-4" not in exceptions:
        sol = ""
        steps = 0

        young = findValue("Young Modulus", objects, values)

        if (young is None) and (find_young := Young_Modulus(values, objects, exceptions+["young-4"])):
            steps += 1; sol += find_young[0] + "$\n\n$"
            young = find_young[1]
    
        length = findValue("Length", objects, values)

        if (length is None) and (find_length := Length(values, objects, "m", exceptions+["young-4"])):
            steps += 1; sol += find_length[0] + "$\n\n$"
            length = find_length[1]
    
        change = findValue("Change in Length", objects, values)

        if (change is None) and (find_change := Change_in_Length(values, objects, "m", exceptions+["young-4"])):
            steps += 1; sol += find_change[0] + "$\n\n$"
            change = find_change[1]
    
        area = findValue("Area", objects, values)

        if (area is None) and (find_area := Area(values, objects, "m²", exceptions+["young-4"])):
            steps += 1; sol += find_area[0] + "$\n\n$"
            area = find_area[1]

        if young and length and change and area:
            a,b,c = False, False, False
            if length.unit != change.unit:
                if a := (length.unit != "m"):
                    sol += "L_{0}$ $=$ $" + length.latex() + "$ $=$ $" + (length := length.in_another_unit("m")).latex() + "$\n"

                if b := (change.unit != "m"):
                    if a: sol += "$"
                    sol += "\\Delta L$ $=$ $" + change.latex() + "$ $=$ $" + (change := change.in_another_unit("m")).latex() + "$\n"

            if c := (area.unit != "m²"):
                if b: sol += "$"
                sol += "A$ $=$ $" + area.latex() + "$ $=$ $" + (area := area.in_another_unit("m²")).latex() + "$\n"

            if a or b or c: sol += "\n$"

            steps += 1

            result = Value("Force", sympy.nsimplify((young.value*area.value*change.value)/length.value), "N", objects)
            sol += "Y$ $=$ $\\frac{F \\cdot L_{0}}{A \\cdot \\Delta L}$\n$" + young.latex() + "$ $=$ $\\frac{F \\times " + length.latex() + "}{" + area.latex() + " \\times " + change.latex() + "}$\n$\\frac{" + young.latex() + " \\times " + area.latex() + " \\times " + change.latex() + "}{" + length.latex() + "}$ $=$ $F$\n$" + result.latex() + "$ $=$ $F"

            solutions.append((sol, result, steps))
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Elasticity_Constant(values: list[Value], objects: list, exceptions: list[str]=[]):
    if "F=kΔL" not in exceptions:
        sol = ""
        
        force = findValue("Force", objects, values)

        if (force is None) and (find_force := Force(values, objects, exceptions+["F=kΔL"])):
            sol += find_force[0] + "$\n\n$"
            force = find_force[1]

        change = findValue("Change in Length", objects, values)

        if (change is None) and (find_change := Change_in_Length(values, objects, "m", exceptions+["F=kΔL"])):
            sol += find_change[0] + "$\n\n$"
            change = find_change[1]

        if force and change:
            if change.unit != "m":
                sol += "\\Delta L$ $=$ $" + change.latex() + "$ $=$ $" + (change := change.in_another_unit("m")).latex() + "$\n$"
                
            result = Value("Elasticity Constant", sympy.nsimplify(force.value/change.value), "N/m", objects)
            sol += "F$ $=$ $k \\Delta L$\n$" + force.latex() + "$ $=$ $k \\times " + change.latex() + "$\n$\\frac{" + force.latex() + "}{" + change.latex() + "}$ $=$ $k$\n$" + result.latex() + "$ $=$ $k"

            return (sol, result)

def Change_in_Length(values: list[Value], objects: list, unit: str, exceptions: list[str]=[]):
    solutions = []

    if "strain" not in exceptions:
        sol = ""
        steps = 0

        strain = findValue("Longitudinal Strain", objects, values)

        if (strain is None) and (find_strain := Longitudinal_Strain(values, objects, exceptions+["strain"])):
            steps += 1; sol += find_strain[0] + "$\n\n$"
            strain = find_strain[1]

        length = findValue("Length", objects, values)

        if (length is None) and (find_length := Length(values, objects, unit, exceptions+["strain"])):
            steps += 1; sol += find_length[0] + "$\n\n$"
            length = find_length[1]

        if strain and length:
            steps += 1

            result = Value("Change in Length", sympy.nsimplify(strain.value*length.value), length.unit, objects)
            sol += "Strain$ $=$ $\\frac{\\Delta L}{L_{0}}$\n$" + strain.latex() + "$ $=$ $\\frac{\\Delta L}{" + length.latex() + "}$\n$" + strain.latex() + " \\times " + length.latex() + "$ $=$ $\\Delta L$\n$" + result.latex() + "$ $=$ $\\Delta L"

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.latex() + "$ $=$ $\\Delta L"

            solutions.append((sol, result, steps))
    
    if "young-4" not in exceptions:
        sol = ""
        steps = 0

        young = findValue("Young Modulus", objects, values)

        if (young is None) and (find_young := Young_Modulus(values, objects, exceptions+["young-4"])):
            steps += 1; sol += find_young[0] + "$\n\n$"
            young = find_young[1]
    
        force = findValue("Force", objects, values)

        if (force is None) and (find_force := Force(values, objects, exceptions+["young-4"])):
            steps += 1; sol += find_force[0] + "$\n\n$"
            force = find_force[1]
    
        length = findValue("Length", objects, values)

        if (length is None) and (find_length := Length(values, objects, "m", exceptions+["young-4"])):
            steps += 1; sol += find_length[0] + "$\n\n$"
            length = find_length[1]
    
        area = findValue("Area", objects, values)

        if (area is None) and (find_area := Area(values, objects, "m²", exceptions+["young-4"])):
            steps += 1; sol += find_area[0] + "$\n\n$"
            area = find_area[1]

        if young and force and length and area:
            print(area.value, type(area.value))
            if area.unit != "m²":
                sol += "A$ $=$ $" + area.latex() + "$ $=$ $" + (area := area.in_another_unit("m²")).latex() + "$\n\n$"

            steps += 1

            result = Value("Change in Length", sympy.nsimplify((force.value*length.value)/(area.value*young.value)), length.unit, objects)
            sol += "Y$ $=$ $\\frac{F \\cdot L_{0}}{A \\cdot \\Delta L}$\n$" + young.latex() + "$ $=$ $\\frac{" + force.latex() + " \\times " + length.latex() + "}{" + area.latex() + " \\times \\Delta L}$\n$\\Delta L$ $=$ $\\frac{" + force.latex() + " \\times " + length.latex() + "}{" + area.latex() + " \\times " + young.latex() + "}$\n$\\Delta L$ $=$ $" + result.latex()

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$\\Delta L$ $=$ $" + result.latex()

            solutions.append((sol, result, steps))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Stress(values: list[Value], objects: list, exceptions: list[str]=[]):
    solutions = []

    if "stress" not in exceptions:
        sol = ""
        steps = 0

    if "young-2" not in exceptions:
        sol = ""
        steps = 0
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Area(values: list[Value], objects: list, unit: str, exceptions: list[str]=[]):
    solutions = []

    if "stress" not in exceptions:
        sol = ""
        steps = 0
    
    if "young-4" not in exceptions:
        sol = ""
        steps = 0

        young = findValue("Young Modulus", objects, values)

        if (young is None) and (find_young := Young_Modulus(values, objects, exceptions+["young-4"])):
            steps += 1; sol += find_young[0] + "$\n\n$"
            young = find_young[1]
    
        length = findValue("Length", objects, values)

        if (length is None) and (find_length := Length(values, objects, "m", exceptions+["young-4"])):
            steps += 1; sol += find_length[0] + "$\n\n$"
            length = find_length[1]
    
        change = findValue("Change in Length", objects, values)

        if (change is None) and (find_change := Change_in_Length(values, objects, "m", exceptions+["young-4"])):
            steps += 1; sol += find_change[0] + "$\n\n$"
            change = find_change[1]
    
        force = findValue("Force", objects, values)

        if (force is None) and (find_area := Force(values, objects, exceptions+["young-4"])):
            steps += 1; sol += find_area[0] + "$\n\n$"
            force = find_area[1]

        if young and length and change and force:
            if length.unit != change.unit:
                if a := (length.unit != "m"):
                    sol += "L_{0}$ $=$ $" + length.latex() + "$ $=$ $" + (length := length.in_another_unit("m")).latex() + "$\n"

                if change.unit != "m":
                    if a: sol += "$"
                    sol += "\\Delta L$ $=$ $" + change.latex() + "$ $=$ $" + (change := change.in_another_unit("m")).latex() + "$\n"

                sol += "\n$"

            steps += 1

            result = Value("Area", sympy.nsimplify((force.value*length.value)/(young.value*change.value)), "m²", objects)
            sol += "Y$ $=$ $\\frac{F \\cdot L_{0}}{A \\cdot \\Delta L}$\n$" + young.latex() + "$ $=$ $\\frac{" + force.latex() + " \\times " + length.latex() + "}{A \\times " + change.latex() + "}$\n$A$ $=$ $\\frac{" + force.latex() + " \\times " + length.latex() + "}{" + young.latex() + " \\times " + change.latex() + "}\n$A$ $=$ $" + result.latex()

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$A$ $=$ $" + result.latex()

            solutions.append((sol, result, steps))
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Longitudinal_Strain(values: list[Value], objects: list, exceptions: list[str]=[]):
    solutions = []

    if "strain" not in exceptions:
        sol = ""
        steps = 0

        change = findValue("Change in Length", objects, values)

        if (change is None) and (find_change := Change_in_Length(values, objects, "m", exceptions+["strain"])):
            steps += 1; sol += find_change[0] + "$\n\n$"
            change = find_change[1]
    
        length = findValue("Length", objects, values)

        if (length is None) and (find_length := Length(values, objects, "m", exceptions+["strain"])):
            steps += 1; sol += find_length[0] + "$\n\n$"
            length = find_length[1]

        if length and change:
            if length.unit != change.unit:
                if a := (length.unit != "m"):
                    sol += "L_{0}$ $=$ $" + length.latex() + "$ $=$ $" + (length := length.in_another_unit("m")).latex() + "$\n"

                if change.unit != "m":
                    if a: sol += "$"
                    sol += "\\Delta L$ $=$ $" + change.latex() + "$ $=$ $" + (change := change.in_another_unit("m")).latex() + "$\n"

                sol += "\n$"

            steps += 1

            result = Value("Longitudinal Strain", sympy.nsimplify(change.value/length.value), "", objects)
            sol += "Longitudinal$ $Strain$ $=$ $\\frac{\\Delta L}{L_{0}}$ $=$ $\\frac{" + change.latex() + "}{" + length.latex() + "}$ $=$ $" + result.latex()

            solutions.append((sol, result, steps))
    
    if "young-2" not in exceptions:
        sol = ""
        steps = 0

        young = findValue("Young Modulus", objects, values)

        if (young is None) and (find_young := Young_Modulus(values, objects, exceptions+["young-2"])):
            steps += 1; sol += find_young[0]
            young = find_young[1]
    
        stress = findValue("Stress", objects, values)

        if (stress is None) and (find_stress := Stress(values, objects, exceptions+["young-2"])):
            steps += 1; sol += find_stress[0]
            stress = find_stress[1]
    
        if young and stress:
            steps += 1

            result = Value("Longitudinal Strain", sympy.nsimplify(stress.value/young.value), "", objects)
            sol += "Y$ $=$ $\\frac{Stress}{Strain}$\n$" + young.latex() + "$ $=$ $\\frac{" + stress.latex() + "}{Strain}$\n$Strain$ $=$ $\\frac{" + stress.latex() + "}{" + young.latex() + "}$\n$Strain$ $=$ $" + result.latex()

            solutions.append((sol, result, steps))
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Length(values: list[Value], objects: list, unit: str, exceptions: list[str]=[]):
    solutions = []

    if "strain" not in exceptions:
        sol = ""
        steps = 0
    
    if "young-4" not in exceptions:
        sol = ""
        steps = 0

        young = findValue("Young Modulus", objects, values)

        if (young is None) and (find_young := Young_Modulus(values, objects, exceptions+["young-4"])):
            steps += 1; sol += find_young[0] + "$\n\n$"
            young = find_young[1]
    
        force = findValue("Force", objects, values)

        if (force is None) and (find_force := Force(values, objects, exceptions+["young-4"])):
            steps += 1; sol += find_force[0] + "$\n\n$"
            force = find_force[1]
    
        change = findValue("Change in Length", objects, values)

        if (change is None) and (find_change := Change_in_Length(values, objects, "m", exceptions+["young-4"])):
            steps += 1; sol += find_change[0] + "$\n\n$"
            change = find_change[1]
    
        area = findValue("Area", objects, values)

        if (area is None) and (find_area := Area(values, objects, "m²", exceptions+["young-4"])):
            steps += 1; sol += find_area[0] + "$\n\n$"
            area = find_area[1]

        if young and force and change and area:
            if area.unit != "m²":
                sol += "A$ $=$ $" + area.latex() + "$ $=$ $" + (area := area.in_another_unit("m²")).latex() + "$\n\n$"

            steps += 1

            result = Value("Length", sympy.nsimplify((young.value*area.value*change.value)/force.value), change.unit, objects)
            sol += "Y$ $=$ $\\frac{F \\cdot L_{0}}{A \\cdot \\Delta L}$\n$" + young.latex() + "$ $=$ $\\frac{" + force.latex() + " \\times L_{0}}{" + area.latex() + " \\times " + change.latex() + "}$\n$\\frac{" + young.latex() + " \\times " + area.latex() + " \\times " + change.latex() + "}{" + force.latex() + "}$ $=$ $L_{0}$\n$" + result.latex() + "$ $=$ $L_{0}"

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.latex() + "$ $=$ $L_{0}"

            solutions.append((sol, result, steps))
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Young_Modulus(values: list[Value], objects: list, exceptions: list[str]=[]):
    solutions = []

    if "young-2" not in exceptions:
        sol = ""
        steps = 0

        strain = findValue("Longitudinal Strain", objects, values)

        if (strain is None) and (find_strain := Longitudinal_Strain(values, objects, exceptions+["young-2"])):
            steps += 1; sol += find_strain[0] + "$\n\n$"
            strain = find_strain[1]

        stress = findValue("Stress", objects, values)

        if (stress is None) and (find_stress := Stress(values, objects, exceptions+["young-2"])):
            steps += 1; sol += find_stress[0] + "$\n\n$"
            stress = find_stress[1]
    
        if stress and strain:
            steps += 1

            result = Value("Young Modulus", sympy.nsimplify(stress.value/strain.value), "N/m²", objects)
            sol += "Y$ $=$ $\\frac{Stress}{Strain}$ $=$ $" + result.latex()
    
    if "young-4" not in exceptions:
        sol = ""
        steps = 0

        force = findValue("Force", objects, values)

        if (force is None) and (find_force := Force(values, objects, exceptions+["young-4"])):
            steps += 1; sol += find_force[0] + "$\n\n$"
            force = find_force[1]
    
        length = findValue("Length", objects, values)

        if (length is None) and (find_length := Length(values, objects, "m", exceptions+["young-4"])):
            steps += 1; sol += find_length[0] + "$\n\n$"
            length = find_length[1]
    
        change = findValue("Change in Length", objects, values)

        if (change is None) and (find_change := Change_in_Length(values, objects, "m", exceptions+["young-4"])):
            steps += 1; sol += find_change[0] + "$\n\n$"
            change = find_change[1]
    
        area = findValue("Area", objects, values)

        if (area is None) and (find_area := Area(values, objects, "m²", exceptions+["young-4"])):
            steps += 1; sol += find_area[0] + "$\n\n$"
            area = find_area[1]

        if force and length and area and change:
            a,b,c = False,False,False
            if length.unit != change.unit:
                if a := (length.unit != "m"):
                    sol += "L_{0}$ $=$ $" + length.latex() + "$ $=$ $" + (length := length.in_another_unit("m")).latex() + "$\n"

                if b := (change.unit != "m"):
                    if a: sol += "$"
                    sol += "\\Delta L$ $=$ $" + change.latex() + "$ $=$ $" + (change := change.in_another_unit("m")).latex() + "$\n"

            if c := (area.unit != "m²"):
                if a or b: sol += "$"
                sol += "A$ $=$ $" + area.latex() + "$ $=$ $" + (area := area.in_another_unit("m²")).latex() + "$\n"

            if a or b or c: sol += "\n$"

            steps += 1

            result = Value("Young Modulus", sympy.nsimplify((force.value*length.value)/(area.value*change.value)), "N/m²", objects)
            sol += "Y$ $=$ $\\frac{F \\cdot L_{0}}{A \\cdot \\Delta L}$\n$Y$ $=$ $\\frac{" + force.latex() + " \\times " + length.latex() + "}{" + area.latex() + " \\times " + change.latex() + "}$\n$Y$ $=$ $" + result.latex() 

            solutions.append((sol, result, steps))
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
    plt.rcParams["mathtext.default"] = "regular"

    g = [["Length", "4", "m", "Wire"], ["Area", "0.05", "cm²", "Wire"], ["Force", "500", "N", "Wire"], ["Young Modulus", "200000000", "N/m²", "Wire"]]
    r = [["Change in Length", "m", "Wire"]]

    # g = [["Stress", "20000000", "N/m²", "Wire"], ["Area", "1.5", "mm²", "Wire"]]
    # r = [["Force", "N", "Wire"]]

    # g = [["Length", "0.4", "m", "Wire"], ["Change in Length", "0.005", "m", "Wire"]]
    # r = [["Longitudinal Strain", "None", "Wire"]]

    # g = [["Length", "2.5", "m", "Wire"], ["Area", "0.001", "cm²", "Wire"], ["Change in Length", "1", "mm", "Wire"], ["Force", "4", "N", "Wire"]]
    # r = [["Young Modulus", "N/m²", "Wire"]]

    # g = [["Force", "0.2", "N", "Wire"], ["Change in Length", "0.6", "cm", "Wire"]]
    # r = [["Elasticity Constant", "N/m", "Wire"]]

    text = getSolution(g,r)

    plt.text(0,0, f"$" + re.sub(r'(\d)\.0(?=\D)', r'\1', text) + "$", fontsize=32)
    plt.show()