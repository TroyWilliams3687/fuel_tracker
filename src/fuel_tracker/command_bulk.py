#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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

from pandas import ExcelWriter

from sqlalchemy import delete

# ------------
# Custom Modules

from .models import (
    Vehicle,
    FuelRecord,
    select_vehicle_by_id,
    select_vehicle_by_name,
)

from .common import is_int

# -------------


@click.group("bulk")
@click.pass_context
def bulk(*args, **kwargs):
    """
    Perform bulk operations on the database such as adding new vehicles
    and records or deleting existing vehicles and records.

    # Usage

    $ ft bulk add ./data/vw-passat-2015.ods
    """
    pass


@bulk.command("add")
@click.pass_context
@click.argument(
    "spreadsheet",
    nargs=-1,  # accept an unlimited number of arguments. This makes it an iterable
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
    - mileage
    - fuel
    - cost
    - partial
    - comment

    NOTE: The order doesn't matter.

    # Usage

    \b
    $ ft bulk add ./data/vw-passat-2015.ods
    $ ft bulk add ./data/vw-passat-2015.ods ./data/dodge-intrepid-1997.ods
    $ ft bulk add ./data/*.ods

    """

    ctx = args[0]
    config = ctx.obj["config"]

    for spreadsheet in kwargs["spreadsheet"]:
        click.echo(f"Processing {spreadsheet}...")

        df = pd.read_excel(spreadsheet, parse_dates=["fill_date"])

        # Fill NaN with 0, before casting to bool. Otherwise we end up
        # with a lot of True values.
        df["partial"] = df["partial"].fillna(0)
        df = df.astype({"partial": bool})

        vehicles = {}
        vehicle_columns = [
            "name",
            "make",
            "model",
            "year",
            "tank_capacity",
            "initial_odometer",
        ]

        for vehicle_values, group in df.groupby(vehicle_columns):
            new_vehicle = Vehicle(
                **{k: v for k, v in zip(vehicle_columns, vehicle_values)}
            )

            # remove the vehicle columns from the dataframe
            fr = group.drop(vehicle_columns, axis=1)

            new_vehicle.fuel_records = [
                FuelRecord(**fuel_record) for fuel_record in fr.to_dict("records")
            ]

            with config["db"].begin() as session:
                session.add(new_vehicle)
                session.flush()  # get the new id

                click.echo(new_vehicle)

                # create a vehicle format function that can handle the
                # units (liters and kilometers)

                click.echo(f"Fuel Records: {len(new_vehicle.fuel_records)}")
                click.echo()


@bulk.command("delete")
@click.pass_context
@click.argument(
    "vehicles",
    nargs=-1,
    type=str,
)
def delete(*args, **kwargs):
    """
    Delete the vehicle (by name or id) from the database along with all
    of its fuel records.

    # Usage

    \b
    $ ft bulk delete passat 2

    """

    ctx = args[0]
    config = ctx.obj["config"]

    with config["db"].begin() as session:

        for vid in kwargs["vehicles"]:

            click.echo(f"Deleting {vid}...")

            if is_int(vid):

                statement = select_vehicle_by_id(vid)

            else:

                statement = select_vehicle_by_name(vid)

            selected_vehicle = session.execute(statement).first()

            # NOTE: session.execute returns an iterable. Deal with it
            # appropriately

            if len(selected_vehicle) == 1:

                delete_query = delete(Vehicle).where(Vehicle.vehicle_id == vid)
                session.execute(delete_query)

            elif len(selected_vehicle) == 0:

                click.secho(f"No matches for: {vid}", fg="cyan")

            else:

                click.secho(
                    f"More than one vehicle returned ({len(selected_vehicle)})! Doing Nothing!",
                    fg="red",
                )

                click.secho("Here are the returned Vehicles:", fg="red")

                for v in selected_vehicle:
                    click.secho(v, fg="red")
                    click.echo()


@bulk.command("export")
@click.pass_context
@click.argument(
    "vehicles",
    nargs=-1,
    type=str,
)
@click.option(
    "--excel",
    type=click.Path(
        exists=False,
        dir_okay=False,
        readable=False,
        path_type=Path,
    ),
    help="Write the vehicle(s) and fuel records to an excel spreadsheet.",
)
@click.option(
    "--ods",
    type=click.Path(
        exists=False,
        dir_okay=False,
        readable=False,
        path_type=Path,
    ),
    help="Write the vehicle(s) and fuel records to an Open Office spreadsheet (*.ods).",
)
@click.option(
    "--csv",
    type=click.Path(
        exists=False,
        dir_okay=False,
        readable=False,
        path_type=Path,
    ),
    help="Write the vehicle(s) and fuel records to a csv file.",
)
def export(*args, **kwargs):
    """
    bulk export the specified vehicles by name or id separated by spaces
    on the command line to:

    \b
    - csv
    - excel
    - ods - open office format
    - stdout

    The vehicle and fuel records will be combined into one table and
    exported to the file. If an output format isn't selected, it will
    be displayed in the terminal.

    # Usage

    $ ft bulk export passat 2
    $ ft bulk export passat interpid --excel=file.xlsx
    $ ft bulk export passat interpid --ods=file.ods
    $ ft bulk export passat interpid --csv=file.csv
    $ ft bulk export passat interpid --excel=file.xlsx --ods=file.ods --csv=file.csv

    $ ft bulk export passat intrepid 2 --ods=./output/file.ods
    $ ft bulk export passat intrepid soul matrix --ods=./output/data.ods --csv=./output/data.csv
    """

    ctx = args[0]
    config = ctx.obj["config"]

    output = []
    with config["db"].begin() as session:

        for vid in kwargs["vehicles"]:

            click.echo(f"Exporting {vid}...")
            click.echo()

            if is_int(vid):

                statement = select_vehicle_by_id(vid, join=True)

            else:

                statement = select_vehicle_by_name(vid, join=True)

            page_name = f"{vid}"

            df = pd.read_sql(statement, session.connection())
            df = df.drop(["vehicle_id", "vehicle_id_1"], axis=1)

            if kwargs.get("csv", False):

                csv_file = kwargs.get("csv")
                df.to_csv(csv_file.parent / Path(f"{csv_file.stem}_{page_name}.csv"))

            output.append((page_name, df))

    if kwargs.get("excel", False):

        with ExcelWriter(kwargs.get("excel")) as writer:

            for page_name, df in output:
                df.to_excel(writer, page_name, index=False)

            writer.save()

    if kwargs.get("ods", False):

        with ExcelWriter(
            kwargs.get("ods"),
            engine="odf",
        ) as writer:

            for page_name, df in output:
                # for some reason, export the fill_date as a datetime to
                # ods assigns the cell formatting as a number. In the
                # spreadsheet we can change the format to date and the
                # value is displayed correctly, but the user shouldn't
                # have to do that. We'll convert it to a string and leave it at that.
                df["fill_date"] = pd.to_datetime(df["fill_date"]).dt.strftime(
                    "%Y-%m-%d"
                )
                df.to_excel(writer, page_name, index=False)

            writer.save()

    if not kwargs.get("excel", False) and kwargs.get("ods", False):

        for page_name, df in output:
            click.echo(
                df.to_markdown(
                    index=False,
                    tablefmt="pretty",
                )
            )
            click.echo()

    click.secho("Completed!", fg="cyan")
