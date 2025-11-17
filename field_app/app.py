"""
Main Streamlit application for the Field Mobile App.
Handles authentication and main navigation.
"""
import streamlit as st
from field_app.config import config
from field_app.utils.auth import is_authenticated, login, logout


# Page configuration - optimized for mobile
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)


def show_login_page():
    """Display login page."""
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.subheader("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if username and password:
                if login(username, password):
                    st.success("Login successful!")
                    st.rerun()
            else:
                st.error("Please enter both username and password.")


def show_main_navigation():
    """Display main navigation page with two buttons."""
    st.title(f"{config.APP_ICON} Site-Steward Field App")
    
    # Display user info
    user = st.session_state.get('user', {})
    st.write(f"**Welcome, {user.get('username', 'User')}!**")
    st.divider()
    
    # Main action buttons - large touch targets for mobile
    st.subheader("What would you like to do?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📷 Scan Asset", use_container_width=True, type="primary"):
            st.switch_page("pages/scan_asset.py")
    
    with col2:
        if st.button("📊 View Compliance", use_container_width=True):
            st.switch_page("pages/view_compliance.py")
    
    st.divider()
    
    # Logout button at bottom
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()


def main():
    """Main application entry point."""
    # Check authentication
    if not is_authenticated():
        show_login_page()
    else:
        show_main_navigation()


if __name__ == "__main__":
    main()
