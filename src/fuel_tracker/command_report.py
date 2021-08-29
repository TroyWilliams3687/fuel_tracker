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

import pandas as pd

# ------------
# Custom Modules

from .models import (
    Vehicle,
    FuelRecord,
    select_vehicle_by_id,
    select_vehicle_by_name,
)

from .common import integer_or_string

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


@report.command('show')
@click.pass_context
@click.argument(
    "vehicles",
    nargs=-1, # accept an unlimited number of arguments. This makes it an iterable
    type=str,
)
@click.option(
    "--records",
    type=int,
    default=10,
    help="The number of fuel records to display. Defaults to 10. Use -1 to select all records.",
)
@click.option(
    "--hide-partial",
    is_flag=True,
    help="Display the partial column.",
)
@click.option(
    "--hide-comments",
    is_flag=True,
    help="Display the comments column.",
)
def show(*args, **kwargs):
    """

    # Usage

    \b
    $ ft report show passat

    $ ft report show passat soul --records=25 --hide-partial --hide-comments

    $ ft report show passat --records=50 --hide-partial --hide-comments




    $ ft report show passat intrepid soul matrix --ods=./output/data.ods --csv=./output/data.csv

    """

    ctx = args[0]
    config = ctx.obj["config"]

    # figure out which vehicles are id and which are names...
    vehicle_ids, vehicle_names = integer_or_string(kwargs['vehicles'])

    with config['db'].begin() as session:

        selected_vehicles = []

        if vehicle_ids:
            selected_vehicles.extend(
                session
                .query(Vehicle)
                .filter(Vehicle.id.in_(vehicle_ids))
                .all() # all returns objects
            )

        if vehicle_names:
            selected_vehicles.extend(
                session.query(Vehicle)
                .filter(Vehicle.name.in_(vehicle_names))
                .all()
            )

        for v in selected_vehicles:

            click.echo('-----')
            click.echo(v)
            click.echo()

             # This call will load all of the records - for small data
             # sets it doesn't matter
            # click.echo(len(v.fuel_records[-10:]))

            # This one will load the subset that we are interested in
            statement = (
                session
                .query(FuelRecord)
                .filter(FuelRecord.vehicle_id == v.vehicle_id)
                .order_by(FuelRecord.fill_date.desc())
                .limit(kwargs['records'])
                .statement
                # .all() # return objects
            )

            df = pd.read_sql(statement, session.connection())
            df = df.drop(['vehicle_id'], axis=1)
            df['partial'].replace(False, '', inplace=True)

            # the dataframe is generated with a statement that sorts the
            # data by fill date in descending order. This means the
            # most recent date will be at the top - I want it at the
            # bottom. We can reverse the dataframe rows to accomplish the ordering I want.

            df = df[::-1]
            df.reset_index(drop=True, inplace=True)

            # Fuel Calculations

            df['$/l'] = df['cost'] / df['fuel']
            df['l/100km'] = 100*df['fuel'] / df['mileage']
            df['mpg (us)'] = (df['mileage']*0.621371) / (df['fuel']*0.264172) # google
            df['mpg (imp)'] = (df['mileage']*0.621371) / (df['fuel']*0.219969) # google
            df['days'] = df['fill_date'].diff().dt.days  # .dt.days removes the 'days' portion that would be listed

            # reorder the columns before we start removing them
            df = df.reindex(
                columns=[
                    'fuel_id',
                    'fill_date',
                    'mileage',
                    'fuel',
                    'cost',
                    '$/l',
                    'l/100km',
                    'mpg (us)',
                    'mpg (imp)',
                    'days',
                    'partial',
                    'comments',
                ],
            )

            if kwargs['hide_partial']:
                df = df.drop(['partial'], axis=1)

            if kwargs['hide_comments']:
                df = df.drop(['comments'], axis=1)

            # -------
            # Summary Rows

            sum_columns = [
                'mileage',
                'fuel',
                'cost',
                'days',
            ]

            average_columns = [
                '$/l',
                'l/100km',
                'mpg (us)',
                'mpg (imp)',
            ]

            # calculate the summary stats on the dataframe before adding the rows.
            totals = df[sum_columns].sum(numeric_only=True, axis=0)
            minimums = df[sum_columns + average_columns].min(numeric_only=True, axis=0)
            maximums = df[sum_columns + average_columns].max(numeric_only=True, axis=0)
            averages = df[sum_columns + average_columns].mean(numeric_only=True, axis=0)

            df.loc['Sum'] = totals
            df.loc['Min'] = minimums
            df.loc['Max'] = maximums
            df.loc['Average'] = averages

            # ----------
            # Round Decimal Places

            df = df.round(
                {
                'mileage':1,
                'fuel':3,
                'cost':2,
                '$/l':3,
                'l/100km':3,
                'mpg (us)':3,
                'mpg (imp)':3,
                'days':1,
                },
            )

            # Remove any residual NaN
            df.fillna("", inplace=True)

            click.echo(df)
            click.echo()

            # Write to excel/ods/csv
