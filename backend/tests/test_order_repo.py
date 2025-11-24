import pytest
from src.db.order_repo import create_order, get_customer_orders_list
from src.db.product_repo import create_product
from src.db.customer_repo import create_customer


class TestOrderRepo:
    """Tests for order repository functions"""
    
    def test_create_order(self, dynamodb_table):
        """Test creating an order"""
        # Create customer and product first
        customer = create_customer('Test Customer', 'Location', '123')
        product = create_product('Test Product', 10.0, 15.0)
        
        order = create_order(
            customer_id=customer['id'],
            order_date=None,
            items=[
                {
                    'productId': product['id'],
                    'quantity': 5.0,
                    'unitPrice': None  # Should fetch from product
                }
            ],
            discount=0.0,
            paid_now=50.0,
            notes='Test order'
        )
        
        assert order['customerId'] == customer['id']
        assert len(order['items']) == 1
        assert order['items'][0]['quantity'] == 5
        assert order['subtotal'] > 0
        assert order['totalAmount'] == order['subtotal'] - order['discount']
        assert order['debtChange'] == order['totalAmount'] - order['paidNow']
        assert 'id' in order
        assert 'orderDate' in order
    
    def test_create_order_with_custom_price(self, dynamodb_table):
        """Test creating an order with custom unit price"""
        customer = create_customer('Test Customer', 'Location', '123')
        product = create_product('Test Product', 10.0, 15.0)
        
        order = create_order(
            customer_id=customer['id'],
            order_date=None,
            items=[
                {
                    'productId': product['id'],
                    'quantity': 3.0,
                    'unitPrice': 12.0  # Custom price
                }
            ],
            discount=0.0,
            paid_now=0.0
        )
        
        assert order['items'][0]['unitPrice'] == 12.0
        assert order['items'][0]['lineTotal'] == 36.0
        assert order['subtotal'] == 36.0
    
    def test_create_order_with_discount(self, dynamodb_table):
        """Test creating an order with discount"""
        customer = create_customer('Test Customer', 'Location', '123')
        product = create_product('Test Product', 10.0, 15.0)
        
        order = create_order(
            customer_id=customer['id'],
            order_date=None,
            items=[
                {
                    'productId': product['id'],
                    'quantity': 10.0,
                    'unitPrice': 15.0
                }
            ],
            discount=10.0,
            paid_now=0.0
        )
        
        assert order['subtotal'] == 150.0
        assert order['discount'] == 10.0
        assert order['totalAmount'] == 140.0
    
    def test_create_order_updates_customer_debt(self, dynamodb_table):
        """Test that creating an order updates customer debt"""
        customer = create_customer('Test Customer', 'Location', '123')
        product = create_product('Test Product', 10.0, 15.0)
        
        initial_debt = customer['totalDebt']
        
        order = create_order(
            customer_id=customer['id'],
            order_date=None,
            items=[
                {
                    'productId': product['id'],
                    'quantity': 5.0,
                    'unitPrice': 15.0
                }
            ],
            discount=0.0,
            paid_now=25.0
        )
        
        # Check customer debt was updated
        from src.db.customer_repo import get_customer
        updated_customer = get_customer(customer['id'])
        
        expected_debt = initial_debt + order['debtChange']
        assert updated_customer['totalDebt'] == expected_debt
    
    def test_create_order_nonexistent_product(self, dynamodb_table):
        """Test creating an order with non-existent product"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        with pytest.raises(ValueError, match="Product.*not found"):
            create_order(
                customer_id=customer['id'],
                order_date=None,
                items=[
                    {
                        'productId': 'nonexistent-product-id',
                        'quantity': 1,
                        'unitPrice': None
                    }
                ]
            )
    
    def test_get_customer_orders_list(self, dynamodb_table):
        """Test getting list of customer orders"""
        customer = create_customer('Test Customer', 'Location', '123')
        product = create_product('Test Product', 10.0, 15.0)
        
        # Create multiple orders
        create_order(
            customer_id=customer['id'],
            order_date=None,
            items=[{'productId': product['id'], 'quantity': 1.0, 'unitPrice': 15.0}]
        )
        create_order(
            customer_id=customer['id'],
            order_date=None,
            items=[{'productId': product['id'], 'quantity': 2.0, 'unitPrice': 15.0}]
        )
        
        orders = get_customer_orders_list(customer['id'])
        
        assert len(orders) == 2
        assert all(o['customerId'] == customer['id'] for o in orders)

