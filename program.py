#vinted backend task
INPUT_FILE = "input.txt"
PRICES_FILE = "prices.txt"

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
            return "True" + " " + self.date + " " + self.size + " " + self.carrier + " " + str(self.shipment_price) + " " + str(self.shipment_discount)
        else:
            return "False" + " " + self.date


def get_input_data():
    prices = []    
    with open(PRICES_FILE) as lines:
        for line in lines:
            fields = line.rstrip().split(" ")
            price = Price(fields[0], fields[1], float(fields[2]))
            prices.append(price)
    
    transactions = []
    with open(INPUT_FILE) as lines:
        for line in lines:
            fields = line.rstrip().split(" ")
            try:
                transaction = Transaction(True, fields[0], fields[1], fields[2], float(0), float(0))
                transactions.append(transaction)
            except:
                transaction = Transaction(False, line.rstrip(), "", "", float(0), float(0))
                transactions.append(transaction) 

    return prices, transactions

def main():
    prices, transactions = get_input_data()
    for i in transactions:
        print(i)

if __name__ == "__main__":
    main()