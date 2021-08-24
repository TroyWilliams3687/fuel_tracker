#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   81ef08b8-0503-11ec-b7e5-a9913e95621d
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-08-24
# -----------

"""
Perform bulk operations on the database.
"""

# ------------
# System Modules - Included with Python

from pathlib import Path
from datetime import date

# ------------
# 3rd Party - From PyPI

import click
import pandas as pd

# ------------
# Custom Modules

from .models import Vehicle
from .models import FuelRecord

# -------------


@click.group("bulk")
@click.pass_context
def bulk(*args, **kwargs):
    """
    Perform bulk operations on the database.

    # Usage

    $ ft bulk add ./data/vw-passat-2015.ods




    """
    pass

@bulk.command('add')
@click.pass_context
@click.argument(
    "spreadsheet",
    nargs=-1, # accept an unlimited number of arguments. This makes it an iterable
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
)
def add(*args, **kwargs):
    """
    Add a new vehicle and fuel records from a spreadsheet to the
    database. You must specify the path to the spreadsheet. This
    methods assumes that the vehicle does not exist in the database and
    none of the fuel records exist either.

    Support for `.ods` Open Office Format and `.xlsx` Excel format. The
    spreadsheet should have the following columns:

    - name
    - make
    - model
    - year
    - tank_capacity
    - initial_odometer
    - fill_date
    - mileage fuel
    - cost
    - partial comment

    NOTE: The order doesn't matter.

    # Usage

    \b
    $ ft bulk add ./data/vw-passat-2015.ods
    $ ft bulk add ./data/vw-passat-2015.ods ./data/dodge-intrepid-1997.ods
    $ ft bulk add ./data/*.ods

    """

    ctx = args[0]
    config = ctx.obj["config"]

    for spreadsheet in kwargs['spreadsheet']:
        click.echo(f'Processing {spreadsheet}...')

        df = pd.read_excel(spreadsheet,  parse_dates=['fill_date'])
        df = df.astype({'partial':bool})

        vehicles = {}
        vehicle_columns = [
            'name',
            'make',
            'model',
            'year',
            'tank_capacity',
            'initial_odometer',
        ]

        for vehicle_values, group in df.groupby(vehicle_columns):
            new_vehicle = Vehicle(**{k:v for k, v in zip(vehicle_columns, vehicle_values)})

            # remove the vehicle columns from the dataframe
            fr = group.drop(vehicle_columns, axis=1)

            new_vehicle.fuel_records = [
                FuelRecord(**fuel_record)
                for fuel_record in fr.to_dict('records')
            ]

            with config['db'].begin() as session:
                session.add(new_vehicle)
                session.flush() # get the new id

                click.echo(new_vehicle) # create a vehicle format function that can handle the units (liters and kilometers)
                click.echo(f'Fuel Records: {len(new_vehicle.fuel_records)}')
                click.echo()


