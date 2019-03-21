from app import app

from emoji import emojize
from app.telegram_connector import botSendMessage

from selenium import webdriver

import time

packt_url = "https://www.packtpub.com/packt/offers/free-learning"


@app.route('/packtpub/todayfree')
def get_free_book_title():
    packt_url = "https://www.packtpub.com/packt/offers/free-learning"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome('/tony/bin/chromedriver', chrome_options=chrome_options, service_args=[ '--logpath=/tony/bin/chromedriver.log' ] )
    app.logger.info("Opening chrome on free packt url")
    driver.get(packt_url)
    app.logger.info("Get pack free learning page")
    app.logger.info("Start sleeping")
    time.sleep(10)
    app.logger.info("search with xpath")
    title_element = driver.find_element_by_class_name('product__title')
    title = title_element.text
    app.logger.info("Title is {}".format(title))
    return title

def packt_freebook_notifier_bot():
    title = get_free_book_title()
    botmsg = emojize(":closed_book: \"{}\" is the today free book of packtpub\n\n:arrow_right: {}".format(title, packt_url), use_aliases=True)
    botSendMessage(botmsg)

@app.route('/packt_notifier_url')
def packt_notifier_url():
    packt_freebook_notifier_bot()
    return("ok")
