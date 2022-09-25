from datetime import datetime
from decimal import Decimal
import logging
from pprint import pprint
from pydoc import describe
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from utils import Utils 
from pydantic import BaseModel, ValidationError, validator



logger = logging.getLogger(__name__)

class EventModel(BaseModel):
    """This class contains all attributes of event setup by CMS"""
    event_creation_datetime: str
    event_inital_month: str
    event_name: str
    event_img_url: str
    event_title: str
    event_description: str
    isFree: bool
    unit_amount: str
    expire_date: str
    max_paticipants: str
    publish_date: str
    status: str
    updated_date: str


    @validator('event_inital_month')
    def eventID_must_notempty(cls, v):
        if len(v) <= 0:
            raise ValueError('event initial month must not empty')
        return v

    @validator('event_name')
    def event_name_must_notempty(cls, v):
        if len(v) <= 0:
            raise ValueError('event name must not empty')
        return v

    @validator('event_title')
    def event_title_must_notempty(cls, v):
        if len(v) <= 0:
            raise ValueError('event title must not empty')
        return v


    @validator('isFree')
    def event_isFree(cls, v):
        if v not in [True, False]:
            raise ValueError('isFree value shoule boolean value True or False')
        return v








        
class EventControl:
    """Encapsulates an Amazon DynamoDB table of movie data."""
    def __init__(self,dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = None
    
    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table 
        in a member variable.
        : param table_name: the name of the table to check
        : return: True when the tables exists; otherwises, False.  
        """
        try:
            table =  self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
                raise
        else:
            self.table = table
        return exists


    

    def add_event(self, event):
        """
        Adds a transaction into the table

        :param txn: transaction object.
        """
        status = None
        try:
            status = self.table.put_item(
                Item=event,
                ConditionExpression="attribute_not_exists(event_inital_month) AND attribute_not_exists(event_name)"
            )
            return status
        except ClientError as err:
            logger.error(
                    "Couldn't add event to table %s. Here's why: %s: %s", self.table.name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    

    def get_event(self, event_init_month, event_name):
        
        try:
            response = self.table.query(
                KeyConditionExpression=(
                    Key('event_inital_month').eq(event_init_month) &
                    Key('event_name').eq(event_name)
                )
            )
        except ClientError as err:
            logger.error(
                "Couldn't get event %s _ %s from table %s. Here's why: %s: %s",
                event_init_month,event_name, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            return None
        else:
            return response['Items']


    def get_all_event(self):
        events = []
        scan_kwargs = {}
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs['ExclusiveStartKey'] = start_key
                response = self.table.scan(**scan_kwargs)
                events.extend(response.get('Items',[]))
                start_key = response.get('LastEvaluatedKey', None)
                done =  start_key is None
        except ClientError as err:
            logger.error(
                "Could not scan for %s. Here us why: %s: %s",
                self.table, err.response['Error']['Code'],
                err.response['Error']['Message'])
            raise
        return events




    def update_event(self, event_):
        try:
            result = self.get_event(event_['event_inital_month'],event_['event_name'])
            if (len(result) == 0)or (result == None):
                result = self.add_event(event=event_)
                response = dict(result_=result,method='putitem')
            else: 
                response = self.table.update_item(
                        Key={'event_inital_month': event_['event_inital_month'], 'event_name': event_['event_name']},
                        UpdateExpression="set #img_url=:img_url, #title=:title, \
                                            #description=:description, #free=:free, #amount=:amount, \
                                            #expire_date=:expire_date, #max_ppl=:max_ppl, #publish_date=:publish_date, \
                                            #status=:status, #updated_date=:update_date ",
                        ExpressionAttributeValues={
                            ':img_url': event_['event_img_url'], 
                            ':title': event_['event_title'], 
                            ':description': event_['event_description'],    
                            ':free': event_['isFree'], 
                            ':amount': event_['unit_amount'], 
                            ':expire_date': event_['expire_date'], 
                            ':max_ppl': event_['max_paticipants'], 
                            ':publish_date': event_['publish_date'], 
                            ':status': event_['status'], 
                            ':update_date': event_['updated_date'], 
                        
                        },
                        ExpressionAttributeNames={
                            '#img_url': 'event_img_url', 
                            '#title': 'event_title', 
                            '#description': 'event_description',    
                            '#free': 'isFree', 
                            '#amount': 'unit_amount', 
                            '#expire_date': 'expire_date', 
                            '#max_ppl': 'max_paticipants', 
                            '#publish_date': 'publish_date', 
                            '#status': 'status', 
                            '#updated_date': 'updated_date',
                        },

                        ReturnValues="UPDATED_NEW"
                    )
                response = dict(result_=response['Attributes'],method='updateitem')
        except ClientError as err:
            logger.error(
                "Couldn't update event information of: %s _ %s from table %s. Here's why: %s: %s",
                event_['event_inital_month'],event_['event_name'], self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:

            return response





# if __name__ == "__main__":
#     m = EventModel(
#         event_creation_datetime=Utils.getTimestampsStr(),
#         eventID='2022q1e1',
#         event_name='event1',
#         event_img_url='https//dddsdsd/str',
#         event_title='deveplppp',
#         event_description="initial event",
#         isFree=1,
#         unit_amount=22,
#         expire_date='20220921',
#         max_paticipants=99,
#         publish_date=Utils.getTimestampsStr(),
#         status='created',
#         updated_date=Utils.getTimestampsStr()  
#         )
#     print(m.dict())