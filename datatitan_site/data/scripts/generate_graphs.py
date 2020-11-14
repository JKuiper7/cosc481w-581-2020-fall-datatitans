# import matplotlib.pyplot as plt
# import mpld3
from data.models import CovidDataClean, Country, Months, CovidDataMonthly
from django.core.cache import cache
import numpy as np
from django.db.models import Sum, F, Window, TextField, FloatField, IntegerField
from django.db.models.functions import TruncMonth, Coalesce, Cast


def gen_graph(
    *iso_codes, category: str, chart_type: str = "line", metric: str = "raw"
) -> dict:
    """Creates a graph that tracks a data category over time for an arbitrary number of countries.

    :param iso_codes: ISO codes of countries to create graphs for
    :param category: The category of data to track (currently supported categories: total_cases, total_deaths)
    :param chart_type: The type of graph to generate (currently supported graphs: line)
    :param metric: Whether to display raw numbers, or to display the numbers per thousand/million
    :return: A dictionary representing the generated graph
    :rtype: dict
    """
    if len(iso_codes) == 0:
        return {}
    category_name = (
        f"""{"new" if chart_type.lower() == "bar" else "total"}_{category}"""
    )
    if metric == "normalized":
        category_name += f"""_per_{"thousand" if category == "tests" else "million"}"""

    selected_countries = Country.objects.filter(iso_code__in=iso_codes)

    title = (
        category_name.replace("_", " ").title()
        + " in "
        + ", ".join(
            cache.get_or_set(
                f"country_name_{code}", selected_countries.get(iso_code=code).name
            )
            if not (country_name := cache.get(f"country_name_{code}"))
            else country_name
            for code in iso_codes
        )
    )

    data_sets = []
    if chart_type.lower() == "line":
        # Fairly simple implementation
        base_query = CovidDataClean.objects.filter(iso_code__in=iso_codes)
        data_sets = [
            {
                "label": code,
                "data": list(
                    base_query.filter(iso_code=code).values(
                        x=Cast(F("date"), TextField()),
                        y=Cast(F(category_name.lower()), IntegerField()),
                    )
                ),
                # "parsing": {
                #     "yAxisKey": category_name.lower()
                # }
            }
            for code in iso_codes
        ]
    elif chart_type.lower() == "bar":
        # This was an absolute nightmare to figure out
        base_query = CovidDataMonthly.objects.filter(iso_code__in=iso_codes)
        data_sets = [
            {
                "label": code,
                "data": list(
                    base_query.filter(iso_code=code).values(
                        x=Cast(F("month"), TextField()),
                        y=Cast(
                            F(category_name.lower()),
                            IntegerField() if metric == "raw" else FloatField(),
                        ),
                    )
                ),
                # "stack": code
            }
            for code in iso_codes
        ]
    return {
        "type": chart_type.lower(),
        "data": {"datasets": data_sets},
        "options": {
            "scales": {
                "xAxes": [
                    {
                        "type": "time",
                        "time": {"unit": "month"},
                        "stacked": chart_type.lower() == "bar",
                        "offset": True,
                    }
                ],
                # "yAxes": [{
                #     "stacked": chart_type.lower() == "bar"
                # }]
            }
        },
    }
