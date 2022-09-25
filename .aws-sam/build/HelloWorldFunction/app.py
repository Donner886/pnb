import json

import requests
from jose import jwt
 

def lambda_handler(event, context):
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

    return {
        "statusCode": 200,
        'body': json.dumps(result.json()),
    }   