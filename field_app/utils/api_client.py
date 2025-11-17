"""
API client utilities for communicating with the Flask backend.
Provides request wrapper with JWT header injection, error handling, and response validation.
"""
import requests
from typing import Optional, Dict, Any, Union
import streamlit as st
from field_app.config import config
import logging

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class APIClient:
    """Client for making authenticated API requests with error handling and response validation."""
    
    def __init__(self, token: Optional[str] = None, timeout: int = 30):
        """
        Initialize API client with optional JWT token.
        
        Args:
            token: JWT token for authentication
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = config.API_BASE_URL
        self.token = token or st.session_state.get('token')
        self.timeout = timeout
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with JWT token if available."""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response with validation and error handling.
        
        Args:
            response: requests Response object
            
        Returns:
            Parsed JSON response data
            
        Raises:
            APIError: If response indicates an error
        """
        try:
            # Try to parse JSON response
            data = response.json()
        except ValueError:
            # Response is not JSON
            if response.ok:
                return {'success': True, 'message': 'Operation completed successfully'}
            else:
                raise APIError(
                    f"Invalid response from server (status {response.status_code})",
                    status_code=response.status_code
                )
        
        # Check for HTTP errors
        if not response.ok:
            error_message = data.get('message', data.get('error', 'Unknown error'))
            raise APIError(
                error_message,
                status_code=response.status_code,
                response_data=data
            )
        
        return data
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request with error handling for network failures.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            files: Files for multipart upload
            
        Returns:
            Parsed response data
            
        Raises:
            APIError: If request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        # Remove Content-Type for file uploads
        if files:
            headers.pop('Content-Type', None)
        
        try:
            logger.debug(f"Making {method} request to {url}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data if not files else None,
                data=data if files else None,
                params=params,
                files=files,
                timeout=self.timeout
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {url}")
            raise APIError("Request timed out. Please check your connection and try again.")
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for {url}")
            raise APIError("Unable to connect to server. Please check your network connection.")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            raise APIError(f"Request failed: {str(e)}")
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and return JWT token.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Dict containing token, user_id, and role
            
        Raises:
            APIError: If authentication fails
        """
        return self._make_request('POST', 'login', data={'username': username, 'password': password})
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Union[Dict[str, Any], list]:
        """
        Make GET request to API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response data (dict or list)
            
        Raises:
            APIError: If request fails
        """
        return self._make_request('GET', endpoint, params=params)
    
    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make POST request to API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            files: Files for multipart upload
            
        Returns:
            Response data
            
        Raises:
            APIError: If request fails
        """
        return self._make_request('POST', endpoint, data=data, files=files)
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make PUT request to API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response data
            
        Raises:
            APIError: If request fails
        """
        return self._make_request('PUT', endpoint, data=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Make DELETE request to API.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Response data
            
        Raises:
            APIError: If request fails
        """
        return self._make_request('DELETE', endpoint)
    
    def validate_token(self) -> bool:
        """
        Validate current JWT token by making a test request.
        
        Returns:
            True if token is valid, False otherwise
        """
        if not self.token:
            return False
        
        try:
            # Try to fetch assets as a token validation check
            self.get('assets')
            return True
        except APIError as e:
            if e.status_code == 401:
                logger.warning("Token validation failed: unauthorized")
                return False
            # Other errors don't necessarily mean invalid token
            return True
        except Exception:
            return False
