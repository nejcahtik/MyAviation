# MyAviation

## Installation

1. In order to initialize the database, run ./SQL/createdb.sql script
2. To load test data, run ./SQL/testdata.sql script
3. Open ./config.json file and set the parameters for SQL server and the main server
4. Run main.py file

## API endpoints

### GET

#### Aircrafts

1. Request: {main_url}/Aircrafts - retrieve all the aircrafts, saved in the database\
Response example:\
[{"id": 1, "serialNumber": "10", "manufacturer": "Boeing"}, {"id": 2, "serialNumber": "11", "manufacturer": "Airbus"}, {"id": 3, "serialNumber": "12", "manufacturer": "Pipistrel"}, {"id": 4, "serialNumber": "13", "manufacturer": "Pilatus"}, {"id": 5, "serialNumber": "14", "manufacturer": "Boeing"}, {"id": 6, "serialNumber": "15", "manufacturer": "Airbus"}, {"id": 7, "serialNumber": "16", "manufacturer": "Pipistrel"}, {"id": 8, "serialNumber": "17", "manufacturer": "Pilatus"}, {"id": 9, "serialNumber": "18", "manufacturer": "Soyuz"}, {"id": 10, "serialNumber": "19", "manufacturer": "BlueOrigin"}]

2. Request: {main_url}/Aircrafts?Id={Id} - retrieve the aircraft with certain Id (should be integer)\
Response example:\
{
    "id": 1,
    "serialNumber": "10",
    "manufacturer": "Boeing"
}


3. Request: {main_url}/Aircrafts?SerialNumber={sn} - retrieve the aircraft with certain serial number\
Response example:\
{
    "id": 6,
    "serialNumber": "15",
    "manufacturer": "Airbus"
}

4. Request {main_url}/Aircrafts?Manufacturer={m} - retrieve all the aircrafts, manufactured by certain manufacturer\
Response example:\
[{"id": 1, "serialNumber": "10", "manufacturer": "Boeing"}, {"id": 5, "serialNumber": "14", "manufacturer": "Boeing"}]

#### Flights

1. Request {main_url}/Flights - retrieve all the flights, saved in the database\
Response example:\
[{"id": 1, "departureAirport": "LTAF", "arrivalAirport": "LTCO", "departureTime": "2022-08-11 10:00:00", "arrivalTime": "2022-08-11 12:00:00", "aircraft": {"id": 1, "serialNumber": "10", "manufacturer": "Boeing"}}, {"id": 2, "departureAirport": "LTAF", "arrivalAirport": "LTAI", "departureTime": "2022-09-11 09:00:00", "arrivalTime": "2022-09-11 13:00:00", "aircraft": {"id": 1, "serialNumber": "10", "manufacturer": "Boeing"}}, {"id": 3, "departureAirport": "EHAM", "arrivalAirport": "LTAI", "departureTime": "2022-09-12 09:00:00", "arrivalTime": "2022-09-12 14:00:00", "aircraft": {"id": 2, "serialNumber": "11", "manufacturer": "Airbus"}}, {"id": 4, "departureAirport": "LEBL", "arrivalAirport": "ORBI", "departureTime": "2022-09-12 09:00:00", "arrivalTime": "2022-09-13 01:00:00", "aircraft": {"id": 2, "serialNumber": "11", "manufacturer": "Airbus"}}, {"id": 5, "departureAirport": "LTCO", "arrivalAirport": "LEBL", "departureTime": "2022-09-13 09:00:00", "arrivalTime": "2022-09-13 11:00:00", "aircraft": {"id": 3, "serialNumber": "12", "manufacturer": "Pipistrel"}}]

3. Request {main_url}/Flights?Id={id} - retrieve the flight with certain id (should be integer)\
Response example:\
{"id": 4, "departureAirport": "LEBL", "arrivalAirport": "ORBI", "departureTime": "2022-09-12 09:00:00", "arrivalTime": "2022-09-13 01:00:00", "aircraft": {"id": 2, "serialNumber": "11", "manufacturer": "Airbus"}}

4. Request {main_url}/Flights?DepartureAirport={dep_air} - retrieve all the flights that departure from certain airport (variable {dep_air} should be ICAO code (4 letter string))\
*NOTE: Instead of the parameter 'DepartureAirport', parameter 'ArrivalAirport' can be used to retrieve all the flights that fly to certain airport (should again be ICAO code)\
Response example:\
[{"id": 5, "departureAirport": "LTCO", "arrivalAirport": "LEBL", "departureTime": "2022-09-13 09:00:00", "arrivalTime": "2022-09-13 11:00:00", "aircraft": {"id": 3, "serialNumber": "12", "manufacturer": "Pipistrel"}}, {"id": 7, "departureAirport": "LTCO", "arrivalAirport": "OBBI", "departureTime": "2022-10-10 09:00:00", "arrivalTime": "2022-10-10 10:00:00", "aircraft": {"id": 4, "serialNumber": "13", "manufacturer": "Pilatus"}}]

