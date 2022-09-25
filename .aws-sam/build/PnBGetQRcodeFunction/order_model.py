from decimal import Decimal
from io import BytesIO
import json
import logging
import os
from pprint import pprint
import requests
from zipfile import ZipFile
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from question import Question

logger = logging.getLogger(__name__)

class Orders:
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

    def create_table(self, table_name):
        """
        Create an Amazon DynamoDB table that can be used to store data
        The table uses the release year of the movies as the partition key and 
        the title as the sort key. 
        :param table_name: the name of the table to create
        :return: the newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[{'AttributeName': 'year', 'KeyType': 'HASH'},
                {'AttributeName': 'title', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'year', 'AttributeType': 'N'},
                    {'AttributeName': 'title', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
            )
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Could not create table %s. Here is why: %s: %s",table_name,
                err.response['Error']['Code'], err.response['Error']['Message']
            )
            raise
        else:
            return self.table


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
    

    def add_movie(self, title, year, plot, rating):
        """
        Adds a movie to the table

        :param title: the title of the movie.
        :param year: the release year of the movie
        :param plot: the plot summary of the movie
        :param rating: the quality rating of the movie
        """
        try:
            self.table.put_item(
                Item={
                    'year':year,
                    'title':title,
                    'info':{
                        'plot':plot,
                        'rating':Decimal(str(rating))
                    }
                }
            )
        except ClientError as err:
            logger.error(
                    "Couldn't add movie %s to table %s. Here's why: %s: %s",
                    title, self.table.name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    
    def get_movie(self, title, year):
        """
        Gets movie data from the table for a specific movie.
        :param title: The title of the movie.
        :param year: The release year of the movie.
        :return: The data about the requested movie.
        """
        try:
            response = self.table.get_item(Key={'year': year, 'title': title})
        except ClientError as err:
            logger.error(
                "Couldn't get movie %s from table %s. Here's why: %s: %s",
                title, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Item']


