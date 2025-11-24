import uuid
from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from .dynamo_client import get_table


def create_product(
    name: str,
    base_buying_price: float,
    base_selling_price: float,
    discount_percent: Optional[float] = None,
    image_key: Optional[str] = None,
    is_active: bool = True
) -> Dict[str, Any]:
    """Create a new product"""
    product_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    discount = discount_percent if discount_percent is not None else 0
    
    item = {
        'pk': f'PRODUCT#{product_id}',
        'sk': 'META',
        'entityType': 'PRODUCT',
        'id': product_id,
        'name': name,
        'baseBuyingPrice': Decimal(str(base_buying_price)),
        'baseSellingPrice': Decimal(str(base_selling_price)),
        'discountPercent': Decimal(str(discount)),
        'imageKey': image_key,
        'isActive': is_active,
        'createdAt': now,
        'updatedAt': now
    }
    
    table = get_table()
    table.put_item(Item=item)
    
    return item


def get_product(product_id: str) -> Optional[Dict[str, Any]]:
    """Get a product by ID"""
    table = get_table()
    response = table.get_item(
        Key={
            'pk': f'PRODUCT#{product_id}',
            'sk': 'META'
        }
    )
    return response.get('Item')


def update_product(
    product_id: str,
    name: Optional[str] = None,
    base_buying_price: Optional[float] = None,
    base_selling_price: Optional[float] = None,
    discount_percent: Optional[float] = None,
    image_key: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Optional[Dict[str, Any]]:
    """Update a product"""
    table = get_table()
    
    update_expression_parts = []
    expression_attribute_names = {}
    expression_attribute_values = {}
    
    if name is not None:
        update_expression_parts.append('#name = :name')
        expression_attribute_names['#name'] = 'name'
        expression_attribute_values[':name'] = name
    
    if base_buying_price is not None:
        update_expression_parts.append('baseBuyingPrice = :baseBuyingPrice')
        expression_attribute_values[':baseBuyingPrice'] = Decimal(str(base_buying_price))
    
    if base_selling_price is not None:
        update_expression_parts.append('baseSellingPrice = :baseSellingPrice')
        expression_attribute_values[':baseSellingPrice'] = Decimal(str(base_selling_price))
    
    if discount_percent is not None:
        update_expression_parts.append('discountPercent = :discountPercent')
        expression_attribute_values[':discountPercent'] = Decimal(str(discount_percent))
    
    if image_key is not None:
        update_expression_parts.append('imageKey = :imageKey')
        expression_attribute_values[':imageKey'] = image_key
    
    if is_active is not None:
        update_expression_parts.append('isActive = :isActive')
        expression_attribute_values[':isActive'] = is_active
    
    if not update_expression_parts:
        return get_product(product_id)
    
    update_expression_parts.append('updatedAt = :updatedAt')
    expression_attribute_values[':updatedAt'] = datetime.now(timezone.utc).isoformat()
    
    update_expression = 'SET ' + ', '.join(update_expression_parts)
    
    response = table.update_item(
        Key={
            'pk': f'PRODUCT#{product_id}',
            'sk': 'META'
        },
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names if expression_attribute_names else None,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    
    return response.get('Attributes')


def list_products(
    search: Optional[str] = None,
    include_inactive: bool = False
) -> List[Dict[str, Any]]:
    """List all products with optional filtering"""
    table = get_table()
    
    # Use GSI to query by entityType
    response = table.query(
        IndexName='EntityTypeIndex',
        KeyConditionExpression='entityType = :entityType',
        ExpressionAttributeValues={
            ':entityType': 'PRODUCT'
        }
    )
    
    products = response.get('Items', [])
    
    # Filter by active status
    if not include_inactive:
        products = [p for p in products if p.get('isActive', True)]
    
    # Filter by search term
    if search:
        search_lower = search.lower()
        products = [p for p in products if search_lower in p.get('name', '').lower()]
    
    return products


def compute_effective_price(base_price: float, discount_percent: Optional[float]) -> float:
    """Compute effective price after discount"""
    from decimal import Decimal
    # Convert Decimal to float if needed
    if isinstance(base_price, Decimal):
        base_price = float(base_price)
    if isinstance(discount_percent, Decimal):
        discount_percent = float(discount_percent)
    if discount_percent is None or discount_percent == 0:
        return base_price
    return base_price * (1 - discount_percent / 100)

