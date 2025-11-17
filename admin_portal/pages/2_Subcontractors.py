"""
Subcontractor Management page for the Admin Portal.
Allows creating, viewing, editing, and deleting subcontractors.
"""
import streamlit as st
import pandas as pd
from admin_portal.config import config
from admin_portal.utils.auth import require_auth
from admin_portal.utils.api_client import APIClient


# Page configuration
st.set_page_config(
    page_title=f"{config.APP_TITLE} - Subcontractors",
    page_icon=config.APP_ICON,
    layout="wide"
)

# Require authentication
require_auth()

# Initialize API client
client = APIClient()


def create_subcontractor_form():
    """Display form to create new subcontractor."""
    st.subheader("👷 Add New Subcontractor")
    
    with st.form("create_subcontractor_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Company Name*", placeholder="e.g., ABC Construction")
        
        with col2:
            email = st.text_input("Email", placeholder="contact@example.com")
        
        with col3:
            phone = st.text_input("Phone", placeholder="+1 (555) 123-4567")
        
        submit = st.form_submit_button("Add Subcontractor", use_container_width=True)
        
        if submit:
            if name:
                try:
                    # Create subcontractor via API
                    response = client.post('subcontractors', data={
                        'name': name,
                        'email': email,
                        'phone': phone
                    })
                    
                    st.success(f"✅ Subcontractor '{name}' added successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Failed to add subcontractor: {str(e)}")
            else:
                st.error("Please enter a company name.")


def display_subcontractors_table():
    """Display table of all subcontractors with edit/delete functionality."""
    st.subheader("📋 All Subcontractors")
    
    try:
        # Fetch subcontractors from API
        response = client.get('subcontractors')
        
        if response and len(response) > 0:
            # Convert to DataFrame
            df = pd.DataFrame(response)
            
            # Display each subcontractor with edit/delete options
            for idx, row in df.iterrows():
                with st.expander(f"**{row['name']}** (ID: {row['id']})", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        # Display subcontractor details
                        st.write(f"**Email:** {row.get('email', 'N/A')}")
                        st.write(f"**Phone:** {row.get('phone', 'N/A')}")
                        st.write(f"**Created:** {row.get('created_at', 'N/A')}")
                    
                    with col2:
                        # Edit button
                        if st.button("✏️ Edit", key=f"edit_{row['id']}", use_container_width=True):
                            st.session_state[f"editing_{row['id']}"] = True
                            st.rerun()
                        
                        # Delete button
                        if st.button("🗑️ Delete", key=f"delete_{row['id']}", use_container_width=True, type="secondary"):
                            st.session_state[f"confirm_delete_{row['id']}"] = True
                            st.rerun()
                    
                    # Edit form (shown when edit button clicked)
                    if st.session_state.get(f"editing_{row['id']}", False):
                        st.divider()
                        st.write("**Edit Subcontractor**")
                        
                        with st.form(f"edit_form_{row['id']}"):
                            new_name = st.text_input("Company Name", value=row['name'])
                            new_email = st.text_input("Email", value=row.get('email', ''))
                            new_phone = st.text_input("Phone", value=row.get('phone', ''))
                            
                            col_save, col_cancel = st.columns(2)
                            
                            with col_save:
                                save = st.form_submit_button("💾 Save", use_container_width=True)
                            
                            with col_cancel:
                                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                            
                            if save:
                                try:
                                    client.put(f"subcontractors/{row['id']}", data={
                                        'name': new_name,
                                        'email': new_email,
                                        'phone': new_phone
                                    })
                                    st.success("✅ Subcontractor updated!")
                                    del st.session_state[f"editing_{row['id']}"]
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Update failed: {str(e)}")
                            
                            if cancel:
                                del st.session_state[f"editing_{row['id']}"]
                                st.rerun()
                    
                    # Delete confirmation (shown when delete button clicked)
                    if st.session_state.get(f"confirm_delete_{row['id']}", False):
                        st.divider()
                        st.warning(f"⚠️ Are you sure you want to delete **{row['name']}**?")
                        
                        col_confirm, col_cancel = st.columns(2)
                        
                        with col_confirm:
                            if st.button("✅ Confirm Delete", key=f"confirm_{row['id']}", use_container_width=True, type="primary"):
                                try:
                                    client.delete(f"subcontractors/{row['id']}")
                                    st.success(f"✅ Deleted {row['name']}")
                                    del st.session_state[f"confirm_delete_{row['id']}"]
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Delete failed: {str(e)}")
                        
                        with col_cancel:
                            if st.button("❌ Cancel", key=f"cancel_delete_{row['id']}", use_container_width=True):
                                del st.session_state[f"confirm_delete_{row['id']}"]
                                st.rerun()
            
            st.caption(f"Total Subcontractors: {len(df)}")
        else:
            st.info("No subcontractors found. Add your first subcontractor above!")
    
    except Exception as e:
        st.error(f"❌ Failed to load subcontractors: {str(e)}")


def main():
    """Main page function."""
    st.title("👷 Subcontractor Management")
    
    # Create subcontractor form
    create_subcontractor_form()
    
    st.divider()
    
    # Display subcontractors table
    display_subcontractors_table()


if __name__ == "__main__":
    main()
