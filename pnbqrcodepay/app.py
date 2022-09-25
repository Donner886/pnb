import json
import resource

import requests
from jose import jwt
from order_model import Orders 
import order_model
import logging
import boto3
import readConfig



logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    config = readConfig.Config('env.ini','hsbcPaymentDev')
    url_ = config.genaratePaymentQrcode
    client_id = config.clientId
    client_sercet = config.clientSecret
    merchant_id = config.merchantId
    notifyUrl = config.notifyUrl
    paymentMethod = config.paymentMethod
    txnChannel = config.txnChannel
    country = config.paymentCountry
    currency = config.currency



    ## request header json 
    headers = {"message_encrypt":"false",
                "x-HSBC-client-id":client_id,
                "x-HSBC-client-secret":client_sercet,
                "Content-Type":"application/json"
                }

    ## request body,



    data = {"txnRef":txnRef,
            "merId":merchant_id}
    
    result = requests.post( url=url_,
                     headers=headers,
                     data=data)
    print(json.dumps(result.json()))  
    
      
    ## python jwt package testing
    token = jwt.encode({'key': 'value'}, 'secret', algorithm='HS256')
    print(token)






















    ## Here we attemp to invoke the database handler funciton
    # 1, Is table existed
    # 2, write batch data into a table
    # 3, get item from table.
    # 4, insert item into table. 
    # 5, Get list from table

    orders = Orders(boto3.resource('dynamodb'))
    table_name = 'movies'
    movies_file_name = 'moviedata.json'
    movies_table_existed = orders.exists(table_name)
    if not movies_table_existed:
        logger.info("table %s does not existed, and start to creat", 
        table_name)
        orders.create_table(table_name)
        logger.info("table %s created", table_name)

    # 2,  write batch data into a table
    print(f"\nReading data from '{movies_file_name}' into your table.")
    movies_data = order_model.get_sample_movie_data(movies_file_name)
    orders.write_batch(movies_data)
    print(f"\nWrote {len(movies_data)} movies into {table_name}.")
    print('-'*88)


    return {
        "statusCode": 200,
        'body': json.dumps(result.json()),
    }