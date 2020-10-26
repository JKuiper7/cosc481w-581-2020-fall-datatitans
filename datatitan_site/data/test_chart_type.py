import unittest
# import forms.py
# import generate_graphs.py

# import sys
# print (sys.path)
# sys.path.insert(0, 'C:/Users/ryanp/git/cosc481w-581-2020-fall-datatitans/datatitan_site/data/scripts')
# import generate_graphs



class ChartTest(unittest.TestCase):
    
    def setUp(self):
        # Arrange
        self.nocodes = ()
        self.none = ()
        self.line = ("LINE")
        
    def tearDown(self):
        # print("tearDown called...")
        self.a = ()
        self.str1 = ()
    
    def test_no_chart(self):
        result = gen_no_chart(*self.nocodes, category=str(""))
        
        # Assert
        self.assertEqual(result, '')

    def test_line_chart(self):
        # No function to call in forms.py, other than init
        result = gen_line_chart(*self.nocodes, category=str("LINE"))
        # Assert
        self.assertEqual(result, "LINE")

    def test_bar_chart(self):
        # No function to call in forms.py, other than init
        result = gen_bar_chart(*self.nocodes, category=str("BAR"))
        # Assert
        self.assertEqual(result, "BAR")


    


def gen_no_chart(*iso_codes, category: str, chart_type="") -> str:
    print("chart type: ", chart_type)
    return chart_type

def gen_line_chart(*iso_codes, category: str, chart_type="LINE") -> str:
    print("chart type: ", chart_type)
    return chart_type

def gen_bar_chart(*iso_codes, category: str, chart_type="BAR") -> str:
    print("chart type: ", chart_type)
    return chart_type

if __name__ == "__main__":
    unittest.main()