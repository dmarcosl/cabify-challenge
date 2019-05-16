import csv
import random
import shelve
import string

from flask import jsonify, Blueprint, request
from flask_cors import cross_origin

from models import Product, Discount

shop_blueprint = Blueprint('shop', __name__)


@shop_blueprint.route('/products', methods=['GET'])
@cross_origin()
def load_all_products():
    """ Read the products csv and returns all the products

    :return: List of Product entities with the values of the products
    """

    with open('./products.csv') as products:
        reader = csv.DictReader(products)
        return jsonify([row for row in reader]), 200


@shop_blueprint.route('/create-basket', methods=['POST'])
@cross_origin()
def create_basket():
    """ Create a basket

    :return: (str) Id of the new basket
    """

    with shelve.open("basket", writeback=True) as db:
        # Generate a random string as id, insert it in the database and return it
        basket_id = _random_string()
        db[basket_id] = dict()
        return jsonify({'basket_id': basket_id}), 200


def _random_string():
    """ Generates a random string of 8 chars

    :return: (str) Random string
    """

    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])


@shop_blueprint.route('/<path:basket_id>/update-product', methods=['PUT'])
@cross_origin()
def add_product(basket_id):
    """ Add or remove a product to the selected basket\n
    Request params:\n
    -product_code: (str) Code of the product\n
    -quantity (int) Number of units to add or remove of the product

    :param basket_id: (str) Id of the basket
    :return: (dict) Content of the basket
    """

    # Get the product code from the params
    product_code = request.args.get('product_code', type=str)
    quantity = request.args.get('quantity', type=int)

    # Check the validity of the parameters
    if not product_code or not quantity:
        return jsonify({'msg': 'Empty parameters.'}), 400
    if not _check_product(product_code):
        return jsonify({'msg': 'Product code invalid.'}), 400

    with shelve.open("basket", writeback=True) as db:

        if db.get(basket_id) is None:
            return jsonify({'msg': 'Basket id invalid.'}), 400

        # Get the current number of units of the product and sum the new quantity
        product_count = db.get(basket_id).get(product_code, 0) + quantity

        # If the final quantity is 0 or less, remove the item, if not, update the quantity
        if product_count <= 0:
            if db.get(basket_id).get(product_code) is None:
                return jsonify({'msg': 'Product not in the basket.'}), 400
            db.get(basket_id).pop(product_code)
        else:
            db.get(basket_id)[product_code] = product_count

        return jsonify(db.get(basket_id)), 200


def _check_product(product_code):
    """ Check if the product code exists in the csv

    :param product_code: (str) Code of the product
    :return: (bool) If exists or not
    """

    with open('./products.csv') as products:
        reader = csv.DictReader(products)
        for product in reader:
            if product.get('code') == product_code:
                return True
    return False


@shop_blueprint.route('/<path:basket_id>/checkout', methods=['GET'])
@cross_origin()
def checkout(basket_id):
    """ Calculate the final price of the items of the bag applying the discounts

    :param basket_id: (str) Id of the basket
    :return: (float) Price of the products with discounts
    """

    with shelve.open("basket") as db:

        if db.get(basket_id) is None:
            return jsonify({'msg': 'Basked id invalid.'}), 400

        product_dict = {**db.get(basket_id)}

    final_price = 0.00

    for product_code, units in product_dict.items():
        # Load the product and calculate the price of all units
        product = _load_product(product_code)
        product_price = product.price * units

        # Load the list of discounts
        discount_list = _load_discounts_by_product(product_code)
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

    return jsonify({'price': final_price}), 200


def _load_product(code):
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


def _load_discounts_by_product(product_code):
    """ Read the discounts csv and return the discounts that can be applied to the selected product

    :param product_code: (str) Code of the product
    :return: (list) List of discounts
    """

    with open('./discounts.csv') as discounts:
        reader = csv.DictReader(discounts)
        return [Discount(**row) for row in reader if row.get('product_code') == product_code]


@shop_blueprint.route('/<path:basket_id>', methods=['DELETE'])
@cross_origin()
def remove_basket(basket_id):
    """ Remove the basket

    :param basket_id: (str) Id of the basket
    """

    with shelve.open("basket", writeback=True) as db:
        if db.get(basket_id) is None:
            return jsonify({'msg': 'Basked id invalid.'}), 400

        db.pop(basket_id)

    return '{}', 200
