#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   b46fcb66-02b4-11ec-8c3c-c906c7d81bd1
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-08-21
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from pathlib import Path

# ------------
# 3rd Party - From PyPI

import click
import toml
from appdirs import AppDirs

# ------------
# Custom Modules

from .models import get_session
from .command_fuel import fuel
from .command_vehicle import vehicle
from .command_bulk import bulk

# -------------

__appname__ = "fuel_tracker"
__company__ = "bluebill.net"


def construct_config():
    """
    Retrieve the user configuration.

    """

    dirs = AppDirs()

    config = {}

    # The location of the settings file
    config["user_config"] = (
        Path(dirs.user_config_dir).joinpath(__company__).joinpath(__appname__)
    )
    config["user_config"].mkdir(parents=True, exist_ok=True)

    settings_file = config["user_config"] / Path("settings.toml")

    # Default settings
    config["settings"] = {
        "database": "fuel.db",  # name of the database to use
        "date_format": "%Y-%m-%d",  # How dates are reported and interpreted. Based on strptime behavior: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        "fuel_unit": "l",  # The unit (l or us_gal) we'll assume the fuel quantity is entered in and the value we'll report on. It will be stored as liters in the database.
        "mileage_unit": "km",  # The unit (km or mi) we'll assume for mileage data. It will be stored as kilometers in the database.
    }

    if settings_file.exists():
        config["settings"] |= toml.loads(settings_file.read_text())

    # Construct the path to the database
    # 1. Does it exist

    db_path = Path(config["settings"]["database"])

    if db_path.is_absolute():
        config["path_db"] = db_path

    else:
        config["path_db"] = config["user_config"] / db_path

    return config


@click.group()
@click.version_option()
@click.pass_context
def main(*args, **kwargs):
    """

    Fuel Tracker is a tool to manage fuel receipts and report on them.


    # Usage

    $ ft

    """

    # Initialize the shared context object to a dictionary and configure
    # it for the app
    ctx = args[0]
    ctx.ensure_object(dict)

    config = construct_config()

    # get a connection to the database (create it if it doesn't exit)
    config["db"] = get_session(config["path_db"])

    ctx.obj["config"] = config


main.add_command(fuel)
main.add_command(vehicle)
main.add_command(bulk)
