"""
Compliance viewer page for the Field Mobile App.
Allows foremen to view project compliance status.
"""
import streamlit as st
from datetime import datetime
from field_app.config import config
from field_app.utils.auth import require_auth
from field_app.utils.api_client import APIClient


# Page configuration - optimized for mobile
st.set_page_config(
    page_title=f"{config.APP_TITLE} - Compliance",
    page_icon=config.APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Require authentication
require_auth()


def get_status_indicator(status: str) -> str:
    """Get emoji indicator for compliance status."""
    if status == 'GREEN':
        return '🟢'
    elif status == 'RED':
        return '🔴'
    else:
        return '⚪'


def format_date(date_str: str) -> str:
    """Format date string for display."""
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime('%Y-%m-%d')
    except:
        return date_str


def show_compliance_status(project_id: str, project_name: str):
    """Fetch and display compliance status for a project."""
    try:
        client = APIClient()
        compliance_data = client.get(f"projects/{project_id}/compliance")
        
        st.subheader(f"📊 {project_name}")
        st.divider()
        
        subcontractors = compliance_data.get('subcontractors', [])
        
        if not subcontractors:
            st.info("No subcontractors assigned to this project.")
            return
        
        # Display compliance status for each subcontractor
        for sub in subcontractors:
            status = sub.get('status', 'UNKNOWN')
            indicator = get_status_indicator(status)
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**{sub.get('name', 'Unknown')}**")
                    
                    # Show document type if available
                    if 'document_type' in sub:
                        st.caption(f"Document: {sub.get('document_type', 'N/A')}")
                    
                    # Show expiry date
                    expiry_date = sub.get('expiry_date')
                    if expiry_date:
                        formatted_date = format_date(expiry_date)
                        st.caption(f"Expires: {formatted_date}")
                    else:
                        st.caption("No expiry date")
                
                with col2:
                    st.markdown(f"<h1 style='text-align: center; margin: 0;'>{indicator}</h1>", unsafe_allow_html=True)
                    st.caption(f"<div style='text-align: center;'>{status}</div>", unsafe_allow_html=True)
                
                st.divider()
        
        # Summary
        green_count = sum(1 for s in subcontractors if s.get('status') == 'GREEN')
        red_count = sum(1 for s in subcontractors if s.get('status') == 'RED')
        
        st.subheader("Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🟢 Compliant", green_count)
        with col2:
            st.metric("🔴 Non-Compliant", red_count)
        
    except Exception as e:
        st.error(f"Failed to fetch compliance data: {str(e)}")


def main():
    """Main page function."""
    st.title("📊 Project Compliance")
    
    # Back button
    if st.button("⬅️ Back to Home", use_container_width=True):
        # Clear state
        if 'selected_project_id' in st.session_state:
            del st.session_state.selected_project_id
        st.switch_page("app.py")
    
    st.divider()
    
    try:
        client = APIClient()
        
        # Fetch all projects
        projects = client.get("projects")
        
        if not projects:
            st.warning("No projects available.")
            return
        
        # Create project selector
        project_options = {p['name']: p['id'] for p in projects}
        
        selected_project_name = st.selectbox(
            "Select Project",
            options=list(project_options.keys()),
            key="project_selector"
        )
        
        if selected_project_name:
            project_id = project_options[selected_project_name]
            
            # Show compliance status
            st.divider()
            show_compliance_status(project_id, selected_project_name)
    
    except Exception as e:
        st.error(f"Failed to load projects: {str(e)}")


if __name__ == "__main__":
    main()
