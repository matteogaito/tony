# -*- coding: utf-8 -*-
from app import app

from sprea_utils import Sprea
from flask_gapps_connector import DriveInizialize
from app.telegram_connector import botSendMessage

# sl object contain logged session in sprea.it
sl = Sprea(app.config['SPREA_USERNAME'], app.config['SPREA_PASSWORD'])

@app.route('/sprea/check_last_pdf')
def checkEsistenceLastPDFintoGdrive():
    #Get Pdf Name by Url
    last_pdf_url = sl.getOnePdfUrlofCampaign(app.config['SPREA_CAMPAIGN'], 0)
    pdfinfo = sl._getPdfInfo(last_pdf_url)

    #Check into Google Drive
    drive = DriveInizialize( app.config['DRIVE_SCOPE'], app.config['GOOGLE_API_ACCESS'])
    file_list = drive.ListFile({'q': "'0B_9s9T8tAnUWTWNUbDZVbVBjOFE' in parents and trashed=false"}).GetList()

    #Loop into file list in order to found pdf
    found=False
    for f in file_list:
        if f['title'] == pdfinfo['name']:
            found=True

    return(last_pdf_url, found)

@app.route('/download_last_pdf_if_missing')
def downloadLastEbookIfMissing():
    last_pdf_url, missing = checkEsistenceLastPDFintoGdrive()
    pdfinfo = sl._getPdfInfo(last_pdf_url)
    if not missing:
        pdf_path = sl.downloadPDFbyURL(last_pdf_url)
        drive = DriveInizialize( app.config['DRIVE_SCOPE'], app.config['GOOGLE_API_ACCESS'])
        f = drive.CreateFile({'title': pdfinfo['name'], "parents": [{"kind": "drive#fileLink", "id": app.config['EBOOK_FOLDER']}]})
        f.SetContentFile(pdf_path)
        f.Upload()
        botSendMessage('File {} downloaded'.format(pdfinfo['name']))
        return(pdf_path)
    else:
        botSendMessage('File {} already downloaded'.format(pdfinfo['name']))
        return("Pdf Presente")

