from customtkinter import *
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from solution import getSolution, quantities_units, quantities

data = open("theme.txt", "r+", encoding="utf-8")

theme = data.read().strip()

set_appearance_mode(theme)
set_default_color_theme("blue")

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
plt.rcParams["mathtext.default"] = "regular"
plt.rcParams["mathtext.fontset"] = "stix"

homeSpaceWidth = 0.05
homeChildWidth = 1 - 2*homeSpaceWidth

homeLabelHeight = 0.2
homeTextBoxHeight = 0.425
homeSpaceHeight = (1 - homeLabelHeight - homeTextBoxHeight) / 3

spaceWidth = 0.02
objWidth = 1-2*spaceWidth

boxHeight = 0.09
listHeight = 3*boxHeight

buttonHeight = 0.05
spaceHeight = (1-2*boxHeight-2*listHeight-buttonHeight)/6

inputFrameSpaceWidth = 0.005
inputFrameSpaceHeight = 0.1
inputFrameChildHeight = 1-2*inputFrameSpaceHeight
insertButtonWidth = inputFrameChildHeight*boxHeight/objWidth

gInputFrameChildWidth = (1-6*inputFrameSpaceWidth-insertButtonWidth)/4
rInputFrameChildWidth = (1-5*inputFrameSpaceWidth-insertButtonWidth)/3

tabMenuWidth = 0.15
tabWidth = 1 - tabMenuWidth

relativeTabMenuSpaceWidth = 0.05
tabMenuSpaceWidth = tabMenuWidth*relativeTabMenuSpaceWidth
tabMenuChildWidth = tabMenuWidth*(1 - 2*relativeTabMenuSpaceWidth)

tabMenuSpaceHeight = 0.0236
tabMenuChildHeight = 0.05

givenValuesDict = {}
givenKey = 0

requiredValuesDict = {}
requiredKey = 0

currentHeight = 0
currentWidth = 0

def update_gQuantityText(*args):
    text = gQuantityOptionVar.get()

    if text not in quantities and text != "Quantity":
        gQuantityOptionVar.set("Quantity")

def setTab(newTab: CTkFrame):
    if newTab.place_info(): return

    tabs: list[CTkFrame] = [homeTab, problemsTab, simulationsTab]
    tabs.remove(newTab)

    for tab in tabs: tab.place_forget()
    newTab.place(relx=tabMenuWidth, rely=0, relwidth=tabWidth, relheight=1)

def update_gUnitOptions(*args):
    quantity = gQuantityOptionVar.get()

    if quantity in quantities:
        if type(gUnitOption) == MyCTkOptionMenu or (gUnitOption.cget("values") != quantities_units[quantity] or gUnitOption.get() not in quantities_units[quantity]):
            unitOptions = quantities_units[quantity]
            gUnitOption.configure(state="normal", values=unitOptions)
            gUnitOption.set(unitOptions[0])

    elif gUnitOption.cget("state") == "normal":
        gUnitOption.set("Unit")
        gUnitOption.configure(state="disabled")

def insertGivenValue():
    global givenKey

    quantity = gQuantityOption.get()
    value = gValueEntry.get()
    unit = gUnitOption.get()
    objects = gObjectsEntry.get()

    frame = CTkFrame(gListFrame, fg_color=("#d8d9d8", "#292929")) if problemsTab == root else CTkFrame(gListFrame)
    frame.pack(fill="x", padx=4, pady=4)

    label = CTkLabel(frame, text=f"{quantity}: {value}{unit} of {objects}", font=font2)
    label.pack(side="left", padx=5)

    removeButton = CTkButton(frame, text="Remove", fg_color=("#d32f2f", "#b71c1c"), hover_color=("#b71c1c", "#8b0000"), command=lambda key=givenKey: removeGivenValue(frame, key))
    removeButton.pack(side="right", padx=5, pady=3)

    givenValuesDict[givenKey] = [quantity, value, unit, objects]
    givenKey += 1

def removeGivenValue(frame: CTkFrame, key: int):
    frame.destroy()
    del givenValuesDict[key]

def update_rQuantityText(*args):
    text = rQuantityOptionVar.get()

    if text not in quantities and text != "Quantity":
        rQuantityOptionVar.set("Quantity")

