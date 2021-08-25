#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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

# -------------

"""
CREATE TABLE VEHICLE(
    vehicle_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT NOT NULL UNIQUE,
    make             TEXT NOT NULL,
    model            TEXT NOT NULL,
    year             INTEGER DEFAULT 0,
    tank_capacity    INTEGER DEFAULT 0,
    initial_odometer INTEGER DEFAULT 0
);"""

"""
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

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'VEHICLE'
    vehicle_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer, default=0)
    tank_capacity = Column(Float, default=0.0)
    initial_odometer = Column(Float, default=0.0)
    fuel_records = relationship(
        "FuelRecord",
        order_by="FuelRecord.fill_date",
        cascade="all,delete-orphan",
        backref="Vehicle",
        # passive_deletes=True,
    )


    def __str__(self):

        msg = (
            f"Name (id):     {self.name} ({self.vehicle_id})",
            f"Make:          {self.make}",
            f"Model:         {self.model}",
            f"Year:          {self.year}",
            f"Tank Capacity: {self.tank_capacity}",
            f"Odometer:      {self.initial_odometer}",
        )

        return '\n'.join(msg)

    def __repr__(self):

        return (
            f"Vehicle(id={self.vehicle_id}, "
            f"name={self.name}, "
            f"make={self.make}, "
            f"model={self.model}, "
            f"year={self.year}, "
            f"tank_capacity={self.tank_capacity}, "
            f"initial_odometer={self.initial_odometer}"
        )

class FuelRecord(Base):
    __tablename__ = 'FUEL'
    __table_args__ = (
        CheckConstraint('mileage >= 0.0'),
        CheckConstraint('fuel >= 0.0'),
        CheckConstraint('cost >= 0.0'),
    )
    fuel_id = Column(Integer, primary_key=True)
    fill_date = Column(Date)
    mileage = Column(Float, default=0.0)
    fuel = Column(Float, default=0.0)
    cost = Column(Float, default=0.0)
    partial = Column(Boolean)
    comment = Column(String)
    vehicle_id = Column(Integer, ForeignKey("VEHICLE.vehicle_id", ondelete="CASCADE"))


def get_session(path):
    """
    Given the path to the sqlite database, return a session instance.
    """

    # https://docs.sqlalchemy.org/en/14/tutorial/engine.html
    engine = create_engine(
        f"sqlite+pysqlite:///{path}",
        echo=False,
        future=True, # enable 2.0 future (Core)
    )

    # make sure all the Tables defined by the Base classes are created
    # https://docs.sqlalchemy.org/en/14/core/metadata.html#creating-and-dropping-database-tables
    Base.metadata.create_all(engine)

    return sessionmaker(engine,future=True)


def select_vehicle(name_id):
    """
    Given the vehicle id or name, return the SQL select statement that
    will correctly select the vehicle from the database.

    """

    # do we have an integer or a string?
    try:

        # If vid is an integer, delete by integer
        int_id = int(name_id)
        return select(Vehicle).where(Vehicle.vehicle_id == int_id)

    except ValueError:

        # we have a string, retrieve it by
        return select(Vehicle).where(Vehicle.name == name_id)


# def add_vehicle(session, vehicles)
#     """

#     # Parameters (kwargs)

#     vehicles:list(Vehicle)

#     """

#     with session.begin():
#         for v in vehicles:
#             session.add(v)



# Session Context, adding items to the database - automatically commits when over
# with Session.begin() as session:
#     session.add(some_object)
#     session.add(some_other_object)


# -------------
# def get_authors(session):
#     """Get a list of author objects sorted by last name"""
#     return session.query(Author).order_by(Author.last_name).all()


# def get_books_by_publishers(session, ascending=True):
#     """Get a list of publishers and the number of books they've published"""
#     if not isinstance(ascending, bool):
#         raise ValueError(f"Sorting value invalid: {ascending}")

#     direction = asc if ascending else desc

#     return (
#         session.query(
#             Publisher.name, func.count(Book.title).label("total_books")
#         )
#         .join(Publisher.books)
#         .group_by(Publisher.name)
#         .order_by(direction("total_books"))
#     )
