from app import app

from app.telegram_connector import botSendMessage

import requests
from bs4 import BeautifulSoup


packt_url = "https://www.packtpub.com/packt/offers/free-learning"

def get_free_book_title():
    packt_url = "https://www.packtpub.com/packt/offers/free-learning"
    session = requests.Session()
    app.logger.info("Get pack free learning page")
    freebook_req = session.get(packt_url, verify=True, headers=app.config['HTTP_HEADERS'])
    page_content = freebook_req.content
    app.logger.info("Parsing page with beautiful soup")
    soup = BeautifulSoup(page_content)
    div_title = soup.find("div", "dotd-title").h2
    title = (div_title.text).strip()
    app.logger.info("Title {}".format(title))
    return title

def packt_freebook_notifier_bot():
    title = get_free_book_title()
    botSendMessage('"{}" is the today free book of packtpub\n\n:arrow_right: {}'.format(title,packt_url))

@app.route('/packt_notifier_url')
def packt_notifier_url():
    packt_freebook_notifier_bot()
    return("ok")
