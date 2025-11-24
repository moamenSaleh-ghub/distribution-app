import pytest
import boto3
import os
from moto import mock_aws
from unittest.mock import patch


@pytest.fixture(autouse=True)
def dynamodb_table():
    """Create a mock DynamoDB table for testing"""
    with mock_aws():
        # Set environment variables
        os.environ['DYNAMODB_TABLE_NAME'] = 'distribution-app-dev'
        os.environ['AWS_REGION'] = 'eu-central-1'
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'
        
        # Create the table
        dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
        table = dynamodb.create_table(
            TableName='distribution-app-dev',
            KeySchema=[
                {'AttributeName': 'pk', 'KeyType': 'HASH'},
                {'AttributeName': 'sk', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'pk', 'AttributeType': 'S'},
                {'AttributeName': 'sk', 'AttributeType': 'S'},
                {'AttributeName': 'entityType', 'AttributeType': 'S'},
                {'AttributeName': 'name', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'EntityTypeIndex',
                    'KeySchema': [
                        {'AttributeName': 'entityType', 'KeyType': 'HASH'},
                        {'AttributeName': 'name', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Patch the dynamo_client to use the mocked table
        from src.db import dynamo_client
        dynamo_client.table = table
        dynamo_client.dynamodb = dynamodb
        
        yield table


@pytest.fixture
def sample_product():
    """Sample product data for testing"""
    return {
        'id': 'prod-123',
        'name': 'Test Product',
        'baseBuyingPrice': 10.0,
        'baseSellingPrice': 15.0,
        'discountPercent': 10,
        'isActive': True
    }


@pytest.fixture
def sample_customer():
    """Sample customer data for testing"""
    return {
        'id': 'cust-123',
        'name': 'Test Customer',
        'location': 'Test Location',
        'phone': '+1234567890',
        'email': 'test@example.com',
        'totalDebt': 0.0,
        'isActive': True
    }

