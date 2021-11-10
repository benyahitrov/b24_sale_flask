from flask import Flask
from settings import *


app = Flask(__name__)

@app.route('/change_products_sale')
def change_products_sale():
    return "!!!!!!!!"

if __name__ == "__main__":
    app.run(debug=True)