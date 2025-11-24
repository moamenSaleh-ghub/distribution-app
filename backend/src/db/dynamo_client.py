import os
import boto3
from typing import Optional

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'distribution-app-dev')
table = dynamodb.Table(table_name)


def get_table():
    """Get the DynamoDB table instance"""
    return table

