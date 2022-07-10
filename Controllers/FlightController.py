from DatabaseRetrievers.FlightRetriever import FlightRetriever
import datetime
from Models.Flight import Flight
from Models.Aircraft import Aircraft

class FlightController:

    def __init__(self, dbconnection):
        self.flightRetriever = FlightRetriever(dbconnection)

    def checkForFlightData(self, id, departureAirport, arrivalAirport, departureTime, arrivalTime, aircraft):

        if not isinstance(id, int):
            return "id"
        if not isinstance(departureAirport, str):
            return "Departure Airport"
        if len(departureAirport) != 4:
            return "Departure Airport is not of length 4"
        if not isinstance(arrivalAirport, str):
            return "Arrival Airport"
        if len(arrivalAirport) != 4:
            return "Arrival Airport is not of length 4"
        if not isinstance(departureTime, datetime.datetime):
            return "Departure Time"
        if not isinstance(arrivalTime, datetime.datetime):
            return "Arrival Time"
        if departureTime <= datetime.datetime.now():
            return "Only future flights can be added"
        if arrivalTime - departureTime <= datetime.timedelta(0):
            return "Difference between departure and arrival time"
        if not isinstance(aircraft, Aircraft) and aircraft is not None:
            return "Aircraft"
        return False

    def fetchAllFlights(self):
        try:
            flights = self.flightRetriever.readAll()
        except Exception as e:
            raise Exception("Error while fetching all the flights: %s" % str(e))

        return flights

    def fetchById(self, id):
        try:
            flight = self.flightRetriever.readById(id)
        except Exception as e:
            raise Exception("Error while fetching flight=%s: %s" % (id, str(e)))
        return flight

    def create(self, departureAirport, arrivalAirport, departureTime, arrivalTime, aircraftId):

        aircraft = None
        if aircraftId is not None:
            aircraftDb = self.flightRetriever.readAircraftById(aircraftId)

            if len(aircraftDb) != 3 or aircraftDb is None:
                raise Exception("Flight cannot be added because its aircraft=%s does "
                                 "not exist in the database." % (aircraftId,))

            aircraft = Aircraft(aircraftDb[0], aircraftDb[1], aircraftDb[2])

        c = self.checkForFlightData(0, departureAirport, arrivalAirport, departureTime, arrivalTime, aircraft)

        if not c:
            flight = Flight(None, departureAirport, arrivalAirport, departureTime, arrivalTime, aircraft)

            try:
                return self.flightRetriever.create(flight)
            except Exception as e:
                raise Exception("Exception when inserting into the database flight with departure airport=%s"
                                 "and arrival airport=%s: %s" % (departureAirport, arrivalAirport, str(e)))
        else:
            raise Exception("Wrong Format Exception (for %s) when inserting flight with departure airport=%s"
                             "and arrival airport %s" % (c, departureAirport, arrivalAirport))

    def delete(self, id):
        try:
            return self.flightRetriever.delete(id)
        except Exception as e:
            raise Exception("Could not delete flight with serial number=%s from the database: %s" %
                            (id, str(e)))

    def update(self, id, departureAirport, arrivalAirport, departureTime, arrivalTime, aircraftId):

        flight = self.fetchById(id)

        if departureAirport is not None:
            flight.departureAirport = departureAirport
        if arrivalAirport is not None:
            flight.arrivalAirport = arrivalAirport
        if departureTime is not None:
            flight.departureTime = departureTime
        if arrivalTime is not None:
            flight.arrivalTime = arrivalTime
        if aircraftId is not None:
            aircraftDb = self.flightRetriever.readAircraftById(aircraftId)
            if len(aircraftDb) != 3 or aircraftDb is None:
                raise Exception("Flight %s cannot be updated because its aircraft=%s does"
                                "not exist." % (id, aircraftId))
            flight.aircraft = Aircraft(aircraftDb[0], aircraftDb[1], aircraftDb[2])

        c = self.checkForFlightData(flight.id, flight.departureAirport, flight.arrivalAirport, flight.departureTime,
                                    flight.arrivalTime, flight.aircraft)
        if not c:
            try:
                return self.flightRetriever.update(flight)
            except Exception as e:
                raise Exception(500, "Exception when updating into the database flight with departure airport=%s"
                                 "and arrival airport=%s: %s" % (departureAirport, arrivalAirport, str(e))
                                 )
        else:
            raise Exception(400, "Wrong Format Exception (for %s) when updating flight with departure airport=%s"
                             "and arrival airport %s" % (c, departureAirport, arrivalAirport))

    def fetchByDepAir(self, depAir):
        try:
            flights = self.flightRetriever.readByDepAir(depAir)
        except Exception as e:
            raise Exception(500, "Error while fetching flights by departure airport=%s: %s" % (depAir, str(e)))
        return flights

    def fetchByArrAir(self, arrAir):
        try:
            flights = self.flightRetriever.readByArrAir(arrAir)
        except Exception as e:
            print(e)
            raise e
        return flights

    def fetchByDepAirArrAir(self, depAir, arrAir):
        try:
            flights = self.flightRetriever.readByDepAirArrAir(depAir, arrAir)
        except Exception as e:
            raise Exception("Error while fetching flights by departure airport=%s and "
                             "arrival airport=%s: %s" % (depAir, arrAir, str(e)))
        return flights

    def fetchByDepTimeInt(self, depTimeFrom, depTimeTo):
        try:
            flights = self.flightRetriever.readByDepTimeInt(depTimeFrom, depTimeTo)
        except Exception as e:
            raise Exception(400, "Error while fetching flights by departure time from=%s to "
                             "%s: %s" % (depTimeFrom, depTimeTo, str(e)))
        return flights

    def fetchByDepAirTime(self, depAir, depTimeFrom, depTimeTo):
        try:
            flights = self.flightRetriever.readByDepAirTime(depAir, depTimeFrom, depTimeTo)
        except Exception as e:
            raise Exception("Error while fetching flights by departure time from %s to "
                             "%s on airport %s: %s" % (depTimeFrom, depTimeTo, depAir, str(e)))
        return flights

    def fetchByDepAirArrAirTime(self, depAir, arrAir, depTimeFrom, depTimeTo):
        try:
            flights = self.flightRetriever.readByDepAirArrAirTime(depAir, arrAir, depTimeFrom, depTimeTo)
        except Exception as e:
            raise Exception(400, "Error while fetching flights by departure time from=%s to "
                             "%s on airport %s to airport %s: %s" % (depTimeFrom, depTimeTo, depAir, arrAir, str(e)))
        return flights

    def readByDepTimeArrTime(self, timeFrom, timeTo):
        try:
            flights = self.flightRetriever.readByDepTimeArrTime(timeFrom, timeTo)
        except Exception as e:
            print(e)
            raise e

        return flights





