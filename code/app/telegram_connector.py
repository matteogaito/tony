import telegram
import time
from emoji import emojize
from app import app

def botSendMessage(msg):
    bot = telegram.Bot(token=app.config['TOKEN_TELEGRAM'])
    chat_id=app.config['TELEGRAM_CHATID']
    max_attempts = 5

    for attempt in range(max_attempts):
        success = False
        try:
            bot.send_message(chat_id=chat_id, text=msg, disable_web_page_preview=True)
            success = True
        except:
            app.logger.info("Failed to send message, I'm trying again")

        if success:
            app.logger.info("Msg sent correctly")
            break
        else:
            app.logger.info("Sleep 5 seconds")
            time.sleep(5)

        if attempt == ( max_attempts -1 ):
            app.logger.error("Max attempts reached, msg not sent")
