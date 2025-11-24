import pytest
from src.db.debt_repo import create_debt_adjustment
from src.db.customer_repo import create_customer, get_customer


class TestDebtRepo:
    """Tests for debt adjustment repository functions"""
    
    def test_create_debt_adjustment(self, dynamodb_table):
        """Test creating a debt adjustment"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        adjustment = create_debt_adjustment(
            customer_id=customer['id'],
            amount=-100.0,
            reason='Customer paid 100 in cash'
        )
        
        assert adjustment['customerId'] == customer['id']
        assert adjustment['amount'] == -100.0
        assert adjustment['reason'] == 'Customer paid 100 in cash'
        assert 'id' in adjustment
        assert 'timestamp' in adjustment
    
    def test_debt_adjustment_updates_customer_debt(self, dynamodb_table):
        """Test that debt adjustment updates customer debt"""
        customer = create_customer('Test Customer', 'Location', '123')
        initial_debt = customer['totalDebt']
        
        # Add debt
        adjustment = create_debt_adjustment(
            customer_id=customer['id'],
            amount=50.0,
            reason='Added debt'
        )
        
        updated_customer = get_customer(customer['id'])
        assert updated_customer['totalDebt'] == initial_debt + 50.0
        
        # Reduce debt
        create_debt_adjustment(
            customer_id=customer['id'],
            amount=-25.0,
            reason='Payment received'
        )
        
        updated_customer = get_customer(customer['id'])
        assert updated_customer['totalDebt'] == initial_debt + 25.0
    
    def test_debt_adjustment_positive_amount(self, dynamodb_table):
        """Test debt adjustment with positive amount (increases debt)"""
        customer = create_customer('Test Customer', 'Location', '123')
        initial_debt = customer['totalDebt']
        
        adjustment = create_debt_adjustment(
            customer_id=customer['id'],
            amount=200.0,
            reason='Manual debt increase'
        )
        
        updated_customer = get_customer(customer['id'])
        assert updated_customer['totalDebt'] == initial_debt + 200.0
    
    def test_debt_adjustment_negative_amount(self, dynamodb_table):
        """Test debt adjustment with negative amount (decreases debt)"""
        customer = create_customer('Test Customer', 'Location', '123')
        
        # First add some debt
        create_debt_adjustment(customer['id'], 100.0, 'Initial debt')
        
        # Then reduce it
        adjustment = create_debt_adjustment(
            customer_id=customer['id'],
            amount=-50.0,
            reason='Payment received'
        )
        
        updated_customer = get_customer(customer['id'])
        assert updated_customer['totalDebt'] == 50.0

