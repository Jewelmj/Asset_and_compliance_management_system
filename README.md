# Asset & Jobsite Management System (OOP-Based)

This project is an Object-Oriented asset and jobsite management system designed for a system design course.  
It models users, assets, documents, and jobsites, and supports features such as QR-based asset tracking, assignment, and document validation.

## Features

### **Users**
The system supports three user roles:
- **Admin** – full control over users, assets, jobsites, and documents  
- **Manager** – manages jobsites, people, and asset assignments  
- **Worker** – scans QR codes and interacts with assigned assets  

### **Assets**
- Each asset has a unique ID, category, name, and photo reference  
- Can be assigned to users, jobsites, or vehicles  
- Can be moved through QR scanning  

### **Documents**
- Stores document metadata and verification status  
- System will perform daily checks for integrity and expiry  

### **Jobsites**
- Contains a list of assigned users and assets  
- Allows checking who/what is currently allocated to a site  

### **QR-Code System**
- Assets have generated QR codes  
- Users can scan QR codes to check in/out assets  
- Supports real-time movement between jobsites or vehicles  


## Usage

```bash
python main.py
```