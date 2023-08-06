from typing import List

import boto3
from botocore.exceptions import ClientError

from komo_aws_dynamodb import settings


class Kaddb:
    _shared_instance: "Kaddb" = None

    @classmethod
    def get_instance(cls, region: str, table: str) -> "Kaddb":
        if cls._shared_instance is None:
            cls._shared_instance = Kaddb(region=region, table=table)
        return cls._shared_instance

    def __init__(self, region: str, table: str):
        self._region = region
        self._dynamodb = boto3.resource('dynamodb', region_name=self._region)
        self._client = boto3.client('dynamodb', region_name=self._region)

        self._table = self._dynamodb.Table(table)
        self._table_exists: bool = False

    def initialize(self):
        self.create_if_table_does_not_exists()

    @property
    def table_exists(self):
        return self._table_exists

    def create_table(self):
        try:
            self._client.create_table(
                TableName=self._table.name,
                # Declare your Primary Key in the KeySchema argument
                KeySchema=settings.table_settings[self._table.name]["key_schema"],
                # Any attributes used in KeySchema or Indexes must be declared in AttributeDefinitions
                AttributeDefinitions=settings.table_settings[self._table.name]["attribute_definitions"],
                # ProvisionedThroughput controls the amount of data you can read or write to DynamoDB per second.
                # You can control read and write capacity independently.
                ProvisionedThroughput=settings.table_settings[self._table.name]["provision_throughput"],
            )
            self._table_exists = True
            # print("Table created successfully!")
        except Exception as e:
            # print("Error creating table:")
            raise e

    def create_if_table_does_not_exists(self):

        if not self.check_if_table_exist():
            self.create_table()

    def check_if_table_exist(self):
        try:
            self._client.describe_table(TableName=self._table.name)
            self._table_exists = True
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "ResourceNotFoundException":
                return False
            else:
                raise e

    def delete_table(self):
        try:
            if not self.check_if_table_exist():
                pass
                # raise Exception(f"Table {self._table.name} does not exist.")

            self._client.delete_table(
                TableName=self._table.name,
            )
            # print("Table deleted successfully!")
        except Exception as e:
            # print(f"Error deleting table: {e}")
            raise e

    """
    :argument key that denotes a timestamp
    :argument document that is associated with the key/timestamp
    """

    def insert_item(self, key: str, document: List[dict]):

        try:
            response = self._table.put_item(
                Item={
                    "timestamp": key,
                    'Formats': document,
                }
            )
            return response
        except Exception as e:
            raise e

    """
    Takes in an attribute name(key) and its search value string.
    :argument key
    :argument value
    :returns document associated with the key.
    """

    def get_item(self, key: str, value: str) -> dict:
        try:
            response = self._table.get_item(Key={key: value})
            return response['Item']
        except Exception as e:
            raise

    def delete_item(self, key: str, value: str):
        try:
            response = self._table.delete_item(
                Key={key: value},
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            return response
