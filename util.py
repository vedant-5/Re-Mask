import base64
import random
import string
import boto3
from botocore.exceptions import ClientError
import logging
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def encode_base64(p):
    password_ascii = p.encode("ascii")
    base64_bytes = base64.b64encode(password_ascii)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def get_random_id():
    random_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    return random_id

def sendUniqueId(_id,email_address, password):
    import requests
    data = {"personalizations": [{"to": [{"email": email_address}]}],
            "from": {"email": "noreply@remask.com"},
            "subject": "Welcome to Remask",
            "content": [{"type": "text/html",
                         "value": '''
                         <!DOCTYPE html>
                                <html>
                                <body>
                                <br>
                                <p>Hello,</p>
                                <p>Thank you for signing up with Remask. You can donate or collect masks here. Once again thank you for signing up.</p>
                                <p>
                                this is your unique ID : <b>{_id}</b>
                                </p>
                                
                                <p>
                                If you ever forget your password or need any assistance kindly reach out to remask.com
                                </p>
                                
                                <p>
                                Thank you. 
                                </p>
                                <p>
                                Admin
                                </p>
                                </body>
                                </html>

                         '''.format(
                             UniqueId= _id)}]}

    header = {'Authorization': 'Bearer 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'}
    res = requests.post("https://api.sendgrid.com/v3/mail/send", headers=header, json=data, verify=False)
    logging.info(res)
    if int(res.status_code) < 205:
        logging.info("valid mail ")
        data = {"personalizations": [{"to": [{"email": "remask.com"}]}],
                "from": {"email": "noreply@remask.com"},
                "subject": "Welcome to Remask",
                "content": [{"type": "text/plain",
                             "value": "Unique Id is: {_id} is this" .format(
                                 UniqueId=_id)}]}
        header = {'Authorization': 'Bearer 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'}
        res = requests.post("https://api.sendgrid.com/v3/mail/send", headers=header, json=data, verify=False)
        logging.info(res)
    else:
        logging.info("invalid mail ")
        data = {"personalizations": [{"to": [{"email": "remask@gmail.com"}]}],
                "from": {"email": "noreply@remask.com"},
                "subject": "Registered User Error",
                "content": [{"type": "text/plain",
                             "value": "Register user email address : {email} and password : {password} is this. This is incorrect or there was an error sending mail. Please validate it manually".format(
                                 email=email_address,
                                 password=password)}]}
        header = {'Authorization': 'Bearer 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'}
        res = requests.post("https://api.sendgrid.com/v3/mail/send", headers=header, json=data, verify=False)
    try:
        logging.info(res.json())
    except Exception as e:
        logging.error(e)

