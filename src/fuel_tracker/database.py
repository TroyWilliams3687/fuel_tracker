#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   9f065888-02c0-11ec-8c3c-c906c7d81bd1
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-08-21
# -----------

"""

"""

# ------------
# System Modules - Included with Python

from dataclasses import dataclass, fields, field
from datetime import date

# ------------
# 3rd Party - From PyPI


# ------------
# Custom Modules

# -------------


# ---------
# SQL Statements

sql = {}

sql["insert"] = {}
sql["select"] = {}
sql["create"] = {}
sql["drop"] = {}

# ---------
# Create

sql["create"]["vehicle"] = """
CREATE TABLE VEHICLE(
    vehicle_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT NOT NULL UNIQUE,
    make             TEXT NOT NULL,
    model            TEXT NOT NULL,
    year             INTEGER DEFAULT 0,
    tank_capacity    INTEGER DEFAULT 0,
    initial_odometer INTEGER DEFAULT 0
);"""

sql["create"][
    "fuel"
] = """
CREATE TABLE FUEL(
    fuel_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    fill_date   TIMESTAMP NOT NULL,
    mileage     FLOAT NOT NULL DEFAULT 0 CHECK (mileage > 0),
    fuel        FLOAT NOT NULL DEFAULT 0 CHECK (fuel > 0),
    cost        FLOAT NOT NULL DEFAULT 0 CHECK (cost >= 0),
    partial     BOOLEAN NOT NULL DEFAULT 0 CHECK (partial IN (0,1)),
    comment     TEXT,
    vehicle_id  INTEGER DEFAULT 0,
    FOREIGN KEY(vehicle_id) REFERENCES VEHICLE(vehicle_id)
);"""

# ---------
# Drop

sql["drop"]["vehicle"] = "DROP TABLE IF EXISTS Vehicle;"
sql["drop"]["fuel"] = "DROP TABLE IF EXISTS Fuel;"


# ---------
# Select Statements

sql["select"]["vehicles"] = """
SELECT
  vehicle_id,
  name,
  make,
  model,
  year,
  tank_capacity,
  initial_odometer,
FROM VEHICLE
"""


sql["select"]["fuel_records"] = """
SELECT
    fuel_id,
    fill_date,
    mileage,
    fuel,
    cost,
    partial,
    comment,
    vehicle_id
FROM FUEL
"""

# ---------
# Insert Statements

sql["insert"]["vehicle"] = """
INSERT INTO
Vehicle(name,
        make,
        model,
        year,
        tank_capacity,
        initial_odometer)
VALUES(?, ?, ?, ?, ?, ?)
"""


sql["insert"]["fuel_record"] = """
INSERT INTO
Fuel(fuel_date,
     mileage,
     fuel,
     cost,
     partial,
     comment,
     vehicle_id)
VALUES(?, ?, ?, ?, ?, ?, ?)
"""


# def prepare_data(item):
#     """
#     Create a dictionary containing the field names and the
#     corresponding values in a form suitable for use in SQL prepared statements.

#     The dictionary will contain the following fields:
#     - table - The name of the class - assumes that the class name matches the table name
#     - columns - Columns names that are not None
#     - values - Column values

#     """

#     results = {}
#     results['table'] = item.__class__.__name__
#     results['columns'] = (f.name for f in fields(item) if getattr(f.name) is not None)
#     results['values'] = (getattr(key) for key in results['fields'] )

#     return results

# --------
# use .astuple or .asdict to get the information in a way that makes sense
# To us in the items, simple do the .astuple and use slicing to skip the first element, i.e. the id


@dataclass()
class Vehicle:
    """

    A simple class to represent a row in the Vehicle table

    # Parameters (kwargs)


    # Attributes

    pk_vehicle_id:int
        - The Database ID of the vehicle
        - OPTIONAL, left as None, indicates this is a new vehicle to
          add to the database

    name: str
        - A friendly name/identifier that is easy to remember so
          specific data can be sent to the vehicle
        - It can be used instead of the dbid of the vehicle
        - This value should be specified at a minimum if dbid is not set
        - DEFAULT - None


    make
    model
    year
    tank_capacity
    initial_odometer

    """

    vehicle_id: int = None
    name: str = None
    make: str = None
    model: str = None
    year: int = None
    tank_capacity: float = None
    initial_odometer: float = None

    def __post_init__(self):
        """ """

        if self.dbid is None and self.name is None:
            raise ValueError("dbid and name is None. At least one must be set!")


