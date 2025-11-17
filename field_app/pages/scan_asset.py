"""
QR code scanning page for the Field Mobile App.
Allows foremen to scan asset QR codes and view asset details.
"""
import streamlit as st
from field_app.config import config
from field_app.utils.auth import require_auth
from field_app.utils.api_client import APIClient
from field_app.utils.qr_scanner import QRScanner


# Page configuration
st.set_page_config(
    page_title=f"{config.APP_TITLE} - Scan Asset",
    page_icon=config.APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Require authentication
require_auth()


def show_move_asset_form(asset: dict):
    """Display form to move asset to a different project."""
    st.subheader("📦 Move Asset")
    st.write(f"Moving: **{asset.get('name', 'Unknown')}**")
    
    try:
        client = APIClient()
        
        # Fetch all projects
        projects = client.get("projects")
        
        if not projects:
            st.warning("No projects available. Please create a project first.")
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_move_form = False
                st.rerun()
            return
        
        # Create project selector
        project_options = {p['name']: p['id'] for p in projects}
        selected_project_name = st.selectbox(
            "Select Project",
            options=list(project_options.keys()),
            key="project_selector"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Confirm Move", use_container_width=True, type="primary"):
                try:
                    project_id = project_options[selected_project_name]
                    response = client.post(
                        f"assets/{asset['id']}/move",
                        data={'project_id': project_id}
                    )
                    st.success(f"✅ {response.get('message', 'Asset moved successfully!')}")
                    
                    # Clear state and refresh
                    st.session_state.show_move_form = False
                    st.session_state.scan_complete = False
                    st.session_state.scanned_asset_id = None
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to move asset: {str(e)}")
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_move_form = False
                st.rerun()
    
    except Exception as e:
        st.error(f"Failed to load projects: {str(e)}")


def show_asset_details(asset_id: str):
    """Fetch and display asset details."""
    try:
        client = APIClient()
        asset = client.get(f"assets/{asset_id}")
        
        st.success(f"✅ Asset Found: {asset.get('name', 'Unknown')}")
        
        # Store asset in session state for move functionality
        st.session_state.current_asset = asset
        
        # Check if we should show move form
        if st.session_state.get('show_move_form'):
            show_move_asset_form(asset)
        else:
            # Display asset information
            st.subheader("Asset Details")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ID:** {asset.get('id', 'N/A')}")
                st.write(f"**Name:** {asset.get('name', 'N/A')}")
            with col2:
                st.write(f"**Category:** {asset.get('category', 'N/A')}")
                st.write(f"**Project:** {asset.get('project_name', 'Unassigned')}")
            
            # Show move button
            st.divider()
            if st.button("📦 Move Asset", use_container_width=True, type="primary"):
                st.session_state.show_move_form = True
                st.rerun()
            
            # Show asset history if available
            if 'history' in asset and asset['history']:
                st.divider()
                st.subheader("Movement History")
                for entry in asset['history'][-5:]:  # Show last 5 movements
                    st.write(f"- {entry.get('moved_at', 'N/A')}: Moved to {entry.get('project_name', 'Unknown')}")
        
    except Exception as e:
        st.error(f"Failed to fetch asset details: {str(e)}")
        st.session_state.scanned_asset_id = None
        st.session_state.scan_complete = False


def main():
    """Main page function."""
    st.title("📷 Scan Asset QR Code")
    
    # Back button
    if st.button("⬅️ Back to Home", use_container_width=True):
        # Clear scan state
        if 'scanned_asset_id' in st.session_state:
            del st.session_state.scanned_asset_id
        if 'scan_complete' in st.session_state:
            del st.session_state.scan_complete
        if 'current_asset' in st.session_state:
            del st.session_state.current_asset
        if 'show_move_form' in st.session_state:
            del st.session_state.show_move_form
        st.switch_page("app.py")
    
    st.divider()
    
    # Check if we have a scanned asset
    if st.session_state.get('scan_complete') and st.session_state.get('scanned_asset_id'):
        show_asset_details(st.session_state.scanned_asset_id)
        
        # Button to scan another asset
        st.divider()
        if st.button("🔄 Scan Another Asset", use_container_width=True):
            st.session_state.scanned_asset_id = None
            st.session_state.scan_complete = False
            if 'current_asset' in st.session_state:
                del st.session_state.current_asset
            if 'show_move_form' in st.session_state:
                del st.session_state.show_move_form
            st.rerun()
    else:
        # Show QR scanner
        st.info("📱 Point your camera at an asset QR code")
        
        scanner = QRScanner()
        scanner.start_scanner()
        
        # Instructions
        st.markdown("""
        ### Instructions:
        1. Allow camera access when prompted
        2. Point camera at QR code
        3. Hold steady until code is detected
        4. Asset details will appear automatically
        """)


if __name__ == "__main__":
    main()
