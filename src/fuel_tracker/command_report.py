#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   47c6d074-08e8-11ec-ba1d-e1435d6e8eeb
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-08-29
# -----------

"""
"""

# ------------
# System Modules - Included with Python

# ------------
# 3rd Party - From PyPI

import click

import pandas as pd

from rich.console import Console
from sqlalchemy import select

# ------------
# Custom Modules

from .models import (
    Vehicle,
    FuelRecord,
    select_vehicle_by_id,
    select_vehicle_by_name,
)

from .queries import vehicle_report, vehicle_report_summary

from .common import integer_or_string

# -------------

console = Console()


@click.group("report")
@click.pass_context
def report(*args, **kwargs):
    """
    Generate reports from various parts of the database.
    """

    pass

def report_show_usage(db):
    """
    Display how to use `$ ft report show` with examples from the
    database. The user should be able to copy/paste one of the commands
    directly.
    """

    console.print()
    console.print('No Arguments :frowning:.')
    console.print('The command can be run with [white]vehicle names[/white]:', style='cyan')
    console.print()

    show_command = '$ ft report show'

    with db.begin() as session:

        result = session.execute(select(Vehicle))

        vehicles = [(v.vehicle_id, v.name) for v in result.scalars().all()]

        for _, name in vehicles:
            console.print(f'[red]{show_command}[/red] [white]{name}[/white]')

        console.print()
        console.print('Or with vehicle [white]IDs[/white]:', style='cyan')
        console.print()

        for vid, _ in vehicles:
            console.print(f'[red]{show_command}[/red] [white]{vid}[/white]')

        console.print()


@report.command("show")
@click.pass_context
@click.argument(
    "vehicles",
    nargs=-1,  # accept an unlimited number of arguments. This makes it an iterable
    type=str,
)
@click.option(
    "--tail",
    type=int,
    default=10,
    help="Display the last `n` records. Defaults to 10. Use -1 to select all records.",
)
@click.option(
    "--hide-partial",
    is_flag=True,
    help="Hide the partial column.",
)
@click.option(
    "--hide-comments",
    is_flag=True,
    help="Hide the comments column.",
)
def show(*args, **kwargs):
    """
    Display fuel information about the vehicles in a tabular format.

    You can specify the vehicles by ID or name (in the database):

    $ ft report show passat

    You can name as many vehicles or IDs as you like, simply use a space
    to separate them:

    $ ft report show passat 3 intrepid

    By default, it will display the last 10 records in the database to
    change that use the `--tail` command:

    $ ft report show passat --tail=50

    To display all the records use `-1`:

    $ ft report show passat --tail=-1

    To hide the partial and/or the comments columns use `--hide-partial`
    and/or `--hide-commments`:

    $ ft report show passat --records=50 --hide-partial --hide-comments

    If you don't remember the name or id of the vehicle, execute:

    $ ft report show

    And it will display a list of valid options.

    """

    ctx = args[0]
    config = ctx.obj["config"]

    # figure out which vehicles are id and which are names...
    vehicle_ids, vehicle_names = integer_or_string(kwargs["vehicles"])


    # do we have any arguments?
    if len(vehicle_ids) == 0 and len(vehicle_names) == 0:

        report_show_usage(config["db"])

        ctx.exit()


    with config["db"].begin() as session:

        selected_vehicles = []

        if vehicle_ids:

            result = session.execute(
                select(Vehicle).where(Vehicle.vehicle_id.in_(vehicle_ids))
            )

            # https://docs.sqlalchemy.org/en/14/orm/queryguide.html#selecting-orm-entities-and-attributes
            selected_vehicles.extend(result.scalars().all())

        if vehicle_names:

            result = session.execute(
                select(Vehicle).where(Vehicle.name.in_(vehicle_names))
            )

            selected_vehicles.extend(result.scalars().all())

        if len(selected_vehicles) == 0:
            console.print('No matching vehicles found.', style='red')
            ctx.exit()

        for v in selected_vehicles:

            console.print()
            console.print(v)
            console.print()

            # This call will load all of the records - for small data
            # sets it doesn't matter
            # console.print(len(v.fuel_records[-10:]))


            # --------------------
            # Load the vehicle report

            statement = vehicle_report(v.vehicle_id, kwargs["tail"])
            df = pd.read_sql(statement, session.connection())

            # reverse the rows as the query will bring them in with the
            # last date as the first entry, I want to see it as the
            # first entry. Not really an elegant way to do it with pure SQL

            df = df[::-1]
            df.reset_index(inplace=True, drop=True)

            # Load the vehicle summary report

            summary_statement = vehicle_report_summary(v.vehicle_id)
            df_totals = pd.read_sql(summary_statement, session.connection())

            # ----------------
            # rename the columns to something more friendly

            df_totals.rename(
                columns={
                    'fill_ups':'Fill-Ups',
                    'total_mileage':'Mileage (Total)',
                    'total_fuel':'Fuel (Total)',
                    'total_cost':'Cost (Total)',
                    'min_mileage':'Mileage (Min)',
                    'max_mileage':'Mileage (Max)',
                    'avg_mileage':'Mileage (Avg)',
                    'min_fuel':'Fuel (Min)',
                    'max_fuel':'Fuel (Max)',
                    'avg_fuel':'Fuel (Avg)',
                    'min_cost':'Cost (Min)',
                    'max_cost':'Cost (Max)',
                    'avg_cost':'Cost (Avg)',
                    'avg_cost_per_liter':'$/l (Avg)',
                    'avg_l_per_100km':'l/100km (Avg)',
                    'mpg_us':'mpg (us) (Avg)',
                    'mpg_imp':'mpg (imp) (Avg)',
                },
                inplace=True,
            )

            # rename the columsn
            df.rename(
                columns={
                    'fuel_id':'fuel (id)',
                    'fill_date':'fill date',
                    'cost_per_liter':'$/l',
                    'l_per_100km':'l/100km',
                    'mpg_us':'mpg (us)',
                    'mpg_imp':'mpg (imp)',
                },
                inplace=True,
            )

            # ----------------

            console.print(
                df.to_markdown(
                    index=True,
                    tablefmt="pretty",
                )
            )

            console.print()
            console.print('Summary by Year:')

            console.print(
                df_totals.to_markdown(
                    index=True,
                    tablefmt="pretty",
                )
            )

            # Write to excel/ods/csv


# - Export to csv, excel, ods <- see bulk export
# - --summary - display per year stats
#   - for every year, display:
#       - total fill ups
#       - total mileage
#       - total fuel
#       - total cost
#       - average mileage
#       - average fuel
#       - average cost
#       - average days
#       - average $/l
#       - l/100km
#       - mpg (us)
#       - mpg (imp)
