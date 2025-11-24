import json
from src.db.product_repo import list_products, compute_effective_price
from src.utils.response import success_response, error_response


def handler(event, context):
    """List all products"""
    try:
        query_params = event.get('queryStringParameters') or {}
        
        search = query_params.get('search')
        include_inactive = query_params.get('includeInactive', 'false').lower() == 'true'
        
        products = list_products(search=search, include_inactive=include_inactive)
        
        # Add computed effective prices
        for product in products:
            product['effectiveBuyingPrice'] = compute_effective_price(
                product['baseBuyingPrice'],
                product.get('discountPercent')
            )
            product['effectiveSellingPrice'] = compute_effective_price(
                product['baseSellingPrice'],
                product.get('discountPercent')
            )
        
        return success_response(200, {
            'items': products,
            'nextToken': None
        })
    
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

