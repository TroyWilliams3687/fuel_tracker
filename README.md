# Fuel Tracker

This application that can track and manage your fuel expenses. It will allow you
to enter fuel expenses based on:

- Date
- Cost
- Liters added
- Mileage since last fill up

You will be able to register different vehicles in the database and associate
the expenses with each vehicle. The information will be stored in an SQLite
database located in `~/.config/bluebill.net/fuel_tracker/data.db`.

# Installation

You will need an operation version of Python installed and it should be at least
version 3.9. You'll need to create a virtual environment and install to that.
Finally, install from Github.

## Linux

If you use Linux, the installation steps are fairly basic. You will need to have
`Python` correctly installed on your path (>= v3.9):

```bash
$ python --version

Python 3.9.5
````

Upgrade `pip`:

```bash
$ python -m pip install --upgrade pip
````

Install the `virtualenv`:

```bash
$ python -m pip install virtualenv
````

Create the installation folder, for example, `~/opt/ft`:

```bash
$ cd ~

$ mkdir ft

$ cd ft
````

Create the virtual environment:

```bash
$ python -m venv .venv
```

Activate the virtual environment:

```bash

$ source .venv/bin/activate
```

Install Fuel Tracker:

```bash

$ python -m pip install git+https://github.com/TroyWilliams3687/fuel_tracker.git

````

## Windows

You will have to follow the same steps as the Linux installation. 

# Usage

## Vehicle

### Add

To add a vehicle to the database, issue the following command:

```bash
$ ft vehicle add
```

Where:

- `ft` - This is the name of the program to execute `ft = fuel tracker`.
- `vehicle` - This command tells fuel tracker we want to work with vehicles.
- `add` - This sub-command tells fuel tracker we want to add a new vehicle to the database.


With the bare command (above) you will be prompted for the missing information.

- name - A name that can be used to identify the vehicle. This can be the model of
 the vehicle or something more memorable or easier to type. It should be
 unique.

- make - The make of the vehicle. For example it could be VW, Ford or Toyota.

- model - This is the type of vehicle. For example it could be Passat, F-150 or
 Hilux

- year - The year of the vehicle. It should be 4 digits - 2021 for example.

- tank - The fuel capacity in liters

- initial-odo - The initial odometer reading in kilometers


Optionally, you can provide a list of switches with the correct information.
Don't worry, if you don't provide the switches, fuel tracker will prompt you
for the missing information. The switches are as follows:

```bash
$ ft vehicle add --name=passat --make=VW --model=Passat --year=2015 --tank=70 --initial-odo=0
```

### Edit

>NOTE: Currently not implemented. On Linux and Windows you can use [DB Browser for SQLite](https://sqlitebrowser.org/).  

### Remove

>NOTE: Currently not implemented. On Linux and Windows you can use [DB Browser for SQLite](https://sqlitebrowser.org/).  

### Show

## Fuel Record

### Add


Add new fuel records to the database for the vehicle. You must specify the
vehicle to attach the fuel record to by database id or by name. You can
optionally specify the switches or be prompted for the minimum data.

If you forget, what you have in the database, you can type:

```bash
$ ft fuel add
```

without a vehicle name or id and it will show you a list of valid entries. It
will show you a list of valid commands, simply copy and paste the correct one.


Add a fuel record by using the vehicle name:

```bash
$ ft fuel add passat
```

or by vehicle id:

```bash
$ ft fuel add 4
```

You can also use switches at the CLI if you like. If not, you will be prompted
for the information.

Switches:

```
  --date [%Y-%m-%d|%d/%m/%y|%m/%d/%y|%d/%m/%Y|%m/%d/%Y]
                                  The date fuel was added to the vehicle.
                                  Support 5 major date formats in the
                                  following order: Y-m-d, d/m/Y, d/m/y, m/d/Y,
                                  m/d/y (first match is taken)
  --fuel FLOAT                    The amount of fuel added to the vehicle.
  --mileage FLOAT                 The mileage since the last fill up.
  --cost FLOAT                    The full cost of the fuel.
  --partial BOOLEAN               Was this a partial fill up. Optional - you
                                  will not be prompted and have to set the
                                  switch.
  --comment TEXT                  A comment about this fuel record. Optional -
                                  you will not be prompted and have to set the
                                  switch.
  --help                          Show this message and exit.
