import csv


def read_csv(filename, types):
    """Reads a given csv file and returns a tuple with type converted values.
    """
    records = []
    with open(filename, 'r') as fileobj:
        reader = csv.reader(fileobj)
        headers = next(reader)

        types = dict(zip(headers, types))

        for row in reader:
            name = types['name'](row[0])
            date = types['date'](row[1])
            count = types['count'](row[2])
            price = types['price'](row[3])
            records.append((name, date, count, price))
    return records
