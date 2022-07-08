# MyAviation

## Installation

1. In order to initialize the database, run ./SQL/createdb.sql script
2. To load test data, run ./SQL/testdata.sql script
3. Open ./config.json file and set the parameters for SQL server and the main server
4. Run main.py file

## API endpoints

### GET

#### Aircrafts

1. Request: {main_url}/Aircrafts - retrieve all the aircrafts, saved in the database
Response example:
[{"id": 1, "serialNumber": "10", "manufacturer": "Boeing"}, {"id": 2, "serialNumber": "11", "manufacturer": "Airbus"}, {"id": 3, "serialNumber": "12", "manufacturer": "Pipistrel"}, {"id": 4, "serialNumber": "13", "manufacturer": "Pilatus"}, {"id": 5, "serialNumber": "14", "manufacturer": "Boeing"}, {"id": 6, "serialNumber": "15", "manufacturer": "Airbus"}, {"id": 7, "serialNumber": "16", "manufacturer": "Pipistrel"}, {"id": 8, "serialNumber": "17", "manufacturer": "Pilatus"}, {"id": 9, "serialNumber": "18", "manufacturer": "Soyuz"}, {"id": 10, "serialNumber": "19", "manufacturer": "BlueOrigin"}]

2. Request: {main_url}/Aircrafts?Id={Id} - retrieve the aircraft with certain Id (should be integer)
Response example:
{
    "id": 1,
    "serialNumber": "10",
    "manufacturer": "Boeing"
}

3. Request: {main_url}/Aircrafts?SerialNumber={sn} - retrieve the aircraft with certain serial number
Response example:
{
    "id": 6,
    "serialNumber": "15",
    "manufacturer": "Airbus"
}

4. Request {main_url}/Aircrafts?Manufacturer={m} - retrieve all the aircrafts, manufactured by certain manufacturer
Response example:
[{"id": 1, "serialNumber": "10", "manufacturer": "Boeing"}, {"id": 5, "serialNumber": "14", "manufacturer": "Boeing"}]

#### Flights

1. Request {main_url}/Flights - retrieve all the flights, saved in the database
Response example:
[{"id": 1, "departureAirport": "LTAF", "arrivalAirport": "LTCO", "departureTime": "2022-08-11 10:00:00", "arrivalTime": "2022-08-11 12:00:00", "aircraft": {"id": 1, "serialNumber": "10", "manufacturer": "Boeing"}}, {"id": 2, "departureAirport": "LTAF", "arrivalAirport": "LTAI", "departureTime": "2022-09-11 09:00:00", "arrivalTime": "2022-09-11 13:00:00", "aircraft": {"id": 1, "serialNumber": "10", "manufacturer": "Boeing"}}, {"id": 3, "departureAirport": "EHAM", "arrivalAirport": "LTAI", "departureTime": "2022-09-12 09:00:00", "arrivalTime": "2022-09-12 14:00:00", "aircraft": {"id": 2, "serialNumber": "11", "manufacturer": "Airbus"}}, {"id": 4, "departureAirport": "LEBL", "arrivalAirport": "ORBI", "departureTime": "2022-09-12 09:00:00", "arrivalTime": "2022-09-13 01:00:00", "aircraft": {"id": 2, "serialNumber": "11", "manufacturer": "Airbus"}}, {"id": 5, "departureAirport": "LTCO", "arrivalAirport": "LEBL", "departureTime": "2022-09-13 09:00:00", "arrivalTime": "2022-09-13 11:00:00", "aircraft": {"id": 3, "serialNumber": "12", "manufacturer": "Pipistrel"}}]

2. Request {main_url}/Flights?DepartureAirport={dep_air} - retrieve all the flights that departure from certain airport
*NOTE: Instead of the parameter 'DepartureAirport', parameter 'ArrivalAirport' can be used to retrieve all the flights that fly to certain airport
Response example:
[{"id": 5, "departureAirport": "LTCO", "arrivalAirport": "LEBL", "departureTime": "2022-09-13 09:00:00", "arrivalTime": "2022-09-13 11:00:00", "aircraft": {"id": 3, "serialNumber": "12", "manufacturer": "Pipistrel"}}, {"id": 7, "departureAirport": "LTCO", "arrivalAirport": "OBBI", "departureTime": "2022-10-10 09:00:00", "arrivalTime": "2022-10-10 10:00:00", "aircraft": {"id": 4, "serialNumber": "13", "manufacturer": "Pilatus"}}]
















