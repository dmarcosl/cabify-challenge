from flask import Flask

from controllers import shop_blueprint


application = Flask(__name__)
application.register_blueprint(shop_blueprint, url_prefix='/shop')

if __name__ == '__main__':
    application.run()
