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


    # statement = (
    #             select(FuelRecord)
    #                 .join(Vehicle)
    #                 .where(FuelRecord.vehicle_id == v.vehicle_id)
    #                 .order_by(FuelRecord.fill_date.desc())
    #                 .limit(kwargs["records"])
    #         )

    # https://stackoverflow.com/questions/60515826/sqlalchemy-difference-between-two-dates

    # NOTE: func.julianday is SQLite specific and won't work with other databases.

    statement = (
        select(
            Vehicle.vehicle_id,
            Vehicle.name,
            FuelRecord.fuel_id,
            FuelRecord.fill_date,
            # func.lag(FuelRecord.fill_date, 1).over(order_by=FuelRecord.fill_date).label('previous'),
            cast(func.julianday(FuelRecord.fill_date) - func.lag(func.julianday(FuelRecord.fill_date), 1).over(order_by=FuelRecord.fill_date), Integer).label('days'),
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
        .order_by(FuelRecord.fill_date.asc())
        .limit(tail)
    )

    return statement


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
