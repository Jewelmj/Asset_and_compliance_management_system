"""
Compliance Upload page for the Admin Portal.
Allows uploading compliance documents for subcontractors.
"""
import streamlit as st
from datetime import datetime, timedelta
from admin_portal.config import config
from admin_portal.utils.auth import require_auth
from admin_portal.utils.api_client import APIClient


# Page configuration
st.set_page_config(
    page_title=f"{config.APP_TITLE} - Compliance",
    page_icon=config.APP_ICON,
    layout="wide"
)

# Require authentication
require_auth()

# Initialize API client
client = APIClient()


def upload_compliance_form():
    """Display form to upload compliance documents."""
    st.subheader("📄 Upload Compliance Document")
    
    try:
        # Fetch subcontractors for dropdown
        subcontractors = client.get('subcontractors')
        
        if not subcontractors or len(subcontractors) == 0:
            st.warning("⚠️ No subcontractors found. Please add subcontractors first.")
            return
        
        # Create subcontractor options
        subcontractor_options = {f"{sub['name']} (ID: {sub['id']})": sub['id'] 
                                  for sub in subcontractors}
        
        with st.form("upload_compliance_form"):
            # Subcontractor selection
            selected_sub = st.selectbox(
                "Select Subcontractor*",
                options=list(subcontractor_options.keys()),
                help="Choose the subcontractor for this document"
            )
            
            # Document type
            document_type = st.selectbox(
                "Document Type*",
                options=[
                    "General Liability Insurance",
                    "Workers Compensation Insurance",
                    "Professional License",
                    "Safety Certification",
                    "Other"
                ],
                help="Type of compliance document"
            )
            
            # Custom document type if "Other" selected
            custom_doc_type = None
            if document_type == "Other":
                custom_doc_type = st.text_input(
                    "Specify Document Type*",
                    placeholder="e.g., Environmental Permit"
                )
            
            # Expiry date
            col1, col2 = st.columns(2)
            
            with col1:
                expiry_date = st.date_input(
                    "Expiry Date*",
                    value=datetime.now() + timedelta(days=365),
                    min_value=datetime.now(),
                    help="When does this document expire?"
                )
            
            with col2:
                st.write("")  # Spacing
                days_until_expiry = (expiry_date - datetime.now().date()).days
                if days_until_expiry <= 30:
                    st.error(f"⚠️ Expires in {days_until_expiry} days!")
                elif days_until_expiry <= 90:
                    st.warning(f"⚠️ Expires in {days_until_expiry} days")
                else:
                    st.success(f"✅ Valid for {days_until_expiry} days")
            
            # File upload
            uploaded_file = st.file_uploader(
                "Upload PDF Document*",
                type=['pdf'],
                help="Upload the compliance document (PDF only, max 10MB)"
            )
            
            # Submit button
            submit = st.form_submit_button("📤 Upload Document", use_container_width=True)
            
            if submit:
                # Validation
                final_doc_type = custom_doc_type if document_type == "Other" else document_type
                
                if not selected_sub:
                    st.error("Please select a subcontractor.")
                elif not final_doc_type:
                    st.error("Please specify the document type.")
                elif not uploaded_file:
                    st.error("Please upload a PDF document.")
                else:
                    try:
                        # Get subcontractor ID
                        subcontractor_id = subcontractor_options[selected_sub]
                        
                        # Prepare file for upload
                        files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
                        data = {
                            'expiry_date': expiry_date.isoformat(),
                            'document_type': final_doc_type
                        }
                        
                        # Upload via API
                        response = client.post(
                            f'subcontractors/{subcontractor_id}/document',
                            data=data,
                            files=files
                        )
                        
                        st.success(f"✅ Document uploaded successfully!")
                        st.info(f"""
                        **Upload Details:**
                        - **Subcontractor:** {selected_sub}
                        - **Document Type:** {final_doc_type}
                        - **Expiry Date:** {expiry_date.strftime('%Y-%m-%d')}
                        - **File:** {uploaded_file.name}
                        - **Status:** {'🟢 GREEN' if days_until_expiry > 30 else '🔴 RED'}
                        """)
                        
                        # Clear the form
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Upload failed: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Failed to load subcontractors: {str(e)}")


def display_recent_uploads():
    """Display recently uploaded compliance documents."""
    st.subheader("📋 Recent Uploads")
    
    try:
        # Fetch subcontractors with their documents
        subcontractors = client.get('subcontractors')
        
        if subcontractors and len(subcontractors) > 0:
            # Display summary
            total_docs = 0
            for sub in subcontractors:
                if 'documents' in sub and sub['documents']:
                    total_docs += len(sub['documents'])
            
            if total_docs > 0:
                st.info(f"📊 Total compliance documents: {total_docs}")
                
                # Display documents by subcontractor
                for sub in subcontractors:
                    if 'documents' in sub and sub['documents']:
                        with st.expander(f"**{sub['name']}** ({len(sub['documents'])} documents)"):
                            for doc in sub['documents']:
                                expiry = datetime.fromisoformat(doc['expiry_date']).date()
                                days_left = (expiry - datetime.now().date()).days
                                status = "🟢 GREEN" if days_left > 30 else "🔴 RED"
                                
                                st.write(f"""
                                - **Type:** {doc['document_type']}
                                - **Expiry:** {expiry.strftime('%Y-%m-%d')} ({days_left} days)
                                - **Status:** {status}
                                - **Uploaded:** {doc.get('uploaded_at', 'N/A')}
                                """)
                                st.divider()
            else:
                st.info("No compliance documents uploaded yet.")
        else:
            st.info("No subcontractors found.")
    
    except Exception as e:
        st.error(f"❌ Failed to load documents: {str(e)}")


def main():
    """Main page function."""
    st.title("📄 Compliance Document Upload")
    
    st.markdown("""
    Upload compliance documents for subcontractors. Documents expiring within 30 days 
    will be marked as 🔴 RED, while documents valid for more than 30 days will be 🟢 GREEN.
    """)
    
    # Upload form
    upload_compliance_form()
    
    st.divider()
    
    # Recent uploads
    display_recent_uploads()


if __name__ == "__main__":
    main()
