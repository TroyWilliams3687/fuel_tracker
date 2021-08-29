# Fuel Tracker

This is an application that can track and manage your fuel expenses. It will allow you to enter fuel expenses based on:

- Date
- Cost
- Liters added
- Mileage since last fill up

You will be able to register different vehicles in the database and associate the expenses with each vehicle.

The information will be stored in an SQLite database located in `~/.config/bluebill.net/fuel_tracker/data.db`.

# Installation

# Usage

## Vehicle

### Add

To add a vehicle to the database, issue the following command:

```bash
$ ft vehicle add --name=passat --make=VW --model=Passat --year=2015 --tank=70 --initial-odo=0
```

Where:

- `ft` - This is the name of the program to execute `ft = fuel tracker`.
- `vehicle` - This command tells fuel tracker we want to work with vehicles.
- `add` - This sub-command tells fuel tracker we want to add a new vehicle to the database.

Optionally, you can provide a list of switches with the correct information. Don't worry, if you don't provide the switches, fuel tracker will prompt you for the correct information. The switches are as follows:

- `--name=passat` - A name used to identify the vehicle. This name will be used by you when communicating with fuel tracker. Alternatively, you will also be able to specify a unique number representing the vehicle in the database. 
- `--make=VW` - The make of the vehicle (i.e. Ford, Toyota, Volkswagen). 
- `--model=Passat` - The model of the vehicle (F-150, Passat, Camry).
- `--year=2015` - The year of the vehicle.
- `--tank=70`  - The tank capacity in liters.
- `--initial-odo=0` - The initial odometer reading when added to the system in kilometers.

### Edit

### Remove

### Show


## Fuel Record

### Add

Add new fuel records to the database for the vehicle. You must specify the vehicle to attach the fuel record to by database id or by name. You can optionally specify the switches or be prompted for the minimum data.

 - `vehicle`
    - The vehicle must already exist in the database.
    - The vehicle must be added prior to adding a fill up.
    - The vehicle can be specified by a unique name or its row id in the database.        
- `--date` - The date fuel was added to the vehicle. The input accepts the following date formats (in that order):
    1. `%Y-%m-%d` - year-month-day  2021-08-12 - `dt = datetime.strptime("2021-08-21", "%Y-%m-%d")`    
    1. `%d/%m/%y` - day/month/year - 12/08/21
    1. `%m/%d/%y` - month/day/year - 08/12/21  - `dt = datetime.strptime("21/11/06", "%d/%m/%y")`
    1. `%d/%m/%Y` - day/month/year - 12/08/2021
    1. `%m/%d/%Y` - month/day/year - 08/12/2021
    - All dates will be stored in the database as ISO-8600 formatted dates (yyyy-mm-dd).    
- `--fuel` 
    - The amount of fuel (liters or gal) added at the fill-up.    
- `--mileage` 
    - The amount of mileage accumulated since the last fill-up.   
- `--cost` 
    - The amount of money spent on the fuel.        
- `--partial`
    - a simple flag that indicates that the fuel record will be for a partial fill.
    - this may be used in some calculations particularly fuel economy.
- `--comment`
    - Some sort of text description about the fuel record. Usually a reason for the `--partial`.


Add a fuel record to the vehicle (prompt):
```bash
$ ft fuel add passat
```

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

>NOTE: It will not prompt for `partial` or `comment`. These switches must be specified as they are optional fields.

Add a fuel record to the vehicle (switches):
```bash
$ ft fuel add passat --date=2021-01-01 --fuel=48 --mileage=750 --cost=56.65 --partial --comment="Some reason"
```

### Edit

### Remove

### Show

## Bulk Operations

### Add

You can bulk add new vehicles and fuel records to the database with a carefully crafted spreadsheet. Fuel tracker supports both Excel and Open Office formatted spreadsheets (`*.xlsx` and `*.ods`). The spreadsheet will need the following columns defined:

- `name` - A name used to identify the vehicle. This name will be used by you when communicating with fuel tracker. Alternatively, you will also be able to specify a unique number representing the vehicle in the database. 
- `make` - The make of the vehicle (i.e. Ford, Toyota, Volkswagen). 
- `model` - The model of the vehicle (F-150, Passat, Camry).
- `year` - The year of the vehicle.
- `tank_capacity` - The tank capacity in liters.
- `initial_odometer` - The initial odometer reading when added to the system in kilometers.
- `fill_date` - The date you put fuel in your vehicle (yyyy-mm-dd).
- `mileage ` - The number of kilometers since the last fill date. Normally you would capture this on your trip meter.
- `fuel` - The amount of fuel added in liters.
- `cost` - The cost of the fuel.
- `partial` - Was this a partial fill up? That is, did you only put a small amount of fuel into the tank? `1` if you did, `0` or leave it empty if you didn't.
- `comment` - An optional description of the fuel record. You can record unusual things or the reason for a partial fill up.

>NOTE: The column order doesn't matter. You will have to duplicate the vehicle information for every fuel record - that is a requirements

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

> NOTE: The spreadsheet format matches the format of the [Bulk Export Option](#export). So you can bulk export all of your records and then import those directly into a new database. It is a great way to backup your data in a format outside the database.

### Remove

You can bulk delete vehicles and all the records associated with them. You specify the vehicle by `name` or by database `id`.

```bash
$ ft bulk delete passat 2
```

### Export

Export the vehicle(s) and its fuel records to various formats. The available export formats are:

- `csv` - Export to CSV
- `excel` - Export to Excel
- `ods` - Export to Open Office
- `stdout` - Export to the terminal

The vehicle and fuel records will be combined into one table and exported to the file. If an output format isn't selected, it will be displayed in the terminal.

Display the records for the vehicles:
```bash
$ ft bulk export passat 2
```

Export the vehicles and fuel records to Excel:
```bash
$ ft bulk export passat interpid --excel=file.xlsx
```

>NOTE: When multiple vehicles are exported to a spreadsheet format new tabs, one for each vehicle will be created inside the spreadsheet. One file is created that contains all of the data separated by different sheets within the file.

Export the vehicles to the Open Office format:
```bash
$ ft bulk export passat interpid --ods=file.ods
```

Export the vehicles to CSV:
```bash
$ ft bulk export passat interpid --csv=file.csv
```

>NOTE: Exporting multiple vehicles to CSV will result in one CSV being created for each vehicle.

Export multiple vehicles to multiple different formats:
```bash
$ ft bulk export passat interpid --excel=file.xlsx --ods=file.ods --csv=file.csv
```

## Report

### Show

```bash
$ ft report show passat
```


### Export

```bash
$ ft report export passat
```

# TODO


# License

[MIT](https://choosealicense.com/licenses/mit/)