def update_rUnitOptions(*args):
    quantity = rQuantityOptionVar.get()

    if quantity in quantities:
        if type(rUnitOption) == MyCTkOptionMenu or (rUnitOption.cget("values") != quantities_units[quantity] or rUnitOption.get().strip() not in quantities_units[quantity]):
            unitOptions = quantities_units[quantity]
            rUnitOption.configure(state="normal", values=unitOptions)
            rUnitOption.set(unitOptions[0])

    elif rUnitOption.cget("state") == "normal":
        rUnitOption.set("Unit")
        rUnitOption.configure(state="disabled")

def insertRequiredValue():
    global requiredKey

    quantity = rQuantityOption.get()
    unit = rUnitOption.get()
    objects = rObjectsEntry.get()
    
    frame = CTkFrame(rListFrame, fg_color=("#d8d9d8", "#292929")) if problemsTab == root else CTkFrame(rListFrame)
    frame.pack(fill="x", padx=4, pady=4)
    
    CTkLabel(frame, text=f"{quantity} in {unit} of {objects}", font=font2).pack(side="left", padx=5)

    removeButton = CTkButton(frame, text="Remove", fg_color=("#d32f2f", "#b71c1c"), hover_color=("#b71c1c", "#8b0000"), font=font2, command=lambda key=requiredKey: removeRequiredValue(frame, key))
    removeButton.pack(side="right", padx=5, pady=3)

    requiredValuesDict[requiredKey] = [quantity, unit, objects]
    requiredKey += 1

def removeRequiredValue(frame: CTkFrame, key: int):
    frame.destroy()
    del requiredValuesDict[key]

def solve():
    if len(givenValuesDict) and len(requiredValuesDict):
        # try:
            # solution = getSolution(list(givenValuesDict.values()), list(requiredValuesDict.values())) # this  a new comment written with the new cursor animation which is causing me a headache for some reason

            plt.figure(1)
            plt.text(0,0, "$" + "\\Delta r_{x} = v_{ix}\\Delta t + \\frac{1}{2}a_{x}\\Delta t^{2} $\n$ \\Delta r_{x} = 5 \\frac{m}{s} \\times 8s + \\frac{1}{2} \\times 2 \\frac{m}{s^{2}} \\times \\left( 8s \\right)^{2}$\n$ \\Delta r_{x} = 104m $").set_fontsize(32)
            plt.axis("off")
            plt.gcf().canvas.manager.set_window_title("Solution Window")
            plt.show()

            # for i, vector in enumerate(solution[1]):
            #     vector.graph(i+2)

        # except: CTkMessagebox(root, title="Input Error", message="Sorry. We ran into a problem while handling your inputs.", icon="cancel", sound=True, width=600)

    else: CTkMessagebox(root, title="Input Error", message="Please, enter the given and required values in your problem in suitable forms.", icon="cancel", sound=True, width=600)

def updateFont(event):
    global currentHeight, currentWidth
    if root.winfo_height() != currentHeight and root.winfo_width() != currentWidth:
        currentHeight = root.winfo_height()
        currentWidth = root.winfo_width()

        ratio = min([root.winfo_width(), root.winfo_height()])/750

        font1.configure(size=round(18*ratio))
        font2.configure(size=round(14*ratio))
        font3.configure(size=round(36*ratio))
        font4.configure(size=round(24*ratio))

def updateTheme(event):
    global theme
    newTheme = themeOption.get().lower()
    if newTheme != theme:
        theme = newTheme

        data.seek(0)
        data.truncate()
        data.write(theme)

        set_appearance_mode(theme)
        set_default_color_theme("blue" if theme == "light" else "dark-blue")

class MyCTkOptionMenu(CTkOptionMenu):
    def _update_dimensions_event(self, event):
        super()._update_dimensions_event(event)

        padx = list(self._text_label.grid_info()['padx'])
        padx[-1] = padx[0] + event.height

        self._text_label.grid(padx=padx)

class MyCTkComboBox(CTkComboBox):
    def _update_dimensions_event(self, event):
        super()._update_dimensions_event(event)

        padx = list(self._entry.grid_info()['padx'])
        padx[-1] = padx[0] + event.height

        self._entry.grid(padx=padx)

