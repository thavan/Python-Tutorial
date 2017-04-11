import unittest
import salespack

from salespack.sales import Sale


class TestSales(unittest.TestCase):
    def setUp(self):
        self.sale = Sale('Apple', '2012-12-23', 10, 20)

    def test_total(self):
        self.assertEqual(3294, salespack.read_sales('data/sales.csv'))

    def test_cost(self):
        self.assertEqual(200, self.sale.cost)

    def test_price_valid(self):
        with self.assertRaises(ValueError):
            self.sale.price = 'invalid'

    def tearDown(self):
        del self.sale


if __name__ == '__main__':
    unittest.main()