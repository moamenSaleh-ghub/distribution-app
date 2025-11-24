import json
from src.db.order_repo import get_customer_orders_list
from src.utils.response import success_response, error_response


def handler(event, context):
    """Get orders for a customer"""
    try:
        customer_id = event.get('pathParameters', {}).get('id')
        
        if not customer_id:
            return error_response(400, 'Customer ID is required', 'MISSING_PARAMETER')
        
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 50))
        
        orders = get_customer_orders_list(customer_id, limit=limit)
        
        # Return simplified order info
        order_list = [
            {
                'id': order.get('id'),
                'orderDate': order.get('orderDate'),
                'totalAmount': order.get('totalAmount'),
                'paidNow': order.get('paidNow'),
                'debtChange': order.get('debtChange'),
                'items': order.get('items', [])
            }
            for order in orders
        ]
        
        return success_response(200, {
            'items': order_list,
            'nextToken': None
        })
    
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

