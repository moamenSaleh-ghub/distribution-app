import json
from src.db.product_repo import update_product, get_product, compute_effective_price
from src.utils.response import success_response, error_response


def handler(event, context):
    """Update a product"""
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
        
        # Add computed effective prices
        product['effectiveBuyingPrice'] = compute_effective_price(
            product['baseBuyingPrice'],
            product.get('discountPercent')
        )
        product['effectiveSellingPrice'] = compute_effective_price(
            product['baseSellingPrice'],
            product.get('discountPercent')
        )
        
        return success_response(200, product)
    
    except json.JSONDecodeError:
        return error_response(400, 'Invalid JSON in request body', 'INVALID_JSON')
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

