class Thrower:
    def __init__(self, canvas, label, x, y):
        self.canvas = canvas
        self.label = label
        self.x = x
        self.y = y
        self.graphic = self.canvas.create_rectangle(x, y, x + 50, y + 50, fill="gray")
        self.text = self.canvas.create_text(
            x + 25, y + 25, text=self.label, fill="white"
        )

    def activate(self):
        self.canvas.itemconfig(self.graphic, fill="red")

    def deactivate(self):
        self.canvas.itemconfig(self.graphic, fill="gray")
