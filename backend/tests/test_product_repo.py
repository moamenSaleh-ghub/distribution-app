import pytest
from src.db.product_repo import (
    create_product,
    get_product,
    update_product,
    list_products,
    compute_effective_price
)


class TestProductRepo:
    """Tests for product repository functions"""
    
    def test_create_product(self, dynamodb_table, sample_product):
        """Test creating a product"""
        product = create_product(
            name=sample_product['name'],
            base_buying_price=sample_product['baseBuyingPrice'],
            base_selling_price=sample_product['baseSellingPrice'],
            discount_percent=sample_product['discountPercent'],
            is_active=sample_product['isActive']
        )
        
        assert product['name'] == sample_product['name']
        assert product['baseBuyingPrice'] == sample_product['baseBuyingPrice']
        assert product['baseSellingPrice'] == sample_product['baseSellingPrice']
        assert product['discountPercent'] == sample_product['discountPercent']
        assert product['isActive'] == sample_product['isActive']
        assert 'id' in product
        assert 'createdAt' in product
        assert 'updatedAt' in product
    
    def test_get_product(self, dynamodb_table, sample_product):
        """Test retrieving a product"""
        created = create_product(
            name=sample_product['name'],
            base_buying_price=sample_product['baseBuyingPrice'],
            base_selling_price=sample_product['baseSellingPrice']
        )
        
        retrieved = get_product(created['id'])
        
        assert retrieved is not None
        assert retrieved['id'] == created['id']
        assert retrieved['name'] == sample_product['name']
    
    def test_get_nonexistent_product(self, dynamodb_table):
        """Test retrieving a non-existent product"""
        result = get_product('nonexistent-id')
        assert result is None
    
    def test_update_product(self, dynamodb_table, sample_product):
        """Test updating a product"""
        created = create_product(
            name=sample_product['name'],
            base_buying_price=sample_product['baseBuyingPrice'],
            base_selling_price=sample_product['baseSellingPrice']
        )
        
        updated = update_product(
            created['id'],
            name='Updated Name',
            base_selling_price=20.0,
            discount_percent=15
        )
        
        assert updated['name'] == 'Updated Name'
        assert updated['baseSellingPrice'] == 20.0
        assert updated['discountPercent'] == 15
        assert updated['id'] == created['id']
    
    def test_list_products(self, dynamodb_table):
        """Test listing products"""
        # Create multiple products
        create_product('Product 1', 10.0, 15.0)
        create_product('Product 2', 20.0, 25.0)
        create_product('Inactive Product', 5.0, 10.0, is_active=False)
        
        products = list_products()
        
        assert len(products) == 2  # Only active products
        assert all(p.get('isActive', True) for p in products)
    
    def test_list_products_with_search(self, dynamodb_table):
        """Test listing products with search filter"""
        create_product('Coca Cola', 2.0, 3.5)
        create_product('Pepsi', 2.0, 3.5)
        create_product('Water', 1.0, 2.0)
        
        products = list_products(search='Cola')
        
        assert len(products) == 1
        assert 'Cola' in products[0]['name']
    
    def test_list_products_include_inactive(self, dynamodb_table):
        """Test listing products including inactive ones"""
        create_product('Active Product', 10.0, 15.0, is_active=True)
        create_product('Inactive Product', 5.0, 10.0, is_active=False)
        
        products = list_products(include_inactive=True)
        
        assert len(products) == 2
    
    def test_compute_effective_price_no_discount(self):
        """Test computing effective price with no discount"""
        price = compute_effective_price(100.0, None)
        assert price == 100.0
        
        price = compute_effective_price(100.0, 0)
        assert price == 100.0
    
    def test_compute_effective_price_with_discount(self):
        """Test computing effective price with discount"""
        price = compute_effective_price(100.0, 10)
        assert price == 90.0
        
        price = compute_effective_price(100.0, 25)
        assert price == 75.0

