#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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

# ------------
# 3rd Party - From PyPI

# https://github.com/kennethreitz/records
import records


# ------------
# Custom Modules

# -------------


# -----------
# -----------
# Example code from: https://github.com/kennethreitz/records/blob/master/examples/randomuser-sqlite.py

# # Valid SQLite URL forms are:
# #   sqlite:///:memory: (or, sqlite://)
# #   sqlite:///relative/path/to/file.db
# #   sqlite:////absolute/path/to/file.db

# # records will create this db on disk if 'users.db' doesn't exist already
# db = records.Database('sqlite:///users.db')

# db.query('DROP TABLE IF EXISTS persons')
# db.query('CREATE TABLE persons (key int PRIMARY KEY, fname text, lname text, email text)')

# for rec in j:
#     user = rec['user']
#     name = user['name']

#     key = user['registered']
#     fname = name['first']
#     lname = name['last']
#     email = user['email']
#     db.query('INSERT INTO persons (key, fname, lname, email) VALUES(:key, :fname, :lname, :email)',
#             key=key, fname=fname, lname=lname, email=email)

# rows = db.query('SELECT * FROM persons')
# print(rows.export('csv'))
# -----------
# -----------


sql_statements = {}

sql_statements["insert_vehicle"] = """
INSERT INTO
Vehicle(Make,
        Model,
        Year,
        TankCapacity,
        InitialOdometer,
        Archive)
VALUES(?, ?, ?, ?, ?, ?)
"""

sql_statements["insert_fill_up"] = """
INSERT INTO
Fill_Up(VehicleID,
        Date,
        Mileage,
        FuelAdded,
        Cost,
        PartialFill_Up,
        Comment,
        Tags)
VALUES(?, ?, ?, ?, ?, ?, ?, ?)
"""

sql_statements["select_vehicles"] = """
SELECT
  ID,
  Make,
  Model,
  Year,
  TankCapacity,
  InitialOdometer,
  Archive
FROM Vehicle
"""

sql_statements["select_fill_up"] = """
SELECT
 ID,
 VehicleID,
 Date,
 Mileage,
 FuelAdded,
 Cost,
 PartialFill_Up,
 Comment,
 Tags
FROM Fill_Up
"""

sql_statements["vehicle_set_archive"] = """
UPDATE Vehicle
SET Archive = ?
WHERE ID = ?
"""


sql_table_statements = {}

sql_table_statements['drop_table']="DROP TABLE IF EXISTS {};"

sql_table_statements['create_table_vehicle']="""
CREATE TABLE Vehicle(
    ID               INTEGER PRIMARY KEY AUTOINCREMENT,
    Name             TEXT NOT NULL,
    Make             TEXT NOT NULL,
    Model            TEXT NOT NULL,
    Year             INTEGER DEFAULT 0,
    TankCapacity     INTEGER DEFAULT 0,
    InitialOdometer  INTEGER DEFAULT 0,
);"""

sql_table_statements['create_table_fuel']="""
CREATE TABLE Fuel(
    ID            INTEGER PRIMARY KEY AUTOINCREMENT,
    Date          TIMESTAMP NOT NULL,
    Mileage       FLOAT NOT NULL DEFAULT 0 CHECK (Mileage > 0),
    Fuel          FLOAT NOT NULL DEFAULT 0 CHECK (Fuel > 0),
    Cost          FLOAT NOT NULL DEFAULT 0 CHECK (Cost > 0),
    Partial       BOOLEAN NOT NULL DEFAULT 0 CHECK (PartialFill_Up IN (0,1)),
    Comment       TEXT,
    VehicleID     INTEGER DEFAULT 0,
    FOREIGN KEY(VehicleID) REFERENCES Vehicle(ID)
);"""
