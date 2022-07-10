from DatabaseRetrievers.AircraftRetriever import AircraftRetriever
from Models.Aircraft import Aircraft


class AircraftController:

    def __init__(self, dbconnection):
        self.aircraftRetriever = AircraftRetriever(dbconnection)

    def checkForAircraftData(self, serialNumber, manufacturer):
        if not isinstance(serialNumber, str):
            return "serial number"
        if not isinstance(manufacturer, str):
            return "manufacturer"
        return False

    def fetchAllAircrafts(self):
        try:
            aircrafts = self.aircraftRetriever.readAll()
        except Exception as e:
            raise Exception("Error while fetching all the aircrafts:" + str(e))

        return aircrafts

    def fetchById(self, serialNumber):
        try:
            aircraft = self.aircraftRetriever.readById(serialNumber)
        except Exception as e:
            raise Exception("Error while fetching aicraft with serial number=%s: %s" % (serialNumber, str(e)))

        return aircraft

    def fetchByManufacturer(self, manufacturer):
        try:
            aircrafts = self.aircraftRetriever.readByManufacturer(manufacturer)
        except Exception as e:
            raise Exception("Error while fecthing aircrafts made by=%s: %s" % (manufacturer, str(e)))

        return aircrafts

    def fetchBySerialNumber(self, serialNumber):
        try:
            aircraft = self.aircraftRetriever.readBySerialNumber(serialNumber)
        except Exception as e:
            raise Exception("Error while fetching aicraft with serial number=%s: %s" % (serialNumber, str(e)))

        return aircraft

    def update(self, id, serialNumber, manufacturer):

        aircraft = self.fetchById(id)

        if serialNumber is not None:
            aircraft.serialNumber = serialNumber
        if manufacturer is not None:
            aircraft.manufacturer = manufacturer

        c = self.checkForAircraftData(aircraft.serialNumber, aircraft.manufacturer)
        if not c:

            try:
                return self.aircraftRetriever.update(aircraft)
            except Exception as e:
                raise Exception("Exception when updating the database for aircraft with id=% and manufacturer=%s.: %s" %
                                (id, manufacturer, str(e)))
        else:
            raise Exception(
                "Wrong Format Exception (for " + c + ") when updating aircraft with serial number=" + serialNumber + " and manufacturer=" + manufacturer + ".")

    def delete(self, id):
        try:
            return self.aircraftRetriever.delete(id)
        except Exception as e:
            raise Exception("Could not delete aircraft with id=%s from the database: %s" %
                            (id, str(e)))

    def create(self, serialNumber, manufacturer):
        c = self.checkForAircraftData(serialNumber, manufacturer)

        if not c:
            aircraft = Aircraft(0, serialNumber, manufacturer)
            try:
                return self.aircraftRetriever.create(aircraft)
            except Exception as e:
                raise Exception("Exception when inserting into the database aircraft with id=%s and "
                                "manufacturer=%s: %s" %
                                (id, manufacturer, str(e)))
        else:
            raise Exception(
                "Wrong Format Exception (for " + c + ") when inserting aircraft with serial number=" + serialNumber + " and manufacturer=" + manufacturer + ".")
