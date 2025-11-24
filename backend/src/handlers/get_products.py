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
        
        # Add computed effective prices (convert Decimal to float for computation)
        from decimal import Decimal
        for product in products:
            base_buying = float(product['baseBuyingPrice']) if isinstance(product['baseBuyingPrice'], Decimal) else product['baseBuyingPrice']
            base_selling = float(product['baseSellingPrice']) if isinstance(product['baseSellingPrice'], Decimal) else product['baseSellingPrice']
            discount = float(product.get('discountPercent', 0)) if isinstance(product.get('discountPercent', 0), Decimal) else product.get('discountPercent', 0)
            
            product['effectiveBuyingPrice'] = compute_effective_price(base_buying, discount)
            product['effectiveSellingPrice'] = compute_effective_price(base_selling, discount)
        
        return success_response(200, {
            'items': products,
            'nextToken': None
        })
    
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

