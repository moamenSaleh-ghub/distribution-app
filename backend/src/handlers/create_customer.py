import json
from src.db.customer_repo import create_customer
from src.utils.response import success_response, error_response


def handler(event, context):
    """Create a new customer"""
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        name = body.get('name')
        location = body.get('location')
        phone = body.get('phone')
        
        if not name:
            return error_response(400, 'name is required', 'MISSING_FIELD')
        if not location:
            return error_response(400, 'location is required', 'MISSING_FIELD')
        if not phone:
            return error_response(400, 'phone is required', 'MISSING_FIELD')
        
        email = body.get('email')
        notes = body.get('notes')
        is_active = body.get('isActive', True)
        
        # Create customer
        customer = create_customer(
            name=name,
            location=location,
            phone=phone,
            email=email,
            notes=notes,
            is_active=is_active
        )
        
        return success_response(201, customer)
    
    except json.JSONDecodeError:
        return error_response(400, 'Invalid JSON in request body', 'INVALID_JSON')
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

