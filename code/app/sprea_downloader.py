# -*- coding: utf-8 -*-
from app import app

import sys
sys.path.insert(0, '/vagrant/sprea-utils')

from sprea_utils import Sprea
from app.gapps_connector import DriveInizialize
from app.telegram_connector import botSendMessage

# sl object contain logged session in sprea.it
sl = Sprea(app.config['SPREA_USERNAME'], app.config['SPREA_PASSWORD'])

import logging
log_sl = logging.getLogger('sprea_utils')
formatter = logging.Formatter("%(asctime)s - [%(process)d] - %(levelname)s %(module)s: %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
log_sl.addHandler(handler)
log_sl.setLevel(logging.DEBUG)

@app.route('/sprea/check_last_pdf')
def checkEsistenceLastPDFintoGdrive():
    # Get Pdf Name by Url
    last_pdf_url = sl.getOnePdfUrlofCampaign(app.config['SPREA_CAMPAIGN'], 0)
    pdfinfo = sl._getPdfInfo(last_pdf_url)

    # Check into Google Drive
    drive = DriveInizialize(app.config['DRIVE_SCOPE'], app.config['GOOGLE_API_ACCESS'])
    q = "'" + app.config['EBOOK_FOLDER'] + "' in parents and trashed=false"
    file_list = drive.ListFile({'q': q}).GetList()

    # Loop into file list in order to found pdf
    found = False
    for f in file_list:
        if f['title'] == pdfinfo['name']:
            found = True

    return(last_pdf_url, found)


@app.route('/download_last_pdf_if_missing')
def downloadLastEbookIfMissing():
    last_pdf_url, found = checkEsistenceLastPDFintoGdrive()
    pdfinfo = sl._getPdfInfo(last_pdf_url)
    if not found:
        pdf_path = sl.downloadPDFbyURL(last_pdf_url)
        drive = DriveInizialize(app.config['DRIVE_SCOPE'], app.config['GOOGLE_API_ACCESS'])
        f = drive.CreateFile({'title': pdfinfo['name'], "parents": [{"kind": "drive#fileLink", "id": app.config['EBOOK_FOLDER']}]})
        f.SetContentFile(pdf_path)
        f.Upload()
        botSendMessage('File "{}" downloaded with name '.format(pdfinfo['title'], pdfinfo['name']))
        return(pdf_path)
    else:
        botSendMessage('File "{}" already downloaded'.format(pdfinfo['title']))
        return("Pdf Presente")
