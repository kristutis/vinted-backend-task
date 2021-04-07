# py.exe -m unittest
import unittest
from program import Transaction, Price
from program import get_lowest_price
from program import get_input_data

price1 = Price("AAA", "X", 5.5)
price2 = Price("BBB", "X", 10.9)
price2 = Price("CCC", "Y", 4.8)
prices = [price1, price2]

class TestLowestPrice(unittest.TestCase):
    # checking returning values from the methods
    def test_price(self):
        self.assertAlmostEqual(get_lowest_price(prices, "X"), 5.5)

    # checking if a program raises an error if a wrong input file was given
    def test_wrong_input_file(self):
        self.assertRaises(FileNotFoundError, get_input_data, "prices.txt", "wrongfile.txt")
