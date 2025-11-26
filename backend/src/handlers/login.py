import json
import boto3
from src.auth import generate_token
from src.utils.response import success_response, error_response

# Initialize SSM client
ssm_client = boto3.client('ssm')


def handler(event, context):
    """Login handler - validates password and returns JWT token"""
    # Handle CORS preflight (OPTIONS) requests
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS' or \
       event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Validate required field
        password = body.get('password')
        
        if not password:
            return error_response(400, 'password is required', 'MISSING_FIELD')
        
        # Get password from SSM Parameter Store
        try:
            parameter_name = '/distribution-app/password'
            response = ssm_client.get_parameter(
                Name=parameter_name,
                WithDecryption=True
            )
            stored_password = response['Parameter']['Value']
        except ssm_client.exceptions.ParameterNotFound:
            return error_response(500, 'Password parameter not found in SSM', 'SSM_ERROR')
        except Exception as e:
            return error_response(500, f'Failed to retrieve password from SSM: {str(e)}', 'SSM_ERROR')
        
        # Compare passwords
        if password != stored_password:
            return error_response(401, 'Invalid credentials', 'INVALID_CREDENTIALS')
        
        # Generate JWT token
        token = generate_token("admin")
        
        return success_response(200, {
            "token": token
        })
    
    except json.JSONDecodeError:
        return error_response(400, 'Invalid JSON in request body', 'INVALID_JSON')
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

