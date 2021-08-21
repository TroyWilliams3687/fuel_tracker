#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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


# -------------

__appname__ = "fuel_tracker"
__company__ = "bluebill.net"

def config():
    """
    Retrieve the user configuration.

    """

    dirs = AppDirs()

    config = {}

    # The location of the settings file
    config['folder'] = Path(dirs.user_config_dir).joinpath(__company__).joinpath(__appname__)
    config['folder'].mkdir(parents=True, exist_ok=True)
    config["settings_path"] = location.joinpath("settings.toml")

    # Default settings
    config["settings"] = {
        'database':'fuel.db',
        'date_format':"%Y-%m-%d",  # How dates are reported and interpreted. Based on strptime behavior: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        'fuel_unit':'l',           # The unit (l or us_gal) we'll assume the fuel quantity is entered in and the value we'll report on. It will be stored as liters in the database.
        'mileage_unit':'km',       # The unit (km or mi) we'll assume for mileage data. It will be stored as kilometers in the database.
    }

    if settings.exists():
        config["settings"] |= toml.loads(config["settings_path"].read_text())

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

    ctx.obj["config"] = config()



# main.add_command(image)
# main.add_command(animation)
