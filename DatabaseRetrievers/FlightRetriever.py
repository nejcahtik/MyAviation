from  Models.Aircraft import Aircraft
from Models.Flight import Flight
from Models.FlightsAnalysis import FlightsAnalysis
from Models.Airport import Airport
from Models.AnalyzedFlight import AnalyzedFlight

class FlightRetriever:

    def __init__(self, dbcnctn):
        self.dbConnection = dbcnctn

    # check if aircraft with 'aid' is already added to the list 'final' on the airport 'airportName'
    # and return the index of the airport 'airportName' in the list 'final'
    def isIn(self, airportName, final, aid):

        # index of the airport, the plane departures from (if the plane is already saved on this airport)
        ix = 0

        # find the airport
        for f in final:

            if f.airportName == airportName:
                break

            ix = ix + 1

        # find the aircraft on this airport (if exists)
        for a in final[ix].flightsFromThisAirport:
            if a.id == aid:
                return -1


        # no aircraft found on this airport
        return ix

    # sinced fetched data is not in the wrong format, transform flights f into the correct one
    def analyse(self, f):

        flights = []
        for flight in f:
            inflighttime = None
            if flight[4] is not None:
                inflighttime = int(flight[4])
            flights.append(FlightsAnalysis(flight[0],flight[1], flight[2], flight[3], inflighttime))

        airportName = flights[0].departureAirport
        airport = Airport(flights[0].departureAirport, flights[0].count)
        final = []
        final.append(airport)

        for flight in flights:

            if flight.departureAirport != airportName:
                airportName = flight.departureAirport
                final.append(Airport(flight.departureAirport, flight.count))

        for flight in flights:
            airportName = flight.departureAirport
            if flight.aircraftId is not None:
                ix = self.isIn(airportName, final, flight.aircraftId)

                if ix != -1:
                    final[ix].flightsFromThisAirport.append(AnalyzedFlight(flight.aircraftId, flight.inFlightTime))

        return final


    def readAircraftById(self, id):

        q = "SELECT * FROM Aircrafts WHERE Id=%s"
        v = (id,)

        return self.dbConnection.query(q, v).fetchone()

    def transformIntoFlightModel(self, flightsDb):

        if flightsDb is None:
            return None

        if not isinstance(flightsDb, list):
            # aircraft id
            aircraftId = flightsDb[5]

            aircraft = None

            # if this flight has an aircraft assigned already
            if aircraftId is not None:
                aircraftDb = self.readAircraftById(aircraftId)

                if aircraftDb is None:
                    raise Exception("Flight cannot be added because its aircraft with id=%s does "
                                    "not exist yet.", flightsDb[0], aircraftId)

                aircraft = Aircraft(aircraftDb[0], aircraftDb[1], aircraftDb[2])

            return Flight(flightsDb[0], flightsDb[1], flightsDb[2], flightsDb[3], flightsDb[4], aircraft)

        elif isinstance(flightsDb, list):
            flights = []

            for f in flightsDb:
                # aircraft id
                aircraftID = f[5]

                aircraft = None

                # if this flight has an aircraft assigned already
                if aircraftID is not None:
                    aircraftDb = self.readAircraftById(aircraftID)

                    if aircraftDb is None:
                        raise Exception("Flight %s cannot be created because its aircraft with id=%s does "
                                        "not exist.", f[0], aircraftID)

                    aircraft = Aircraft(aircraftDb[0], aircraftDb[1], aircraftDb[2])

                flights.append(Flight(f[0], f[1], f[2], f[3], f[4], aircraft))

            return flights

        else:
            raise Exception("Something happened that theoretically should not have happened.")

    def create(self, flight):

        if flight.aircraft is not None:
            q = "INSERT INTO Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId)" \
                "Values(%s, %s, %s, %s, %s)"
            v = (flight.departureAirport, flight.arrivalAirport, flight.departureTime, flight.arrivalTime, flight.aircraft.id)
        else:
            q = "INSERT INTO Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime)" \
                "Values(%s, %s, %s, %s)"
            v = (flight.departureAirport, flight.arrivalAirport, flight.departureTime, flight.arrivalTime)

        return self.dbConnection.query(q, v)

    def readAll(self):

        q = "SELECT * FROM Flights"

        flightsDb = self.dbConnection.query(q, None).fetchall()

        return self.transformIntoFlightModel(flightsDb)

    def readById(self, flightId):

        q = "SELECT * FROM Flights WHERE Id=%s"
        v = (flightId,)

        flightDb = self.dbConnection.query(q, v).fetchone()

        return self.transformIntoFlightModel(flightDb)

    def readByDepAir(self, depAir):

        q = "SELECT * FROM Flights WHERE DepartureAirport=%s"
        v = (depAir,)

        flightsDb = self.dbConnection.query(q, v).fetchall()

        return self.transformIntoFlightModel(flightsDb)

    def readByArrAir(self, arrAir):

        q = "SELECT * FROM Flights WHERE ArrivalAirport=%s"
        v = (arrAir,)

        flightsDb = self.dbConnection.query(q, v).fetchall()

        return self.transformIntoFlightModel(flightsDb)

    def readByDepAirArrAir(self, depAir, arrAir):

        q = "SELECT * FROM Flights WHERE DepartureAirport=%s AND ArrivalAirport=%s"
        v = (depAir, arrAir)

        flightsDb = self.dbConnection.query(q, v).fetchall()

        return self.transformIntoFlightModel(flightsDb)

    def readByDepTimeInt(self, depTimeFrom, depTimeTo):

        q = "SELECT * FROM Flights WHERE DepartureTime>=%s AND DepartureTime<=%s"
        v = (depTimeFrom, depTimeTo)

        flightsDb = self.dbConnection.query(q, v).fetchall()

        return self.transformIntoFlightModel(flightsDb)

    def readByDepAirTime(self, depAir, depTimeFrom, depTimeTo):

        q = "SELECT * FROM Flights WHERE DepartureAirport=%s AND DepartureTime>=%s AND DepartureTime<=%s"
        v = (depAir, depTimeFrom, depTimeTo)

        flightsDb = self.dbConnection.query(q, v).fetchall()

        return self.transformIntoFlightModel(flightsDb)

    def readByDepAirArrAirTime(self, depAir, arrAir, depTimeFrom, depTimeTo):
        q = "SELECT * FROM Flights WHERE DepartureAirport=%s AND ArrivalAirport=%s " \
            "AND DepartureTime>=%s AND DepartureTime<=%s"
        v = (depAir, arrAir, depTimeFrom, depTimeTo)

        flightsDb = self.dbConnection.query(q, v).fetchall()

        return self.transformIntoFlightModel(flightsDb)

    def readByDepTimeArrTime(self, timeFrom, timeTo):
        if timeFrom < timeTo:
            q = "SELECT F.Id, A.AircraftId, F.DepartureAirport, C.cnt, P.inflighttime FROM Flights F " \
                "INNER JOIN (SELECT AircraftId, Id FROM Flights) A ON F.Id=A.Id " \
                "INNER JOIN (SELECT L.AircraftId, SUM(TIMESTAMPDIFF(MINUTE, L.f, L.t)) as inflighttime FROM Flights A " \
                "INNER JOIN (SELECT AircraftId, Id, GREATEST(DepartureTime, %s) as f, LEAST(ArrivalTime, %s) as t " \
                "FROM Flights " \
                "WHERE DepartureTime>=%s AND DepartureTime <=%s OR ArrivalTime>=%s " \
                "AND ArrivalTime<=%s) L ON L.AircraftId = A.AircraftId " \
                "WHERE DepartureTime>=%s AND DepartureTime <=%s OR ArrivalTime>=%s " \
                "AND ArrivalTime<=%s " \
                "GROUP BY L.AircraftId" \
                ") P ON A.AircraftId=P.AircraftId " \
                "INNER JOIN (SELECT DepartureAirport, COUNT(DepartureAirport) AS cnt " \
                "FROM Flights " \
                "WHERE DepartureTime>=%s AND DepartureTime <=%s OR ArrivalTime>=%s " \
                "AND ArrivalTime<=%s GROUP BY DepartureAirport) C ON F.DepartureAirport=C.DepartureAirport " \
                "UNION " \
                "SELECT F.Id,  null, F.DepartureAirport, C.cnt, null FROM Flights F " \
                "INNER JOIN (SELECT AircraftId, Id FROM Flights) A ON F.Id=A.Id " \
                "INNER JOIN (SELECT DepartureAirport, COUNT(DepartureAirport) AS cnt " \
                "FROM Flights " \
                "WHERE DepartureTime>=%s AND DepartureTime <=%s OR ArrivalTime>=%s " \
                "AND ArrivalTime<=%s GROUP BY DepartureAirport) C ON F.DepartureAirport=C.DepartureAirport " \
                "WHERE F.AircraftId IS NULL " \
                "ORDER BY DepartureAirport "

            v = (timeFrom, timeTo, timeFrom, timeTo, timeFrom, timeTo, timeFrom, timeTo, timeFrom, timeTo,
                 timeFrom, timeTo, timeFrom, timeTo,
                 timeFrom, timeTo, timeFrom, timeTo)

            flightsWithDb = self.dbConnection.query(q, v).fetchall()

            # since fetched data 'flightsWithDb' is in the wrong format, transform it into the correct one
            return self.analyse(flightsWithDb)

        else:
            raise Exception("time from is larger than time to")

    def update(self, flight):
        q = "UPDATE Flights SET DepartureAirport=%s, ArrivalAirport=%s, " \
            "DepartureTime=%s, ArrivalTime=%s, AircraftId=%s WHERE Id=%s"
        v = (flight.departureAirport, flight.arrivalAirport,
             flight.departureTime, flight.arrivalTime, flight.aircraft.id, flight.id)

        return self.dbConnection.query(q, v)

    def delete(self, flightId):
        q = "DELETE FROM Flights WHERE Id=%s"
        v = (flightId,)

        return self.dbConnection.query(q, v)
