"""
Project Hub dashboard for the Admin Portal.
Displays project compliance status with color-coded indicators.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from admin_portal.config import config
from admin_portal.utils.auth import require_auth
from admin_portal.utils.api_client import APIClient


# Page configuration
st.set_page_config(
    page_title=f"{config.APP_TITLE} - Project Hub",
    page_icon=config.APP_ICON,
    layout="wide"
)

# Require authentication
require_auth()

# Initialize API client
client = APIClient()


def display_project_selector():
    """Display project selection dropdown and return selected project."""
    try:
        # Fetch projects from API
        projects = client.get('projects')
        
        if not projects or len(projects) == 0:
            st.warning("⚠️ No projects found. Please create projects first.")
            return None
        
        # Create project options
        project_options = {f"{proj['name']} - {proj.get('location', 'N/A')}": proj['id'] 
                          for proj in projects}
        
        # Project selector
        selected_project = st.selectbox(
            "Select Project",
            options=list(project_options.keys()),
            help="Choose a project to view compliance status"
        )
        
        if selected_project:
            return project_options[selected_project]
        
        return None
    
    except Exception as e:
        st.error(f"❌ Failed to load projects: {str(e)}")
        return None


def calculate_status(expiry_date_str: str) -> tuple:
    """
    Calculate compliance status based on expiry date.
    Returns (status_text, status_color, days_remaining)
    """
    try:
        expiry_date = datetime.fromisoformat(expiry_date_str).date()
        days_remaining = (expiry_date - datetime.now().date()).days
        
        if days_remaining <= 0:
            return ("🔴 EXPIRED", "red", days_remaining)
        elif days_remaining <= 30:
            return ("🔴 RED", "red", days_remaining)
        else:
            return ("🟢 GREEN", "green", days_remaining)
    except:
        return ("⚪ UNKNOWN", "gray", 0)


def display_compliance_dashboard(project_id: str):
    """Display compliance status dashboard for selected project."""
    try:
        # Fetch compliance status for project
        response = client.get(f'projects/{project_id}/compliance')
        
        if not response:
            st.info("No compliance data available for this project.")
            return
        
        project_name = response.get('project_name', 'Unknown Project')
        subcontractors = response.get('subcontractors', [])
        
        st.subheader(f"📊 Compliance Status: {project_name}")
        
        if not subcontractors or len(subcontractors) == 0:
            st.info("No subcontractors assigned to this project.")
            return
        
        # Calculate overall statistics
        total_subs = len(subcontractors)
        red_count = sum(1 for sub in subcontractors if sub.get('status') == 'RED')
        green_count = sum(1 for sub in subcontractors if sub.get('status') == 'GREEN')
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Subcontractors", total_subs)
        
        with col2:
            st.metric("🟢 GREEN", green_count)
        
        with col3:
            st.metric("🔴 RED", red_count)
        
        with col4:
            compliance_rate = (green_count / total_subs * 100) if total_subs > 0 else 0
            st.metric("Compliance Rate", f"{compliance_rate:.0f}%")
        
        st.divider()
        
        # Display detailed compliance table
        st.subheader("Detailed Compliance Status")
        
        # Prepare data for table
        table_data = []
        for sub in subcontractors:
            status_text, status_color, days_remaining = calculate_status(sub.get('expiry_date', ''))
            
            table_data.append({
                'Subcontractor': sub.get('name', 'Unknown'),
                'Document Type': sub.get('document_type', 'N/A'),
                'Expiry Date': sub.get('expiry_date', 'N/A'),
                'Days Remaining': days_remaining,
                'Status': status_text
            })
        
        if table_data:
            df = pd.DataFrame(table_data)
            
            # Style the dataframe
            def style_status(val):
                if '🔴' in val:
                    return 'background-color: #ffcccc; color: #cc0000; font-weight: bold'
                elif '🟢' in val:
                    return 'background-color: #ccffcc; color: #006600; font-weight: bold'
                else:
                    return ''
            
            def style_days(val):
                if val <= 0:
                    return 'background-color: #ffcccc; color: #cc0000; font-weight: bold'
                elif val <= 30:
                    return 'background-color: #ffe6cc; color: #cc6600; font-weight: bold'
                else:
                    return 'color: #006600'
            
            # Display styled dataframe
            styled_df = df.style.applymap(style_status, subset=['Status'])
            styled_df = styled_df.applymap(style_days, subset=['Days Remaining'])
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Display warnings for RED status
            red_subs = [item for item in table_data if '🔴' in item['Status']]
            if red_subs:
                st.warning(f"⚠️ **Action Required:** {len(red_subs)} subcontractor(s) have expired or expiring documents!")
                
                with st.expander("View Details"):
                    for item in red_subs:
                        st.write(f"""
                        - **{item['Subcontractor']}**
                          - Document: {item['Document Type']}
                          - Expiry: {item['Expiry Date']}
                          - Days Remaining: {item['Days Remaining']}
                        """)
        
        # Export option
        st.divider()
        if st.button("📥 Export Compliance Report", use_container_width=False):
            # Convert to CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"compliance_report_{project_name}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    except Exception as e:
        st.error(f"❌ Failed to load compliance data: {str(e)}")


def main():
    """Main page function."""
    st.title("🏗️ Project Hub Dashboard")
    
    st.markdown("""
    Monitor compliance status for all subcontractors on your projects. 
    Documents are color-coded based on expiry dates:
    - 🟢 **GREEN**: Valid for more than 30 days
    - 🔴 **RED**: Expired or expiring within 30 days
    """)
    
    st.divider()
    
    # Project selector
    selected_project_id = display_project_selector()
    
    if selected_project_id:
        st.divider()
        # Display compliance dashboard
        display_compliance_dashboard(selected_project_id)


if __name__ == "__main__":
    main()
