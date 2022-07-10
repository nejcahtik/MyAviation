CREATE DATABASE MyAviation2;

use MyAviation2;

CREATE TABLE Aircrafts (
	Id int NOT NULL AUTO_INCREMENT,
	SerialNumber varchar(128) NOT NULL,
    Manufacturer varchar(128) NOT NULL,
    PRIMARY KEY (Id)
);

CREATE TABLE Flights (
	Id int NOT NULL AUTO_INCREMENT,
    DepartureAirport varchar(4) NOT NULL,
    ArrivalAirport varchar(4) NOT NULL,
    DepartureTime datetime NOT NULL,
    ArrivalTime datetime NOT NULL,
    AircraftId int,
    PRIMARY KEY (Id),
    FOREIGN KEY(AircraftId) REFERENCES Aircrafts(Id)
);