# Site-Steward Field Mobile App

Mobile-optimized Streamlit application for site foremen to scan asset QR codes and view project compliance status.

## Features

- **Authentication**: Secure login with JWT tokens
- **QR Code Scanning**: Use device camera to scan asset QR codes
- **Asset Details**: View asset information and movement history
- **Asset Movement**: Move assets between projects
- **Compliance Viewer**: Check project compliance status on the go

## Running the App

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export API_URL=http://localhost:5000

# Run the app
streamlit run field_app/app.py --server.port 8502
```

### Docker

```bash
docker-compose up field_app
```

The app will be available at `http://localhost:8502`

## Usage

### Login
1. Open the app in your mobile browser
2. Enter your username and password
3. Click "Login"

### Scan Asset
1. Click "📷 Scan Asset" on the home page
2. Allow camera access when prompted
3. Point camera at asset QR code
4. Asset details will appear automatically
5. Click "📦 Move Asset" to reassign to a different project

### View Compliance
1. Click "📊 View Compliance" on the home page
2. Select a project from the dropdown
3. View compliance status with RED/GREEN indicators
4. Check expiry dates for each subcontractor

## Mobile Optimization

The app is optimized for mobile devices with:
- Centered layout for better mobile viewing
- Large touch targets for buttons
- Collapsed sidebar by default
- Responsive design
- Minimal UI elements

## Camera Permissions

For QR scanning to work, you need to:
1. Use HTTPS in production (required for camera access)
2. Grant camera permissions when prompted
3. Ensure good lighting for QR code detection

## Troubleshooting

### Camera Not Working
- Check browser permissions for camera access
- Use HTTPS (required by most browsers)
- Try a different browser (Chrome/Safari recommended)
- Ensure QR code is well-lit and in focus

### API Connection Issues
- Verify API_URL environment variable is set correctly
- Check that the Flask API is running
- Ensure network connectivity

### Login Issues
- Verify credentials are correct
- Check that the API is accessible
- Clear browser cache and try again
