class Product:

    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = float(price)


class Discount:

    def __init__(self, product_code, discount_code, discount, min_units, units_applied):
        self.product_code = product_code
        self.discount_code = discount_code
        self.discount = float(discount)
        self.min_units = int(min_units)
        self.units_applied = units_applied