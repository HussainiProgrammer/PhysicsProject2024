from customtkinter import *
from PIL import ImageTk, Image
import os 
import threading
from tkinter import Text , Label, Frame
import tkinter.font as fonts
import matplotlib.pyplot as plt
from CTkMessagebox import *
import json
from physical_problems import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

abtUs = '''ثانوية الذرى للمتميزين 
طلاب الرابع علمي


بإشراف: الاستاذ لؤي العيداني  


Programming Team:

حسين علاء مصطفى

رضا حسن هادي


Designers:

حسين ماهر عبدالصاحب

سجاد علي عبد عبدالحسين

'''


plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
plt.rcParams["mathtext.default"] = "regular"


correct_color = '#33FF57'
error_color = '#FF3333'
button_color = '#FF4433'
hover_color = '#FA8072'
text_color = '#cccccc'

def quit_root(): threading.Thread(target=root.quit()).start

def NewFrame():return CTkFrame(root, height=800, width=500)

def validate_input(text): return True

def on_entry_click(event):valuesEntery.configure(validate="key", validatecommand=validate_cmd)

quantities = ["Force", "Elasticity Constant", "Change in Length", "Stress", "Area", "Longitudinal Strain", "Length", "Young Modulus"]

quantites_units = {
    "Force": ["N"],
    "Elasticity Constant": ["N/m"],
    "Change in Length": ["m", "cm", "mm"],
    "Stress": ["N/m²"],
    "Area": ["m²", "cm²", "mm²"],
    "Longitudinal Strain": ["None"],
    "Length": ["m", "cm", "mm"],
    "Young Modulus": ["N/m²"],
}

def get_sol():
    with open(path+"\\values.json",'r+',encoding="utf8") as file:
        file.truncate(0)
        data = {
            "order":[],
            "count":0,
            "count_required":0
        }
        json.dump(data,file,indent=4)

    widgets = givenValuesFrame.winfo_children()
    values = []

    for i in widgets:
        for w in i.winfo_children():
            if w.cget('text') != "X":
                values.append(w.cget('text').split(':'))

    for index, value in enumerate(values):
        quan = value[0]
        val = value[1].split('in')[1].split()[0]
        unit = value[1].split('in')[1].split()[1].replace("None", "")
        obj = value[2]

        with open(path+"\\values.json",'r+',encoding="utf8") as file:
                JSON_FILE = json.load(file)
                count = int(JSON_FILE["count"]) + 1

                data = {f"value{count}": {"Quantity":quan, "Value":val, "Unit":unit, "Object":obj}}

                JSON_FILE.update(data)
                JSON_FILE["count"] = count
                JSON_FILE["order"].append(f'value{count}')

                file.seek(0)
                json.dump(JSON_FILE,file,indent=4)

        values[index] = [quan, val, unit, obj]
            
    widgets2 = requiredValuesFrameBar.winfo_children()
    requireds = []

    for i in widgets2:
        for w in i.winfo_children():
            if w.cget('text') != "X":
                requireds.append(w.cget('text').split(':'))

    for index, require in enumerate(requireds):
        quan2 = require[0]
        unit2 = require[1].replace(" in ", "").replace("None", "")
        obj2 = require[2]

        with open(path+"\\values.json",'r+',encoding="utf8") as file:
            JSON_FILE = json.load(file)
            count2 = int(JSON_FILE["count_required"]) + 1

            data = {f"required{count2}": {"Quantity":quan2, "Unit":unit2, "Object":obj2}}

            JSON_FILE.update(data)
            JSON_FILE["count_required"] = count2
            JSON_FILE["order"].append(f'required{count2}')

            file.seek(0)
            json.dump(JSON_FILE,file,indent=4)

        requireds[index] = [quan2, unit2, obj2]

    figure = plt.figure(figsize=(7,5))
    ab = figure.add_subplot(111)
    ab.clear()

    ab.text(0, 0, f"${getSolution(values, requireds)}$", fontsize=32)

    ab.get_xaxis().set_visible(False)
    ab.get_yaxis().set_visible(False)
    ab.spines["right"].set_visible(False)
    ab.spines["left"].set_visible(False)
    ab.spines["top"].set_visible(False)
    ab.spines["bottom"].set_visible(False)

    plt.show()

def changeFrame(newFrame: CTkFrame):
    frames: list[CTkFrame] = [AboutFrame, HomeFrame, problemsFrame]
    frames.remove(newFrame)

    newFrame.place(relx=0.239, rely=0.03, relwidth=0.4*1.8, relheight=0.3999*3 - 0.2688)

    for frame in frames: frame.place_forget()

