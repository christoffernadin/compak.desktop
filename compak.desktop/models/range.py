from .thrower import Thrower
from .station import Station


class Range:
    def __init__(self, canvas, thrower_positions):
        self.canvas = canvas
        self.throwers = []
        self.stations = []
        self.active_shooters = []
        self.waiting_shooters = []
        self.waiting_station = Station(canvas, station_number=6, x=50, y=325)

        for label, thrower_position in thrower_positions.items():
            self.throwers.append(
                Thrower(canvas, label, thrower_position[0], thrower_position[1])
            )

        for i in range(5):
            self.stations.append(
                Station(canvas, station_number=i + 1, x=800/6+(i*(800/6)), y=300)
            )

    def activate_thrower(self, label):
        for thrower in self.throwers:
            if thrower.label == label:
                thrower.activate()

    def deactivate_all_throwers(self):
        for thrower in self.throwers:
            thrower.deactivate()

    def highlight_station(self, station_number):
        for station in self.stations:
            if station.station_number == station_number:
                station.highlight()
            else:
                station.unhighlight()
        self.waiting_station.unhighlight()
    def get_stations(self):
        return self.stations
    def add_shooter(self, shooter):
        if len(self.active_shooters) < 6:
            self.active_shooters.append(shooter)
            inserted = False
            for id, station in enumerate(self.stations):
                if station.get_shooter() is None and inserted is False:
                    station.set_shooter(shooter)
                    inserted = True
                elif id == 4 and station.get_shooter is not None and inserted is False:
                    self.waiting_station.set_shooter(shooter)
        else: self.waiting_shooters.append(shooter)
    def move_shooters(self):
        next_shooter = self.waiting_station.get_shooter()
        for id, station in enumerate(self.stations):
            if id == 4:
                self.waiting_station.set_shooter(station.get_shooter())
                station.set_shooter(next_shooter)
            else:
                temp_shooter = station.get_shooter()
                station.set_shooter(next_shooter)
                next_shooter = temp_shooter
    def moveback_shooters(self):
        next_shooter = self.waiting_station.get_shooter()
        list_copy = self.stations.copy()
        list_copy.reverse()
        for id, station in enumerate(list_copy):
            if id == 4:
                self.waiting_station.set_shooter(station.get_shooter())
                station.set_shooter(next_shooter)
            else:
                temp_shooter = station.get_shooter()
                station.set_shooter(next_shooter)
                next_shooter = temp_shooter


            
