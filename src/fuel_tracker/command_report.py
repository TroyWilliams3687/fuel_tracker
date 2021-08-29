#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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

# ------------
# Custom Modules

# -------------

@click.group("report")
@click.pass_context
def report(*args, **kwargs):
    """
    Generate reports from various parts of the database.

    # Usage

    $ ft report

    """
    pass