root = CTk()
root.title("Physics Problem Solver")
root.minsize(672, 560)
root.after(201, lambda: root.iconbitmap("icon.ico"))
root.after(202, lambda: root.state("zoomed"))

font1 = CTkFont("Calibri")
font2 = CTkFont("Calibri")
font3 = CTkFont("Calibri")
font4 = CTkFont("Calibri")

problemsTab = root

homeTab = CTkFrame(root, corner_radius=0)

CTkLabel(homeTab, text="Physics Problem Solver", font=font3).place(relx=homeSpaceWidth, rely=homeSpaceHeight, relwidth=homeChildWidth, relheight=homeLabelHeight)

labelFrame = CTkFrame(homeTab)
labelFrame.place(relx=homeSpaceWidth, rely=2*homeSpaceHeight+homeLabelHeight, relwidth=homeChildWidth, relheight=homeTextBoxHeight)

try:
    with open("info.txt", "r", encoding="utf-8") as file:
        CTkLabel(labelFrame, text=file.read(), font=font4).pack(expand=True)
        
except:
    CTkLabel(labelFrame, text="text not found!", font=font4).pack(expand=True)

problemsTab = CTkFrame(root, corner_radius=0)
simulationsTab = CTkFrame(root, corner_radius=0)

setTab(homeTab)

homeButton = CTkButton(root, text="Home", font=font1, command=lambda: setTab(homeTab))
homeButton.place(relx=tabMenuSpaceWidth, rely=tabMenuSpaceHeight, relwidth=tabMenuChildWidth, relheight=tabMenuChildHeight)

problemsButton = CTkButton(root, text="Problems", font=font1, command=lambda: setTab(problemsTab))
problemsButton.place(relx=tabMenuSpaceWidth, rely=2*tabMenuSpaceHeight+1*tabMenuChildHeight, relwidth=tabMenuChildWidth, relheight=tabMenuChildHeight)

simulationsButton = CTkButton(root, text="Simulations", font=font1, state="disabled", command=lambda: setTab(simulationsTab))
simulationsButton.place(relx=tabMenuSpaceWidth, rely=3*tabMenuSpaceHeight+2*tabMenuChildHeight, relwidth=tabMenuChildWidth, relheight=tabMenuChildHeight)

themeOption = MyCTkOptionMenu(root, values=["Dark", "Light"], font=font1, dropdown_font=font2, command=updateTheme)
themeOption.set(theme.capitalize())
themeOption.place(relx=tabMenuSpaceWidth, rely=4*tabMenuSpaceHeight+3*tabMenuChildHeight, relwidth=tabMenuChildWidth, relheight=tabMenuChildHeight)

gInputFrame = CTkFrame(problemsTab)
gInputFrame.place(relx=spaceWidth, rely=spaceHeight, relwidth=objWidth, relheight=boxHeight)

gQuantityOptionVar = StringVar()
gQuantityOption = MyCTkComboBox(gInputFrame, values=quantities, variable=gQuantityOptionVar, font=font1, dropdown_font=font2)
gQuantityOption.place(relx=inputFrameSpaceWidth, rely=inputFrameSpaceHeight, relwidth=gInputFrameChildWidth, relheight=inputFrameChildHeight)
gQuantityOptionVar.set("Quantity")
gQuantityOptionVar.trace_add("write", update_gUnitOptions)

gValueEntry = CTkEntry(gInputFrame, placeholder_text="Value", font=font1)
gValueEntry.place(relx=2*inputFrameSpaceWidth+gInputFrameChildWidth, rely=inputFrameSpaceHeight, relwidth=gInputFrameChildWidth, relheight=inputFrameChildHeight)

gUnitOption = MyCTkOptionMenu(gInputFrame, values=["Unit 1", "Unit 2", "Unit 3"], font=font1, corner_radius=10, dropdown_font=font2)
gUnitOption.place(relx=3*inputFrameSpaceWidth+2*gInputFrameChildWidth, rely=inputFrameSpaceHeight, relwidth=gInputFrameChildWidth, relheight=inputFrameChildHeight)
gUnitOption.set("Unit")
gUnitOption.configure(state="disabled")

