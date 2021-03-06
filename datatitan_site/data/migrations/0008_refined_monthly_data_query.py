# Generated by Django 3.1.2 on 2020-11-05 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0007_updated_monthly_data"),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP MATERIALIZED VIEW IF EXISTS data_coviddatamonthly;
            CREATE MATERIALIZED VIEW data_coviddatamonthly AS
            SELECT data_coviddataclean.iso_code,
                   data_coviddataclean.continent,
                   data_coviddataclean.location,
                   date(date_trunc('month'::text,
                                   data_coviddataclean.date::timestamp with time zone))      AS month,
                   sum(
                           COALESCE(data_coviddataclean.new_cases, 0::numeric))              AS new_cases,
                   sum(
                           COALESCE(data_coviddataclean.new_deaths, 0::numeric))             AS new_deaths,
                   sum(
                           COALESCE(data_coviddataclean.new_tests, 0::numeric))              AS new_tests,
                   sum(
                           COALESCE(data_coviddataclean.new_cases_per_million, 0::numeric))  AS new_cases_per_million,
                   sum(
                           COALESCE(data_coviddataclean.new_deaths_per_million, 0::numeric)) AS new_deaths_per_million,
                   sum(
                           COALESCE(data_coviddataclean.new_tests_per_thousand, 0::numeric)) AS new_tests_per_thousand,
                   concat(date(date_trunc(
                           'month'::text,
                           data_coviddataclean.date::timestamp with time zone)))             AS data_key
            FROM data_coviddataclean
            GROUP BY iso_code, month, continent, location
            ORDER BY data_coviddataclean.iso_code, month;

            ALTER MATERIALIZED VIEW data_coviddatamonthly OWNER TO "DataTitans";
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS data_coviddatamonthly;
            CREATE MATERIALIZED VIEW data_coviddatamonthly AS
            SELECT
            DISTINCT ON ("data_coviddataclean"."iso_code", DATE(DATE_TRUNC('month', data_coviddataclean.date :: timestamp with time zone))) "data_coviddataclean"."iso_code",
                "data_coviddataclean"."continent",
                "data_coviddataclean"."location",
                DATE(DATE_TRUNC('month', "data_coviddataclean"."date")) AS "month",
                SUM(COALESCE("data_coviddataclean"."new_cases", 0)) OVER (PARTITION BY "data_coviddataclean"."iso_code", DATE_TRUNC('month', "data_coviddataclean"."date")) AS "new_cases",
                SUM(COALESCE("data_coviddataclean"."new_deaths", 0)) OVER (PARTITION BY "data_coviddataclean"."iso_code", DATE_TRUNC('month', "data_coviddataclean"."date")) AS "new_deaths",
                SUM(COALESCE("data_coviddataclean"."new_tests", 0)) OVER (PARTITION BY "data_coviddataclean"."iso_code", DATE_TRUNC('month', "data_coviddataclean"."date")) AS "new_tests",
                SUM(COALESCE("data_coviddataclean"."new_cases_per_million", 0)) OVER (PARTITION BY "data_coviddataclean"."iso_code", DATE_TRUNC('month', "data_coviddataclean"."date")) AS "new_cases_per_million",
                SUM(COALESCE("data_coviddataclean"."new_deaths_per_million", 0)) OVER (PARTITION BY "data_coviddataclean"."iso_code", DATE_TRUNC('month', "data_coviddataclean"."date")) AS "new_deaths_per_million",
                SUM(COALESCE("data_coviddataclean"."new_tests_per_thousand", 0)) OVER (PARTITION BY "data_coviddataclean"."iso_code", DATE_TRUNC('month', "data_coviddataclean"."date")) AS "new_tests_per_thousand",
                CONCAT(DATE(DATE_TRUNC('month'::text, data_coviddataclean.date::timestamp with time zone))) as data_key
            FROM "data_coviddataclean" ORDER BY "data_coviddataclean"."iso_code", "month";

            ALTER MATERIALIZED VIEW data_coviddatamonthly OWNER TO "DataTitans";
            """,
        )
    ]
