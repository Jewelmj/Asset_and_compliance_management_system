"""
Asset Management page for the Admin Portal.
Allows creating assets, generating QR codes, and viewing all assets.
"""
import streamlit as st
import pandas as pd
from admin_portal.config import config
from admin_portal.utils.auth import require_auth
from admin_portal.utils.api_client import APIClient
from admin_portal.utils.qr_generator import generate_qr_code, qr_code_to_bytes


# Page configuration
st.set_page_config(
    page_title=f"{config.APP_TITLE} - Assets",
    page_icon=config.APP_ICON,
    layout="wide"
)

# Require authentication
require_auth()

# Initialize API client
client = APIClient()


def create_asset_form():
    """Display form to create new asset."""
    st.subheader("📦 Create New Asset")
    
    with st.form("create_asset_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            asset_name = st.text_input("Asset Name*", placeholder="e.g., Excavator #1")
        
        with col2:
            asset_category = st.text_input("Category*", placeholder="e.g., Heavy Equipment")
        
        submit = st.form_submit_button("Create Asset", use_container_width=True)
        
        if submit:
            if asset_name and asset_category:
                try:
                    # Create asset via API
                    response = client.post('assets', data={
                        'name': asset_name,
                        'category': asset_category
                    })
                    
                    asset_id = response.get('id')
                    st.success(f"✅ Asset created successfully! ID: {asset_id}")
                    
                    # Generate and display QR code
                    st.subheader("QR Code Generated")
                    qr_img = generate_qr_code(asset_id)
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(qr_img, caption=f"Asset ID: {asset_id}", width=300)
                    
                    with col2:
                        st.info(f"""
                        **Asset Details:**
                        - **Name:** {asset_name}
                        - **Category:** {asset_category}
                        - **ID:** {asset_id}
                        
                        Download the QR code and attach it to the asset for tracking.
                        """)
                        
                        # Download button
                        qr_bytes = qr_code_to_bytes(qr_img)
                        st.download_button(
                            label="⬇️ Download QR Code",
                            data=qr_bytes,
                            file_name=f"asset_{asset_id}_qr.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    # Trigger refresh of asset list
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Failed to create asset: {str(e)}")
            else:
                st.error("Please fill in all required fields.")


def display_assets_table():
    """Display table of all assets."""
    st.subheader("📋 All Assets")
    
    try:
        # Fetch assets from API
        response = client.get('assets')
        
        if response and len(response) > 0:
            # Convert to DataFrame
            df = pd.DataFrame(response)
            
            # Reorder columns for better display
            columns = ['id', 'name', 'category', 'project_name', 'created_at']
            available_columns = [col for col in columns if col in df.columns]
            df = df[available_columns]
            
            # Rename columns for display
            column_config = {
                'id': 'Asset ID',
                'name': 'Name',
                'category': 'Category',
                'project_name': 'Current Location',
                'created_at': 'Created At'
            }
            
            # Display dataframe
            st.dataframe(
                df,
                column_config=column_config,
                use_container_width=True,
                hide_index=True
            )
            
            st.caption(f"Total Assets: {len(df)}")
        else:
            st.info("No assets found. Create your first asset above!")
    
    except Exception as e:
        st.error(f"❌ Failed to load assets: {str(e)}")


def main():
    """Main page function."""
    st.title("📦 Asset Management")
    
    # Create asset form
    create_asset_form()
    
    st.divider()
    
    # Display assets table
    display_assets_table()


if __name__ == "__main__":
    main()
