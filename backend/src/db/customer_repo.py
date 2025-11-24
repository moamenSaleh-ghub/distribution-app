import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from .dynamo_client import get_table


def create_customer(
    name: str,
    location: str,
    phone: str,
    email: Optional[str] = None,
    notes: Optional[str] = None,
    is_active: bool = True
) -> Dict[str, Any]:
    """Create a new customer"""
    customer_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    item = {
        'pk': f'CUSTOMER#{customer_id}',
        'sk': 'META',
        'entityType': 'CUSTOMER',
        'id': customer_id,
        'name': name,
        'location': location,
        'phone': phone,
        'email': email,
        'totalDebt': 0.0,
        'notes': notes,
        'isActive': is_active,
        'createdAt': now,
        'updatedAt': now
    }
    
    table = get_table()
    table.put_item(Item=item)
    
    return item


def get_customer(customer_id: str) -> Optional[Dict[str, Any]]:
    """Get a customer by ID"""
    table = get_table()
    response = table.get_item(
        Key={
            'pk': f'CUSTOMER#{customer_id}',
            'sk': 'META'
        }
    )
    return response.get('Item')


def update_customer_debt(customer_id: str, debt_change: float) -> Optional[Dict[str, Any]]:
    """Update customer's total debt"""
    table = get_table()
    
    response = table.update_item(
        Key={
            'pk': f'CUSTOMER#{customer_id}',
            'sk': 'META'
        },
        UpdateExpression='ADD totalDebt :debtChange SET updatedAt = :updatedAt',
        ExpressionAttributeValues={
            ':debtChange': debt_change,
            ':updatedAt': datetime.now(timezone.utc).isoformat()
        },
        ReturnValues='ALL_NEW'
    )
    
    return response.get('Attributes')


def list_customers(
    search: Optional[str] = None,
    include_inactive: bool = False
) -> List[Dict[str, Any]]:
    """List all customers with optional filtering"""
    table = get_table()
    
    # Use GSI to query by entityType
    response = table.query(
        IndexName='EntityTypeIndex',
        KeyConditionExpression='entityType = :entityType',
        ExpressionAttributeValues={
            ':entityType': 'CUSTOMER'
        }
    )
    
    customers = response.get('Items', [])
    
    # Filter by active status
    if not include_inactive:
        customers = [c for c in customers if c.get('isActive', True)]
    
    # Filter by search term
    if search:
        search_lower = search.lower()
        customers = [c for c in customers if search_lower in c.get('name', '').lower()]
    
    return customers


def get_customer_orders(customer_id: str, limit: int = 50) -> List[Dict[str, Any]]:
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


def get_customer_debt_adjustments(customer_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get all debt adjustments for a customer"""
    table = get_table()
    
    response = table.query(
        KeyConditionExpression='pk = :pk AND begins_with(sk, :sk_prefix)',
        ExpressionAttributeValues={
            ':pk': f'CUSTOMER#{customer_id}',
            ':sk_prefix': 'DEBT#'
        },
        ScanIndexForward=False,  # Most recent first
        Limit=limit
    )
    
    return response.get('Items', [])

