import pytest
import json
from src.utils.response import success_response, error_response


class TestResponseUtils:
    """Tests for response utility functions"""
    
    def test_success_response(self):
        """Test creating a successful response"""
        body = {'message': 'Success', 'data': {'id': '123'}}
        response = success_response(200, body)
        
        assert response['statusCode'] == 200
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert response['headers']['Access-Control-Allow-Origin'] == '*'
        
        parsed_body = json.loads(response['body'])
        assert parsed_body['message'] == 'Success'
        assert parsed_body['data']['id'] == '123'
    
    def test_error_response(self):
        """Test creating an error response"""
        response = error_response(400, 'Bad Request', 'INVALID_INPUT')
        
        assert response['statusCode'] == 400
        assert 'Access-Control-Allow-Origin' in response['headers']
        
        parsed_body = json.loads(response['body'])
        assert parsed_body['message'] == 'Bad Request'
        assert parsed_body['code'] == 'INVALID_INPUT'
    
    def test_error_response_without_code(self):
        """Test creating an error response without error code"""
        response = error_response(500, 'Internal Server Error')
        
        assert response['statusCode'] == 500
        parsed_body = json.loads(response['body'])
        assert parsed_body['message'] == 'Internal Server Error'
        assert 'code' not in parsed_body

