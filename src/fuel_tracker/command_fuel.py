#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   596020f8-0382-11ec-acf9-452d5e2bc00d
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-08-22
# -----------

"""
"""

# ------------
# System Modules - Included with Python

# ------------
# 3rd Party - From PyPI

import click

from sqlalchemy import select
from rich.console import Console

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

console = Console()

date_format_strings = [
    "%Y-%m-%d",
    "%d/%m/%y",
    "%m/%d/%y",
    "%d/%m/%Y",
    "%m/%d/%Y",
]


@click.group("fuel")
@click.pass_context
def fuel(*args, **kwargs):
    """
    Manage vehicle fuel records.
    """
    pass


def fuel_add_usage(vid, session):
    """
    Display how to use `$ ft fuel add` with examples from the
    database. The user should be able to copy/paste one of the commands
    directly.

    If vid is not None, we'll assume it is invalid.
    """

    console.print()

    if vid is None:

        console.print('No Arguments :frowning:!')

    else:

        console.print(
            f"{vid} does not resolve to a vehicle!",
            style="red",
        )


    console.print()
    console.print('The command can be run with [white]vehicle names[/white]:', style='cyan')
    console.print()

    show_command = '$ ft fuel add'

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
    console.print('use `--help` to see more detailed information.')
    console.print()


@fuel.command("add")
@click.pass_context
@click.argument(
    "vehicle",
    type=str,
    required=False,
)
@click.option(
    "--date",
    type=click.DateTime(formats=date_format_strings),
    prompt=False,
    help=(
        "The date fuel was added to the vehicle. "
        "Support 5 major date formats in the following order: "
        "Y-m-d, d/m/Y, d/m/y, m/d/Y, m/d/y (first match is taken)"
    ),
)
@click.option(
    "--fuel",
    type=float,
    prompt=False,
    help="The amount of fuel added to the vehicle.",
)
@click.option(
    "--mileage",
    type=float,
    prompt=False,
    help="The mileage since the last fill up.",
)
@click.option(
    "--cost",
    type=float,
    prompt=False,
    help="The full cost of the fuel.",
)
@click.option(
    "--partial",
    type=bool,
    prompt=False,
    help=(
        "Was this a partial fill up. "
        "Optional - you will not be prompted and have "
        "to set the switch."
    ),
)
@click.option(
    "--comment",
    type=str,
    prompt=False,
    help=(
        "A comment about this fuel record. "
        "Optional - you will not be prompted and "
        "have to set the switch."
    ),
)
def add(*args, **kwargs):
    """
    Add a new fuel record to the database. You can add a fuel record by
    vehicle name:

    $ ft fuel add passat

    or by vehicle id:

    $ ft fuel add 4

    If you do not specify the switches, you will be prompted for the
    information automatically.

    If you don't remember the name or id of the vehicle, execute:

    $ ft fuel add

    And it will display a list of valid options.

    \b
    NOTE: The date format can be one of the following:

    1. `%Y-%m-%d` - year-month-day  2021-08-12

    2. `%d/%m/%y` - day/month/year  12/08/21

    3. `%m/%d/%y` - month/day/year  08/12/21

    4. `%d/%m/%Y` - day/month/year  12/08/2021

    5. `%m/%d/%Y` - month/day/year  08/12/2021

    NOTE: The first format to produce a correct date is used. The date
    is matched against the list in the order specified above. For
    example, `02/03/2021` can match 2 or 3 but will match 2 first.
    Beware. It is best to use the ISO 8601 representation.

    NOTE: If you use any of the date formats that have a `/`in them you
    will have to use quote marks when using them directly in switches.
    """

    ctx = args[0]
    config = ctx.obj["config"]

    vid = kwargs["vehicle"]

    if vid is None:

        with config["db"].begin() as session:
            fuel_add_usage(vid, session)

        ctx.exit()

    with config["db"].begin() as session:

        # do we have an integer or a string?
        if is_int(vid):

            statement = select_vehicle_by_id(vid)

        else:

            statement = select_vehicle_by_name(vid)

        # NOTE: select(Vehicle) returns the SQL statement that must be
        # executed against the engine.

        selected_vehicle = session.execute(statement).first()

        if selected_vehicle is None:

            fuel_add_usage(vid, session)

            ctx.exit()

        selected_vehicle = selected_vehicle[0]

        # Now that we have a valid vehicle, let's make sure we have
        # valid data.

        data = {}

        data["date"] = (
            click.prompt(
                "Date",
                type=click.DateTime(formats=date_format_strings),
            )
            if kwargs["date"] is None
            else kwargs["date"]
        )

        for key in ("fuel", "mileage", "cost"):

            data[key] = (
                click.prompt(
                    f"{key.title()}",
                    type=float,
                )
                if kwargs[key] is None
                else kwargs[key]
            )

        data["partial"] = kwargs["partial"]
        data["comment"] = kwargs["comment"]

        data["fill_date"] = data.pop("date")

        # plot the records and ask for confirmation to proceed:

        console.print()
        console.print(f"{selected_vehicle.vehicle_id} - {selected_vehicle.name}")
        console.print(f'Date    = {data["fill_date"]}')
        console.print(f'Fuel    = {data["fuel"]}')
        console.print(f'Mileage = {data["mileage"]}')
        console.print(f'Cost    = {data["cost"]}')
        console.print(f'Partial = {data["partial"]}')
        console.print(f'Comment = {data["comment"]}')

        if click.confirm("Is the Fuel Record Correct?", abort=True, default=True):

            selected_vehicle.fuel_records.append(FuelRecord(**data))
            session.flush()

            console.print(
                f"{len(selected_vehicle.fuel_records)} "
                "Fuel Records associated with the vehicle."
            )


# ft fuel show passat --records=10 <- default
# ft fuel show passat --records="all"
# - show the fuel records for the vehicle sorted in descending order
# - show the fuel record ids + stats (last program) probably need to use a dataframe
# - can specify --excel, --ods, --csv to write the report. See bulk export for details

# ft fuel delete 45
# - delete the fuel record with id=45
# - would use the show command to determine that

# ft fuel edit 45 --cost=45.67
# - same switches as the add command
# - will not prompt, any value that is not specified is not changed
# - add values to a dictionary and create a FuelRecord object and commit that to the database
#   - verify that it does get updated...
# - NOTE: should be able to change the vehicle_id foreign key as well.
