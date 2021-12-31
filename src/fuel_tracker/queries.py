#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   006be758-69b6-11ec-a7f9-47c8c6b577fc
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-12-30
# -----------

"""
Contains SQLite specific queries. Modifications would need to be made to handle other databases.

"""

# ------------
# System Modules - Included with Python

# ------------
# 3rd Party - From PyPI

from sqlalchemy import (
    select,
    distinct,
    func,
    text,
    Integer,
)

from sqlalchemy.sql.expression import cast

# ------------
# Custom Modules

from .models import (
    Vehicle,
    FuelRecord,
)

# -------------


def vehicle_report(vid, tail=-1):
    """
    """

    # --------------
    # /*
    # This script is specific for SQLite. Mostly around the JULIANDAY function. Other
    # dialects will use DATEDIFF or other variant more directly
    # */

    # SELECT

    #     v.vehicle_id,
    #     f.fuel_id,
    #     f.fill_date,

    #     -- Determine the number of days since the last fill-up casting the value to
    #     -- an INTEGER to prevent the decimal place. We are not interested in
    #     -- partial days. If we were, we would use ROUND.

    #     CAST(JULIANDAY(f.fill_date) - LAG(JULIANDAY(f.fill_date), 1) OVER (
    #         ORDER BY f.fill_date ASC
    #     ) as INTEGER) AS days,

    #     f.mileage, -- in kilometers
    #     f.fuel,    -- in liters
    #     f.cost,    -- in dollars - could be USD or CAD or really any amount as long as they are all the same units

    #     -- Calculate cost per liter
    #     ROUND(f.cost/f.fuel, 3) AS cost_per_liter,

    #     -- Calculate l/100km
    #     ROUND(100*f.fuel/f.mileage, 3) AS l_per_100km,

    #     -- Calculate mpg using both the US and Imperial gallons - numbers from
    #     -- google

    #     ROUND((f.mileage*0.621371) / (f.fuel* 0.264172),3) AS mpg_us,
    #     ROUND((f.mileage*0.621371) / (f.fuel* 0.219969),3) AS mpg_imp

    # FROM VEHICLE AS v
    # INNER JOIN FUEL AS f
    #     ON f.vehicle_id = v.vehicle_id

    # WHERE v.vehicle_id = 4
    # ORDER By f.fill_date ASC
    # --------------


    # https://stackoverflow.com/questions/60515826/sqlalchemy-difference-between-two-dates

    # NOTE: func.julianday is SQLite specific and won't work with other
    # databases.

    # NOTE: if we remove the julianday, then it cannot use the lag
    # function and get the days for the previous fill up, leaving null.
    # This way we can see the n - 1 count, i.e. the number of days
    # since the last fill-up not in the tail.

    statement = (
        select(
            # Vehicle.vehicle_id,
            # Vehicle.name,
            FuelRecord.fuel_id,
            FuelRecord.fill_date,
            cast(func.julianday(FuelRecord.fill_date) - func.lag(func.julianday(FuelRecord.fill_date), 1, func.julianday(FuelRecord.fill_date)).over(order_by=FuelRecord.fill_date), Integer).label('days'),
            FuelRecord.mileage,
            FuelRecord.fuel,
            FuelRecord.cost,
            func.round(FuelRecord.cost/FuelRecord.fuel, 3).label('cost_per_liter'),
            func.round(100*FuelRecord.fuel/FuelRecord.mileage, 3).label('l_per_100km'),
            func.round((FuelRecord.mileage*0.621371)/(FuelRecord.fuel*0.264172), 3).label('mpg_us'),
            func.round((FuelRecord.mileage*0.621371)/(FuelRecord.fuel*0.219969), 3).label('mpg_imp'),
        )
        .select_from(Vehicle)
        .join(FuelRecord)
        .filter(Vehicle.vehicle_id == vid)
        .order_by(FuelRecord.fill_date.desc())
        .limit(tail)
    )

    return statement


