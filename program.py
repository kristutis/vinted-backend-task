#vinted backend task
INPUT_FILE = "input.txt"
PRICES_FILE = "prices.txt"
MAX_DISCOUNT = 10
LOWEST_PRICE_SIZE = "S"
FREE_SHIPMENT_SIZE = "L"
FREE_SHIPMENT_PROVIDER = "LP"
FREE_SHIPMENTS_IN_MONTH = 1
FREE_SHIPMENT_ITERATIVE = 3

class Price:
    def __init__(self, provider, package_size, price):
        self.provider = provider
        self.package_size = package_size
        self.price = price

    def __str__(self):
        return self.provider + " " + self.package_size + " " + str(self.price)

class Transaction:
    def __init__(self, valid, date, size, carrier, shipment_price, shipment_discount):
        self.valid = valid
        self.date = date
        self.size = size
        self.carrier = carrier
        self.shipment_price = float(0)
        self.shipment_discount = float(0)

    def __str__(self):
        if self.valid:
            if self.shipment_discount == 0:
                discount = "-"
            else:
                discount = str(self.shipment_discount)
            return self.date + " " + self.size + " " + self.carrier + " " + str(self.shipment_price) + " " + discount
        else:
            return self.date + " Ignored"
    
    def get_yyyy_mm(self):
        fields = self.date.split("-")
        return fields[0] + "-" + fields[1]


def get_input_data(prices_file, input_file):
    prices = []    
    with open(prices_file) as lines:
        for line in lines:
            fields = line.rstrip().split(" ")
            price = Price(fields[0], fields[1], float(fields[2]))
            prices.append(price)
    
    transactions = []
    with open(input_file) as lines:
        for line in lines:
            fields = line.rstrip().split(" ")
            try:
                transaction = Transaction(True, fields[0], fields[1], fields[2], float(0), float(0))
                transactions.append(transaction)
            except:
                transaction = Transaction(False, line.rstrip(), "", "", float(0), float(0))
                transactions.append(transaction) 

    return prices, transactions

def get_lowest_price(prices, target):
    lowest = float('inf')
    for i in prices:
        if i.package_size == target and i.price < lowest:
            lowest = i.price
    return lowest

def apply_rule1(transaction, prices, lowest_price, applied_discount):
    for i in prices:
        if i.provider == transaction.carrier and i.package_size == transaction.size:
            discount = i.price - lowest_price
            if discount + applied_discount > MAX_DISCOUNT:
                discount = MAX_DISCOUNT - applied_discount
            transaction.shipment_price = i.price - discount
            transaction.shipment_discount = discount
            return transaction.shipment_price, transaction.shipment_discount, float(applied_discount + discount)

def apply_rule2(transaction, price, free_shipments_counter, free_shipments_iterator, applied_discount):
    month = transaction.get_yyyy_mm()

    if free_shipments_counter[month] > 0:
        if free_shipments_iterator[month] == 1:
            free_shipments_iterator[month] = 3
            free_shipments_counter[month] -= 1
            if applied_discount + price > MAX_DISCOUNT:
                discount = MAX_DISCOUNT - applied_discount
                return price - discount, free_shipments_counter, free_shipments_iterator, applied_discount + discount
            else:
                return 0, price, free_shipments_counter, free_shipments_iterator, applied_discount + price
        else:
            free_shipments_iterator[month] -= 1
            return price, 0, free_shipments_counter, free_shipments_iterator, applied_discount
    else:
        return price, 0, free_shipments_counter, free_shipments_iterator, applied_discount

def format_months_dict(transactions):    
    counter = dict()
    iterator = dict()
    applied_discount = dict()
    for i in transactions:
        month = i.get_yyyy_mm()
        if not month in counter:
            counter[month] = FREE_SHIPMENTS_IN_MONTH
            iterator[month] = FREE_SHIPMENT_ITERATIVE
            applied_discount[month] = float(0)
    return counter, iterator, applied_discount

def get_provider_shipment_price(prices, provider, size):
    for i in prices:
        if i.provider == provider and i.package_size == size:
            return i.price

def calculate_transactions(prices, transactions):    
    free_shipments_counter, free_shipments_iterator, applied_discount = format_months_dict(transactions)
    lowest_price = get_lowest_price(prices, LOWEST_PRICE_SIZE)

    for i in transactions:
        calculated = False
        if not i.valid:
            continue
        if i.size == LOWEST_PRICE_SIZE:
            month = i.get_yyyy_mm()
            i.shipment_price, i.shipment_discount, applied_discount[month] = apply_rule1(i, prices, lowest_price, applied_discount[month])
            calculated = True
        if i.size == FREE_SHIPMENT_SIZE and i.carrier == FREE_SHIPMENT_PROVIDER:
            month = i.get_yyyy_mm()
            price = get_provider_shipment_price(prices, FREE_SHIPMENT_PROVIDER, FREE_SHIPMENT_SIZE)
            i.shipment_price, i.shipment_discount, free_shipments_counter, free_shipments_iterator, applied_discount[month] = apply_rule2(i, price, free_shipments_counter, free_shipments_iterator, applied_discount[month])
            calculated = True
        if not calculated:
            i.shipment_price = get_provider_shipment_price(prices, i.carrier, i.size)

    for i in transactions:
        print(i)

def main():
    prices, transactions = get_input_data(PRICES_FILE, INPUT_FILE)
    calculate_transactions(prices, transactions)

if __name__ == "__main__":
    main()