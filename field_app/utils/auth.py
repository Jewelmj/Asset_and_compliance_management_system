"""
Authentication utilities for the Field Mobile App.
"""
import streamlit as st
from typing import Optional
from field_app.utils.api_client import APIClient, APIError


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return 'token' in st.session_state and st.session_state.token is not None


def get_current_user() -> Optional[dict]:
    """Get current user information from session state."""
    return st.session_state.get('user')


def login(username: str, password: str) -> bool:
    """
    Authenticate user and store JWT token in session state.
    Returns True if login successful, False otherwise.
    """
    try:
        client = APIClient()
        response = client.login(username, password)
        
        # Store token and user info in session state
        st.session_state.token = response.get('token')
        st.session_state.user = {
            'user_id': response.get('user_id'),
            'username': username,
            'role': response.get('role')
        }
        return True
    except APIError as e:
        # Handle API-specific errors with better messaging
        if e.status_code == 401:
            st.error("Invalid username or password")
        else:
            st.error(f"Login failed: {e.message}")
        return False
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return False


def logout():
    """Clear authentication data from session state."""
    if 'token' in st.session_state:
        del st.session_state.token
    if 'user' in st.session_state:
        del st.session_state.user


def require_auth():
    """Decorator/helper to require authentication for a page."""
    if not is_authenticated():
        st.warning("Please log in to access this page.")
        st.stop()