def vehicle_report_summary(vid):
    """
    """

    # /*
    # This script is specific for SQLite. Mostly around the strftime function.
    # */

    # SELECT

    #     v.vehicle_id,
    #     strftime('%Y', f.fill_date) as year,
    #     COUNT(f.fill_date) as fill_ups,
    #     SUM(f.mileage) as total_mileage, -- in kilometers
    #     SUM(f.fuel) as total_fuel,    -- in liters
    #     SUM(f.cost) as total_cost,    -- in dollars - could be USD or CAD or really any amount as long as they are all the same units

    #     MIN(f.mileage) as min_mileage,
    #     MAX(f.mileage) as max_mileage,
    #     ROUND(AVG(f.mileage), 1) as avg_mileage,

    #     MIN(f.fuel) as min_fuel,
    #     MAX(f.fuel) as max_fuel,
    #     ROUND(AVG(f.fuel),3) as avg_fuel,


    #     MIN(f.cost) AS min_cost,
    #     MAX(f.cost) AS max_cost,
    #     ROUND(AVG(f.cost),3) AS avg_cost,

    #     -- Calculate overall cost per liter - also avg cost over the year
    #     ROUND(SUM(f.cost)/SUM(f.fuel), 3) AS cost_per_liter,

    #     -- Calculate overall l/100km
    #     ROUND(100*SUM(f.fuel)/SUM(f.mileage), 3) AS l_per_100km,

    #     -- Calculate mpg using both the US and Imperial gallons - numbers from
    #     -- google
    #     ROUND((SUM(f.mileage)*0.621371) / (SUM(f.fuel)* 0.264172),3) AS mpg_us,
    #     ROUND((SUM(f.mileage)*0.621371) / (SUM(f.fuel)* 0.219969),3) AS mpg_imp

    # FROM VEHICLE AS v
    # INNER JOIN FUEL AS f ON f.vehicle_id = v.vehicle_id
    # WHERE v.vehicle_id = 4
    # GROUP BY strftime('%Y', f.fill_date)
    # ORDER By f.fill_date DESC

    statement = (
        select(
            # Vehicle.vehicle_id,
            # Vehicle.name,
            func.strftime('%Y', FuelRecord.fill_date).label('year'),
            func.count(FuelRecord.fill_date).label('fill_ups'),

            func.round(func.sum(FuelRecord.mileage), 1).label('total_mileage'),
            func.round(func.sum(FuelRecord.fuel), 3).label('total_fuel'),
            func.round(func.sum(FuelRecord.cost), 2).label('total_cost'),

            func.round(func.sum(FuelRecord.cost)/func.sum(FuelRecord.fuel), 3).label('avg_cost_per_liter'),
            func.round(100*func.sum(FuelRecord.fuel)/func.sum(FuelRecord.mileage), 3).label('avg_l_per_100km'),
            func.round((func.sum(FuelRecord.mileage)*0.621371)/(func.sum(FuelRecord.fuel)*0.264172), 3).label('mpg_us'),
            func.round((func.sum(FuelRecord.mileage)*0.621371)/(func.sum(FuelRecord.fuel)*0.219969), 3).label('mpg_imp'),

            func.round(func.min(FuelRecord.mileage), 1).label('min_mileage'),
            func.round(func.max(FuelRecord.mileage), 1).label('max_mileage'),
            func.round(func.avg(FuelRecord.mileage), 1).label('avg_mileage'),

            func.round(func.min(FuelRecord.fuel), 3).label('min_fuel'),
            func.round(func.max(FuelRecord.fuel), 3).label('max_fuel'),
            func.round(func.avg(FuelRecord.fuel), 3).label('avg_fuel'),

            func.round(func.min(FuelRecord.cost), 2).label('min_cost'),
            func.round(func.max(FuelRecord.cost), 2).label('max_cost'),
            func.round(func.avg(FuelRecord.cost), 2).label('avg_cost'),
        )
        .select_from(Vehicle)
        .join(FuelRecord)
        .filter(Vehicle.vehicle_id == vid)
        .order_by(FuelRecord.fill_date.asc())
        .group_by(func.strftime('%Y', FuelRecord.fill_date))
    )

    return statement


