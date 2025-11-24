import json
from src.db.customer_repo import list_customers
from src.utils.response import success_response, error_response


def handler(event, context):
    """List all customers"""
    try:
        query_params = event.get('queryStringParameters') or {}
        
        search = query_params.get('search')
        include_inactive = query_params.get('includeInactive', 'false').lower() == 'true'
        
        customers = list_customers(search=search, include_inactive=include_inactive)
        
        return success_response(200, {
            'items': customers,
            'nextToken': None
        })
    
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

