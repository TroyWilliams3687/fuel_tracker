#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   48487126-0454-11ec-9b10-af5d2370e08b
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-08-23
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from datetime import date

# ------------
# 3rd Party - From PyPI

import click

# ------------
# Custom Modules

from .models import Vehicle

# -------------


@click.group("vehicle")
@click.pass_context
def vehicle(*args, **kwargs):
    """
    Work with vehicles.

    # Usage

    \b
    $ ft vehicle add passat --make=Volkswagen --model=passat --year=2015 --tank=70 --inital-odo=15

    """
    pass


@vehicle.command("add")
@click.pass_context
@click.option(
    "--name",
    type=str,
    prompt=True,
    help="A name that can be used to identify the vehicle. This can be the model of the vehicle or something more memorable or easier to type.",
)
@click.option(
    "--make",
    type=str,
    prompt=True,
    help="The make of the vehicle. For a car this could be VW, Ford or Toyota.",
)
@click.option(
    "--model",
    type=str,
    prompt=True,
    help="This is the type of vehicle. For a car it could be Passat, F-150 or Hilux",
)
@click.option(
    "--year",
    type=click.DateTime(formats=["%Y"]),
    prompt=True,
    help="The year of the vehicle. It should be 4 digits - 2021 for example.",
)
@click.option(
    "--tank",
    "tank_capacity",
    type=float,
    prompt=True,
    help="The fuel capacity in either liters (default) or gallons.",
)
@click.option(
    "--initial-odo",
    "initial_odometer",
    type=str,
    prompt=True,
    help="The initial odometer reading in either kilometers (default) or miles.",
)
def add(*args, **kwargs):
    """
    Add new Vehicles to the database.

    # Usage

    \b
    $ ft vehicle add --name=passat --make=VW --model=Passat --year=2015 --tank=70 --initial-odo=0

    """

    ctx = args[0]
    config = ctx.obj["config"]

    if kwargs["name"] is None:
        kwargs["name"] = kwargs["model"]

    kwargs["year"] = int(kwargs["year"].strftime("%y"))

    new_vehicle = Vehicle(**kwargs)

    with config["db"].begin() as session:
        session.add(new_vehicle)

        session.flush()  # get the new id

        click.echo()
        click.echo("Added:")
        click.echo(
            new_vehicle
        )  # create a vehicle format function that can handle the units (liters and kilometers)
        click.echo()


# ft vehicle show <- display all of the vehicles in the database by id and name
#   - --id=0
#   - --name=passat
#   - either of those two options will display the full detail of the vehicle


# `ft vehicle remove passat --dry-run`


# `ft vehicle edit passat --tank=71`
