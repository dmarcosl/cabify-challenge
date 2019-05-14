import csv


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


def load_all_products():
    """ Read the products csv and returns all the products

    :return: List of Product entities with the values of the products
    """

    with open('./products.csv') as products:
        reader = csv.DictReader(products)
        return [Product(**row) for row in reader]


def load_product(code):
    """ Read the products csv and return the selected product

    :param code: (str) Code of the product
    :return: (Product) Selected product or None if not found
    """

    with open('./products.csv') as products:
        reader = csv.DictReader(products)
        for row in reader:
            if row.get('code') == code:
                return Product(**row)
    return None


def load_discounts_by_product(product_code):
    """ Read the discounts csv and return the discounts that can be applied to the selected product

    :param product_code: (str) Code of the product
    :return: (list) List of discounts
    """

    with open('./discounts.csv') as discounts:
        reader = csv.DictReader(discounts)
        return [Discount(**row) for row in reader if row.get('product_code') == product_code]


def checkout(product_dict):
    """ Calculate the final price of the items of the bag applying the discounts

    :param product_dict: (dict) Dictionary of code products and number of units (Example: {'TSHIRT': 1, 'VOUCHER': 2})
    :return: (float) Price of the products with discounts
    """

    final_price = 0.00

    for product_code, units in product_dict.items():
        # Load the product and calculate the price of all units
        product = load_product(product_code)
        product_price = product.price * units

        # Load the list of discounts
        discount_list = load_discounts_by_product(product_code)
        discount_value = 0.00

        for discount in discount_list:
            # Check if the bag has the minimum number of units
            if units // discount.min_units > 0:

                # Check if the discount apply to all units
                if discount.units_applied == '*':
                    discount_value += (units * discount.discount)
                # Or else the discount is applied to X units of every Y units
                else:
                    discount_value += (units // discount.min_units) * int(discount.units_applied) * discount.discount

        # Control that the product price doesn't go down less than 0
        if discount_value < product_price:
            product_price -= discount_value
        else:
            product_price = 0.00

        final_price += product_price

    return final_price


print(checkout({'TSHIRT': 1, 'VOUCHER': 1, 'MUG': 1}))
print(checkout({'TSHIRT': 1, 'VOUCHER': 2}))
print(checkout({'TSHIRT': 4, 'VOUCHER': 1}))
print(checkout({'TSHIRT': 3, 'VOUCHER': 3, 'MUG': 1}))