gObjectsEntry = CTkEntry(gInputFrame, placeholder_text="Objects", font=font1)
gObjectsEntry.place(relx=4*inputFrameSpaceWidth+3*gInputFrameChildWidth, rely=inputFrameSpaceHeight, relwidth=gInputFrameChildWidth, relheight=inputFrameChildHeight)

gInsertButton = CTkButton(gInputFrame, text="+", command=insertGivenValue, font=font3)
gInsertButton.place(relx=5*inputFrameSpaceWidth+4*gInputFrameChildWidth, rely=inputFrameSpaceHeight, relwidth=insertButtonWidth, relheight=inputFrameChildHeight)

gListFrame = CTkScrollableFrame(problemsTab)
gListFrame.place(relx=spaceWidth, rely=spaceHeight+boxHeight+spaceHeight, relwidth=objWidth, relheight=listHeight)

rInputFrame = CTkFrame(problemsTab)
rInputFrame.place(relx=spaceWidth, rely=spaceHeight+boxHeight+spaceHeight+listHeight+spaceHeight, relwidth=objWidth, relheight=boxHeight)

rQuantityOptionVar = StringVar()
rQuantityOption = MyCTkComboBox(rInputFrame, values=quantities, variable=rQuantityOptionVar, font=font1, corner_radius=10, dropdown_font=font2)
rQuantityOption.place(relx=inputFrameSpaceWidth, rely=inputFrameSpaceHeight, relwidth=rInputFrameChildWidth, relheight=inputFrameChildHeight)
rQuantityOptionVar.set("Quantity")
rQuantityOptionVar.trace_add("write", update_rUnitOptions)

rUnitOption = MyCTkOptionMenu(rInputFrame, values=["Unit 1", "Unit 2", "Unit 3"], font=font1, corner_radius=10, dropdown_font=font2)
rUnitOption.place(relx=2*inputFrameSpaceWidth+rInputFrameChildWidth, rely=inputFrameSpaceHeight, relwidth=rInputFrameChildWidth, relheight=inputFrameChildHeight)
rUnitOption.set("Unit")
rUnitOption.configure(state="disabled")

rObjectsEntry = CTkEntry(rInputFrame, placeholder_text="Objects", font=font1)
rObjectsEntry.place(relx=3*inputFrameSpaceWidth+2*rInputFrameChildWidth, rely=inputFrameSpaceHeight, relwidth=rInputFrameChildWidth, relheight=inputFrameChildHeight)

rInsertButton = CTkButton(rInputFrame, text="+", command=insertRequiredValue, font=font3)
rInsertButton.place(relx=4*inputFrameSpaceWidth+3*rInputFrameChildWidth, rely=inputFrameSpaceHeight, relwidth=insertButtonWidth, relheight=inputFrameChildHeight)

rListFrame = CTkScrollableFrame(problemsTab)
rListFrame.place(relx=spaceWidth, rely=spaceHeight+boxHeight+spaceHeight+listHeight+spaceHeight+boxHeight+spaceHeight, relwidth=objWidth, relheight=listHeight)

solveButton = CTkButton(problemsTab, text="Find Solution", command=solve, font=font1)
solveButton.place(relx=spaceWidth, rely=spaceHeight+boxHeight+spaceHeight+listHeight+spaceHeight+boxHeight+spaceHeight+listHeight+spaceHeight, relwidth=objWidth, relheight=buttonHeight)

if type(gQuantityOption) == MyCTkComboBox and type(rQuantityOption) == MyCTkComboBox:
    gQuantityOption.bind("<FocusOut>", update_gQuantityText) # When the entry text is edited with keyboard but is not a quantity, replace
    rQuantityOption.bind("<FocusOut>", update_rQuantityText) # it with "Quantity".

if type(gUnitOption) == MyCTkComboBox and type(rUnitOption) == MyCTkComboBox:
    gUnitOption.bind("<FocusOut>", update_gUnitOptions)
    rUnitOption.bind("<FocusOut>", update_rUnitOptions) # Do the same for units, but reset it to 1st unit instead of just "Unit".

root.bind("<Configure>", updateFont)
root.mainloop()

data.close()