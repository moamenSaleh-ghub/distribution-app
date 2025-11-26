import json
from src.db.product_repo import update_product, get_product, compute_effective_price
from src.utils.response import success_response, error_response
from src.auth import extract_and_verify_token, AuthenticationError


def handler(event, context):
    """Update a product"""
    # Verify JWT token
    try:
        extract_and_verify_token(event)
    except AuthenticationError as e:
        return error_response(401, str(e), 'UNAUTHORIZED')
    
    try:
        product_id = event.get('pathParameters', {}).get('id')
        
        if not product_id:
            return error_response(400, 'Product ID is required', 'MISSING_PARAMETER')
        
        body = json.loads(event.get('body', '{}'))
        
        # Validate numeric fields if provided
        base_buying_price = body.get('baseBuyingPrice')
        if base_buying_price is not None:
            try:
                base_buying_price = float(base_buying_price)
                if base_buying_price < 0:
                    return error_response(400, 'baseBuyingPrice must be non-negative', 'INVALID_INPUT')
            except (ValueError, TypeError):
                return error_response(400, 'baseBuyingPrice must be a valid number', 'INVALID_INPUT')
        
        base_selling_price = body.get('baseSellingPrice')
        if base_selling_price is not None:
            try:
                base_selling_price = float(base_selling_price)
                if base_selling_price < 0:
                    return error_response(400, 'baseSellingPrice must be non-negative', 'INVALID_INPUT')
            except (ValueError, TypeError):
                return error_response(400, 'baseSellingPrice must be a valid number', 'INVALID_INPUT')
        
        discount_percent = body.get('discountPercent')
        if discount_percent is not None:
            try:
                discount_percent = float(discount_percent)
                if discount_percent < 0 or discount_percent > 100:
                    return error_response(400, 'discountPercent must be between 0 and 100', 'INVALID_INPUT')
            except (ValueError, TypeError):
                return error_response(400, 'discountPercent must be a valid number', 'INVALID_INPUT')
        
        # Update product
        product = update_product(
            product_id=product_id,
            name=body.get('name'),
            base_buying_price=base_buying_price,
            base_selling_price=base_selling_price,
            discount_percent=discount_percent,
            image_key=body.get('imageKey'),
            is_active=body.get('isActive')
        )
        
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
    
    except json.JSONDecodeError:
        return error_response(400, 'Invalid JSON in request body', 'INVALID_JSON')
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

