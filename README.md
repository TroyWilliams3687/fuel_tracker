# Fuel Tracker

This is an application that can track and manage your fuel expenses. It will allow you to enter fuel expenses based on:

- Date
- Cost
- Liters added
- Mileage since last fill up

You will be able to register different vehicles in the database and associate the expenses with each vehicle.

The information will be stored in an SQLite database located in `~/.config/bluebill.net/fuel_tracker/data.db`.


## TODO

- `ft fuel add passat --date=2021-01-01 --fuel=48 --mileage=750 --cost=56.65 --partial --comment="Some reason"`

    - This will add a new fuel record to the database for the specified name of the vehicle (can also specify the vehicle_id).

    - `vehicle`
        - The vehicle must already exist in the database
        - The vehicle must be added prior to adding a fill up
        - The vehicle can be specified by a unique name or its row id in the database        

    - `--date` - The date in YYYY-mm-dd format, but should be setting in the configuration file as a format string for ` datetime.strptime()`
        - `%Y-%m-%d` - 2021-08-21 - `dt = datetime.strptime("2021-08-21", "%Y-%m-%d")`
        - `%d/%m/%y` - 21/11/06   - `dt = datetime.strptime("21/11/06", "%d/%m/%y")`
        - `%m/%d/%y` - 11/21/06
        - `%d/%m/%Y` - 21/11/2006
        - All dates will be stored in the database as ISO-8600 formatted dates (yyyy-mm-dd)
        - Default - `%Y-%m-%d`

    - `--fuel` 
        - The amount of fuel (liters or gal) added at the fill-up
        - Unit - liters (l) or US gallons (us_gal) - Default - l

    - `--mileage` 
        - The amount of mileage accumulated since the last fill-up
        - Unit - kilometers (km) or miles (mi) - Default - km

    - `--cost` 
        - The amount of money spent on the fill-up
        - assumed units of dollars.
        - In reality, we will store a number. We won't tag a currency unit to it. It will be up to the user to do the conversion to ensure a common currency is stored in the database

    - `--partial`
        - a simple flag that indicates that the fuel record will be for a partial fill.
        - this may be used in some calculations particularly fuel economy

    - `--comment`
        - Some sort of text description about the fuel record. Usually a reason for the `--partial`.

    - if the user simply issues `ft add passat`, they will be prompted for the information using the click prompt system:

    ```bash
    $ ft add
    >Date (YYYY-mm-dd): 2021-06-12
    >fuel (l): 45.35
    >mileage (km): 650.4
    >cost: 56.65
    >car:passat
    ```

    - The entry will be validated and incorrect values will be written so the user has the opportunity to correct them
        - The should simply have to enter them again - don't bother prompting for incorrect information
    - If the values are correct and valid (as best as the software can tell) it will display the values again with the record number in the database

>NOTE: If the `--vehicle` switch and any of the following are present on the CLI: `--date`, `--fuel`, `--mileage`, `--cost` fuel tracker will assume we are trying to enter an individual fuel entry.


- `ft fuel add passat --csv=file.csv`
- `ft fuel add passat --odf=data.ods`
- `ft fuel add passat --excel=data.xlsx`
    - It should be possible to add fuel records from a csv, ods or excel file, if the columns have the same names as the switches (the order doesn't matter)
    - We should provide a detailed exception report if there are problems with the data so it is easy to fix
    - need to have duplicate record checking for this
    - maybe this would be better as `ft fuel add passat bulk file.csv|data.ods|data.xlsx` <- not sure about this...


- `ft fuel remove 45 --dry-run`
    - The delete command will delete the fuel record with id
    - The delete process will print the details of the fuel record to STDOUT in-case they need to re-enter the record - it will be printed in a format that they can cut and past it to re-enter it into the database
    - if the `--dry-run` switch is used, it will print the fuel record it would remove


- `ft fuel edit 45 --cost=65.65`
    - Edit any of the values of the fuel record specified by the record id.
    - The values are switches that are the same as the `add` command.
    - at least one switch needs to be specified

- `ft database --new new_date.db`
    - create a new database at the location specified in the configuration file with the specified name
    - if no name is included it will use the name in the database    
    - If a database doesn't exist, one will be created automatically with the application starts and it hits the database for the first time
    - NOTE: This will overwrite an existing database - use with caution
    - NOTE: This shouldn't be something the user would have to do under normal circumstances

- `ft database`
    - lists various stats about the database
        - car count
        - fuel record count
        - table count
        - size
        - etc.

- `ft vehicle add passat --make=Volkswagen --model=passat --year=2015 --tank=70 --inital-odo=15`
    - adds a new car to the database with the identifier `passat`. The identifier can be used in other commands to easily select the car to work on. You will also be able to use the car record id.

- `ft vehicle remove passat --dry-run`
    - remove the car from the database and all
    - if the `--dry-run` switch is used, it will print the car it would remove along with the fuel records associated with it.
    - can specify the car by the identifier or the car record number

- `ft vehicle edit passat --tank=71`
    - edit a column of a car record
    - the switches match the `ft vehicle add` command
    - can specify the car by the identifier or the car record number

- `ft report passat soul matrix --date=-5 --excel --summary --yearly --monthly`
    - Generate a report on the fuel records for the car identifier for a particular date
    - it should be possible to get a report for a number of different cars

    - NOTE: it make make sense to add a command for each report type instead of switches

    - the `--date` switch can be 
        - a negative number from 0 to -inf. Which will be the weeks from the current date i.e. -1 represents last week to the current week. -5 represents 5 weeks ago all the way to the current week.
        - a start date and end date
        - a year - show all records for the year
        - a year-month - show all records for the month
    - `--excel`
        - display the report in excel, launching it
        - there should be a separate sheet for each car, for each report type
    - `--ods`
        - display the report in libre office calc

    - `--csv`
        - display the report as a csv file, launching it in the appropriate editor




## License

[MIT](https://choosealicense.com/licenses/mit/)

