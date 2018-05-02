# -*- coding: utf-8 -*-

import os
import imaplib
import base64
import email

download_dir = "/tmp/imap_downloads"


class Imap(object):
    def __init__(self, server=None, port=993, username=None, password=None, timeout=10):
        # connect to server
        print("inizializing")
        if port == 993:
            try:
                conn = imaplib.IMAP4_SSL(server, port)
                #conn.starttls()
            except:
                raise
        elif port == 143:
            try:
                conn = imaplib.IMAP4(server, port)
            except:
                raise
        try:
            conn.login(username, password)
            self.conn = conn
        except:
            raise


    def __enter__(self):
        print("Entering")
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        self.conn.logout()
        print("Uscito")

    def search(self, mailbox="INBOX", pattern=None ):
        self.conn.select(mailbox)
        typ, search = self.conn.search(None, pattern)
        if len(search) > 0:
            self.search_result = search
            return search
        else:
            return None

    def get_attachments(self, mailbox="INBOX", msg_id=None):
        self.conn.select(mailbox)
        typ, msg_as_string = self.conn.fetch(msg_id, '(RFC822)')
        email_body = msg_as_string[0][1]
        msg = email.message_from_bytes(email_body)
        attacchments = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            #print(dir(part))
            #print(part.get_content_maintype())
            #print(part.get_content_subtype())
            #print(part.get_content_type())
            #print(dir(part.get_content_type()))
            attacchments.append(part)
        if len(attacchments) > 0:
            return attacchments
        else:
            return None


class Email(object):
    def download_attachments(self, attachments=None, download_dir=download_dir):
        if not attachments:
            return None

        for a in attachments:
            #print(a)
            filename = a.get_filename()
            filepath = download_dir + '/' + filename
            print(filepath)
            if not os.path.isfile(filepath):
                fp = open(filepath, 'wb')
                fp.write(a.get_payload(decode=True))
                fp.close()


