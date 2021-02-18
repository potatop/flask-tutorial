from lxml import html
from app.models import Product, Price
from app import db
import requests

RETAIL = {
    "3070": 500,
    "3080": 700,
    "6800": 580,
    "6800 XT": 650,
}
TARGET = "https://www.microcenter.com/search/search_results.aspx"

def gfxcards():
    resp = requests.get(
        TARGET,
        params={
            "Ntk": "all",
            "sortby": "match",
            "N": "4294808485 4294808505 4294808740 4294808774",
            "myStore": "false",
        },
        headers={"referer": "https://www.microcenter.com"},
        timeout=25,
        cookies={
            "MicrocenterPrivacy": "Accepted",
            "SortBy": "match",
            "storeSelected": "065",
            "rpp": "48",
        },
    )
    products = {}
    if resp.status_code == 200:
        tree = html.fromstring(resp.content)
        list = tree.xpath('//article[@id="productGrid"]/ul/li/div[@class="result_right"]')
        for elem in list:
            a = elem.xpath('.//a')[0]
            product = Product(id=a.get('data-id'), name=a.text)
            t = elem.xpath('.//div[@class="stock"]/strong//text()')
            status = False if t[1] == 'Sold Out' else True
            price = Price(instock=status, price=a.get('data-price'), product_id=product.id)
            products[product] = price
    return products

def save():
    products = gfxcards()
    for k, v in products.items():
        if Product.query.filter(Product.id == k.id).first() is None:
            db.session.add(k)
        for kk, vv in RETAIL.items():
            if kk in k.name:
                v.premium = (float(v.price) - vv) / vv
        db.session.add(v)
    db.session.commit()
