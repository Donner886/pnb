import json
import resource

import requests
from jose import jwt
from order_model import Orders 
import logging
import boto3




logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    url_ = "https://devcluster.api.p2g.netd2.hsbc.com.hk/glcm-mobilecoll-mchk-ea-merchantservices-cert-proxy/v1/payment/enquiry"
    client_id = "8b915a4f5b5047f091f210e2232b5ced"
    client_sercet = "1bb456a541dc416dB6016B5F9583C606"
    merchant_id = "0002900F0645774"
    txnRef = "0002900F06457710500000001"

    ## python https request tesing
    headers = {"message_encrypt":"false",
                "x-HSBC-client-id":client_id,
                "x-HSBC-client-secret":client_sercet,
                "Content-Type":"application/json"
                }
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

    orders = Orders(boto3,resource('dynamdb'))
    table_name = "movies"
    movies_file_name = "moviedata.json"
    movies_table_existed = orders.exists(table_name)
    if not movies_table_existed:
        logger.info("table %s does not existed, and start to creat", 
        table_name)
        orders.create_table(table_name)
        logger.info("table %s created", table_name)

    # 2,  write batch data into a table
    print(f"\nReading data from '{movies_file_name}' into your table.")
    movies_data = orders.get_sample_movie_data(movies_file_name)
    orders.write_batch(movies_data)
    print(f"\nWrote {len(movies_data)} movies into {table_name}.")
    print('-'*88)


    return {
        "statusCode": 200,
        'body': json.dumps(result.json()),
    }