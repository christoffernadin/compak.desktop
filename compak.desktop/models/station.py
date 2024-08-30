from .shooter import Shooter

class Station:
    def __init__(self, canvas, station_number, x, y):
        self.canvas = canvas
        self.station_number = station_number
        self.x = x
        self.y = y
        self.graphic = self.canvas.create_rectangle(x-25,y-25, x+25, y+25, outline="black", width=2)
        self.shooter: Shooter = None
    def highlight(self):
        if self.shooter is not None:
            self.shooter.highlight()
        self.canvas.itemconfig(self.graphic, outline="blue", width=3)
        self.canvas.itemconfig(self.graphic, fill="green")
    def unhighlight(self):
        if self.shooter is not None:
            self.shooter.unhighlight()
        self.canvas.itemconfig(self.graphic, outline="black", width=2)
        self.canvas.itemconfig(self.graphic, fill="white")
    def get_position(self):
        return self.x, self.y
    def get_station_number(self):
        return self.station_number
    def get_shooter(self):
        return self.shooter
    def set_shooter(self, shooter: Shooter):
        self.shooter = shooter
        shooter.update_station(self)