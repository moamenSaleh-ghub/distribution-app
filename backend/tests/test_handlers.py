import pytest
import json
from src.handlers.create_product import handler as create_product_handler
from src.handlers.get_products import handler as get_products_handler
from src.handlers.get_product import handler as get_product_handler
from src.handlers.update_product import handler as update_product_handler
from src.handlers.create_customer import handler as create_customer_handler
from src.handlers.get_customers import handler as get_customers_handler
from src.handlers.get_customer_detail import handler as get_customer_detail_handler
from src.handlers.create_order import handler as create_order_handler
from src.handlers.get_customer_orders import handler as get_customer_orders_handler
from src.handlers.adjust_customer_debt import handler as adjust_customer_debt_handler
from src.db.product_repo import create_product
from src.db.customer_repo import create_customer


class TestProductHandlers:
    """Tests for product Lambda handlers"""
    
    def test_create_product_handler_success(self, dynamodb_table):
        """Test successful product creation"""
        event = {
            'body': json.dumps({
                'name': 'Test Product',
                'baseBuyingPrice': 10.0,
                'baseSellingPrice': 15.0,
                'discountPercent': 10
            })
        }
        
        response = create_product_handler(event, None)
        
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['name'] == 'Test Product'
        assert body['baseBuyingPrice'] == 10.0
        assert 'id' in body
    
    def test_create_product_handler_missing_fields(self, dynamodb_table):
        """Test product creation with missing required fields"""
        event = {
            'body': json.dumps({
                'name': 'Test Product'
                # Missing prices
            })
        }
        
        response = create_product_handler(event, None)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'message' in body
    
    def test_get_products_handler(self, dynamodb_table):
        """Test getting list of products"""
        create_product('Product 1', 10.0, 15.0)
        create_product('Product 2', 20.0, 25.0)
        
        event = {'queryStringParameters': None}
        response = get_products_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert len(body['items']) == 2
    
    def test_get_product_handler(self, dynamodb_table):
        """Test getting a single product"""
        product = create_product('Test Product', 10.0, 15.0)
        
        event = {
            'pathParameters': {'id': product['id']}
        }
        response = get_product_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['id'] == product['id']
    
    def test_update_product_handler(self, dynamodb_table):
        """Test updating a product"""
        product = create_product('Test Product', 10.0, 15.0)
        
        event = {
            'pathParameters': {'id': product['id']},
            'body': json.dumps({
                'name': 'Updated Product',
                'baseSellingPrice': 20.0
            })
        }
        response = update_product_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['name'] == 'Updated Product'
        assert body['baseSellingPrice'] == 20.0


class TestCustomerHandlers:
    """Tests for customer Lambda handlers"""
    
    def test_create_customer_handler_success(self, dynamodb_table):
        """Test successful customer creation"""
        event = {
            'body': json.dumps({
                'name': 'Test Customer',
                'location': 'Test Location',
                'phone': '+1234567890',
                'email': 'test@example.com'
            })
        }
        
        response = create_customer_handler(event, None)
        
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['name'] == 'Test Customer'
        assert body['totalDebt'] == 0.0
    
    def test_create_customer_handler_missing_fields(self, dynamodb_table):
        """Test customer creation with missing required fields"""
        event = {
            'body': json.dumps({
                'name': 'Test Customer'
                # Missing location and phone
            })
        }
        
        response = create_customer_handler(event, None)
        
        assert response['statusCode'] == 400
    
    def test_get_customers_handler(self, dynamodb_table):
        """Test getting list of customers"""
        create_customer('Customer 1', 'Location 1', '123')
        create_customer('Customer 2', 'Location 2', '456')
        
        event = {'queryStringParameters': None}
        response = get_customers_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert len(body['items']) == 2
    
    def test_get_customer_detail_handler(self, dynamodb_table):
        """Test getting customer detail"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        event = {
            'pathParameters': {'id': customer['id']}
        }
        response = get_customer_detail_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['customer']['id'] == customer['id']
        assert 'recentOrders' in body


class TestOrderHandlers:
    """Tests for order Lambda handlers"""
    
    def test_create_order_handler_success(self, dynamodb_table):
        """Test successful order creation"""
        customer = create_customer('Test Customer', 'Location', '123')
        product = create_product('Test Product', 10.0, 15.0)
        
        event = {
            'body': json.dumps({
                'customerId': customer['id'],
                'items': [
                    {
                        'productId': product['id'],
                        'quantity': 5
                    }
                ],
                'paidNow': 50.0
            })
        }
        
        response = create_order_handler(event, None)
        
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['customerId'] == customer['id']
        assert len(body['items']) == 1
    
    def test_create_order_handler_missing_items(self, dynamodb_table):
        """Test order creation with missing items"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        event = {
            'body': json.dumps({
                'customerId': customer['id'],
                'items': []
            })
        }
        
        response = create_order_handler(event, None)
        
        assert response['statusCode'] == 400


class TestDebtHandlers:
    """Tests for debt adjustment Lambda handlers"""
    
    def test_adjust_customer_debt_handler_success(self, dynamodb_table):
        """Test successful debt adjustment"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        event = {
            'pathParameters': {'id': customer['id']},
            'body': json.dumps({
                'amount': -100.0,
                'reason': 'Customer paid 100 in cash'
            })
        }
        
        response = adjust_customer_debt_handler(event, None)
        
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['amount'] == -100.0
        assert 'newTotalDebt' in body
    
    def test_adjust_customer_debt_handler_missing_fields(self, dynamodb_table):
        """Test debt adjustment with missing fields"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        event = {
            'pathParameters': {'id': customer['id']},
            'body': json.dumps({
                'amount': -100.0
                # Missing reason
            })
        }
        
        response = adjust_customer_debt_handler(event, None)
        
        assert response['statusCode'] == 400

