import time
import uvicorn
from models import *
from fastapi import FastAPI,Response
from cacheout import Cache
from utils.dutils import mongodb_connection
from utils.util import *


app = FastAPI()
cache = Cache(maxsize=556000, ttl=0, default=None)


@app.post("/v1/api/user/signup")
async def sign_up(item: SignUpModel):
    if(item.type == 'Hospital'):
        existing_email = mongodb_connection('Hospital').find_one({'emailAddress': item.emailAddress})
        existing_phone = mongodb_connection('Hospital').find_one({'contactNo': item.contactNo})
        if existing_email is None and existing_phone is None:
            password = encode_base64(item.password)
            _id = get_random_id()
            m_item = item.dict()
            logging.info(m_item)
            m_item['_id'] = _id
            m_item['userId'] = _id
            m_item['password'] = password
            mongodb_connection("Hospital").insert_one(m_item)
            # sendUniqueId(_id,item.emailAddress, item.password)
            return {'msg': 'successful'}

    else:
        existing_email = mongodb_connection('Recycle_Industry').find_one({'emailAddress': item.emailAddress})
        existing_phone = mongodb_connection('Recycle_Industry').find_one({'contactNo': item.contactNo})
        if existing_email is None and existing_phone is None:
            password = encode_base64(item.password)
            _id = get_random_id()
            m_item = item.dict()
            logging.info(m_item)
            m_item['_id'] = _id
            m_item['userId'] = _id
            m_item['password'] = password
            mongodb_connection("Recycle_Industry").insert_one(m_item)
            # sendUniqueId(_id,item.emailAddress, item.password)
            return {'msg': 'successful'}

    return {'msg': 'email or phone number already exists'}
           

@app.post("/v1/api/user/login")
async def login(item2: LoginModel, response: Response):
    key = encode_base64(item2.emailAddress + ":" + encode_base64(item2.password))
    user = mongodb_connection('Hospital').find_one(
        {'emailAddress': item2.emailAddress, 'password': encode_base64(item2.password)})
    if user is None:
        return {'msg': 'login failed'}
    else:
        userId = user["_id"]
        cache.set(key, userId)
        response.headers['x-session-token'] = key
        return {'msg': 'login successful'}          


if __name__ == "__main__":
    print("starting server ")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")

