import json
from src.db.product_repo import get_product, compute_effective_price
from src.utils.response import success_response, error_response


def handler(event, context):
    """Get a single product by ID"""
    try:
        product_id = event.get('pathParameters', {}).get('id')
        
        if not product_id:
            return error_response(400, 'Product ID is required', 'MISSING_PARAMETER')
        
        product = get_product(product_id)
        
        if not product:
            return error_response(404, f'Product {product_id} not found', 'NOT_FOUND')
        
        # Add computed effective prices (convert Decimal to float for computation)
        from decimal import Decimal
        base_buying = float(product['baseBuyingPrice']) if isinstance(product['baseBuyingPrice'], Decimal) else product['baseBuyingPrice']
        base_selling = float(product['baseSellingPrice']) if isinstance(product['baseSellingPrice'], Decimal) else product['baseSellingPrice']
        discount = float(product.get('discountPercent', 0)) if isinstance(product.get('discountPercent', 0), Decimal) else product.get('discountPercent', 0)
        
        product['effectiveBuyingPrice'] = compute_effective_price(base_buying, discount)
        product['effectiveSellingPrice'] = compute_effective_price(base_selling, discount)
        
        return success_response(200, product)
    
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

