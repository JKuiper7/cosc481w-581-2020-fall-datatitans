# Generated by Django 3.1.2 on 2020-11-13 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0009_delete_post"),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP MATERIALIZED VIEW IF EXISTS data_country;
            CREATE MATERIALIZED VIEW data_country AS
            SELECT
                   iso_code,
                   location AS name,
                   continent,
                   population,
                   SUM(new_cases) AS total_cases,
                   SUM(new_deaths) AS total_deaths,
                   SUM(new_tests) AS total_tests,
                   SUM(new_cases / population * 1000000) AS total_cases_per_million,
                   SUM(new_deaths / population * 1000000) AS total_deaths_per_million,
                   SUM(new_tests / population * 1000) AS total_tests_per_thousand
            FROM data_coviddataraw
            WHERE iso_code IS NOT NULL AND continent IS NOT NULL
            GROUP BY iso_code, name, continent, population
            ORDER BY iso_code;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS data_country;
            CREATE MATERIALIZED VIEW data_country AS
            SELECT DISTINCT ON (data_coviddataclean.iso_code) data_coviddataclean.iso_code,
                                                              data_coviddataclean.location AS name,
                                                              data_coviddataclean.continent,
                                                              data_coviddataclean.population
            FROM data_coviddataclean
            ORDER BY data_coviddataclean.iso_code;
            """,
        )
    ]
