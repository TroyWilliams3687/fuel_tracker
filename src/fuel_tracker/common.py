#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   a1012b68-05bd-11ec-803b-99db2a5fa4d5
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-08-25
# -----------

"""

"""

# ------------
# System Modules - Included with Python

# ------------
# 3rd Party - From PyPI

# ------------
# Custom Modules

# -------------

# https://stackoverflow.com/a/9859202
def is_int(s):
    """
    A method to determine if the string is indeed an integer.

    Returns True if it is an integer, False otherwise

    """
    try:

        return float(str(s)).is_integer()

    except:

        return False
