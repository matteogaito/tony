# Decrypt password-protected PDF in Python.
# cleaned-up version of http://stackoverflow.com/a/26537710/329263
# https://gist.github.com/bzamecnik/1abb64affb21322256f1c4ebbb59a364 # # Requirements: # pip install PyPDF2 #
# Usage: decrypt_pdf('encrypted.pdf', 'decrypted.pdf', 'secret_password')


from PyPDF2 import PdfFileReader, PdfFileWriter

def decrypt_pdf(input_path, output_path, password):
  with open(input_path, 'rb') as input_file, \
    open(output_path, 'wb') as output_file:
    reader = PdfFileReader(input_file)
    reader.decrypt(password)

    writer = PdfFileWriter()

    for i in range(reader.getNumPages()):
      writer.addPage(reader.getPage(i))

    writer.write(output_file)

def PdfIsEncrypted(input_path):
    with open(input_path, 'rb') as input_file:
        doc = PdfFileReader(input_file, "rb")
        result = doc.isEncrypted
        return(result)
