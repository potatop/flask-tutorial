from lxml import html
from app.models import History
from app import db, celery
import requests

TARGET = "https://www.microcenter.com/search/search_results.aspx"
AGENT = ('Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit'
    '/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')

@celery.task
def microcenter():
    resp = requests.get(
        TARGET,
        params={
            "Ntk": "all",
            "sortby": "match",
            "N": "4294966995 4294808559",
            "myStore": "false",
        },
        headers={"referer": "https://www.microcenter.com", "user-agent": AGENT},
        timeout=25,
        cookies={
            "MicrocenterPrivacy": "Accepted",
            "SortBy": "match",
            "storeSelected": "065",
        },
    )
    if resp.status_code == 200:
        tree = html.fromstring(resp.content)
        list = tree.xpath('//article[@id="productGrid"]/ul/li/div[@class="result_right"]')
        for elem in list:
            name = elem.xpath('.//a/text()')[0]
            if "5900X" in name:
                t = elem.xpath('.//div[@class="stock"]/strong//text()')
                status = False if t[1] == 'Sold Out' else True
                history = History.query.order_by(History.timestamp.desc()).first()
                if history is None or history.instock != status:
                    p = elem.xpath('.//span[@itemprop="price"]/text()')
                    history = History(name=name, instock=status, price=p[0])
                    db.session.add(history)
                    db.session.commit()
                return 0
        return 404
    else:
        return resp.status_code