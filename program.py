#vinted backend task

# constants
INPUT_FILE = "input.txt"            # member's transactions data
PRICES_FILE = "prices.txt"          # data with a list of providers, sizes and prices for shipment
MAX_DISCOUNT = 10                   # maximum discount available for a month
LOWEST_PRICE_SIZE = "S"             # size of a package, that the cost above the lowest of all providers will be covered
FREE_SHIPMENT_SIZE = "L"            # size of a package. Every third package of this size will sent for free (once in a month)
FREE_SHIPMENT_PROVIDER = "LP"       # provider of which every third L size package shipment cost will covered
FREE_SHIPMENTS_IN_MONTH = 1         # number of L size free shipments in a month
FREE_SHIPMENT_ITERATIVE = 3         # number of L size packages to be sent until a member gets one free shipment

'''
class to save prices of diferent providers and package sizes
e. g. provider = "LP", package_size = S, price = 5.50
'''
class Price:
    def __init__(self, provider, package_size, price):
        self.provider = provider
        self.package_size = package_size
        self.price = price

    def __str__(self):
        return self.provider + " " + self.package_size + " " + str(self.price)

'''
class to save input data from .txt file
valid - true if data is correct
date - date of transaction
size - size of a package (S, M, L)
carrier - provider service (LP, MR)
shipment_price - price to be paid by a member
shipment_discount - discount, price to be paid by Vinted
'''
class Transaction:
    def __init__(self, valid, date, size, carrier):
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
                discount = "{0:.2f}".format(round(self.shipment_discount, 2))
            return "{0} {1} {2} {3:.2f} {4}".format(self.date, self.size, self.carrier, round(self.shipment_price, 2), discount)
        else:
            return self.date + " Ignored"
    
    def get_yyyy_mm(self):
        if self.valid:
            fields = self.date.split("-")
            return fields[0] + "-" + fields[1]
        else:
            return "Invalid data"

# method to get data from input files
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
            try:
                fields = line.rstrip().split(" ")
                transaction = Transaction(True, fields[0], fields[1], fields[2])
                transactions.append(transaction)
            except:
                transaction = Transaction(False, line.rstrip(), "", "")
                transactions.append(transaction) 

    return prices, transactions

# method to get lowest price for a targeted package size
def get_lowest_price(prices, target):
    lowest = float('inf')
    for i in prices:
        if i.package_size == target and i.price < lowest:
            lowest = i.price
    return lowest

# method to calculate discount and price to be paid by a memeber, if package size is S
def apply_rule1(transaction, prices, lowest_price, applied_discount):
    for i in prices:
        if i.provider == transaction.carrier and i.package_size == transaction.size:
            discount = i.price - lowest_price
            if discount + applied_discount > MAX_DISCOUNT:
                discount = MAX_DISCOUNT - applied_discount
            transaction.shipment_price = i.price - discount
            transaction.shipment_discount = discount
            return transaction.shipment_price, transaction.shipment_discount, float(applied_discount + discount)

# method to calculate discount and price to be paid by a memeber, if package is size of L
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

# method to get key-value pairs that will be used count the amount of L size packages sent in a month
def format_months_dict(transactions, free_shipments_in_month, free_shipment_iterative):    
    counter = dict()
    iterator = dict()
    applied_discount = dict()
    for i in transactions:
        month = i.get_yyyy_mm()
        if not month in counter:
            counter[month] = free_shipments_in_month
            iterator[month] = free_shipment_iterative
            applied_discount[month] = float(0)
    return counter, iterator, applied_discount

# method to get a price required to pay for the given transaction
def get_provider_shipment_price(prices, provider, size):
    for i in prices:
        if i.provider == provider and i.package_size == size:
            return i.price

# method to find how much a member has to pay and to find the discount for the shipment
def calculate_transactions(prices, transactions):    
    free_shipments_counter, free_shipments_iterator, applied_discount = format_months_dict(transactions, FREE_SHIPMENTS_IN_MONTH, FREE_SHIPMENT_ITERATIVE)
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
            i.shipment_price, i.shipment_discount, free_shipments_counter, free_shipments_iterator, applied_discount[month] = apply_rule2(
                                                        i, price, free_shipments_counter, free_shipments_iterator, applied_discount[month]
                                                        )
            calculated = True
        if not calculated:
            i.shipment_price = get_provider_shipment_price(prices, i.carrier, i.size)

    return transactions

# the program starts here
def main():
    prices, transactions = get_input_data(PRICES_FILE, INPUT_FILE)
    transactions = calculate_transactions(prices, transactions)
    for i in transactions:
        print(i)

if __name__ == "__main__":
    main()