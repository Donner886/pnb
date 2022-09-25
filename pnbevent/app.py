import json
import resource
from unittest import result

import requests
from jose import jwt
from eventmodel import EventModel 
from eventmodel import EventControl 
import logging
import boto3
from utils import Utils 



logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    uri = event['path']
    method = event['httpMethod']
    if (method.upper() != 'GET'):
        body = event['body']
        event_sample_dict = json.loads(body)
        if (uri == '/pnbupdateevent'):
            ## here start to wrap the event_ sample_str object json string
            event_creation_datetime = Utils.getTimestampsStr()
            updated_date = event_creation_datetime
            event_sample_dict['event_creation_datetime'] = event_creation_datetime
            event_sample_dict['updated_date'] = updated_date
            ## here start to create event_ object 
            event_sample = EventModel(
                event_inital_month = event_sample_dict['event_inital_month'], 
                event_name = event_sample_dict['event_name'],
                event_img_url = event_sample_dict['event_img_url'],
                event_title = event_sample_dict['event_title'], 
                event_description = event_sample_dict['event_description'], 
                isFree = event_sample_dict['isFree'], 
                unit_amount = event_sample_dict['unit_amount'], 
                expire_date = event_sample_dict['expire_date'], 
                max_paticipants = event_sample_dict['max_paticipants'], 
                publish_date = event_sample_dict['publish_date'], 
                status = event_sample_dict['status'], 
                event_creation_datetime = event_sample_dict['event_creation_datetime'], 
                updated_date = event_sample_dict['updated_date']
            )
        
    ## dynamodb connection
    eventSchema = EventControl(boto3.resource('dynamodb'))
    table_name = 'event'
    event_table_existed = eventSchema.exists(table_name)
    
    if not event_table_existed:
        logger.info("table %s does not existed, and please contract your admins to create this table", 
        table_name)

    if ( (uri == '/pnbupdateevent') and  (method.upper() == 'POST')):
        logger.info(f"start to insert or update record to table'{table_name}' into your table.")
        result = eventSchema.update_event(event_sample.dict())
        logger.info(f"end to insert record to table'{table_name}' into your table.")
       
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    elif ((uri == '/pnbgetevent')and (method.upper() == 'POST')):
        event_init_month_ = event_sample_dict['event_inital_month']
        event_name_ = event_sample_dict['event_name']
        logger.info(f"start to get record from table'{table_name}' into your table.")
        result = eventSchema.get_event(event_init_month=event_init_month_, event_name=event_name_)
        logger.info(f"end to get record from table'{table_name}' into your table.")
        response = {
            "events": result
        }
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }

    elif ((uri == '/pnbgetevents') and (method.upper() == 'GET')):
        logger.info(f"start to get all records to table'{table_name}' into your table.")
        result = eventSchema.get_all_event()
        logger.info(f"end to get all records to table'{table_name}' into your table.")
        response = {
            "events": result
        }
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
   