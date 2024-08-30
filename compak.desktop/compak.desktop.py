import tkinter as tk
import json
from models.shooter import Shooter
from models.range import Range
from models.station import Station

# Ladda kastprogram från JSON-fil
with open("compak.desktop/compak.programs.json", "r") as f:
    compak_programs = json.load(f)

# Globala variabler
current_pair = 0  # Index för nuvarande sekvens (vilken duva)
current_program = 1  # Börjar med program 1
current_series = 1  # Index fö nuvarande serie
current_station = 0
num_of_shooters = 6

# Lista över skyttarnas positioner på stationerna (5 stationer + 1 väntstation)
shooter_positions = [0, 1, 2, 3, 4, 5]  # Skytt 6 börjar på väntstationen (index 5)

# Huvudfönster och Canvas
root = tk.Tk()
root.title("Compak Sporting Banvisualisering")
root.geometry("800x400")

canvas = tk.Canvas(root, width=800, height=400, bg="lightblue")
canvas.pack()

# Beräkna storlek för "Target over Flight Area"
target_width = 250  # Bredden på 40 meter i skala
target_height = 156  # Höjden på 25 meter i skala
x0 = (800 - target_width) // 2
y0 = 100
x1 = x0 + target_width
y1 = y0 + target_height

# Justera positioner för kastare A-F enligt specifikationer
thrower_positions = {
    "A": (x0 - 75, y0 + (target_height // 2) - 25),  # Till vänster om TOFA, i mitten
    "B": (x0 + (target_width // 3) - 75, y0 - 75),  # Ovanför TOFA, till vänster
    "C": (x0 + (target_width // 2) - 25, y0 - 75),  # Ovanför TOFA, i mitten
    "D": (x0 + (2 * target_width // 3) + 25, y0 - 75),  # Ovanför TOFA, till höger
    "E": (x1 + 25, y0 + (target_height // 2) - 25),  # Till höger om TOFA, i mitten
    "F": (
        x0 + (target_width // 2) - 25,
        y0 + (target_height // 2) + 25,
    ),  # Inuti TOFA, centrerad
}
shooting_range = Range(canvas, thrower_positions)

for i in range(num_of_shooters):
    shooting_range.add_shooter(Shooter(canvas, f"Skytt {i+1}"))

# Rita "Target over Flight Area"-boxen
flight_area = canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2)
canvas.create_text(
    (x0 + x1) // 2,
    (y0 + y1) // 2,
    text="Target over Flight Area",
    fill="red",
    font=("Helvetica", 10),
)

# Flytta informationsrutan längre åt vänster
info_box = canvas.create_rectangle(
    x0 - 250, y0, x0 - 150, y0 + 130, outline="black", width=2
)
program_label = canvas.create_text(
    x0 - 200,
    y0 + 20,
    text=f"Program: {current_program}",
    fill="black",
    font=("Helvetica", 15),
)
series_label = canvas.create_text(
    x0 - 200,
    y0 + 60,
    text=f"Serie: {current_series}",
    fill="black",
    font=("Helvetica", 15),
)
pair_label = canvas.create_text(
    x0 - 200,
    y0 + 100,
    text=f"Par/duva: {current_pair+1}",
    fill="black",
    font=("Helvetica", 15),
)

# Knapp för "Släpp duva" till höger om TOFA
release_button = tk.Button(root, text="Släpp Duvor", command=lambda: cast_clay())
release_button.place(x=x1 + 100, y=y0 + 20)

# Knapp för att stega tillbaka i programmet
back_button = tk.Button(root, text="Stega Tillbaka", command=lambda: step_back())
back_button.place(x=x1 + 100, y=y0 + 80)


# Funktion för att uppdatera visningen
def update_display():
    global current_pair, current_program, current_series, current_station
    # Highlighta rätt station
    shooting_range.highlight_station(current_station + 1)

    # Highlighta nästa kastare
    shooting_range.deactivate_all_throwers()
    current_throwers = compak_programs[str(current_program)][str(current_station + 1)][
        current_pair
    ]
    for label in current_throwers:
        shooting_range.activate_thrower(label)

    # Uppdatera informationsrutan
    canvas.itemconfig(program_label, text=f"Program: {current_program}")
    canvas.itemconfig(series_label, text=f"Serie: {current_series}")
    canvas.itemconfig(pair_label, text=f"Par/duva: {current_pair+1}")


# Funktion för att hantera kast
def cast_clay():
    global current_pair, current_program, current_series, current_station
    update_display()
    current_station += 1
    if current_station == 5:
        current_station = 0
        current_pair += 1
        if (
            len(compak_programs[str(current_program)][str(current_station + 1)])
            == current_pair
        ):  # Om alla sekvenser är skjutna, rotera skyttarna
            current_pair = 0
            current_series += 1
            shooting_range.move_shooters()
    update_display()


# Funktion för att stega tillbaka i programmet
def step_back():
    global current_pair, current_station, current_program, current_series
    # Stega tillbaka skytt
    if current_station == 0 and (current_pair > 0 or current_series > 1):
        current_station = 4
        current_pair -= 1
        if current_pair < 0:
            if current_series > 1:
                current_series -= 1
                shooting_range.moveback_shooters()
            current_pair = (
                len(compak_programs[str(current_program)][str(current_station + 1)]) - 1
            )
        
    elif current_station > 0 or current_series > 1:
        current_station -= 1
    update_display()


# Starta displayen
update_display()
root.mainloop()
