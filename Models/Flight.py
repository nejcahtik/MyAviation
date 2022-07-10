class Flight:

    def __init__(self, i, da, aa, dt, at, aid):
        self.id = i
        self.departureAirport = da
        self.arrivalAirport = aa
        self.departureTime = dt
        self.arrivalTime = at
        self.aircraft = aid

    def encode(self):
        return self.__dict__
