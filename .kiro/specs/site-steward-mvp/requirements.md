# Requirements Document

## Introduction

The Site-Steward MVP is a construction site management system designed to validate two core business propositions:
1. Reduce Asset Loss via QR code tracking
2. Mitigate Compliance Risk via document expiry alerts

The system consists of a Flask API backend, two Streamlit frontends (Admin Portal and Field Mobile App), and a PostgreSQL database. The architecture follows a decoupled, service-oriented approach with clear separation of concerns.

## Glossary

- **System**: The Site-Steward MVP application
- **API**: The Flask-based RESTful backend service
- **Admin Portal**: The Streamlit-based desktop application for office administrators
- **Field App**: The Streamlit-based mobile web application for site foremen
- **Asset**: Physical equipment or materials tracked via QR codes
- **Project**: A construction project that contains assets and subcontractors
- **Subcontractor**: A third-party contractor working on projects
- **Compliance Document**: PDF documents (insurance, certifications) with expiry dates
- **JWT**: JSON Web Token used for authentication
- **QR Code**: Quick Response code used to identify assets

## Requirements

### Requirement 1: User Authentication

**User Story:** As a user (Admin or Foreman), I want to securely log in to the system, so that I can access protected features and data.

#### Acceptance Criteria

1. WHEN a user submits valid credentials to the login endpoint, THE System SHALL return a valid JWT token
2. WHEN a user includes a valid JWT token in the Authorization header, THE System SHALL authenticate the request and grant access to protected endpoints
3. WHEN a user submits invalid credentials, THE System SHALL return an authentication error with appropriate HTTP status code
4. WHEN a JWT token expires, THE System SHALL reject requests and return an unauthorized error

### Requirement 2: Asset Management

**User Story:** As an Admin, I want to create and manage assets with QR codes, so that I can track equipment across construction sites.

#### Acceptance Criteria

1. WHEN an Admin creates a new asset via the API, THE System SHALL generate a unique identifier and store the asset in the database
2. WHEN an asset is created, THE System SHALL support generating a QR code containing the asset identifier
3. WHEN a user requests asset details by ID, THE System SHALL return the asset information including name, category, and current location
4. WHEN an asset is moved to a project, THE System SHALL update the asset's location and maintain the relationship
5. WHEN a user requests all assets, THE System SHALL return a list of all assets in the system

### Requirement 3: Project Management

**User Story:** As an Admin, I want to manage projects, so that I can organize assets and track subcontractor compliance per project.

#### Acceptance Criteria

1. WHEN an Admin creates a project, THE System SHALL store the project with a unique identifier
2. WHEN assets are assigned to a project, THE System SHALL maintain the relationship between assets and projects
3. WHEN a user requests project details, THE System SHALL return project information including associated assets
4. WHEN a user requests compliance status for a project, THE System SHALL return the compliance status for all subcontractors on that project

### Requirement 4: Subcontractor Management

**User Story:** As an Admin, I want to manage subcontractors and their compliance documents, so that I can ensure all contractors meet regulatory requirements.

#### Acceptance Criteria

1. WHEN an Admin creates a subcontractor, THE System SHALL store the subcontractor information in the database
2. WHEN an Admin uploads a compliance document for a subcontractor, THE System SHALL store the PDF file and record the expiry date
3. WHEN a compliance document is stored, THE System SHALL save the file path in the database
4. WHEN a user requests all subcontractors, THE System SHALL return a list of all subcontractors
5. WHEN a user requests compliance status, THE System SHALL calculate status based on document expiry dates

### Requirement 5: Compliance Monitoring

**User Story:** As an Admin, I want to receive alerts for expiring compliance documents, so that I can proactively address compliance issues.

#### Acceptance Criteria

1. WHEN the compliance check script runs, THE System SHALL query all compliance documents expiring within 30 days
2. WHEN expiring documents are found, THE System SHALL send email notifications to designated recipients
3. WHEN calculating compliance status, THE System SHALL mark documents as RED if expired or expiring within 30 days
4. WHEN calculating compliance status, THE System SHALL mark documents as GREEN if valid for more than 30 days
5. WHEN the compliance check completes, THE System SHALL log the results

### Requirement 6: Admin Portal Interface

**User Story:** As an Admin, I want a desktop web interface to manage the system, so that I can perform administrative tasks efficiently.

#### Acceptance Criteria

1. WHEN an Admin accesses the portal, THE System SHALL display a login page
2. WHEN an Admin logs in successfully, THE System SHALL store the JWT token in session state
3. WHEN an Admin navigates to Asset Management, THE System SHALL display a form to create new assets and generate QR codes
4. WHEN an Admin navigates to Subcontractor Management, THE System SHALL display a CRUD interface for subcontractors
5. WHEN an Admin navigates to Compliance Upload, THE System SHALL display file upload and date input controls
6. WHEN an Admin navigates to Project Hub, THE System SHALL display project selection and compliance status dashboard

### Requirement 7: Field Mobile App Interface

**User Story:** As a Site Foreman, I want a mobile web app to scan asset QR codes and check compliance, so that I can manage assets in the field.

#### Acceptance Criteria

1. WHEN a Foreman accesses the app, THE System SHALL display a login page
2. WHEN a Foreman logs in successfully, THE System SHALL display two options: Scan Asset and View Project Compliance
3. WHEN a Foreman selects Scan Asset, THE System SHALL activate the device camera for QR code scanning
4. WHEN a QR code is successfully scanned, THE System SHALL retrieve and display the asset details
5. WHEN viewing an asset, THE System SHALL provide a Move button to reassign the asset to a different project
6. WHEN a Foreman selects View Project Compliance, THE System SHALL display a project list
7. WHEN a project is selected, THE System SHALL display the compliance status with RED/GREEN indicators

### Requirement 8: Database Schema

**User Story:** As a developer, I want a well-structured database schema, so that data is organized and relationships are maintained properly.

#### Acceptance Criteria

1. THE System SHALL define a Users table with authentication credentials
2. THE System SHALL define an Assets table with id, name, category, and project relationship
3. THE System SHALL define a Projects table with id, name, and location
4. THE System SHALL define a Subcontractors table with id, name, and contact information
5. THE System SHALL define a ComplianceDocuments table with id, subcontractor relationship, file path, and expiry date
6. THE System SHALL use foreign keys to maintain referential integrity between related tables

### Requirement 9: API Documentation

**User Story:** As a frontend developer, I want automatically generated API documentation, so that I can understand and integrate with the backend endpoints.

#### Acceptance Criteria

1. THE System SHALL use Flask-Smorest to define API endpoints
2. THE System SHALL automatically generate OpenAPI (Swagger) documentation
3. WHEN a developer accesses the API documentation endpoint, THE System SHALL display interactive API documentation
4. THE System SHALL document all request parameters, response schemas, and authentication requirements

### Requirement 10: QR Code Scanning

**User Story:** As a Site Foreman, I want to scan QR codes using my mobile device camera, so that I can quickly access asset information.

#### Acceptance Criteria

1. THE Field App SHALL use streamlit-webrtc component to access device camera
2. THE Field App SHALL use pyzbar library to decode QR codes from video stream
3. WHEN a QR code is detected, THE Field App SHALL extract the asset ID
4. WHEN an asset ID is extracted, THE Field App SHALL call the API to retrieve asset details
5. WHEN the camera fails to initialize, THE Field App SHALL display an appropriate error message
