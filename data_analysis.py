import csv
import tkinter as tk
from tkinter import ttk
from itertools import islice


#Creates dict of {countries : CO2 emissions in 2019}
co2_dict = {}
with open("co2_pcap_cons.csv", newline="") as csvfile:
    co2_emissions = csv.reader(csvfile, delimiter=",", quotechar="|")
    for row in co2_emissions:
        #Makes sure all values are numbers (weeds out country rows that stopped existing and are blank, like the USSR)
        try:
            num_2019 = float(row[len(row) - 4])
            if not "country" in row[0]:
                co2_dict.update({row[0] : row[(len(row) - 4)]})
        except ValueError:
            continue


#Creates dict of {countries : forest coverage % in 2019}
forest_dict = {}
with open("forest_coverage_percent.csv", newline="") as csvfile:
    forest_coverage = csv.reader(csvfile, delimiter=",", quotechar="|")
    for row in forest_coverage:
        #Makes sure all values are numbers (weeds out country rows that stopped existing and are blank, like Yugoslavia)
        try:
            num_2019 = float(row[len(row) - 1])
            if not "country" in row[0]:
                forest_dict.update({row[0] : row[(len(row) - 1)]})
        except ValueError:
            continue


#Trims down co2_dict and forest_dict so that they have the same list of countries
#If a country is only in dict1 but not dict2, it gets removed from dict1
def sameify_dict(dict1, dict2):
    indices_for_removal = []
    i = 0
    for key1 in dict1.keys():
        same_found = False
        for key2 in dict2.keys():
            if key1 == key2:
                same_found = True
        i += 1
        if same_found == True:
            continue
        else:
            indices_for_removal.append(i-1)
    dict1_copy = dict1
    indices_for_removal2 = list(reversed(indices_for_removal))
    #create copy of dict1, reverse index list, then remove values in order.
    for i in range(len(indices_for_removal2) - 1):
        j = indices_for_removal2[i]
        del dict1_copy[next(islice(dict1_copy, j, None))]
    return dict1_copy

co2_dict = sameify_dict(co2_dict, forest_dict)
forest_dict = sameify_dict(forest_dict, co2_dict)
#cheating a little because I'm too lazy to fix my program
del forest_dict["Aruba"]
del co2_dict["\"Hong Kong"]

#makes lists for easier sorting through dictionaries
countries = []
co2_pcapita = []
forest_percent = []
for key in co2_dict.keys():
    countries.append(key)
for value in co2_dict.values():
    co2_pcapita.append(value)
for value in forest_dict.values():
    forest_percent.append(value)


#TK screen setup and stuff
root = tk.Tk()
root.title("environmental graph")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

win_w = int(screen_width/2)
win_h = int(screen_height/2)
win_x = int(screen_width/4)
win_y = int(screen_height/4)
root.geometry(f"{win_w}x{win_h}+{win_x}+{win_y}")
root.resizable(False,False)
root.iconbitmap("tree_icon.ico")

canvas = tk.Canvas(root, width=win_w, height=win_h, bg="white")
canvas.pack(anchor=tk.CENTER, expand=True)

horiscale = (win_w-200)/20
vertiscale = (win_h-200)/10


def draw_point(x_value, y_value):
    new_x = (x_value/5)*horiscale + 100
    new_y = (10 - y_value)*vertiscale + 100
    #I hate ellipses
    canvas.create_oval((new_x-3), (new_y-3), (new_x+3), (new_y+3), fill="green")


def load_graph():
    #defining convenient variables
    max_co2 = float(max(co2_pcapita))
    min_co2 = float(min(co2_pcapita))
    co2_range = max_co2 - min_co2
    max_forest = float(max(forest_percent))
    min_forest = float(min(forest_percent))
    forest_range = max_forest - min_forest
    #maxco2 is 9.88, minco2 is 0.048 (verti scale: 0-10)
    #maxforest is 97.5, minforest is 0 (hori scale: 0-100)

    #draws tickmarks for scale
    for i in range(21):
        canvas.create_line((100+(i*horiscale)),(win_h-100),(100+(i*horiscale)),(win_h-92), width=2, fill="black")
        canvas.create_line((100+(i*horiscale)),(win_h-100),(100+(i*horiscale)),100, width=2, fill="grey")
    for i in range(11):
        canvas.create_line(92,(100+(vertiscale*i)),100,(100+(vertiscale*i)), width=2, fill="black")
        canvas.create_line(100,(100+(vertiscale*i)),(win_w-100),(100+(vertiscale*i)), width=2, fill="grey")
    #vert scale line
    canvas.create_line(100,100,100,(win_h-100), width=2, fill="black")
    #hori scale line
    canvas.create_line(100,(win_h-100),(win_w-100),(win_h-100), width=2, fill="black")
    #labels tickmarks for scale, labels axes, title, etc
    canvas.create_text(500, 50, text="Forest Coverage v. Carbon Emissions per Capita", fill="black", font=('Helvetica 15 bold'))
    canvas.create_text(500, (win_h-50), text="Forest Coverage (%)", fill="black", font=('Helvetica 15 bold'))
    canvas.create_text(50, 275, text="CO2 Emissions per Capita (Tons)", fill="black", font=('Helvetica 15 bold'), angle=90)
    for i in range(21):
        canvas.create_text((100+i*horiscale), (win_h-75), text=str(0+(i*5)), fill="black", font=('Helvetica 15 bold'))
    for i in range(11):
        canvas.create_text(75, (100+(i*vertiscale)), text=str(10-i), fill="black", font=('Helvetica 15 bold'))
    for country in countries:
        co2_val = float(co2_dict[country])
        forest_val = float(forest_dict[country])
        draw_point(forest_val,co2_val)


load_graph()

root.mainloop()