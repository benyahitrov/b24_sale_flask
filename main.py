from flask import Flask, request, render_template
from typing import Optional, Dict, List
import json
import logging.config
import requests


from settings import *


app = Flask(__name__)


logging.config.dictConfig(logger_config)
logger = logging.getLogger('b24_sale')


def get_deal_sales(deal_id: int) -> Dict:
    logger.debug('==Start get deal sale==')
    logger.debug(f'deal id: {deal_id}')
    url = f'{B24_WEBHOOK_URL}crm.deal.get'
    params = {'id': deal_id}
    sales = {
        'new': 0,
        'old': 0
    }
    response = requests.get(url, params=params).json()
    print(response)
    if response.get('result'):
        new_sale = response.get('result').get('UF_CRM_1632104084')
        if new_sale:
                sales['new'] = int(new_sale)
        old_sale = response.get('result').get('UF_CRM_1632193466')
        if old_sale:
            sales['old'] = int(old_sale)
    else:
        logger.debug(f'Error get sales by id = {id}, {response.get("error_description")}')
    return sales

def get_deal_products(deal_id: int) -> List:
    logger.debug('== Start get deal products ==')
    logger.debug('deal id: {deal_id}')
    url = f'{B24_WEBHOOK_URL}crm.deal.productrows.get'
    params = {'id': deal_id }
    response = requests.get(url, params=params).json()
    result = response.get('result')
    if result:
        return result
    else:
        logger.debug(f'Error get products by id = {id}, {response.get("error_description")}')
    return []

def add_sale_to_produts(products: List, sale: int) -> List:
    logger.debug('==Start add sale to products==')
    logger.debug(f'products: {products}')
    saled_products = []
    for product in products:
        product['DISCOUNT_TYPE_ID'] = 2
        product['DISCOUNT_RATE'] = sale
        sale_sum = int(product['PRICE_NETTO']) * sale / 100
        product['DISCOUNT_SUM'] = sale_sum
        new_price = product['PRICE_NETTO'] - sale_sum
        product['PRICE'] = new_price
        product['PRICE_EXCLUSIVE'] = new_price
        product['PRICE_ACCOUNT'] = new_price
        saled_products.append(product)
    return saled_products

def set_deal_products(deal_id: int, products: List) -> Dict:
    logger.debug('== Start set deal products ==')
    logger.debug(f'deal id: {deal_id}')
    url = f'{B24_WEBHOOK_URL}crm.deal.productrows.set'
    data = {
        'id': deal_id,
        'rows': products
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers).json()
    result = response.get('result')
    if result:
        logger.debug(f'Set deal products result {result}')
        return result 
    else:
        logger.debug(f'Error get deal sale: {response.get("error_description")}')
    return {}

def update_b24_old_sale(id: int, sale: int) -> Dict:
    logger.debug('==Start update b24 old sale==')
    url = f'{B24_WEBHOOK_URL}crm.deal.update'
    data = {
        'ID': id,
        'fields':{
            'UF_CRM_1632193466': sale
        }          
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers).json()
    result = response.get('result')
    if result:
        logger.debug(f'Update deal result {result}')
        return result 
    else:
        logger.debug(f'Error update deal sale: {response.get("error_description")}')
    return 'ok'


@app.route('/change_products_sale', methods=['POST', 'GET'])
def change_products_sale():
    #print('REQ',request.form.)
    if request.method == 'POST':
        #print("TTT",request.form.to_dict())
        app_token = request.form.to_dict().get('auth[application_token]')
        if app_token != APP_TOKEN:
            logger.debug(f'Access error. Request: {request.form.to_dict()}')
            return  "Forbidden", 403
        deal_id = request.form.to_dict()['data[FIELDS][ID]']
        logger.debug(f'deal_id: {deal_id}')
    sales = get_deal_sales(deal_id)
    print('SALES', sales)
    if sales['new'] != sales['old'] and sales['new'] > 0:
        products = get_deal_products(deal_id)
        saled_products = add_sale_to_produts(products, sales['new'])
        set_deal_products(deal_id, saled_products)
        update_b24_old_sale(deal_id, sales['new'])
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)