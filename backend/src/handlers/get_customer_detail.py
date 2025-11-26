import json
from src.db.customer_repo import get_customer, get_customer_orders
from src.utils.response import success_response, error_response
from src.auth import extract_and_verify_token, AuthenticationError


def handler(event, context):
    """Get customer detail with recent orders"""
    # Verify JWT token
    try:
        extract_and_verify_token(event)
    except AuthenticationError as e:
        return error_response(401, str(e), 'UNAUTHORIZED')
    
    try:
        customer_id = event.get('pathParameters', {}).get('id')
        
        if not customer_id:
            return error_response(400, 'Customer ID is required', 'MISSING_PARAMETER')
        
        customer = get_customer(customer_id)
        
        if not customer:
            return error_response(404, f'Customer {customer_id} not found', 'NOT_FOUND')
        
        # Get recent orders
        orders = get_customer_orders(customer_id, limit=10)
        
        # Format orders for response (simplified)
        recent_orders = [
            {
                'id': order.get('id'),
                'orderDate': order.get('orderDate'),
                'totalAmount': order.get('totalAmount'),
                'paidNow': order.get('paidNow'),
                'debtChange': order.get('debtChange')
            }
            for order in orders
        ]
        
        return success_response(200, {
            'customer': customer,
            'recentOrders': recent_orders
        })
    
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

