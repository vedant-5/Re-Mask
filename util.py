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


