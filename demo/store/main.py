
import time

import salespack

if __name__ == '__main__':
    start = time.perf_counter()
    total_cost = salespack.read_sales('data/sales.csv')
    total_time = time.perf_counter() - start
    print("Total Cost: {}".format(total_cost))
    print("Total Time: {:.6f}".format(total_time))