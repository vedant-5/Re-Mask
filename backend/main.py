import time
import uvicorn
from models import *
from cacheout import Cache
from utils.dutils import mongodb_connection
from utils.util import *
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, Response, Header
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel, EmailStr
from fastapi_mail.email_utils import DefaultChecker

# from dotenv import dotenv_values

# credentials = dotenv_values(".env")


app = FastAPI()
cache = Cache(maxsize=556000, ttl=0, default=None)


@app.post("/v1/api/user/signup")
async def sign_up(item: SignUpModel):
    Name = mongodb_connection('verification').find_one({'name': item.name})
    referenceId = mongodb_connection('verification').find_one({'referenceId': item.referenceId})
    if Name is not None and referenceId is not None:
        existing_email = mongodb_connection('userInfo').find_one({'emailAddress': item.emailAddress})
        existing_phone = mongodb_connection('userInfo').find_one({'contactNo': item.contactNo})
        if existing_email is None and existing_phone is None:
            password = encode_base64(item.password)
            _id = get_random_id()
            m_item = item.dict()
            logging.info(m_item)
            m_item['_id'] = _id
            m_item['userId'] = _id
            m_item['password'] = password
            if(item.type == 'Hospital'):
                m_item['userType'] = True
            else:
                m_item['userType'] = False
            mongodb_connection('userInfo').insert_one(m_item)
            # sendUniqueId(_id,item.emailAddress, item.password)
            return {'msg': 'successful'}
    else:
        return{'msg': 'access denied'}
    return {'msg': 'email or phone number already exists'}
           


@app.post("/v1/api/user/login")
async def login(item2: LoginModel, response: Response):
    key = encode_base64(item2.emailAddress + ":" + encode_base64(item2.password))
    user = mongodb_connection('userInfo').find_one(
        {'emailAddress': item2.emailAddress, 'password': encode_base64(item2.password)})
    if user is None:
        return {'msg': 'login failed'}
    else:
        userId = user['_id']
        cache.set(key, userId)
        response.headers['x-session-token'] = key
        return {'msg': 'login successful'}          


conf = ConnectionConfig(
    MAIL_USERNAME = "Re.Mask.withus@gmail.com",
    MAIL_PASSWORD = "VISAVISA",
    MAIL_FROM = "Re.Mask.withus@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False
    # USE_CREDENTIALS = True
)

@app.post('/v1/api/user/email/')
async def sendEmail(content: EmailContent, email: EmailSchema):
    
    # referenceId = await Product.get(id = product_id)
    # supplier = await product.supplied_by
    # supplier_email = [supplier.email]
    template = """
    <html>
    <h5>Welcome to Re-Mask</h5> 
    <br>
    <p>Your Registeration is succesful. Kindly go to login page and fill the credentials.</p>
    <br>
    </body>
    </html>
    """
    message = MessageSchema(
    subject= "Registeration Confirmed!",
    recipients= email.dict().get('email'),# List of recipients, as many as you can pass 
    body= template, 
    subtype="html" 
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"status":"ok"}

        
@app.get("/v1/api/user/hospitalData")
async def hospitalData():
    # _id = cache.get(x_access_token)
    # user_access = mongodb_connection('userInfo').find_one({'_id': _id})
    # if user_access is not None:
    listofitems = []
    for x in mongodb_connection('donateInfo').find({'type': True}):
        listofitems.append(x)
    return listofitems
    # else:
    #     return {'msg': 'permission denied'}

@app.post("/v1/api/user/donate")
async def donate( donate: DonateModel, x_access_token: str = Header(None)):
    _id = cache.get(x_access_token)
    user_access = mongodb_connection('userInfo').find_one({'_id' : _id})
    if user_access is not None:
        m_item = donate.dict()
        logging.info(m_item)
        m_item['_id'] = _id
        m_item['name'] = user_access['name']
        m_item['address'] = user_access['address']
        m_item['contactNo'] = user_access['contactNo']
        m_item['emailAddress'] = user_access['emailAddress']
        m_item['type'] = user_access['userType']
        mongodb_connection('donateInfo').insert_one(m_item)
        return {'msg': 'successful'}

    return{'msg': 'access denied'}

@app.get("/v1/api/user/logout")
async def logout(x_access_token: str = Header(None)):
    cache.delete(x_access_token)
    return {'msg': 'successfully logged out'}



if __name__ == "__main__":
    print("starting server ")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")

