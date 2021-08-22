#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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

# ------------
# Custom Modules

# -------------

@click.command("fuel")
@click.pass_context
def fuel(*args, **kwargs):
    """


    """

    # Initialize the shared context object to a dictionary and configure
    # it for the app
    ctx = args[0]

    # planned = ctx.obj["planned"]
    # plan_stope = ctx.obj["plan_stope"]
    # survey_stope = ctx.obj["survey_stope"]
    # common_rings = ctx.obj["common_rings"]
    # bbox = ctx.obj["bbox"]

    click.secho('ft fuel....', fg='blue')
    pass
