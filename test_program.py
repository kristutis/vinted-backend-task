# py.exe -m unittest
import unittest
from program import Transaction, Price
from program import get_lowest_price
from program import get_input_data
from program import get_provider_shipment_price
from program import apply_rule1
from program import apply_rule2
from program import format_months_dict

# mock data
price1 = Price("AAA", "X", 1.50)
price2 = Price("BBB", "X", 10.9)
price3 = Price("CCC", "Y", 4.8)
price4 = Price("MR", "S", 2)
prices = [price1, price2, price3, price4]

class TestPrices(unittest.TestCase):
    # checking returning values from the methods
    def test_lowest_price(self):        
        self.assertAlmostEqual(get_lowest_price(prices, "X"), 1.5)

    def test_shipment_price(self):
        self.assertAlmostEqual(get_provider_shipment_price(prices, "BBB", "X"), 10.9)

class TestExceptions(unittest.TestCase):
    # checking if a program raises an error if a wrong input file was given
    def test_wrong_input_file(self):
        self.assertRaises(FileNotFoundError, get_input_data, "prices.txt", "wrongfile.txt")

    def test_wrong_type(self):
        with self.assertRaises(NotImplementedError):
            t = Transaction(True, "", "", "")
            price1==t

transaction = Transaction(True, "2015-02-06", "S", "MR")
transaction1 = Transaction(True, "2015-02-05", "L", "LP")
transaction2 = Transaction(True, "2015-02-07", "L", "LP")
transaction3 = Transaction(True, "2015-02-24", "L", "LP")
transaction4 = Transaction(True, "2015-02-10", "L", "LP")
transaction5 = Transaction(True, "2015-03-24", "L", "LP")
transaction6 = Transaction(True, "2015-03-24", "L", "LP")
transactions = [transaction1, transaction2, transaction3, transaction4, transaction5, transaction6]

class TestRules(unittest.TestCase):
    def test_discount_rules1(self):        
        shipment_price, discount, total_discount = apply_rule1(transaction, prices, 1.5, 9.90)
        self.assertAlmostEqual(shipment_price, 1.90)
        self.assertAlmostEqual(discount, 0.10)
        self.assertAlmostEqual(total_discount, 10)

    def test_discount_rule2(self):
        counter, iterator, applied_discount = format_months_dict(transactions, 1, 2)
        # tests start
        shipment_price, discount, counter, iterator, applied_discount[transactions[0].get_yyyy_mm()] = apply_rule2(transactions[0], 4.40, counter, iterator, applied_discount[transactions[0].get_yyyy_mm()])
        self.assertEqual(shipment_price, 4.40)
        self.assertEqual(discount, 0)
        shipment_price, discount, counter, iterator, applied_discount[transactions[1].get_yyyy_mm()] = apply_rule2(transactions[1], 4.40, counter, iterator, applied_discount[transactions[1].get_yyyy_mm()])
        self.assertEqual(shipment_price, 0)
        self.assertEqual(discount, 4.40)
        shipment_price, discount, counter, iterator, applied_discount[transactions[2].get_yyyy_mm()] = apply_rule2(transactions[2], 4.40, counter, iterator, applied_discount[transactions[2].get_yyyy_mm()])
        self.assertEqual(shipment_price, 4.40)
        self.assertEqual(discount, 0)
        shipment_price, discount, counter, iterator, applied_discount[transactions[3].get_yyyy_mm()] = apply_rule2(transactions[3], 4.40, counter, iterator, applied_discount[transactions[3].get_yyyy_mm()])
        self.assertEqual(shipment_price, 4.40)
        self.assertEqual(discount, 0)
        shipment_price, discount, counter, iterator, applied_discount[transactions[4].get_yyyy_mm()] = apply_rule2(transactions[4], 4.40, counter, iterator, applied_discount[transactions[4].get_yyyy_mm()])
        self.assertEqual(shipment_price, 4.40)
        self.assertEqual(discount, 0)
        shipment_price, discount, counter, iterator, applied_discount[transactions[5].get_yyyy_mm()] = apply_rule2(transactions[5], 4.40, counter, iterator, applied_discount[transactions[5].get_yyyy_mm()])
        self.assertEqual(shipment_price, 0)
        self.assertEqual(discount, 4.40)

class TestOverrides(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(transaction1==transaction2, False)

    def test_lt(self):
        self.assertEqual(price1 < price2, True)