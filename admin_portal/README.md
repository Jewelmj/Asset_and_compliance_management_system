# Admin Portal - Site-Steward MVP

The Admin Portal is a Streamlit-based web application for managing the Site-Steward system.

## Features

- **Authentication**: Secure login with JWT tokens
- **Asset Management**: Create assets and generate QR codes
- **Subcontractor Management**: Add, edit, and delete subcontractors
- **Compliance Upload**: Upload compliance documents with expiry dates
- **Project Hub**: Monitor compliance status with color-coded dashboard

## Running the Application

### Prerequisites

1. Ensure the Flask API is running on `http://localhost:5000`
2. Install dependencies: `pip install -r requirements.txt`

### Start the Admin Portal

```bash
streamlit run admin_portal/app.py
```

The application will open in your browser at `http://localhost:8501`

## Configuration

Set the following environment variables in `.env`:

```
API_URL=http://localhost:5000
SESSION_TIMEOUT_MINUTES=1440
QR_CODE_SIZE=10
QR_CODE_BORDER=4
```

## Pages

1. **Home** - Dashboard with quick navigation
2. **Asset Management** - Create assets and generate QR codes
3. **Subcontractors** - Manage subcontractor information
4. **Compliance Upload** - Upload compliance documents
5. **Project Hub** - View compliance status dashboard

## Usage

1. Log in with your credentials
2. Navigate using the sidebar menu
3. Create assets and generate QR codes for tracking
4. Add subcontractors to the system
5. Upload compliance documents with expiry dates
6. Monitor compliance status in the Project Hub

## Status Indicators

- 🟢 **GREEN**: Document valid for more than 30 days
- 🔴 **RED**: Document expired or expiring within 30 days
