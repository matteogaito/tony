# -*- coding: utf-8 -*-
from app import app

from app.mail_libs import *
from app.pdf_utils import *
from app.telegram_connector import botSendMessage
from app.gapps_connector import DriveInizialize
from emoji import emojize


# Dada Office365
DADA_EMAIL = app.config['DADA_EMAIL']
DADA_PASSWORD = app.config['DADA_PASSWORD']
DADA_IMAP = app.config['DADA_IMAP']
PASSWORD_CEDO = app.config['PASSWORD_CEDO']
PATTERN = '(FROM "info@studiosignorinifirenze.com")'
PATTERN = app.config['CEDO_PATTERN']

@app.route('/download_job_docs')
def download_job_docs():
    # Search {pattern} trought imap and get only the last
    search_result = Imap(
        server = DADA_IMAP,
        username = DADA_EMAIL,
        password = DADA_PASSWORD
    ).search(pattern=PATTERN)
    last_mail = search_result[-1].split()[-1]

    # Get all attachments of last email
    attachments = Imap(
        server = DADA_IMAP,
        username = DADA_EMAIL,
        password = DADA_PASSWORD
    ).get_attachments(msg_id=last_mail)

    # Decrypt pdfs and put the documents into google drive
    for attachment in attachments:
        file_attached = Email.download_attachment(attachment=attachment)
        extension = file_attached.split('.')[-1]
        filename = file_attached.split('/')[-1]
        upload_file = file_attached
        if extension == 'pdf':
            file_isencrypted = PdfIsEncrypted(file_attached)
            if file_isencrypted:
                output_file = file_attached + '_d.pdf'
                filename = output_file.split('/')[-1]
                decrypt_pdf(file_attached, output_file, PASSWORD_CEDO)
                upload_file = output_file
        drive = DriveInizialize(app.config['DRIVE_SCOPE'], app.config['GOOGLE_API_ACCESS'])
        f = drive.CreateFile({'title': filename, "parents": [{"kind": "drive#fileLink", "id": app.config['DOC_FOLDER']}]})
        f.SetContentFile(upload_file)
        f.Upload()
        botmsg = emojize(":man_technologist: \"{}\" uploaded on google drive".format(filename))
        botSendMessage(botmsg)

    # Delete the message
    Imap(
        server = DADA_IMAP,
        username = DADA_EMAIL,
        password = DADA_PASSWORD
    ).delete_message(msg_id=last_mail)

    return("ok")
