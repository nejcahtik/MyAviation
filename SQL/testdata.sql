use MyAviation2;

insert into Aircrafts(SerialNumber, Manufacturer) values ("10", "Boeing");
insert into Aircrafts(SerialNumber, Manufacturer) values ("11", "Airbus");
insert into Aircrafts(SerialNumber, Manufacturer) values ("12", "Pipistrel");
insert into Aircrafts(SerialNumber, Manufacturer) values ("13", "Pilatus");
insert into Aircrafts(SerialNumber, Manufacturer) values ("14", "Boeing");
insert into Aircrafts(SerialNumber, Manufacturer) values ("15", "Airbus");
insert into Aircrafts(SerialNumber, Manufacturer) values ("16", "Pipistrel");
insert into Aircrafts(SerialNumber, Manufacturer) values ("17", "Pilatus");
insert into Aircrafts(SerialNumber, Manufacturer) values ("18", "Soyuz");
insert into Aircrafts(SerialNumber, Manufacturer) values ("19", "BlueOrigin");

insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("LTAF", "LTCO", "2022-08-11 10:00:00", "2022-08-11 12:00:00", 1);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("LTAF", "LTAI", "2022-09-11 09:00:00", "2022-09-11 13:00:00", 1);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("EHAM", "LTAI", "2022-09-12 09:00:00", "2022-09-12 14:00:00", 2);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("LEBL", "ORBI", "2022-09-12 09:00:00", "2022-09-13 01:00:00", 2);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("LTCO", "LEBL", "2022-09-13 09:00:00", "2022-09-13 11:00:00", 3);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("EHAM", "LEBL", "2022-09-13 12:00:00", "2022-09-13 15:00:00", 3);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("LTCO", "OBBI", "2022-10-10 09:00:00", "2022-10-10 10:00:00", 4);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("LEBL", "ORBI", "2023-01-01 09:00:00", "2023-01-01 17:00:00", 4);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("LIPE", "LSGG", "2023-01-01 09:00:00", "2023-01-01 17:00:00", 5);
insert into Flights(DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftId) values ("LIPE", "LSGG", "2023-01-09 09:00:00", "2023-01-09 17:00:00", 5);

