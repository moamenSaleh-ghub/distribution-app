import pytest
from src.db.customer_repo import (
    create_customer,
    get_customer,
    update_customer_debt,
    list_customers,
    get_customer_orders,
    get_customer_debt_adjustments
)


class TestCustomerRepo:
    """Tests for customer repository functions"""
    
    def test_create_customer(self, dynamodb_table, sample_customer):
        """Test creating a customer"""
        customer = create_customer(
            name=sample_customer['name'],
            location=sample_customer['location'],
            phone=sample_customer['phone'],
            email=sample_customer['email']
        )
        
        assert customer['name'] == sample_customer['name']
        assert customer['location'] == sample_customer['location']
        assert customer['phone'] == sample_customer['phone']
        assert customer['email'] == sample_customer['email']
        assert customer['totalDebt'] == 0.0
        assert customer['isActive'] is True
        assert 'id' in customer
        assert 'createdAt' in customer
    
    def test_get_customer(self, dynamodb_table, sample_customer):
        """Test retrieving a customer"""
        created = create_customer(
            name=sample_customer['name'],
            location=sample_customer['location'],
            phone=sample_customer['phone']
        )
        
        retrieved = get_customer(created['id'])
        
        assert retrieved is not None
        assert retrieved['id'] == created['id']
        assert retrieved['name'] == sample_customer['name']
    
    def test_get_nonexistent_customer(self, dynamodb_table):
        """Test retrieving a non-existent customer"""
        result = get_customer('nonexistent-id')
        assert result is None
    
    def test_update_customer_debt(self, dynamodb_table, sample_customer):
        """Test updating customer debt"""
        created = create_customer(
            name=sample_customer['name'],
            location=sample_customer['location'],
            phone=sample_customer['phone']
        )
        
        # Add debt
        updated = update_customer_debt(created['id'], 100.0)
        assert updated['totalDebt'] == 100.0
        
        # Add more debt
        updated = update_customer_debt(created['id'], 50.0)
        assert updated['totalDebt'] == 150.0
        
        # Reduce debt
        updated = update_customer_debt(created['id'], -25.0)
        assert updated['totalDebt'] == 125.0
    
    def test_list_customers(self, dynamodb_table):
        """Test listing customers"""
        create_customer('Customer 1', 'Location 1', '123')
        create_customer('Customer 2', 'Location 2', '456')
        create_customer('Inactive Customer', 'Location 3', '789', is_active=False)
        
        customers = list_customers()
        
        assert len(customers) == 2  # Only active customers
        assert all(c.get('isActive', True) for c in customers)
    
    def test_list_customers_with_search(self, dynamodb_table):
        """Test listing customers with search filter"""
        create_customer('Ahmed Market', 'Nazareth', '123')
        create_customer('Mohammed Shop', 'Haifa', '456')
        create_customer('Ahmed Store', 'Tel Aviv', '789')
        
        customers = list_customers(search='Ahmed')
        
        assert len(customers) == 2
        assert all('Ahmed' in c['name'] for c in customers)
    
    def test_get_customer_orders(self, dynamodb_table):
        """Test getting customer orders"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        # Orders are created via order_repo, but we can test the query
        orders = get_customer_orders(customer['id'])
        
        assert isinstance(orders, list)
        # Initially empty, but function should work
    
    def test_get_customer_debt_adjustments(self, dynamodb_table):
        """Test getting customer debt adjustments"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        # Adjustments are created via debt_repo, but we can test the query
        adjustments = get_customer_debt_adjustments(customer['id'])
        
        assert isinstance(adjustments, list)
        # Initially empty, but function should work