# ---------------------
# This uses the raw sql and the text() function - it works, but is specific to SQLite
# def vehicle_report(vid, tail=-1):
#     """
#     """

#     # --------------
#     # /*
#     # This script is specific for SQLite. Mostly around the JULIANDAY function. Other
#     # dialects will use DATEDIFF or other variant more directly
#     # */

#     # SELECT

#     #     v.vehicle_id,
#     #     f.fuel_id,
#     #     f.fill_date,

#     #     -- Determine the number of days since the last fill-up casting the value to
#     #     -- an INTEGER to prevent the decimal place. We are not interested in
#     #     -- partial days. If we were, we would use ROUND.

#     #     CAST(JULIANDAY(f.fill_date) - LAG(JULIANDAY(f.fill_date), 1) OVER (
#     #         ORDER BY f.fill_date ASC
#     #     ) as INTEGER) AS days,

#     #     f.mileage, -- in kilometers
#     #     f.fuel,    -- in liters
#     #     f.cost,    -- in dollars - could be USD or CAD or really any amount as long as they are all the same units

#     #     -- Calculate cost per liter
#     #     ROUND(f.cost/f.fuel, 3) AS cost_per_liter,

#     #     -- Calculate l/100km
#     #     ROUND(100*f.fuel/f.mileage, 3) AS l_per_100km,

#     #     -- Calculate mpg using both the US and Imperial gallons - numbers from
#     #     -- google

#     #     ROUND((f.mileage*0.621371) / (f.fuel* 0.264172),3) AS mpg_us,
#     #     ROUND((f.mileage*0.621371) / (f.fuel* 0.219969),3) AS mpg_imp

#     # FROM VEHICLE AS v
#     # INNER JOIN FUEL AS f
#     #     ON f.vehicle_id = v.vehicle_id

#     # WHERE v.vehicle_id = 4
#     # ORDER By f.fill_date ASC
#     # --------------


#     # statement = (
#     #             select(FuelRecord)
#     #                 .join(Vehicle)
#     #                 .where(FuelRecord.vehicle_id == v.vehicle_id)
#     #                 .order_by(FuelRecord.fill_date.desc())
#     #                 .limit(kwargs["records"])
#     #         )

#     # https://stackoverflow.com/questions/60515826/sqlalchemy-difference-between-two-dates

#     # NOTE: func.julianday is SQLite specific and won't work with other databases.

#     statement = (
#         "SELECT",
#         "v.vehicle_id,",
#         "f.fuel_id,",
#         "f.fill_date,",
#         "CAST(JULIANDAY(f.fill_date) - LAG(JULIANDAY(f.fill_date), 1) OVER (",
#             "ORDER BY f.fill_date ASC",
#         ") as INTEGER) AS days,",
#         "f.mileage,",
#         "f.fuel,",
#         "f.cost,",
#         "ROUND(f.cost/f.fuel, 3) AS cost_per_liter,",
#         "ROUND(100*f.fuel/f.mileage, 3) AS l_per_100km,",
#         "ROUND((f.mileage*0.621371) / (f.fuel* 0.264172),3) AS mpg_us,",
#         "ROUND((f.mileage*0.621371) / (f.fuel* 0.219969),3) AS mpg_imp",
#         "FROM VEHICLE AS v",
#         "INNER JOIN FUEL AS f",
#         "ON f.vehicle_id = v.vehicle_id",
#         f"WHERE v.vehicle_id = {vid}",
#         "ORDER By f.fill_date ASC",
#         f"LIMIT {tail}"
#     )

#     return text('\n'.join(statement))
