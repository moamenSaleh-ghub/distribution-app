import json
from src.db.order_repo import create_order
from src.utils.response import success_response, error_response


def handler(event, context):
    """Create a new order"""
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        customer_id = body.get('customerId')
        items = body.get('items', [])
        
        if not customer_id:
            return error_response(400, 'customerId is required', 'MISSING_FIELD')
        if not items or len(items) == 0:
            return error_response(400, 'items array is required and cannot be empty', 'MISSING_FIELD')
        
        # Validate items
        for item in items:
            if not item.get('productId'):
                return error_response(400, 'Each item must have a productId', 'INVALID_INPUT')
            quantity = item.get('quantity')
            if quantity is None:
                return error_response(400, 'Each item must have a quantity', 'INVALID_INPUT')
            try:
                quantity = float(quantity)
                if quantity <= 0:
                    return error_response(400, 'Quantity must be positive', 'INVALID_INPUT')
                item['quantity'] = quantity
            except (ValueError, TypeError):
                return error_response(400, 'Quantity must be a valid number', 'INVALID_INPUT')
            
            # Validate unitPrice if provided
            if 'unitPrice' in item and item['unitPrice'] is not None:
                try:
                    unit_price = float(item['unitPrice'])
                    if unit_price < 0:
                        return error_response(400, 'unitPrice must be non-negative', 'INVALID_INPUT')
                    item['unitPrice'] = unit_price
                except (ValueError, TypeError):
                    return error_response(400, 'unitPrice must be a valid number', 'INVALID_INPUT')
        
        # Validate numeric fields
        discount = body.get('discount', 0)
        try:
            discount = float(discount)
            if discount < 0:
                return error_response(400, 'discount must be non-negative', 'INVALID_INPUT')
        except (ValueError, TypeError):
            return error_response(400, 'discount must be a valid number', 'INVALID_INPUT')
        
        paid_now = body.get('paidNow', 0)
        try:
            paid_now = float(paid_now)
            if paid_now < 0:
                return error_response(400, 'paidNow must be non-negative', 'INVALID_INPUT')
        except (ValueError, TypeError):
            return error_response(400, 'paidNow must be a valid number', 'INVALID_INPUT')
        
        order_date = body.get('orderDate')
        notes = body.get('notes')
        
        # Create order
        order = create_order(
            customer_id=customer_id,
            order_date=order_date,
            items=items,
            discount=discount,
            paid_now=paid_now,
            notes=notes
        )
        
        return success_response(201, order)
    
    except json.JSONDecodeError:
        return error_response(400, 'Invalid JSON in request body', 'INVALID_JSON')
    except ValueError as e:
        return error_response(400, str(e), 'INVALID_INPUT')
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