def addValues():
    if quantityMenuButton.get() == "Quantity" or not valuesEntery.get() or   unitsMenuButton.get() == "Unit" or not objectsEntery.get():CTkMessagebox(title="Error", message='Please enter a useful vaule!',icon='cancel', font=Desired2_font)
    else:
        _ = valuesEntery.get().replace('π','pi')
        frame = CTkFrame(givenValuesFrame,width=300,height=65);frame.pack(padx=5,pady=10, fill=X);CTkLabel(frame,text=f'{quantityMenuButton.get()}: in {_} {unitsMenuButton.get()}: {objectsEntery.get()}',font=Desired2_font).pack(side=LEFT,padx=10,pady=5);CTkButton(frame,fg_color=error_color,hover_color='#eb4034',text="X",font=Desired2_font,width=50,command=lambda: frame.destroy()).pack(side=RIGHT, padx=10,pady=5)

def addValues2():
    if quantityMenuButton2.get() == "Quantity"  or   unitsMenuButton2.get() == "Unit" or not objectsEntery2.get():CTkMessagebox(title="Error", message='Please enter a useful vaule!',icon='cancel', font=Desired2_font)

    else: frame = CTkFrame(requiredValuesFrameBar,width=300,height=65);frame.pack(padx=5,pady=10, fill=X);CTkLabel(frame,text=f'{quantityMenuButton2.get()}: in {unitsMenuButton2.get()}: {objectsEntery2.get()}',font=Desired2_font).pack(side=LEFT,padx=10,pady=5);CTkButton(frame,fg_color=error_color,hover_color='#eb4034',text="X",font=Desired2_font,width=50,command=lambda: frame.destroy()).pack(side=RIGHT, padx=10,pady=5)



def unit_quant(choice):


    units = quantites_units[choice]


    unitsMenuButton.configure(state=ACTIVE, values = units)


def unit_quant2(choice):


    units = quantites_units[choice]


    unitsMenuButton2.configure(state=ACTIVE, values = units)


#=========================== OLD CODE ====================================
path = os.path.dirname(__file__)


root = CTk()


root.geometry('1100x600+150+50')


root.minsize(width=1050, height=600)


root.title('Physical Problem Solver')


root.protocol("WM_DELETE_WINDOW", quit_root)



validate_cmd = (root.register(validate_input), '%P')



"""img = ImageTk.PhotoImage(Image.open(path+'\\Data\\widgets images\\Chmicon.ico'))


root.iconphoto(False,img)"""



Desired_font = CTkFont(family="Comic Sans MS", size=30,)


Desired2_font = CTkFont(family="Comic Sans MS", size=20,)


Desired3_font = CTkFont(family="Comic Sans MS", size=50,)


Desired4_font = CTkFont(family="Comic Sans MS", size=50,)


Desired5_font = CTkFont(family="Comic Sans MS", size=35,)


Desired6_font = CTkFont(family="Comic Sans MS", size=40,)




HomeFrame = CTkFrame(root, height=800, width=500)

MenuFrame = CTkFrame(root, corner_radius=4, height=3000, width=100)
MenuFrame.place(relx=.0, rely=.0, relwidth=.2001)



AboutFrame = CTkFrame(root, height=800, width=500)



HomesButton = CTkButton(MenuFrame, corner_radius=7, text='Problems', font=Desired2_font,


                        height=40, width=140, command=lambda: changeFrame(problemsFrame),fg_color=button_color,hover_color=hover_color,text_color=text_color)


HomesButton.place(relx=0.06666, rely=0.011, relheight=.017, relwidth=.87575)



AboutButton = CTkButton(MenuFrame, corner_radius=7, text='About Us', font=Desired2_font,


                    height=60, width=140, command=lambda: changeFrame(AboutFrame),fg_color=button_color,hover_color=hover_color,text_color=text_color)


AboutButton.place(relx=0.06666, rely=0.061+0.025, relheight=.017, relwidth=.87575)



AButton = CTkButton(MenuFrame, corner_radius=7, text='Astronomy', font=CTkFont(


    family="Comic Sans MS", size=20,), height=40, width=140, command=lambda: changeFrame(HomeFrame),fg_color=button_color,hover_color=hover_color,text_color=text_color, state=DISABLED)


AButton.place(relx=0.06666, rely=0.061, relheight=.017, relwidth=.87575)



CEQButton = CTkButton(MenuFrame, corner_radius=7, text='Physical Equations',


                      font=Desired2_font, height=40, width=140, state='disabled',fg_color=button_color,hover_color=hover_color,text_color=text_color)


CEQButton.place(relx=0.06666, rely=0.036, relheight=.017, relwidth=.87575)



_f = fonts.Font(family="Courier", size=40, weight='bold')


AbtUsText = Text(AboutFrame, height=10,font=_f,  width=50, foreground='silver',  background='#2b2b2b', bd=0, border=0, borderwidth=0)



AbtUsText.place(relx=0.024, rely=0.0244,


                relheight=.97575, relwidth=0.99575)


AbtUsText.delete("1.0", "end")


AbtUsText.insert(END,abtUs)


AbtUsText.configure(state=DISABLED)



#=========================== END OLD CODE ====================================


