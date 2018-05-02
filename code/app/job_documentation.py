# -*- coding: utf-8 -*-
from app import app

from app.mail_libs import *


# Dada Office365
DADA_EMAIL = app.config['DADA_EMAIL']
DADA_PASSWORD = app.config['DADA_PASSWORD']
DADA_IMAP = app.config['DADA_IMAP']
PATTERN = '(FROM "info@studiosignorinifirenze.com")'

#search_result = Imap(
#    server = DADA_IMAP,
#    username = DADA_EMAIL,
#    password = DADA_PASSWORD
#).search(pattern=PATTERN)
#print(search_result)
#
#msg_id = search_result[0].split()[-1]
#print(msg_id)

#attachments = Imap(
#    server = DADA_IMAP,
#    username = DADA_EMAIL,
#    password = DADA_PASSWORD
#).get_attachments(msg_id=msg_id)
#
#print(attachments)
#
#Email().download_attachments(attachments = attachments)


@app.route('/scarica_busta_paga')
def scarica_busta_paga():
    search_result = Imap(
        server = DADA_IMAP,
        username = DADA_EMAIL,
        password = DADA_PASSWORD
    ).search(pattern=PATTERN)
    last_mail = search_result[-1].split()[-1]

    attachments = Imap(
        server = DADA_IMAP,
        username = DADA_EMAIL,
        password = DADA_PASSWORD
    ).get_attachments(msg_id=last_mail)

    print(attachments)
    return("ok")
