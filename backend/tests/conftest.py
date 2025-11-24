import pytest
import boto3
from moto import mock_dynamodb
from src.db.dynamo_client import get_table


@pytest.fixture
def dynamodb_table():
    """Create a mock DynamoDB table for testing"""
    with mock_dynamodb():
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
        
        # Set environment variable for the table name
        import os
        os.environ['DYNAMODB_TABLE_NAME'] = 'distribution-app-dev'
        
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