#=========================== NEW CODE ========================================



problemsFrame = CTkFrame(root, height=800, width=500, fg_color='#2b2b2b')


problemsFrame.place(relx=0.239, rely=0.03, relwidth=0.4*1.8, relheight=0.3999*3 - 0.2688)





valuesFrame = CTkFrame(problemsFrame,width=300,height=50,fg_color='#242424')


valuesFrame.place(relx=0.05004, rely=0.01, relheight=.117, relwidth=.887575)





CTkLabel(valuesFrame, text="Given Values", font=Desired2_font).pack(side=LEFT,padx=12,pady=5)


quantityMenuButton = CTkOptionMenu(valuesFrame,values=quantities,height=50,width=0, font=Desired2_font, button_color='#2b2b2b', fg_color='#2b2b2b', button_hover_color='#363434',command=unit_quant)


quantityMenuButton.pack(side=LEFT,padx = 10 , pady= 5)


quantityMenuButton.set("Quantity")



valuesEntery = CTkEntry(valuesFrame,width=70,height=50, fg_color='#2b2b2b',border_color='#2b2b2b', font=Desired2_font,placeholder_text="Value")


valuesEntery.pack(side=LEFT,padx = 10 , pady= 5)


valuesEntery.bind("<FocusIn>", on_entry_click)





unitsMenuButton = CTkOptionMenu(valuesFrame,height=50,width=0, font=Desired2_font, button_color='#2b2b2b', fg_color='#2b2b2b', button_hover_color='#363434',state=DISABLED)


unitsMenuButton.pack(side=LEFT,padx = 10 , pady= 5)


unitsMenuButton.set("Unit")



objectsEntery = CTkEntry(valuesFrame,width=100,height=50, fg_color='#2b2b2b',border_color='#2b2b2b', font=Desired2_font,placeholder_text="Objects")


objectsEntery.pack(side=LEFT,padx = 10 , pady= 5)



addValueButton = CTkButton(valuesFrame,text='+',font=Desired3_font,command=addValues,fg_color=button_color,hover_color=hover_color,text_color=text_color)


addValueButton.pack(side=LEFT,padx=10,pady=5)




givenValuesFrame = CTkScrollableFrame(problemsFrame,width=300,height=50,fg_color='#242424')


givenValuesFrame.place(relx=0.05004, rely=0.134, relwidth=.887575)




requiredValuesFrame = CTkFrame(problemsFrame,width=300,height=50,fg_color='#242424')


requiredValuesFrame.place(relx=0.05004, rely=0.5, relheight=.117, relwidth=.887575)





CTkLabel(requiredValuesFrame, text="Required Values", font=Desired2_font).pack(side=LEFT,padx=10,pady=5)


quantityMenuButton2 = CTkOptionMenu(requiredValuesFrame,values=quantities,height=40,width=0, font=Desired2_font, button_color='#2b2b2b', fg_color='#2b2b2b', button_hover_color='#363434',command=unit_quant2)


quantityMenuButton2.pack(side=LEFT,padx = 10 , pady= 5)


quantityMenuButton2.set("Quantity")




unitsMenuButton2 = CTkOptionMenu(requiredValuesFrame,height=40,width=0, font=Desired2_font, button_color='#2b2b2b', fg_color='#2b2b2b', button_hover_color='#363434',state=DISABLED)


unitsMenuButton2.pack(side=LEFT,padx = 10 , pady= 5)


unitsMenuButton2.set("Unit")



objectsEntery2 = CTkEntry(requiredValuesFrame,width=100,height=40, fg_color='#2b2b2b',border_color='#2b2b2b', font=Desired2_font,placeholder_text="Objects")


objectsEntery2.pack(side=LEFT,padx = 10 , pady= 5)



addValueButton2 = CTkButton(requiredValuesFrame,text='+',font=Desired3_font,text_color=text_color


                            ,command=addValues2,fg_color=button_color,hover_color=hover_color)


addValueButton2.pack(side=LEFT,padx=10,pady=5)



requiredValuesFrameBar = CTkScrollableFrame(problemsFrame,width=300,height=40,fg_color='#242424')


requiredValuesFrameBar.place(relx=0.05004, rely=0.62, relwidth=.887575)



solButton = CTkButton(problemsFrame,text="Get Soulutions", font=Desired2_font, height=40,


                      command=get_sol,fg_color=button_color,hover_color=hover_color,text_color=text_color)


solButton.place(relx=0.05004, rely=0.92, relwidth=.887575)




root.mainloop()



"""widgets = givenValuesFrame.winfo_children()


values = []


for i in widgets:


    for widget in i.winfo_children():


        values.append(widget.cget('text').split(':'))



for value in values:


    if value == ["X"]:value.remove("X")


    else: 


        quan = value[0]


        val = value[1].split('in')[0]


        unit = value[1].split('in')[1]


        obj = value[2]


        print(quan,val,unit,obj)
        
"""