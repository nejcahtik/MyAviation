class Aircraft:

    def __init__(self, i, sn, mnf):
        self.id = i
        self.serialNumber = sn
        self.manufacturer = mnf

    def encode(self):
        return self.__dict__
