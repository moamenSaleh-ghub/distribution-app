import json
from src.db.customer_repo import list_customers
from src.utils.response import success_response, error_response
from src.auth import extract_and_verify_token, AuthenticationError


def handler(event, context):
    """List all customers"""
    # Handle CORS preflight (OPTIONS) requests
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS' or \
       event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    # Verify JWT token
    try:
        extract_and_verify_token(event)
    except AuthenticationError as e:
        return error_response(401, str(e), 'UNAUTHORIZED')
    
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

