class FlightsAnalysis:
        def __init__(self, i, aid, da, cnt, ift):
            self.id = i
            self.departureAirport = da
            self.inFlightTime = ift
            self.count = cnt
            self.aircraftId = aid

        def encode(self):
            return self.__dict__