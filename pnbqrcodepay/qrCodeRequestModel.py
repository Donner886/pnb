from datetime import datetime
from decimal import Decimal
from io import BytesIO
import json
import logging
import os
from pprint import pprint
from pydoc import describe
import requests
from zipfile import ZipFile
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from utils import Utils 

logger = logging.getLogger(__name__)

class PnbClientTransaction:
    """This class contains all attributes of transaction assigned to customer"""
    def __init__(self):
        now = Utils.getNowtime()
        self.txn_timestamp = str(now.strftime("%Y-%m-%d %H:%M:%S%f"))
        self.txn_date = str(now.strftime("%Y-%m-%d"))
        txnStrForTxn = str(now.strftime("%Y%m%d%H%M%S%f"))
        self.txnRef = Utils.getTxnRef(txnStrForTxn,25)
        self.txn_description = "initial transaction, please update"
        self.amount = "0.00"
        self.txn_status = "initial"
        self.payment = "initial"
        self.txnChannel = "initial"
        self.payment_country = "initial"
        self.payment_currency = "initial"
        self.paymentQRcode_token = "not yet got from hkbc"

    def convertToDict(self):
        txnDict_ = dict(txn_timestamp = self.txn_timestamp,
            txn_date = self.txn_date,
            txnRef = self.txnRef,
            txn_description = self.txn_description,
            amount = self.amount,
            txn_status = self.txn_status,
            payment = self.payment,
            txnChannel = self.txnChannel,
            payment_country = self.payment_country,
            payment_currency = self.payment_currency,
            paymentQRcode_token = self.paymentQRcode_token
        )
        return txnDict_



    def setTxnDescription(self, describe):
        self.txn_description = describe
    def setAmount(self, amount):
        self.amount = amount
    def setTxnStatus(self, status):
        self.txn_status = status
    def setTxnPayment(self, payment):
        self.payment = payment
    def setTxnChannel(self, channel):
        self.txnChannel = channel
    def setTxnPaymentCountry(self, country):
        self.payment_country = country
    def setTxnPaymentCurrency(self, currency):
        self.payment_currency = currency
    def setTxnQrToken(self, qrtoken):
        self.aymentQRcode_token = qrtoken






        
class QRCodePayment:
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



    def write_batch(self,movies):
        """
        Fills an Amozon DynamDB table with the specified data, using 
        the Boto3 Table.batch_writer() function to put the items in the table. 
        Inside the context manager, Table.batch_writer builds a list of 
        requests.
        :param movies: The data to put in the table. Each item must contain
        at least the keys requires by the schema that was specified when the 
        table was created.
        """
        try:
            with self.table.batch_writer() as writer:
                for movie in movies:
                    writer.put_item(Item=movie)
        except ClientError as err:
            logger.error(
                "Couldn't load data into table %s. Here's why: %s: %s", self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    

    def add_txn(self, txn: PnbClientTransaction):
        """
        Adds a transaction into the table

        :param txn: transaction object.
        """
        try:
            self.table.put_item(
                Item=txn
            )
        except ClientError as err:
            logger.error(
                    "Couldn't add movie %s to table %s. Here's why: %s: %s",
                    title, self.table.name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    
    def get_txn_with_txnRef(self, txnref):
        
        try:
            response = self.table.get_item(Key={'txnRef': txnref})
        except ClientError as err:
            logger.error(
                "Couldn't get movie %s from table %s. Here's why: %s: %s",
                title, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Item']

