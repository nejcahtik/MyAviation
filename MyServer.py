from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json
from DatabaseConnection import DatabaseConnection
from Controllers.AircraftController import AircraftController
from Controllers.FlightController import FlightController
from urllib.parse import urlparse
import simplejson


class MyServer(BaseHTTPRequestHandler):
    dbconnection = DatabaseConnection()
    aircraftController = AircraftController(dbconnection)
    flightController = FlightController(dbconnection)

    def set_headers(self, res):
        self.send_response(res)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):

        parsed = urlparse(self.path)

        if parsed.path.startswith("/Aircrafts"):

            # Fetch all aircrafts
            if self.path == "/Aircrafts":

                try:
                    aircrafts = self.aircraftController.fetchAllAircrafts()
                    parse = "No aircrafts found in the database."
                    if aircrafts is not None:
                        parse = json.dumps([aircraft.__dict__ for aircraft in aircrafts])
                    self.set_headers(200)
                    self.wfile.write(parse.encode(encoding='utf_8'))
                except Exception as e:
                    print(e)
                    self.set_headers(500)
                    self.wfile.write(bytes("ERROR: Something went wrong when fetching aircrafts: "+str(e), 'UTF-8'))

            else:
                queryparams = parsed.query.split("&")
                # Fetch aircraft by serial number
                if len(queryparams) == 1 and queryparams[0].split("=")[0] == "SerialNumber":
                    try:
                        serialNumber = str(queryparams[0].split("=")[1])
                        try:
                            aircraft = self.aircraftController.fetchBySerialNumber(serialNumber)
                            parse = "Aircraft with this serial number not found in the database."
                            if aircraft is not None:
                                parse = json.dumps(aircraft, default=lambda o: o.encode(), indent=4)
                            self.set_headers(200)
                            self.wfile.write(bytes(parse, 'UTF-8'))
                        except Exception as e:
                            print(e)
                            self.set_headers(500)
                            self.wfile.write(bytes("ERROR: Something went wrong when fetching the aircraft:"+str(e), "UTF-8"))

                    except Exception as e:
                        print(e)
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: Serial number is not in the correct format.", 'UTF-8'))

                # Fetch aircrafts by manufacturer
                elif len(queryparams) == 1 and queryparams[0].split("=")[0] == "Manufacturer":
                    try:
                        manufacturer = str(queryparams[0].split("=")[1])

                        try:
                            aircrafts = self.aircraftController.fetchByManufacturer(manufacturer)

                            parse = "No aircrafts made by this manufacturer found in the database."
                            if aircrafts is not None:
                                parse = json.dumps([aircraft.__dict__ for aircraft in aircrafts])

                            self.set_headers(200)
                            self.wfile.write(parse.encode(encoding='utf_8'))
                        except Exception as e:
                            print(e)
                            self.set_headers(500)
                            self.wfile.write(bytes("ERROR: Something went wrong when fetching aircrafts: "+str(e), "UTF-8"))
                    except Exception as e:
                        print(e)
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: Manufacturer should be string.", 'UTF-8'))
                # Fetch aircraft by id
                elif len(queryparams) == 1 and queryparams[0].split("=")[0] == "Id":
                    try:
                        id = int(queryparams[0].split("=")[1])

                        try:
                            aircraft = self.aircraftController.fetchById(id)
                            parse = "Aircraft with this id not found in the database."
                            if aircraft is not None:
                                parse = json.dumps(aircraft, default=lambda o: o.encode(), indent=4)
                            self.set_headers(200)
                            self.wfile.write(bytes(parse, 'UTF-8'))
                        except Exception as e:
                            print(e)
                            self.set_headers(500)
                            self.wfile.write(bytes("ERROR: Something went wrong when fetching the aircraft: "+str(e), "UTF-8"))
                    except Exception as e:
                        print(e)
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: Id should be integer.", 'UTF-8'))
                else:
                    self.set_headers(400)

        elif parsed.path == "/Flights":

            # Fetch all flights
            if self.path == "/Flights":
                try:
                    flights = self.flightController.fetchAllFlights()
                    self.set_headers(200)
                    if flights is None:
                        self.wfile.write(bytes("No flights found in the database.", 'UTF-8'))
                    else:
                        for flight in flights:
                            if flight.aircraft is not None:
                                flight.aircraft = flight.aircraft.__dict__

                        parse = json.dumps([flight.__dict__ for flight in flights], default=str)
                        self.wfile.write(parse.encode(encoding='utf_8'))
                except Exception as e:
                    print(e)
                    self.set_headers(500)
                    self.wfile.write(bytes("ERROR: Something went wrong when fetching flights: "+str(e), "UTF-8"))

            # Fetch flight by id
            else:
                queryparams = parsed.query.split("&")
                if len(queryparams) == 1 and queryparams[0].split("=")[0] == "Id":
                    try:
                        id = int(queryparams[0].split("=")[1])

                        try:
                            flight = self.flightController.fetchById(id)
                            self.set_headers(200)
                            parse = "No flight with this id found in the database."
                            if flight is not None:
                                if flight.aircraft is not None:
                                    flight.aircraft = flight.aircraft.__dict__
                                parse = json.dumps(flight.__dict__, default=str)
                            self.wfile.write(parse.encode(encoding='utf_8'))
                        except Exception as e:
                            print(e)
                            self.set_headers(500)
                            self.wfile.write(bytes("ERROR: Something went wrong when fetching the flight: "+str(e), 'UTF-8'))
                    except Exception as e:
                        print(e)
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: Id should be integer.", 'UTF-8'))

                # Fetch flights by departure airport
                elif len(queryparams) == 1 and queryparams[0].split("=")[0] == "DepartureAirport":
                    try:
                        depAir = str(queryparams[0].split("=")[1])

                        if len(depAir) == 4:
                            try:
                                flights = self.flightController.fetchByDepAir(depAir)
                                self.set_headers(200)
                                if flights is None:
                                    self.wfile.write(bytes("No flights that departure from this airport found in the database.", 'UTF-8'))
                                else:
                                    for flight in flights:
                                        if flight.aircraft is not None:
                                            flight.aircraft = flight.aircraft.__dict__

                                    parse = json.dumps([flight.__dict__ for flight in flights], default=str)
                                    self.wfile.write(parse.encode(encoding='utf_8'))
                            except Exception as e:
                                print(e)
                                self.set_headers(500)
                                self.wfile.write(bytes("ERROR: Something went wrong when fetching the flights: "+str(e), 'UTF-8'))
                        else:
                            self.set_headers(400)
                            self.wfile.write(bytes("ERROR: DepartureAirport should contain 4 letters.", 'UTF-8'))
                    except Exception as e:
                        print(e)
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: DepartureAirport should be string.", 'UTF-8'))

                # Fetch flights by arrival airport
                elif len(queryparams) == 1 and queryparams[0].split("=")[0] == "ArrivalAirport":
                    try:
                        arrAir = str(queryparams[0].split("=")[1])

                        if len(arrAir) == 4:
                            try:
                                flights = self.flightController.fetchByArrAir(arrAir)
                                self.set_headers(200)
                                if flights is None:
                                    self.wfile.write(
                                        bytes("No flights that fly to this airport found in the database.",
                                              'UTF-8'))
                                else:
                                    for flight in flights:
                                        if flight.aircraft is not None:
                                            flight.aircraft = flight.aircraft.__dict__

                                    parse = json.dumps([flight.__dict__ for flight in flights], default=str)
                                    self.wfile.write(parse.encode(encoding='utf_8'))
                            except Exception as e:
                                print(e)
                                self.set_headers(500)
                                self.wfile.write(bytes("ERROR: Something went wrong when fetching the flights: "+str(e), 'UTF-8'))
                        else:
                            self.set_headers(400)
                            self.wfile.write(bytes("ERROR: ArrivalAirport should contain 4 letters.", 'UTF-8'))
                    except Exception as e:
                        print(e)
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: ArrivalAirport should be string.", 'UTF-8'))

                # Fetch flights by departure airport and arrival airport
                elif len(queryparams) == 2 and queryparams[0].split("=")[0] == "DepartureAirport" \
                        and queryparams[1].split("=")[0] == "ArrivalAirport":
                    try:
                        depAir = str(queryparams[0].split("=")[1])
                        arrAir = str(queryparams[1].split("=")[1])

                        if len(depAir) == 4 and len(arrAir) == 4:
                            try:
                                flights = self.flightController.fetchByDepAirArrAir(depAir, arrAir)
                                self.set_headers(200)
                                if flights is None:
                                    self.wfile.write(
                                        bytes("No flights that fly to this airport found in the database.",
                                              'UTF-8'))
                                else:
                                    for flight in flights:
                                        if flight.aircraft is not None:
                                            flight.aircraft = flight.aircraft.__dict__

                                    parse = json.dumps([flight.__dict__ for flight in flights], default=str)
                                    self.wfile.write(parse.encode(encoding='utf_8'))
                            except Exception as e:
                                print(e)
                                self.set_headers(500)
                                self.wfile.write(bytes("ERROR: Something went wrong when fetching the flights: "+str(e), 'UTF-8'))
                        else:
                            self.set_headers(400)
                            self.wfile.write(bytes("ERROR: DepartureAirport and ArrivalAirport should both contain 4 letters.", 'UTF-8'))
                    except Exception as e:
                        print(e)
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: DepartureAirport and ArrivalAirport should both be strings.", 'UTF-8'))

                # Fetch flights by departure time
                elif len(queryparams) == 2 and queryparams[0].split("=")[0] == "DepartureTimeFrom" \
                        and queryparams[1].split("=")[0] == "DepartureTimeTo":
                    try:
                        depTimeFrom = datetime.strptime(queryparams[0].split("=")[1].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        depTimeTo = datetime.strptime(queryparams[1].split("=")[1].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        try:
                            flights = self.flightController.fetchByDepTimeInt(depTimeFrom, depTimeTo)
                            self.set_headers(200)
                            for flight in flights:
                                if flight.aircraft is not None:
                                    flight.aircraft = flight.aircraft.__dict__

                            parse = json.dumps([flight.__dict__ for flight in flights], default=str)
                            self.wfile.write(parse.encode(encoding='utf_8'))
                        except Exception as e:
                            print(e)
                            self.set_headers(500)
                            self.wfile.write(bytes("ERROR: Something went wrong when fetching the flights: "+str(e), 'UTF-8'))
                    except Exception as e:
                        print(e)
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: DepartureTimeFrom and DepartureTimeTo should be of format datetime.", 'UTF-8'))

                # Fetch flights by departure airport and departure time
                elif len(queryparams) == 3 and queryparams[0].split("=")[0] == "DepartureAirport" \
                        and queryparams[1].split("=")[0] == "DepartureTimeFrom" \
                        and queryparams[2].split("=")[0] == "DepartureTimeTo":
                    try:
                        depAir = str(queryparams[0].split("=")[1])
                        depTimeFrom = datetime.strptime(queryparams[1].split("=")[1].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        depTimeTo = datetime.strptime(queryparams[2].split("=")[1].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        if len(depAir) == 4:
                            try:
                                flights = self.flightController.fetchByDepAirTime(depAir, depTimeFrom, depTimeTo)
                                self.set_headers(200)
                                for flight in flights:
                                    if flight.aircraft is not None:
                                        flight.aircraft = flight.aircraft.__dict__

                                parse = json.dumps([flight.__dict__ for flight in flights], default=str)
                                self.wfile.write(parse.encode(encoding='utf_8'))
                            except Exception as e:
                                self.set_headers(500)
                                self.wfile.write(bytes("ERROR: Something went wrong when fetching the flights: "+str(e), 'UTF-8'))
                        else:
                            self.set_headers(400)
                            self.wfile.write(bytes("ERROR: DepartureAirport should contain 4 letters.", 'UTF-8'))

                    except Exception as e:
                            print(e)
                            self.set_headers(400)
                            self.wfile.write(bytes("ERROR: DepTimeFrom and DepTimeTo should both be of format datetime, DepartureAirport should be string.", 'UTF-8'))

                # Fetch flights by departure airport, arrival airport and departure time
                elif len(queryparams) == 4 and queryparams[0].split("=")[0] == "DepartureAirport" \
                        and queryparams[1].split("=")[0] == "ArrivalAirport" \
                        and queryparams[2].split("=")[0] == "DepartureTimeFrom"\
                        and queryparams[3].split("=")[0] == "DepartureTimeTo":
                    try:
                        depAir = str(queryparams[0].split("=")[1])
                        arrAir = str(queryparams[1].split("=")[1])
                        depTimeFrom = datetime.strptime(queryparams[2].split("=")[1].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        depTimeTo = datetime.strptime(queryparams[3].split("=")[1].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        if len(depAir) == 4 and len(arrAir) == 4:
                            try:
                                flights = self.flightController.fetchByDepAirArrAirTime(depAir, arrAir, depTimeFrom, depTimeTo)
                                for flight in flights:
                                    if flight.aircraft is not None:
                                        flight.aircraft = flight.aircraft.__dict__
                                parse = json.dumps([flight.__dict__ for flight in flights], default=str)
                                self.set_headers(200)
                                self.wfile.write(parse.encode(encoding='utf_8'))
                            except Exception as e:
                                self.set_headers(500)
                                self.wfile.write(bytes("ERROR: Something went wrong when fetching the flights: "+str(e), 'UTF-8'))
                        else:
                            self.set_headers(400)
                            self.wfile.write(bytes("ERROR: DepartureAirport and ArrivalAirport should both contain 4 letters.", 'UTF-8'))
                    except Exception as e:
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: TimeTo and TimeFrom should be of format datetime, DepartureAirport and ArrivalAirport should be strings.", 'UTF-8'))

               # That nice to have thing
                elif len(queryparams) == 2 and queryparams[0].split("=")[0] == "TimeFrom" \
                        and queryparams[1].split("=")[0] == "TimeTo":
                    try:
                        timeFrom = datetime.strptime(queryparams[0].split("=")[1].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        timeTo = datetime.strptime(queryparams[1].split("=")[1].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        if timeTo > timeFrom:
                            try:
                                flights = self.flightController.readByDepTimeArrTime(timeFrom, timeTo)
                                for flight in flights:
                                    i = 0
                                    for aircraft in flight.flightsFromThisAirport:
                                        flight.flightsFromThisAirport[i] = flight.flightsFromThisAirport[i].__dict__
                                        i = i + 1
                                parse = json.dumps([flight.__dict__ for flight in flights], default=str)
                                self.set_headers(200)
                                self.wfile.write(parse.encode(encoding='utf_8'))
                            except Exception as e:
                                print(e)
                                self.set_headers(500)
                                self.wfile.write(bytes("Something is wrong with the most complicated part of the code. "
                                                       "Sorry for that :*(: "+str(e), 'UTF-8'))
                        else:
                            self.set_headers(400)
                            self.wfile.write(bytes("ERROR: TimeFrom should be smaller than TimeTo.", 'UTF-8'))

                    except Exception as e:
                        self.set_headers(400)
                        self.wfile.write(bytes("ERROR: TimeFrom and TimeTo should be of format datetime.", 'UTF-8'))
                else:
                    self.set_headers(404)

        elif parsed.path == "/":
            self.set_headers(200)
            self.wfile.write(bytes("Welcome to MyAviation API.", 'UTF-8'))

        else:
            self.set_headers(404)
            self.wfile.write(bytes("ERROR: Page not found.", 'UTF-8'))

    def do_POST(self):
        try:
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = simplejson.loads(body)

            parsed = urlparse(self.path)

            # Create aircraft
            if parsed.path == "/Aircrafts":
                try:
                    serialNumber = str(data["SerialNumber"])
                    manufacturer = str(data["Manufacturer"])
                    try:
                        self.aircraftController.create(serialNumber, manufacturer)
                        self.set_headers(200)
                    except Exception as e:
                        print(e)
                        self.set_headers(500)
                        self.wfile.write(bytes(
                            "ERROR: Something went wrong when inserting the aircraft. Aircraft was not inserted: "+str(e),
                            'UTF-8'))
                except Exception as e:
                    print(str(e) + "is not in the correct format.")
                    self.set_headers(400)
                    self.wfile.write(bytes(
                        "Serial number of manufacturer are not in the correct format or are missing.",
                        'UTF-8'))

            # Create flight
            elif parsed.path == "/Flights":
                try:
                    departureAirport = str(data["DepartureAirport"])
                    arrivalAirport = str(data["ArrivalAirport"])
                    departureTime = datetime.strptime(data["DepartureTime"].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                    arrivalTime = datetime.strptime(data["ArrivalTime"].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                    aircraftId = None
                    try:
                        aircraftId = int(data["AircraftId"])
                    except:
                        pass
                    try:
                        self.flightController.create(departureAirport, arrivalAirport, departureTime, arrivalTime, aircraftId)
                        self.set_headers(200)
                    except Exception as e:
                        print(e)
                        self.set_headers(500)
                        self.wfile.write(bytes(
                            "ERROR: Something went wrong when saving the flight. Flight was not saved: "+str(e),
                            'UTF-8'))


                except Exception as e:
                    print(e)
                    self.set_headers(400)
                    self.wfile.write(bytes(
                        "Flight cannot be saved. Input data is in the wrong format.",
                        'UTF-8'))
            else:
                self.set_headers(404)
        except Exception as e:
            print(e)
            self.set_headers(400)
            self.wfile.write(bytes(
                "Error parsing input parameters.",
                'UTF-8'))

    def do_PUT(self):
        try:
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = simplejson.loads(body)

            parsed = urlparse(self.path)

            if parsed.path.startswith("/Aircrafts"):
                try:
                    id = int(self.path.split("/")[2])
                    serialNumber = None
                    try:
                        serialNumber = str(data["SerialNumber"])
                    except:
                        pass
                    manufacturer = None
                    try:
                        manufacturer = str(data["Manufacturer"])
                    except:
                        pass
                    if serialNumber is None and manufacturer is None:
                        self.set_headers(400)
                        self.wfile.write(bytes(
                            "Parameters are not in the correct format.",
                            'UTF-8'))
                        return
                    try:
                        self.aircraftController.update(id, serialNumber, manufacturer)
                        self.set_headers(200)
                    except Exception as e:
                        print(e)
                        self.set_headers(500)
                        self.wfile.write(bytes(
                            "ERROR: Something went wrong when updating the aircraft. Aircraft was not updated: " + str(
                                e),
                            'UTF-8'))
                except Exception as e:
                    print(e)
                    self.set_headers(400)
                    self.wfile.write(bytes(
                        "Parameters are not in the correct format.",
                        'UTF-8'))
            elif parsed.path.startswith("/Flights"):
                try:
                    id = int(self.path.split("/")[2])
                    departureAirport = None
                    try:
                        departureAirport = str(data["DepartureAirport"])
                    except:
                        pass
                    arrivalAirport = None
                    try:
                        arrivalAirport = str(data["ArrivalAirport"])
                    except:
                        pass
                    departureTime = None
                    try:
                        a = data["DepartureTime"]
                        try:
                            departureTime = datetime.strptime(data["DepartureTime"].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        except Exception as e:
                            print(e)
                            self.set_headers(400)
                            self.wfile.write(bytes(
                                "Departure time in the wrong format.",
                                'UTF-8'))
                            return
                    except:
                        pass
                    arrivalTime = None
                    try:
                        a = data["ArrivalTime"]
                        try:
                            arrivalTime = datetime.strptime(data["ArrivalTime"].replace("_", " "), '%Y-%m-%d %H:%M:%S')
                        except Exception as e:
                            print(e)
                            self.set_headers(400)
                            self.wfile.write(bytes(
                                "Arrival time in the wrong format.",
                                'UTF-8'))
                            return
                    except:
                        pass
                    aircraftId = None
                    try:
                        a = data["AircraftId"]
                        try:
                            aircraftId = int(data["AircraftId"])
                        except Exception as e:
                            print(e)
                            self.set_headers(400)
                            self.wfile.write(bytes(
                                "AircraftId should be integer.",
                                'UTF-8'))
                            return
                    except:
                        pass

                    if departureAirport is None and arrivalAirport is None and \
                            departureTime is None and arrivalTime \
                            is None and aircraftId is None:
                        self.set_headers(400)
                        self.wfile.write(bytes(
                            "Parameters are not in the correct format.",
                            'UTF-8'))
                    else:
                        try:
                            self.flightController.update(id, departureAirport, arrivalAirport, departureTime, arrivalTime,
                                                         aircraftId)
                            self.set_headers(200)
                        except Exception as e:
                            print(e)
                            self.set_headers(500)
                            self.wfile.write(bytes(
                                "ERROR: Something went wrong when updating the flight. Flight was not saved: " + str(e),
                                'UTF-8'))

                except Exception as e:
                    print(e)
                    self.set_headers(400)
                    self.wfile.write(bytes(
                        "Flight cannot be updated. Input data is in the wrong format.",
                        'UTF-8'))
            else:
                self.set_headers(404)
        except Exception as e:
            print(e)
            self.set_headers(400)
            self.wfile.write(bytes(
                "Error parsing input parameters.",
                'UTF-8'))

    def do_DELETE(self):
        try:
            parsed = urlparse(self.path)

            if parsed.path.startswith("/Aircrafts"):
                try:
                    id = int(parsed.path.split("/")[2])

                    try:
                        self.aircraftController.delete(id)
                        self.set_headers(200)
                    except Exception as e:
                        print(e)
                        self.set_headers(500)
                        self.wfile.write(bytes(
                            "Something went wrong when deleting the aircraft.",
                            'UTF-8'))

                except Exception as e:
                    print(e)
                    self.set_headers(400)
                    self.wfile.write(bytes(
                        "Id is not in the correct format.",
                        'UTF-8'))
            elif parsed.path.startswith("/Flights"):
                try:
                    id = int(parsed.path.split("/")[2])

                    try:
                        self.flightController.delete(id)
                        self.set_headers(200)
                    except Exception as e:
                        print(e)
                        self.set_headers(500)
                        self.wfile.write(bytes(
                            "Something went wrong when deleting the flight.",
                            'UTF-8'))

                except Exception as e:
                    print(e)
                    self.set_headers(400)
                    self.wfile.write(bytes(
                        "Id is not in the correct format.",
                        'UTF-8'))
            else:
                self.set_headers(404)
        except:
            self.set_headers(400)
            self.wfile.write(bytes("Error parsing the url."))




    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()