from Models.Aircraft import Aircraft


class AircraftRetriever:

    def __init__(self, dbcnctn):
        self.dbConnection = dbcnctn

    def transformIntoAircraftModel(self, aircraftsDb):

        if aircraftsDb is None:
            return None

        if not isinstance(aircraftsDb, list):
            return Aircraft(aircraftsDb[0], aircraftsDb[1], aircraftsDb[2])
        else:
            aircrafts = []

            for a in aircraftsDb:
                aircrafts.append(Aircraft(a[0], a[1], a[2]))
            return aircrafts

    def create(self, aircraft):

        q = "INSERT INTO Aircrafts(SerialNumber, Manufacturer) Values(%s, %s)"
        v = (aircraft.serialNumber, aircraft.manufacturer)

        return self.dbConnection.query(q, v)

    def readAll(self):
        q = "SELECT * FROM Aircrafts"

        aircraftsDb = self.dbConnection.query(q, None).fetchall()

        return self.transformIntoAircraftModel(aircraftsDb)

    def readById(self, id):

        q = "SELECT * FROM Aircrafts WHERE Id=%s"
        v = (str(id),)

        aircraftDb = self.dbConnection.query(q, v).fetchone()

        return self.transformIntoAircraftModel(aircraftDb)

    def readBySerialNumber(self, serialNumber):

        q = "SELECT * FROM Aircrafts WHERE SerialNumber=%s"
        v = (serialNumber,)

        aircraftDb = self.dbConnection.query(q, v).fetchone()

        return self.transformIntoAircraftModel(aircraftDb)

    def readByManufacturer(self, manufacturer):

        q = "SELECT * FROM Aircrafts WHERE Manufacturer=%s"
        v = (manufacturer,)

        aircraftsDb = self.dbConnection.query(q, v).fetchall()

        return self.transformIntoAircraftModel(aircraftsDb)

    def update(self, aircraft):

        q = "UPDATE Aircrafts SET SerialNumber=%s, Manufacturer=%s WHERE Id=%s"
        v = (aircraft.serialNumber, aircraft.manufacturer, aircraft.id)

        return self.dbConnection.query(q, v)

    def delete(self, aircraftId):

        q = "DELETE FROM Aircrafts WHERE Id=%s"
        v = (aircraftId,)

        return self.dbConnection.query(q, v)
