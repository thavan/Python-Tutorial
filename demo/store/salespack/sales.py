from .reader import read_csv  # relative import

import logging
import traceback

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class Sale(object):
    """Represents a single Sale
    """
    def __init__(self, name, date, count, price):
        self.name = name
        self.date = date
        self.count = count
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        try:
            value = float(value)
        except ValueError:
            logging.debug(traceback.format_exc())
            raise ValueError('Invalid price {}'.format(value))
        else:
            self._price = value

    @property
    def cost(self):
        return self.count * self.price


def read_sales(filename):
    total_cost = 0

    items = read_csv(filename, [str, str, int, float])
    sales = [Sale(name, date, count, price) for (name, date, count, price) in items]
    for sale in sales:
        total_cost += sale.cost
    return total_cost
