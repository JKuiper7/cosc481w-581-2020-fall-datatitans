from django.test import TestCase
from data.models import CovidDataRaw, Post, CovidDataClean, Country
from data.scripts.generate_graphs import gen_graph
import pandas as pd
from data.scripts.database_handler import input_file_path, initialize_table
import urllib.request


# Create your tests here.


class DatabaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Initialize the test database, and read the input csv file into a pandas dataframe"""
        cls.raw_data: pd.DataFrame = pd.read_csv(
            "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        )
        decimals = {
            "stringency_index": 2,
            "median_age": 1,
            "extreme_poverty": 1,
            "diabetes_prevalence": 2,
            "life_expectancy": 2,
        }
        cls.raw_data = (
            cls.raw_data.round(decimals=3)
            .round(decimals=decimals)
            .where(cls.raw_data.notnull(), None)
        )
        initialize_table()

    def test_upload(self) -> None:
        """Verify that the number of entries in the database match the data pulled from the csv file"""
        stored_raw_data = CovidDataRaw.objects.values("iso_code", "date")
        self.assertEqual(stored_raw_data.count(), len(self.raw_data), f"Expected number of rows: {len(self.raw_data)}; Actual number of rows: {stored_raw_data.count()}")

    def test_materialized_views(self) -> None:
        """Verify that the materialized views work for the test database"""
        clean_data_count = len(self.raw_data.dropna(subset=["iso_code", "continent"]))
        stored_clean_data_count = CovidDataClean.objects.count()
        self.assertNotEqual(stored_clean_data_count, 0)
        self.assertEqual(
            stored_clean_data_count,
            clean_data_count,
            f"Expected number of rows: {clean_data_count}; Actual number of rows: {stored_clean_data_count}",
        )

    def test_graph(self) -> None:
        """Verify that the graph generator outputs a graph"""
        result = gen_graph("USA", category="deaths", chart_type="LINE")
        self.assertIs(type(result), str, "Test failed: output is not a string.")
        self.assertNotEqual(result, "", "Test failed: graph was not generated.")

    def test_graph_without_codes(self) -> None:
        """Verify that the graph generator does not output a graph when provided with no countries"""
        result = gen_graph(*[], category="cases", chart_type="LINE")
        self.assertIs(type(result), str, "Test failed: output is not a string.")
        self.assertEqual(result, "", "Test failed: graph has been generated.")


class BlogTestCase(TestCase):
    """Rewrite of Ben Potter's test"""

    def setUp(self) -> None:
        """Generate a blog post from a call to a Lorem Ipsum API"""
        self.blog_post = {
            "author": "Marcus Tullius Cicero",
            "title": "Lorem Ipsum",
            "text": urllib.request.urlopen(
                url="https://loripsum.net/api/3/medium/plaintext"
            )
            .read()
            .decode("UTF-8"),
        }
        self.test_post = Post(**self.blog_post)
        self.test_post.save()

    def test_blog(self) -> None:
        """Verify that the contents of the blog post match what was generated"""
        for key, val in self.blog_post.items():
            self.assertEqual(val, self.test_post.__getattribute__(key))