5. Request {main_url}/Flights?DepartureAirport={dep_air}&ArrivalAirport={arr_air} - retrieve all the flights that departure from certain departure airport and fly to certain arrival airport (both of the variables should be ICAO codes)

6. Request {main_url}/Flights?DepartureTimeFrom={dep_time_from}&DepartureTimeTo={dep_time_to} - retrieve all the flights with departure time inside the given time interval (times should always be of format: "YYYY-MM-DD_HH:MM:SS")

7. Request {main_url}/Flights?DepartureAirport={dep_air}&DepartureTimeFrom={dep_time_from}&DepartureTimeTo={dep_time_to} - retrieve all the flights that departure from certain airport inside the given time interval ({dep_air} should be a ICAO code and times should be of format: "YYYY-MM-DD_HH:MM:SS")

8. Request {main_url}/Flights?DepartureAirport={dep_air}&ArrivalAirport={arr_air}&DepartureTimeFrom={dep_time_from}&DepartureTimeTo={dep_time_to} - retrieve all the flights that departure from certain airport and fly to certain airport inside the given time interval ({dep_air} and {arr_air} should be ICAO codes and times should be of format "YYYY-MM-DD_HH:MM:SS")

9. (Nice to have thing): Request {main_url}/Flights?TimeFrom={time_from}&TimeTo={time_to} - retrieve, for a given period of time, the list of the departure airports of all flights flying - partially or not - within this time range, and for each departure airport, the number of flights as well as the in-flight time for each aircraft. The in-flight time taken into account should be strictly within the time range, and the average time is expressed in minutes.
Response example:
[[('EHAM', 3), (2, Decimal('2520')), (3, Decimal('600'))], [('LEBL', 2), (2, Decimal('2520')), (4, Decimal('1080'))], [('LIPE', 2), (5, Decimal('67320'))], [('LTAF', 2), (1, Decimal('720'))], [('LTCO', 2), (3, Decimal('600')), (4, Decimal('1080'))]]\


What does [('EHAM', 3), (2, Decimal('2520')), (3, Decimal('600'))] mean?

"('EHAM', 3)" - there are three flights that fly (partially or not) in the given time interval departure from the airport 'EHAM'\

"(2, Decimal('2520')), (3, Decimal('600')" - flights that have aircrafts already assigned and departure from 'EHAM' are listed here - the list consists of aircraft id (first element of a tuple) and total in-flight time in the given time interval (second element of a tuple)\

The format of the response is a subject of future improvements

### POST

#### Aircrafts

1. Request {main_url}/Aircrafts\
body:
{
    "SerialNumber"="{serial_number}",
    "Manufacturer"="{manufacturer}"
}

save a new aircraft into the database

#### Flights

1. Request {main_url}/Flights\
body:\
{\
    "DepartureAirport": "{departure_airport}",\
    "ArrivalAirport": "{arrival_airport}",\
    "DepartureTime": "{departure_time}",\
    "ArrivalTime": "arrival_time",
    "AircraftId": "{aircraft_id}"\
}\

save a new flight into the database\

NOTE: Departure and arrival airport should be ICAO codes, times should be of format "YYYY-MM-DD_HH:MM:SS"\
NOTE: AircraftId can be omitted (null value is saved to the database instead)\


### PUT

#### Aircrafts

1. Request {main_url}/Aircrafts/{id}\
body:\ 
{\
    "SerialNumber"="{serial_number}",\
    "Manufacturer"="{manufacturer}"\
}\

update the aircraft with id={id}\
The body should consist only of values needed to be updated

#### Flights

1. Request {main_url}/Flights/{id}\
body:\
{\
    "DepartureAirport": "{departure_airport}",\
    "ArrivalAirport": "{arrival_airport}",\
    "DepartureTime": "{departure_time}",\
    "ArrivalTime": "arrival_time",
    "AircraftId": "{aircraft_id}"\
}\

update the flight with id={id}\
The body should consist only of values needed to be updated

NOTE: Departure and arrival airport should be ICAO codes, times should be of format "YYYY-MM-DD_HH:MM:SS"\

### DELETE

#### Aircrafts

1. Request {main_url}/Aircrafts/{id} - delete the aircraft with id={id} from the database

#### Flights

1. Request {main_url}/Flights/{id} - delete the flight with id={id} from the database















