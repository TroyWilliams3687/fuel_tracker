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

    ctx = args[0]

    config = ctx.obj["config"]


    pass


# how to format datetime - can accept multiple value strings in try them in a particular order
# click.DateTime(formats=[`%Y-%m-%d`, `%d/%m/%y`, `%m/%d/%y`, `%d/%m/%Y`])
# https://click.palletsprojects.com/en/8.0.x/api/#click.DateTime
