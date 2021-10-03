#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   cabfd3e8-0444-11ec-9b10-af5d2370e08b
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-08-23
# -----------

"""


Reference:
- https://realpython.com/python-sqlite-sqlalchemy/#working-with-sqlalchemy-and-python-objects
- https://docs.sqlalchemy.org/en/14/core/type_basics.html
"""

# ------------
# System Modules - Included with Python

# ------------
# 3rd Party - From PyPI


from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy import Integer, Float, String, Boolean, Date
from sqlalchemy import select

# from sqlalchemy import Table
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


# ------------
# Custom Modules

import sqlite3
import numpy as np

# -------------
# sqlite adapters

# https://stackoverflow.com/questions/57628273/saving-numpy-integers-in-sqlite-database-with-sqlalchemy
# https://docs.sqlalchemy.org/en/14/orm/cascades.html?highlight=cascade%20save%20update#cascade-save-update

# Register the following adapter so that numpy integers can vb converted
# to regular integers otherwise they will be blobs

sqlite3.register_adapter(np.int64, lambda val: int(val))

# -------------

Base = declarative_base()


class Vehicle(Base):
    """
    A model of the Vehicle table.
    """

    __tablename__ = "VEHICLE"

    vehicle_id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer, default=0)
    tank_capacity = Column(Float, default=0.0)
    initial_odometer = Column(Float, default=0.0)

    fuel_records = relationship(
        "FuelRecord",
        cascade="all, delete, delete-orphan, save-update",
        order_by="FuelRecord.fill_date",
        primaryjoin="Vehicle.vehicle_id == FuelRecord.vehicle_id",
        # lazy='select', # https://blog.theodo.com/2020/03/sqlalchemy-relationship-performance/
        # order_by="desc(FuelRecord.fill_date)",
    )

    def __str__(self):

        msg = (
            f"id:            {self.vehicle_id}",
            f"Name:          {self.name}",
            f"Make:          {self.make}",
            f"Model:         {self.model}",
            f"Year:          {self.year}",
            f"Tank Capacity: {self.tank_capacity}",
            f"Odometer:      {self.initial_odometer}",
        )

        return "\n".join(msg)

    def __repr__(self):

        return (
            f"Vehicle(id={self.vehicle_id}, "
            f"name={self.name}, "
            f"make={self.make}, "
            f"model={self.model}, "
            f"year={self.year}, "
            f"tank_capacity={self.tank_capacity}, "
            f"initial_odometer={self.initial_odometer})"
        )


class FuelRecord(Base):
    """
    A model of the FUEL table.
    """

    __tablename__ = "FUEL"
    __table_args__ = (
        CheckConstraint("mileage >= 0.0"),
        CheckConstraint("fuel >= 0.0"),
        CheckConstraint("cost >= 0.0"),
    )

    fuel_id = Column(Integer, primary_key=True)
    fill_date = Column(Date)
    mileage = Column(Float, default=0.0)
    fuel = Column(Float, default=0.0)
    cost = Column(Float, default=0.0)
    partial = Column(Boolean)
    comment = Column(String)
    vehicle_id = Column(Integer, ForeignKey("VEHICLE.vehicle_id", ondelete="CASCADE"))

    def __repr__(self):

        return (
            f"FuelRecord(fuel_id={self.fuel_id}, "
            f"fill_date={self.fill_date}, "
            f"mileage={self.mileage}, "
            f"fuel={self.fuel}, "
            f"cost={self.cost}, "
            f"partial={self.partial}, "
            f"comment={self.comment}, "
            f"vehicle_id={self.vehicle_id})"
        )


def get_session(path):
    """
    Given the path to the sqlite database, return a session instance.
    """

    # https://docs.sqlalchemy.org/en/14/tutorial/engine.html
    engine = create_engine(
        f"sqlite+pysqlite:///{path}",
        echo=False,
        future=True,  # enable 2.0 future (Core)
    )

    # https://docs.sqlalchemy.org/en/14/core/metadata.html#creating-and-dropping-database-tables
    # make sure all the Tables defined by the Base classes are created
    Base.metadata.create_all(engine)

    return sessionmaker(engine, future=True)


def select_vehicle_by_id(vid, **kwargs):
    """
    Given the vehicle id, return the SQL select statement that
    will correctly select the vehicle from the database.

    Optionally you can pass in the join=True and it will return a query
    to join the Vehicle and FuelRecord tables and return the results.
    """

    if kwargs.get("join", False):

        return (
            select(Vehicle, FuelRecord)
            .where(Vehicle.vehicle_id == vid)
            .join(Vehicle.fuel_records)
        )

    else:

        return select(Vehicle).where(Vehicle.vehicle_id == vid)


def select_vehicle_by_name(name, **kwargs):
    """
    Given the vehicle name, return the SQL select statement that
    will correctly select the vehicle from the database.

    Optionally you can pass in the join=True and it will return a query
    to join the Vehicle and FuelRecord tables and return the results.
    """

    if kwargs.get("join", False):

        return (
            select(Vehicle, FuelRecord)
            .where(Vehicle.name == name)
            .join(Vehicle.fuel_records)
        )

    else:

        return select(Vehicle).where(Vehicle.name == name)
