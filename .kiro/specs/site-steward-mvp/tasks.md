# Implementation Plan

- [x] 1. Set up project infrastructure and dependencies





  - Update requirements.txt with all necessary packages (Flask-Smorest, Flask-JWT-Extended, bcrypt, qrcode, streamlit, streamlit-webrtc, pyzbar)
  - Create configuration management system for environment variables
  - Set up database connection and session management
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [x] 2. Implement database models and schema





  - Create User model with authentication fields
  - Create Project model with relationships
  - Create Subcontractor model
  - Create ComplianceDocument model with file path and expiry date
  - Create ProjectSubcontractor junction table model
  - Create AssetHistory model for tracking movements
  - Update existing Asset model to include project relationship
  - Create database initialization script with migrations
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [x] 3. Implement authentication system






- [x] 3.1 Create authentication endpoints

  - Implement POST /api/login endpoint with JWT generation
  - Implement password hashing using bcrypt
  - Create JWT token generation with user_id and role claims
  - _Requirements: 1.1, 1.2, 1.3, 1.4_


- [x] 3.2 Create authentication middleware

  - Implement JWT validation middleware for protected routes
  - Add token expiration checking
  - Add role-based authorization helpers
  - _Requirements: 1.2, 1.4_

- [x] 4. Implement asset management API





- [x] 4.1 Create asset endpoints


  - Implement GET /api/assets endpoint to list all assets
  - Implement POST /api/assets endpoint to create new assets
  - Implement GET /api/assets/<asset_id> endpoint for asset details
  - Implement POST /api/assets/<asset_id>/move endpoint to move assets
  - _Requirements: 2.1, 2.3, 2.4, 2.5_

- [x] 4.2 Add asset history tracking


  - Create service to record asset movements in asset_history table
  - Include user_id and timestamp in history records
  - _Requirements: 2.4_

- [x] 5. Implement project management API





- [x] 5.1 Create project endpoints


  - Implement GET /api/projects endpoint to list all projects
  - Implement POST /api/projects endpoint to create new projects
  - Implement GET /api/projects/<project_id>/compliance endpoint
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 5.2 Implement compliance status calculation


  - Create service to calculate RED/GREEN status based on expiry dates
  - Mark documents as RED if expired or expiring within 30 days
  - Mark documents as GREEN if valid for more than 30 days
  - _Requirements: 5.3, 5.4_

- [x] 6. Implement subcontractor management API




- [x] 6.1 Create subcontractor endpoints


  - Implement GET /api/subcontractors endpoint to list all subcontractors
  - Implement POST /api/subcontractors endpoint to create new subcontractors
  - Implement POST /api/subcontractors/<sub_id>/document endpoint for file uploads
  - _Requirements: 4.1, 4.4, 4.2_

- [x] 6.2 Implement file upload handling


  - Create uploads/compliance/ directory structure
  - Implement file validation (PDF only, size limits)
  - Implement file naming convention with timestamp
  - Store file path in database
  - _Requirements: 4.2, 4.3_

- [x] 7. Create compliance check script





- [x] 7.1 Implement expiry checking logic


  - Create check_expiry.py script with database connection
  - Query compliance documents expiring within 30 days
  - _Requirements: 5.1, 5.2_


- [x] 7.2 Implement email notification system

  - Configure SMTP connection using environment variables
  - Create email template for expiry notifications
  - Send emails for each expiring document
  - Log notification results
  - _Requirements: 5.2, 5.5_

- [x] 8. Build Admin Portal (Streamlit)





- [x] 8.1 Create authentication and navigation


  - Implement login page with username/password inputs
  - Store JWT token in st.session_state on successful login
  - Create navigation sidebar with page links
  - Add logout functionality
  - _Requirements: 6.1, 6.2_

- [x] 8.2 Create Asset Management page


  - Build form to create new assets (name, category inputs)
  - Call POST /api/assets endpoint on form submission
  - Generate QR code using qrcode library
  - Display QR code image with download button
  - Show table of all assets with current locations
  - _Requirements: 6.3, 2.2_

- [x] 8.3 Create Subcontractor Management page



  - Build form to add new subcontractors
  - Display table of existing subcontractors
  - Add inline edit/delete functionality
  - _Requirements: 6.4_

- [x] 8.4 Create Compliance Upload page


  - Add dropdown to select subcontractor
  - Add file uploader for PDF documents
  - Add date picker for expiry date
  - Add document type selector
  - Implement upload button with API call
  - _Requirements: 6.5_

- [x] 8.5 Create Project Hub dashboard


  - Add dropdown to select project
  - Display compliance status table with color coding
  - Show 🟢 GREEN / 🔴 RED status indicators
  - Display expiry dates for each document
  - _Requirements: 6.6_

- [x] 9. Build Field Mobile App (Streamlit)





- [x] 9.1 Create authentication and main navigation


  - Implement login page
  - Store JWT token in session state
  - Create main page with two buttons: "Scan Asset" and "View Project Compliance"
  - _Requirements: 7.1, 7.2_

- [x] 9.2 Implement QR scanning functionality


  - Integrate streamlit-webrtc component for camera access
  - Implement pyzbar QR code detection in video callback
  - Extract asset ID from decoded QR code
  - Call GET /api/assets/<asset_id> on successful scan
  - Display asset details
  - _Requirements: 7.3, 7.4, 10.1, 10.2, 10.3, 10.4_

- [x] 9.3 Implement asset movement feature


  - Add "Move Asset" button on asset details page
  - Show project selector dropdown
  - Call POST /api/assets/<asset_id>/move endpoint
  - Display success/error message
  - _Requirements: 7.5_

- [x] 9.4 Create compliance viewer


  - Display project list on compliance page
  - Call GET /api/projects/<project_id>/compliance on selection
  - Display RED/GREEN status indicators
  - Optimize for mobile viewing
  - _Requirements: 7.6, 7.7_

- [x] 10. Create API client utilities




  - Create shared API client module for Streamlit apps
  - Implement request wrapper with JWT header injection
  - Add error handling for network failures
  - Add response parsing and validation
  - _Requirements: 6.2, 7.1_

- [x] 11. Set up Docker deployment






- [x] 11.1 Create Dockerfiles

  - Create Dockerfile for Flask API
  - Create Dockerfile for Admin Portal
  - Create Dockerfile for Field App
  - _Requirements: 9.1_


- [x] 11.2 Create Docker Compose configuration

  - Define PostgreSQL service with volume
  - Define API service with database dependency
  - Define Admin Portal service
  - Define Field App service
  - Configure environment variables
  - _Requirements: 9.1, 9.2_

- [x] 12. Create database initialization and seed data





  - Create database initialization script
  - Add seed data for testing (sample users, projects, assets)
  - Create admin user with default credentials
  - _Requirements: 8.1_

- [ ] 13. Add error handling and validation
  - Implement API error response formatting
  - Add input validation for all endpoints
  - Add Streamlit error display helpers
  - Handle authentication errors with redirect to login
  - _Requirements: 1.3, 1.4_

- [ ] 14. Create configuration management
  - Create config.py for API with environment variable loading
  - Create config.py for Admin Portal
  - Create config.py for Field App
  - Document required environment variables
  - _Requirements: 9.1, 9.2_

- [ ] 15. Add API documentation
  - Configure Flask-Smorest for OpenAPI generation
  - Add endpoint descriptions and schemas
  - Create API documentation endpoint
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ]* 16. Create README and documentation
  - Write README with setup instructions
  - Document API endpoints
  - Document environment variables
  - Add troubleshooting guide
  - _Requirements: 9.1, 9.2_