```


>NOTE: The date format can be one of the following:
>
>  1. `%Y-%m-%d` - year-month-day  2021-08-12
>
>  2. `%d/%m/%y` - day/month/year  12/08/21
>
>  3. `%m/%d/%y` - month/day/year  08/12/21
>
>  4. `%d/%m/%Y` - day/month/year  12/08/2021
>
>  5. `%m/%d/%Y` - month/day/year  08/12/2021
>
 >NOTE: The first format to produce a correct date is used. The date is matched
  against the list in the order specified above. For example, `02/03/2021` can
  match 2 or 3 but will match 2 first. Beware. It is best to use the ISO 8601
  representation.

 > NOTE: If you use any of the date formats that have a `/`in them you will have
   to escape them on the CLI using quotation marks.


Example of prompts: 

```bash
$ ft fuel add passat
>Date: 2021-08-29
>Fuel: 45.893
>Mileage: 645.8
>Cost: 54.35

4 - passat
Date    = 2021-08-29 00:00:00
Fuel    = 45.893
Mileage = 645.8
Cost    = 54.35
Partial = None
Comment = None
Is the Fuel Record Correct? [Y/n]: 
```

>NOTE: It will not prompt for `partial` or `comment`. These switches must be
 specified as they are optional fields.

Add a fuel record to the vehicle (switches):

```bash
$ ft fuel add passat --date=2021-01-01 --fuel=48 --mileage=750 --cost=56.65 --partial --comment="Some reason"
```

### Edit

>NOTE: Currently not implemented. On Linux and Windows you can use [DB Browser for SQLite](https://sqlitebrowser.org/).  

### Remove

>NOTE: Currently not implemented. On Linux and Windows you can use [DB Browser for SQLite](https://sqlitebrowser.org/).  

### Show

>NOTE: Currently not implemented. On Linux and Windows you can use [DB Browser for SQLite](https://sqlitebrowser.org/).  

## Bulk Operations

### Add

You can bulk add new vehicles and fuel records to the database with a carefully
crafted spreadsheet. Fuel tracker supports both Excel and Open Office formatted
spreadsheets (`*.xlsx` and `*.ods`). The spreadsheet will need the following
columns defined:

- `name` - A name used to identify the vehicle. This name will be used by you
  when communicating with fuel tracker. Alternatively, you will also be able to
  specify a unique number representing the vehicle in the database. 

- `make` - The make of the vehicle (i.e. Ford, Toyota, Volkswagen). 

- `model` - The model of the vehicle (F-150, Passat, Camry).

- `year` - The year of the vehicle.

- `tank_capacity` - The tank capacity in liters.

- `initial_odometer` - The initial odometer reading when added to the system in
  kilometers.

- `fill_date` - The date you put fuel in your vehicle (yyyy-mm-dd).

- `mileage ` - The number of kilometers since the last fill date. Normally you
  would capture this on your trip meter.

- `fuel` - The amount of fuel added in liters.

- `cost` - The cost of the fuel.

- `partial` - Was this a partial fill up? That is, did you only put a small
  amount of fuel into the tank? `1` if you did, `0` or leave it empty if you
  didn't.

- `comment` - An optional description of the fuel record. You can record unusual
  things or the reason for a partial fill up.

>NOTE: The column order doesn't matter. You will have to duplicate the vehicle
 information for every fuel record - that is a requirement.

You can point directly to the spreadsheet:

```bash
$ ft bulk add ./data/vw-passat-2015.ods
```

You can specify multiple different spreadsheets:

```bash
$ ft bulk add ./data/vw-passat-2015.ods ./data/dodge-intrepid-1997.ods
```

You can specify a wild card to include all of the spreadsheets:

```bash
$ ft bulk add ./data/*.ods
```

> NOTE: The spreadsheet format matches the format of the [Bulk Export Option]
  (#export). So you can bulk export all of your records and then import those
  directly into a new database. It is a great way to backup your data in a
  format outside the database.

### Remove

You can bulk delete vehicles and all the records associated with them. You
specify the vehicle by `name` or by database `id`:

```bash
$ ft bulk delete passat 2
```

### Export

Export the vehicle(s) and its fuel records to various formats. The available
export formats are:

- `csv` - Export to CSV
- `excel` - Export to Excel
- `ods` - Export to Open Office
- `stdout` - Export to the terminal

The vehicle and fuel records will be combined into one table and exported to the
file. If an output format isn't selected, it will be displayed in the
terminal.

Display the records for the vehicles:

```bash
$ ft bulk export passat 2
```

Export the vehicles and fuel records to Excel:

```bash
$ ft bulk export passat interpid --excel=file.xlsx
```

>NOTE: When multiple vehicles are exported to a spreadsheet format new tabs, one
 for each vehicle will be created inside the spreadsheet. One file is created
 that contains all of the data separated by different sheets within the file.

Export the vehicles to the Open Office format (ODS):

```bash
$ ft bulk export passat interpid --ods=file.ods
```

Export the vehicles to CSV:

```bash
$ ft bulk export passat interpid --csv=file.csv
```

>NOTE: Exporting multiple vehicles to CSV will result in one CSV being created
 for each vehicle.

Export multiple vehicles to multiple different formats:

```bash
$ ft bulk export passat interpid --excel=file.xlsx --ods=file.ods --csv=file.csv
```

>NOTE: This is a good way of backing up the database in a different format.

## Report

### Show

Display the fuel records for the vehicle (by name or id). This option will also
show a yearly summary.

If you forget the vehicle name or id, type the command and a list of possible
values will be suggested. Copy/paste the command:

```bash
$ ft report show
```

Options:

```text
--tail INTEGER   Display the last `n` records. Defaults to 10. Use -1 to
               select all records.
--hide-partial   Hide the partial column.
--hide-comments  Hide the comments column.
--extra-summary  Include extra columns in the summary report
--help           Show this message and exit.
```

Display the summary for a specific vehicle:

```bash
$ ft report show passat
```

```text

id:            4
Name:          passat
Make:          Volkswagen
Model:         Passat
Year:          2015
Tank Capacity: 70.0
Odometer:      0.0

+---+-----------+------------+------+---------+--------+-------+-------+---------+----------+-----------+
|   | fuel (id) | fill date  | days | mileage |  fuel  | cost  |  $/l  | l/100km | mpg (us) | mpg (imp) |
+---+-----------+------------+------+---------+--------+-------+-------+---------+----------+-----------+
| 0 |    832    | 2021-01-31 |  48  |  778.0  | 26.278 | 29.41 | 1.119 |  3.378  |  69.639  |  83.633   |
| 1 |    833    | 2021-03-14 |  42  |  384.9  | 24.019 | 30.0  | 1.249 |  6.24   |  37.693  |  45.267   |
| 2 |    829    | 2021-06-05 |  83  |  273.5  | 47.281 | 60.0  | 1.269 | 17.287  |  13.606  |   16.34   |
| 3 |    828    | 2021-07-15 |  40  |  738.0  | 46.154 | 60.0  |  1.3  |  6.254  |  37.611  |  45.169   |
| 4 |    827    | 2021-08-17 |  33  |  861.5  | 45.872 | 60.0  | 1.308 |  5.325  |  44.175  |  53.051   |
| 5 |    838    | 2021-11-04 |  79  |  790.6  | 41.125 | 60.0  | 1.459 |  5.202  |  45.218  |  54.305   |
| 6 |    837    | 2021-11-22 |  18  |  759.8  | 41.152 | 60.0  | 1.458 |  5.416  |  43.428  |  52.155   |
| 7 |    834    | 2021-12-05 |  13  |  731.7  | 41.152 | 60.0  | 1.458 |  5.624  |  41.822  |  50.226   |
| 8 |    836    | 2021-12-12 |  7   |  551.3  | 41.152 | 60.0  | 1.458 |  7.465  |  31.511  |  37.843   |
| 9 |    835    | 2021-12-27 |  15  |  833.1  | 41.152 | 60.0  | 1.458 |  4.94   |  47.618  |  57.187   |
+---+-----------+------------+------+---------+--------+-------+-------+---------+----------+-----------+

Summary by Year:
+---+------+----------+-----------------+--------------+--------------+-----------+---------------+----------------+-----------------+
|   | year | Fill-Ups | Mileage (Total) | Fuel (Total) | Cost (Total) | $/l (Avg) | l/100km (Avg) | mpg (us) (Avg) | mpg (imp) (Avg) |
+---+------+----------+-----------------+--------------+--------------+-----------+---------------+----------------+-----------------+
| 0 | 2015 |    33    |     30787.0     |   1703.345   |    1818.9    |   1.068   |     5.533     |     42.514     |     51.057      |
| 1 | 2016 |    28    |     26317.3     |   1476.104   |   1378.62    |   0.934   |     5.609     |     41.936     |     50.363      |
| 2 | 2017 |    30    |     26221.8     |   1483.908   |   1561.36    |   1.052   |     5.659     |     41.564     |     49.917      |
| 3 | 2018 |    20    |     16975.6     |   980.231    |   1201.23    |   1.225   |     5.774     |     40.734     |      48.92      |
| 4 | 2019 |    26    |     22831.9     |   1327.747   |   1582.42    |   1.192   |     5.815     |     40.447     |     48.575      |
| 5 | 2020 |    15    |     13179.8     |   800.271    |    882.02    |   1.102   |     6.072     |     38.738     |     46.522      |
| 6 | 2021 |    10    |     6702.4      |   395.337    |    539.41    |   1.364   |     5.898     |     39.877     |     47.891      |
+---+------+----------+-----------------+--------------+--------------+-----------+---------------+----------------+-----------------+

```

# License

[MIT](https://choosealicense.com/licenses/mit/)

