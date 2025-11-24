import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from .dynamo_client import get_table
from .product_repo import get_product, compute_effective_price


def create_order(
    customer_id: str,
    order_date: Optional[str],
    items: List[Dict[str, Any]],
    discount: float = 0.0,
    paid_now: float = 0.0,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new order"""
    order_id = str(uuid.uuid4())
    
    if order_date:
        timestamp = datetime.fromisoformat(order_date.replace('Z', '+00:00'))
    else:
        timestamp = datetime.now(timezone.utc)
    
    order_date_str = timestamp.isoformat()
    sk_timestamp = order_date_str
    
    # Process items and compute prices
    processed_items = []
    subtotal = 0.0
    
    for item in items:
        product_id = item['productId']
        quantity = item['quantity']
        unit_price = item.get('unitPrice')
        
        # If unitPrice not provided, fetch product and compute
        if unit_price is None:
            product = get_product(product_id)
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            discount_percent = product.get('discountPercent', 0)
            base_selling_price = product['baseSellingPrice']
            unit_price = compute_effective_price(base_selling_price, discount_percent)
            product_name = product['name']
        else:
            product_name = item.get('productNameSnapshot', 'Unknown Product')
        
        line_total = unit_price * quantity
        subtotal += line_total
        
        processed_items.append({
            'productId': product_id,
            'productNameSnapshot': product_name,
            'unitPrice': unit_price,
            'quantity': quantity,
            'lineTotal': line_total
        })
    
    total_amount = subtotal - discount
    debt_change = total_amount - paid_now
    
    order_item = {
        'pk': f'CUSTOMER#{customer_id}',
        'sk': f'ORDER#{sk_timestamp}',
        'entityType': 'ORDER',
        'id': order_id,
        'customerId': customer_id,
        'orderDate': order_date_str,
        'items': processed_items,
        'subtotal': subtotal,
        'discount': discount,
        'totalAmount': total_amount,
        'paidNow': paid_now,
        'debtChange': debt_change,
        'notes': notes
    }
    
    table = get_table()
    table.put_item(Item=order_item)
    
    # Update customer debt
    from .customer_repo import update_customer_debt
    update_customer_debt(customer_id, debt_change)
    
    return order_item


def get_order(customer_id: str, order_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific order (requires scanning customer orders)"""
    orders = get_customer_orders_list(customer_id, limit=1000)
    for order in orders:
        if order.get('id') == order_id:
            return order
    return None


def get_customer_orders_list(customer_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get all orders for a customer"""
    table = get_table()
    
    response = table.query(
        KeyConditionExpression='pk = :pk AND begins_with(sk, :sk_prefix)',
        ExpressionAttributeValues={
            ':pk': f'CUSTOMER#{customer_id}',
            ':sk_prefix': 'ORDER#'
        },
        ScanIndexForward=False,  # Most recent first
        Limit=limit
    )
    
    return response.get('Items', [])

