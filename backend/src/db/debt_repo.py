import uuid
from decimal import Decimal
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from .dynamo_client import get_table
from .customer_repo import update_customer_debt


def create_debt_adjustment(
    customer_id: str,
    amount: float,
    reason: str,
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """Create a debt adjustment"""
    adjustment_id = str(uuid.uuid4())
    
    if timestamp:
        ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    else:
        ts = datetime.now(timezone.utc)
    
    timestamp_str = ts.isoformat()
    sk_timestamp = timestamp_str
    
    adjustment_item = {
        'pk': f'CUSTOMER#{customer_id}',
        'sk': f'DEBT#{sk_timestamp}',
        'entityType': 'DEBT_ADJUSTMENT',
        'id': adjustment_id,
        'customerId': customer_id,
        'timestamp': timestamp_str,
        'amount': Decimal(str(amount)),
        'reason': reason
    }
    
    table = get_table()
    table.put_item(Item=adjustment_item)
    
    # Update customer debt
    update_customer_debt(customer_id, amount)
    
    return adjustment_item

