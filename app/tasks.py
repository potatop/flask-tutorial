from lxml import html
from app.models import History
from app import app, db, celery
from celery.utils.log import get_task_logger
import requests

logger = get_task_logger(__name__)

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
            a = elem.xpath('.//a')[0]
            logger.info("found product {}".format(a.text))
            id = int(a.get('data-id'))
            history = History.query.filter(History.id == id).order_by(History.timestamp.desc()).first()
            if history is None or history.instock != status:
                t = elem.xpath('.//div[@class="stock"]/strong//text()')
                status = False if t[1] == 'Sold Out' else True
                history = History(id=id, name=a.text, instock=status, price=a.get('data-price'))
                db.session.add(history)
                db.session.commit()
                if "5900X" in history.name and history.instock:
                    requests.post(app.config["TILL_URL"], json={
                        "phone": ["16157152079"],
                        "text" : "X5900 in stock!"
                    })
        return 0
    else:
        return resp.status_code