@dataclass()
class FuelRecord:
    """


    # Parameters (kwargs)


    # Attributes

    pk_fuel_id:int
        - The Database ID of the record
        - OPTIONAL, left as None, indicates this is a new record to
          add to the database



    fuel_date
    mileage
    fuel
    cost
    partial
    comment
    vehicle_id

    """

    fuel_id: int = None
    fuel_date: date = None
    mileage: float = None
    fuel: float = None
    cost: float = None
    partial: bool = False
    comment: str = None
    vehicle_id: int = None

    def __post_init__(self):
        """ """

        # Check for values that cannot be None
        for k in ("fuel_date", "mileage", "vehicle_id", "fuel", "cost"):

            if getattr(self, k) is None:
                raise ValueError(f"{k} cannot be None!")

        # Is Mileage >= 0?
        if self.mileage <= 0:
            raise ValueError("mileage cannot be less than or equal to 0!")

        # Is Cost > 0?
        if self.cost < 0:
            raise ValueError("cost cannot be less than 0!")


class Database:
    """
    """

    def __init__(self, database):
        """
        """

        self.database = database

        self.connection = sqlite3.connect(
            database,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def last_row_id(self):
        """
        """

        return self.cursor.lastrowid


    def insert_vehicles(self, vehicles):
        """
        Insert the list of vehicles into the database. If you have one
        vehicle, wrap it in a list. The will be added as new entries.


        Given the prepared SQL statement, insert all of the data items
        into the database.

        Essentially, it will iterate through all of the items in the
        iterable and execute the SQL for each item

        """

        self.cursor.executemany(
            sql["insert"]["vehicle"],
            [v.astuple()[1:] for v in vehicles], # We don't include the pk_vehicle_id field included
        )

        self.connection.commit()

    def insert_fuel_records(self, fuel_records):
        """
        Insert the list of fuel records into the database. If you have
        one, wrap it in a list. These will be added as new entries.

                Given the prepared SQL statement, insert all of the data items
        into the database.

        Essentially, it will iterate through all of the items in the
        iterable and execute the SQL for each item

        """

        self.cursor.executemany(
            sql["insert"]["fuel_record"],
            [fr.astuple()[1:] for fr in fuel_records], # We don't include the pk_fuel_record_id field
        )

        self.connection.commit()

    def select_vehicles(self, **kwargs):
        """
        Retrieve all of the vehicles from the database and return a list
        of Vehicle objects.

        If kwargs contains 'vehicle_id' it will attempt to
        retrieve that row

        """

        # Execute the query, iterate through the results and construct
        # the list of Vehicles stored in the database

        sql = sql["select"]["vehicles"]

        # Do we need to make a prepared statement?
        if 'vehicle_id' in kwargs:
            sql += 'Where vehicle_id = ?'

        return [
            Vehicle(*row)
            for row in self.cursor.execute(sql, kwargs.get('vehicle_id', None))
        ]

    def select_fuel_records(self, **kwargs):
        """
        Retrieve all of the fuel_records from the database and return a
        list of FuelRecord objects.

        if kwargs contains 'vehicle_id' it will attempt to filter the
        rows to the ones that contain that value.
        """

        sql = sql["select"]["fuel_records"]

        # Do we need to make a prepared statement?
        if 'vehicle_id' in kwargs:
            sql += 'Where vehicle_id = ?'

        # if we have more things to filter that are passed into kwargs we
        # should construct a list of values to pass to the prepared
        # statement

        return [
            FuelRecord(*row)
            for row in self.cursor.execute(sql, kwargs.get('vehicle_id', None))
        ]





def get_database(db_path):
    """

    # Parameters

    db_path:pathlib.Path
        - The path to the database

    """

    # db = records.Database(f"sqlite:///{db_path}")

    # # Do we need to create the tables?
    # if 'VEHICLE' not in db.get_table_names():
    #     db.query(sql["create"]["vehicle"])

    # if 'FUEL' not in db.get_table_names():
    #     db.query(sql["create"]["fuel"])

    # return db
