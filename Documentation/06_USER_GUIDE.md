# Site-Steward MVP - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Admin Portal Guide](#admin-portal-guide)
3. [Field Mobile App Guide](#field-mobile-app-guide)
4. [Common Workflows](#common-workflows)
5. [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### Accessing the System

**Admin Portal**: http://localhost:8501 (or your configured domain)
**Field Mobile App**: http://localhost:8502 (or your configured domain)

### User Roles

#### Administrator
- Full system access
- Manage assets, projects, and subcontractors
- Upload compliance documents
- View all dashboards and reports
- Create and manage user accounts

#### Foreman
- Field operations access
- Scan QR codes to view asset details
- Move assets between projects
- View compliance status
- Limited to operational tasks

### Default Credentials

**Admin User**:
- Username: `admin`
- Password: `admin123`

**Foreman User**:
- Username: `foreman`
- Password: `foreman123`

**⚠️ Important**: Change these passwords immediately after first login in production!

---

## Admin Portal Guide

### Logging In

1. Navigate to the Admin Portal URL
2. Enter your username and password
3. Click "Login"
4. You'll be redirected to the home page

### Home Page

The home page provides:
- Quick navigation to all sections
- System overview metrics
- Recent activity summary

### Asset Management

#### Creating a New Asset

1. Click "📦 Asset Management" in the sidebar
2. Fill in the asset details:
   - **Name**: Descriptive name (e.g., "Excavator CAT 320")
   - **Category**: Select from dropdown (Heavy Equipment, Power Equipment, Safety Equipment, etc.)
3. Click "Create Asset"
4. Asset is created and appears in the list

#### Generating QR Codes

1. Go to Asset Management page
2. Find the asset in the list
3. Click "Generate QR Code" button
4. QR code is displayed on screen
5. Click "Download QR Code" to save as PNG file
6. Print and attach to physical asset

#### Viewing Asset Details

1. Select an asset from the list
2. View current location (project assignment)
3. View movement history with timestamps
4. See who moved the asset and when

#### Moving Assets (Admin Portal)

1. Select an asset
2. Choose new project from dropdown
3. Click "Move Asset"
4. Asset location is updated
5. Movement is recorded in history

### Subcontractor Management

#### Adding a New Subcontractor

1. Click "👷 Subcontractors" in the sidebar
2. Click "Add New Subcontractor"
3. Fill in details:
   - **Name**: Company name (required)
   - **Email**: Contact email
   - **Phone**: Contact phone number
4. Click "Create Subcontractor"

#### Editing Subcontractor Information

1. Go to Subcontractors page
2. Select subcontractor from list
3. Click "Edit" button
4. Update information
5. Click "Save Changes"

#### Deleting a Subcontractor

1. Select subcontractor from list
2. Click "Delete" button
3. Confirm deletion
4. **Note**: This will also delete associated compliance documents

### Compliance Document Upload

#### Uploading a Document

1. Click "📄 Compliance Upload" in the sidebar
2. Select subcontractor from dropdown
3. Choose document type:
   - Liability Insurance
   - Workers Compensation Insurance
   - Safety Certification
   - License
   - Bond
   - Other
4. Select PDF file (max 10MB)
5. Set expiry date using date picker
6. Click "Upload Document"
7. Document is uploaded and status is calculated

#### Document Requirements

- **File Format**: PDF only
- **File Size**: Maximum 10MB
- **Expiry Date**: Required for all documents
- **Document Type**: Must be specified

#### Understanding Status Indicators

- **🟢 GREEN**: Document valid for more than 30 days
- **🔴 RED**: Document expired or expiring within 30 days

### Project Hub (Compliance Dashboard)

#### Viewing Project Compliance

1. Click "🏗️ Project Hub" in the sidebar
2. Select a project from dropdown
3. View compliance status for all subcontractors on that project

#### Reading the Dashboard

**Subcontractor Cards**:
- Company name
- Overall status (RED/GREEN)
- List of all compliance documents
- Individual document status
- Expiry dates

**Status Interpretation**:
- **All GREEN**: Subcontractor is fully compliant
- **Any RED**: Immediate action required

#### Taking Action on RED Status

1. Identify which document is RED
2. Contact subcontractor to request updated document
3. Once received, upload new document via Compliance Upload page
4. Status will automatically update to GREEN if valid

### Creating Projects

1. Navigate to Project Hub
2. Click "Create New Project"
3. Fill in details:
   - **Name**: Project name
   - **Location**: Project address
4. Click "Create Project"
5. Project is now available for asset assignment

### Assigning Subcontractors to Projects

1. Go to Project Hub
2. Select project
3. Click "Manage Subcontractors"
4. Select subcontractors to assign
5. Click "Save Assignments"

---

## Field Mobile App Guide

### Logging In (Mobile)

1. Open Field App URL on mobile device
2. Enter username and password
3. Tap "Login"
4. You'll see the main navigation screen

### Main Navigation

Two primary actions:
- **📷 Scan Asset**: Scan QR codes to view and move assets
- **📊 View Compliance**: Check project compliance status

### Scanning Assets

#### Using the QR Scanner

1. Tap "📷 Scan Asset"
2. Allow camera access when prompted
3. Point camera at asset QR code
4. Hold steady until QR code is detected
5. Asset details appear automatically

#### Viewing Asset Information

After scanning, you'll see:
- Asset name and category
- Current project location
- Movement history
- Option to move asset

#### Moving an Asset

1. After scanning asset, tap "📦 Move Asset"
2. Select destination project from dropdown
3. Tap "Confirm Move"
4. Asset is moved and history is updated
5. Success message is displayed

#### QR Scanning Tips

- **Lighting**: Ensure good lighting for best results
- **Distance**: Hold phone 6-12 inches from QR code
- **Stability**: Keep phone steady while scanning
- **Focus**: Ensure QR code is in focus
- **Size**: QR code should fill most of the camera view

### Viewing Compliance Status (Mobile)

1. Tap "📊 View Compliance"
2. Select project from dropdown
3. View compliance status for all subcontractors
4. Scroll through list to see all documents
5. RED indicators show which documents need attention

### Mobile Browser Compatibility

**Recommended Browsers**:
- iOS: Safari 14+
- Android: Chrome 90+

**Camera Access**:
- Must grant camera permissions
- HTTPS required for camera access in production
- Some browsers may not support camera on HTTP

---

## Common Workflows

### Workflow 1: Onboarding a New Asset

1. **Admin**: Create asset in Asset Management
2. **Admin**: Generate and download QR code
3. **Admin**: Print QR code and attach to physical asset
4. **Admin**: Assign asset to initial project
5. **Foreman**: Scan QR code to verify setup
6. **Foreman**: Move asset as needed during operations

### Workflow 2: Onboarding a New Subcontractor

1. **Admin**: Add subcontractor in Subcontractors page
2. **Admin**: Request compliance documents from subcontractor
3. **Admin**: Upload documents via Compliance Upload page
4. **Admin**: Assign subcontractor to relevant projects
5. **Admin**: Verify GREEN status in Project Hub
6. **Admin**: Set calendar reminder for document renewal

### Workflow 3: Daily Asset Tracking

1. **Foreman**: Arrive at job site
2. **Foreman**: Scan assets as they arrive
3. **Foreman**: Move assets to current project
4. **Foreman**: Scan assets as they leave
5. **Foreman**: Move assets to next destination
6. **Admin**: Review movement history at end of day

### Workflow 4: Compliance Monitoring

1. **System**: Daily automated check runs at 8:00 AM
2. **System**: Identifies documents expiring within 30 days
3. **System**: Sends email notification to administrators
4. **Admin**: Reviews email alert
5. **Admin**: Contacts subcontractors with RED status
6. **Admin**: Uploads renewed documents
7. **Admin**: Verifies GREEN status in Project Hub

### Workflow 5: Project Setup

1. **Admin**: Create new project in Project Hub
2. **Admin**: Assign subcontractors to project
3. **Admin**: Verify all subcontractors have GREEN status
4. **Admin**: Assign initial assets to project
5. **Foreman**: Scan assets on arrival at job site
6. **Foreman**: Confirm assets are at correct project

---

## Tips and Best Practices

### Asset Management

✅ **DO**:
- Use descriptive asset names (include model numbers)
- Generate QR codes immediately after creating assets
- Print QR codes on durable, weather-resistant material
- Attach QR codes in visible, accessible locations
- Scan assets regularly to maintain accurate location data

❌ **DON'T**:
- Use generic names like "Tool 1" or "Equipment A"
- Delay QR code generation
- Print QR codes on paper that can fade or tear
- Place QR codes where they can be damaged or obscured

### Compliance Management

✅ **DO**:
- Upload documents as soon as received
- Set calendar reminders for document renewals
- Review Project Hub dashboard weekly
- Act immediately on RED status indicators
- Keep digital copies of all documents
- Verify document expiry dates before uploading

❌ **DON'T**:
- Wait until documents expire to request renewals
- Ignore RED status indicators
- Upload expired documents
- Forget to update documents after renewal
- Rely solely on automated alerts

### QR Code Scanning

✅ **DO**:
- Ensure good lighting when scanning
- Hold phone steady
- Keep QR codes clean and undamaged
- Use HTTPS in production for camera access
- Test QR codes after printing

❌ **DON'T**:
- Scan in poor lighting conditions
- Move phone while scanning
- Allow QR codes to become dirty or damaged
- Use HTTP in production (camera won't work)

### Security

✅ **DO**:
- Change default passwords immediately
- Use strong, unique passwords
- Log out when finished
- Keep credentials confidential
- Review user access regularly

❌ **DON'T**:
- Share login credentials
- Use simple passwords
- Leave sessions logged in
- Write passwords down
- Give unnecessary access to users

### Data Management

✅ **DO**:
- Review asset locations regularly
- Archive old projects when complete
- Back up database regularly
- Clean up unused assets
- Maintain accurate subcontractor information

❌ **DON'T**:
- Let asset locations become outdated
- Keep unnecessary data indefinitely
- Forget to back up
- Create duplicate assets
- Leave subcontractor information outdated

---

## Keyboard Shortcuts

### Admin Portal

- `Ctrl + /`: Focus search (if available)
- `Esc`: Close modals/dialogs
- `Tab`: Navigate between form fields
- `Enter`: Submit forms

### Field Mobile App

- Touch-optimized interface
- No keyboard shortcuts (mobile-first design)

---

## Accessibility Features

- High contrast mode support
- Screen reader compatible
- Keyboard navigation support
- Large touch targets for mobile
- Clear visual indicators

---

## Getting Help

### In-App Help

- Hover over ℹ️ icons for tooltips
- Check status messages for guidance
- Review error messages for troubleshooting

### Documentation

- [System Overview](01_SYSTEM_OVERVIEW.md)
- [API Reference](03_API_REFERENCE.md)
- [Troubleshooting Guide](09_TROUBLESHOOTING.md)

### Support Contacts

- Technical Support: support@yourdomain.com
- Administrator: admin@yourdomain.com

---

## Frequently Asked Questions

**Q: Can I scan multiple assets at once?**
A: No, scan one asset at a time for accurate tracking.

**Q: What happens if I lose internet connection while scanning?**
A: The scan will fail. Ensure stable internet connection for field operations.

**Q: Can I upload documents other than PDF?**
A: No, only PDF format is supported for compliance documents.

**Q: How long are JWT tokens valid?**
A: Tokens expire after 24 hours. You'll need to log in again.

**Q: Can I delete an asset?**
A: Currently not implemented. Contact administrator for asset removal.

**Q: What if a QR code is damaged?**
A: Generate a new QR code from the Admin Portal and replace the damaged one.

**Q: Can I view compliance status offline?**
A: No, internet connection is required to access current compliance data.

**Q: How do I change my password?**
A: Contact your administrator to reset your password.

---

## Related Documentation
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [Deployment Guide](05_DEPLOYMENT_GUIDE.md)
- [Troubleshooting](09_TROUBLESHOOTING.md)
