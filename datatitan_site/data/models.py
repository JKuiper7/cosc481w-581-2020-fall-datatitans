# The "model" in django MVC architecture which sets up the database.

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


# Create your models here.
class Country(models.Model):
    iso_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=55)
    continent = models.CharField(max_length=15)
    population = models.IntegerField()

    def __str__(self):
        return self.name

    @cached_property
    def country_names(self):
        return list(Country.objects.values_list("iso_code", "name"))

    class Meta:
        managed = False


class CovidDataRaw(models.Model):
    iso_code = models.CharField(max_length=8, unique_for_date="date", null=True)
    continent = models.CharField(max_length=15, unique_for_date="date", null=True)
    location = models.CharField(max_length=55, unique_for_date="date", null=True)
    date = models.DateField()
    total_cases = models.IntegerField(null=True)
    new_cases = models.IntegerField(default=0, null=True)
    new_cases_smoothed = models.FloatField(null=True)
    total_deaths = models.IntegerField(null=True)
    new_deaths = models.IntegerField(default=0, null=True)
    new_deaths_smoothed = models.FloatField(null=True)
    total_cases_per_million = models.FloatField(null=True)
    new_cases_per_million = models.FloatField(null=True)
    new_cases_smoothed_per_million = models.FloatField(null=True)
    total_deaths_per_million = models.FloatField(null=True)
    new_deaths_per_million = models.FloatField(null=True)
    new_deaths_smoothed_per_million = models.FloatField(null=True)
    icu_patients = models.IntegerField(null=True)
    icu_patients_per_million = models.FloatField(null=True)
    hosp_patients = models.IntegerField(
        verbose_name="hospital patients", db_column="hosp_patients", null=True
    )
    hosp_patients_per_million = models.FloatField(
        verbose_name="hospital patients per million",
        db_column="hosp_patients_per_million",
        null=True,
    )
    weekly_icu_admissions = models.FloatField(null=True)
    weekly_icu_admissions_per_million = models.FloatField(null=True)
    weekly_hosp_admissions = models.FloatField(
        verbose_name="weekly hospital admissions",
        db_column="weekly_hosp_admissions",
        null=True,
    )
    weekly_hosp_admissions_per_million = models.FloatField(
        verbose_name="weekly hospital admissions per million",
        db_column="weekly_hosp_admissions_per_million",
        null=True,
    )
    new_tests = models.IntegerField(default=0, null=True)
    total_tests = models.IntegerField(null=True)
    total_tests_per_thousand = models.FloatField(null=True)
    new_tests_per_thousand = models.FloatField(null=True)
    new_tests_smoothed = models.FloatField(null=True)
    new_tests_smoothed_per_thousand = models.FloatField(null=True)
    tests_per_case = models.FloatField(null=True)
    positive_rate = models.FloatField(null=True)
    tests_units = models.TextField(null=True)
    stringency_index = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    population = models.PositiveBigIntegerField(null=True)
    population_density = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    median_age = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    aged_65_older = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    aged_70_older = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    gdp_per_capita = models.DecimalField(max_digits=9, decimal_places=3, null=True)
    extreme_poverty = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    cardiovasc_death_rate = models.DecimalField(
        max_digits=7, decimal_places=3, null=True
    )
    diabetes_prevalence = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    female_smokers = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    male_smokers = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    handwashing_facilities = models.DecimalField(
        max_digits=6, decimal_places=3, null=True
    )
    hospital_beds_per_thousand = models.DecimalField(
        max_digits=6, decimal_places=3, null=True
    )
    life_expectancy = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    human_development_index = models.DecimalField(
        max_digits=4, decimal_places=3, null=True
    )

    class Meta:
        indexes = [models.Index(fields=["iso_code", "date"])]
        ordering = ["iso_code", "date"]
        unique_together = ["iso_code", "date"]
        managed = False


class CovidDataClean(models.Model):
    iso_code = models.CharField(max_length=8, unique_for_date="date")
    continent = models.CharField(max_length=15, unique_for_date="date")
    location = models.CharField(max_length=55, unique_for_date="date")
    date = models.DateField()
    total_cases = models.IntegerField()
    new_cases = models.IntegerField(default=0)
    new_cases_smoothed = models.FloatField()
    total_deaths = models.IntegerField()
    new_deaths = models.IntegerField(default=0)
    new_deaths_smoothed = models.FloatField()
    total_cases_per_million = models.FloatField()
    new_cases_per_million = models.FloatField()
    new_cases_smoothed_per_million = models.FloatField()
    total_deaths_per_million = models.FloatField()
    new_deaths_per_million = models.FloatField()
    new_deaths_smoothed_per_million = models.FloatField()
    new_tests = models.IntegerField(default=0)
    total_tests = models.IntegerField()
    total_tests_per_thousand = models.FloatField()
    new_tests_per_thousand = models.FloatField()
    # new_tests_smoothed = models.FloatField()
    # new_tests_smoothed_per_thousand = models.FloatField()
    # tests_per_case = models.FloatField(null=True)
    # positive_rate = models.FloatField(null=True)
    # tests_units = models.TextField(null=True)
    # stringency_index = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    population = models.IntegerField()
    data_key = models.CharField(primary_key=True, max_length=20)

    class Meta:
        indexes = [models.Index(fields=["iso_code", "date"])]
        ordering = ["iso_code", "date"]
        unique_together = ["iso_code", "date"]
        managed = False


class Months(models.Model):
    month = models.DateField(primary_key=True)

    class Meta:
        indexes = [models.Index(fields=["month"])]
        ordering = ["month"]
        managed = False


class CovidDataMonthly(models.Model):
    iso_code = models.CharField(max_length=8, unique_for_month="month")
    continent = models.CharField(max_length=15, unique_for_month="month")
    location = models.CharField(max_length=55, unique_for_month="month")
    month = models.DateField()
    new_cases = models.IntegerField()
    new_deaths = models.IntegerField()
    new_tests = models.IntegerField()
    data_key = models.CharField(primary_key=True, max_length=20)

    class Meta:
        indexes = [models.Index(fields=["iso_code", "month"])]
        ordering = ["iso_code", "month"]
        unique_together = ["iso_code", "month"]
        managed = False


class Post(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


def publish(self):
    self.published_date = timezone.now()
    self.save()


def __str__(self):
    return self.title
