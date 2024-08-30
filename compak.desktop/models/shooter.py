class Shooter:
    def __init__(self, canvas, label):
        self.canvas = canvas
        self.x = -200
        self.y = -200
        self.graphic = self.canvas.create_oval(
            self.x-25, self.y-25, self.x + 25, self.y + 25, fill="gray"
        )
        self.text = self.canvas.create_text(
            self.x-25, self.y-25, text=label, fill="white"
        )

    def move_to(self, new_x, new_y):
        self.canvas.coords(self.graphic, new_x-25, new_y-25, new_x + 25, new_y + 25)
        self.canvas.coords(self.text, new_x, new_y)
        self.x = new_x
        self.y = new_y

    def update_station(self, new_station):
        self.station = new_station
        pos = new_station.get_position()
        self.move_to(pos[0], pos[1])  

    def get_position(self):
        return self.x, self.y

    def get_station(self):
        return self.station

    def highlight(self):
        self.canvas.itemconfig(self.graphic, fill="green")

    def unhighlight(self):
        self.canvas.itemconfig(self.graphic, fill="gray")
