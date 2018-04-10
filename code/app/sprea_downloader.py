# -*- coding: utf-8 -*-
from app import app

from sprea_utils.sprea_utils import Sprea
from flask_gapps_connector.flask_gapps_connector import DriveInizialize

# sl object contain logged session in sprea.it
sl = Sprea(app.config['SPREA_USERNAME'], app.config['SPREA_PASSWORD'])

@app.route('/checklastpdf')
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

@app.route('/checkifmissed')
def downloadLastEbookIfMissing():
    last_pdf_url, missing = checkEsistenceLastPDFintoGdrive()
    pdfinfo = sl._getPdfInfo(last_pdf_url)
    if not missing:
        pdf_path = sl.downloadPDFbyURL(last_pdf_url)
        drive = DriveInizialize( app.config['DRIVE_SCOPE'], app.config['GOOGLE_API_ACCESS'])
        f = drive.CreateFile({'title': pdfinfo['name'], "parents": [{"kind": "drive#fileLink", "id": app.config['EBOOK_FOLDER']}]})
        f.SetContentFile(pdf_path)
        f.Upload()
        return(pdf_path)
    else:
        return("Pdf Presente")

def downloadPdf():
	# If not already downloaded
	pdfname, anagrafica = getPdfMetadata()
	checkondb=models.spreaPdfDownload.query.filter(models.spreaPdfDownload.pdfname==pdfname).first()
	pdfpath = "pdfs/" + pdfname
	if not checkondb:
		print(pdfname)
		print(anagrafica)
		r = requests.post(POSTURL, data = {'id_anagrafica': anagrafica, 'doc': pdfname})
		time.sleep(4)
		#get download url from previous post and put pdf on pdfs directory
		print(r.text)

		if r.text:
			dpdfurl = urlopen(r.text)
			try:
				print(pdfpath)
				with open(pdfpath, 'wb') as pdf:
					print("downloading")
					pdf.write(dpdfurl.read())
					pdf.close()
					print("Finisched")
					logdownload=models.spreaPdfDownload(pdfname=pdfname)
					db.session.add(logdownload)
					db.session.commit()
			except IOError as e:
				print("I/O error({0}): {1}".format(e.errno, e.strerror))
				print(os.getcwd())

	else:
		print('File Already downloaded')
		botSendMessage('File Already downloaded')

	return(pdfpath, pdfname)

def downloadAndPutIntoGdrive():
	pdfpath, pdfname = downloadPdf()
	print(pdfpath)
	print(pdfname)
	drive = gdrive_connector.inizialize()
	ebookdir='0B_9s9T8tAnUWTWNUbDZVbVBjOFE'
	file_list = drive.ListFile({'q': "'" + ebookdir + "' in parents and trashed=false"}).GetList()
	found=False
	for file1 in file_list:
		print('title: %s, id: %s' % (file1['title'], file1['id']))
		if file1['title'] == pdfname:
			found=True

	if not found:
		print("File non presente")
		f = drive.CreateFile({'title': pdfname, "parents": [{"kind": "drive#fileLink","id": ebookdir}]})
		f.SetContentFile(pdfpath)
		f.Upload()
		print('title: %s, mimeType: %s' % (f['title'], f['mimeType']))


def listFilesGdrive():
	drive = gdrive_connector.inizialize()
	file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	for file1 in file_list:
		print('title: %s, id: %s' % (file1['title'], file1['id']))

	print("ListEbook")
	file_list = drive.ListFile({'q': "'0B_9s9T8tAnUWTWNUbDZVbVBjOFE' in parents and trashed=false"}).GetList()
	for file1 in file_list:
                print('title: %s, id: %s' % (file1['title'], file1['id']))
                #here
                botSendMessage(file1['title'])



## View PDF viewer
#pdfviewer = browser.get(pdflist)
#
#print(pdfviewer.url)
#
#driver = webdriver.PhantomJS() # or add to your PATH
#driver.set_window_size(1280, 1024) # optional
#driver.get(pdfviewer.url)
#time.sleep(4)
#driver.save_screenshot('screen.png') # save a screenshot to disk

#dbtn = driver.find_element_by_xpath('//*[@class="flowpaper_bttnDownload flowpaper_tbbutton download"]')

#print(driver.current_url)

#curl --data "id_anagrafica=2016003589&doc=c837f6f2b716c0c055c12418a8a0066ff52f031e.pdf" http://pdf.sprea.it/r/php/downloader.php
#http://pdf.sprea.it/r/php/pdf/temp/2016003589-c837f6f2b716c0c055c12418a8a0066ff52f031e.pdf

#print(pdfviewer.text)
#pdfdownload = pdfviewer.
#print(pdfdownload)

#print(lastpdf)

#downloadurl = "http://pdf.sprea.it/r/php/pdf/temp/" + USER + "-" + pdfname

#print(downloadurl)
#print(pdfname)
#
#res = urlopen(lastpdf)
#pdf = open("pdfs/" + pdfname, 'wb')
#pdf.write(res.read())
#pdf.close()
