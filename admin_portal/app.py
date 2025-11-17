"""
Main Streamlit application for the Admin Portal.
Handles authentication and navigation.
"""
import streamlit as st
from admin_portal.config import config
from admin_portal.utils.auth import is_authenticated, login, logout


# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


def show_login_page():
    """Display login page."""
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.subheader("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                if login(username, password):
                    st.success("Login successful!")
                    st.rerun()
            else:
                st.error("Please enter both username and password.")


def show_navigation():
    """Display navigation sidebar."""
    with st.sidebar:
        st.title(f"{config.APP_ICON} Admin Portal")
        
        # Display user info
        user = st.session_state.get('user', {})
        st.write(f"**User:** {user.get('username', 'Unknown')}")
        st.write(f"**Role:** {user.get('role', 'Unknown')}")
        st.divider()
        
        # Navigation links
        st.page_link("app.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/1_Assets.py", label="📦 Asset Management", icon="📦")
        st.page_link("pages/2_Subcontractors.py", label="👷 Subcontractors", icon="👷")
        st.page_link("pages/3_Compliance.py", label="📄 Compliance Upload", icon="📄")
        st.page_link("pages/4_Project_Hub.py", label="🏗️ Project Hub", icon="🏗️")
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()


def show_home_page():
    """Display home page after login."""
    st.title(f"{config.APP_ICON} Welcome to Site-Steward Admin Portal")
    
    st.markdown("""
    ### Quick Navigation
    
    Use the sidebar to navigate to different sections:
    
    - **📦 Asset Management**: Create and manage assets, generate QR codes
    - **👷 Subcontractors**: Manage subcontractor information
    - **📄 Compliance Upload**: Upload compliance documents
    - **🏗️ Project Hub**: View project compliance status dashboard
    
    ### Getting Started
    
    1. Create assets and generate QR codes for tracking
    2. Add subcontractors to the system
    3. Upload compliance documents with expiry dates
    4. Monitor compliance status in the Project Hub
    """)
    
    # Display some quick stats
    st.subheader("System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Assets", "—", help="Total assets in system")
    
    with col2:
        st.metric("Projects", "—", help="Active projects")
    
    with col3:
        st.metric("Subcontractors", "—", help="Registered subcontractors")
    
    with col4:
        st.metric("Compliance Docs", "—", help="Total compliance documents")


def main():
    """Main application entry point."""
    # Check authentication
    if not is_authenticated():
        show_login_page()
    else:
        show_navigation()
        show_home_page()


if __name__ == "__main__":
    main()
