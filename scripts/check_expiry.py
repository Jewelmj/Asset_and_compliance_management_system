#!/usr/bin/env python3
"""
Compliance Document Expiry Check Script

This script checks for compliance documents that are expired or expiring within 30 days
and sends email notifications to designated recipients.

Requirements: 5.1, 5.2, 5.5
"""
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import and_
from database.db import SessionLocal
from database.models import ComplianceDocumentORM, SubcontractorORM, ProjectORM
from api.config import get_config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_expiring_documents(db_session):
    """
    Query compliance documents expiring within 30 days.
    
    Requirements: 5.1
    
    Args:
        db_session: SQLAlchemy database session
        
    Returns:
        List of ComplianceDocumentORM objects that are expired or expiring within 30 days
    """
    today = datetime.now().date()
    thirty_days_from_now = today + timedelta(days=30)
    
    # Query documents where expiry_date is between today and 30 days from now
    # This includes both expired documents (expiry_date < today) and expiring documents
    expiring_docs = db_session.query(ComplianceDocumentORM).filter(
        ComplianceDocumentORM.expiry_date <= thirty_days_from_now
    ).all()
    
    return expiring_docs


def get_document_status(expiry_date):
    """
    Determine if a document is expired or expiring soon.
    
    Requirements: 5.3, 5.4
    
    Args:
        expiry_date: Date object representing document expiry
        
    Returns:
        Tuple of (status_color, status_text, days_until_expiry)
    """
    today = datetime.now().date()
    days_until_expiry = (expiry_date - today).days
    
    if days_until_expiry < 0:
        return "RED", "EXPIRED", days_until_expiry
    elif days_until_expiry <= 30:
        return "RED", "EXPIRING SOON", days_until_expiry
    else:
        return "GREEN", "VALID", days_until_expiry


def format_email_body(expiring_docs):
    """
    Create HTML email body with expiring document details.
    
    Requirements: 5.2
    
    Args:
        expiring_docs: List of tuples (document, subcontractor, projects)
        
    Returns:
        HTML string for email body
    """
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            h2 { color: #d32f2f; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th { background-color: #f5f5f5; padding: 12px; text-align: left; border: 1px solid #ddd; }
            td { padding: 10px; border: 1px solid #ddd; }
            .expired { color: #d32f2f; font-weight: bold; }
            .expiring { color: #f57c00; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>⚠️ Compliance Document Expiry Alert</h2>
        <p>The following compliance documents are expired or expiring within 30 days:</p>
        <table>
            <thead>
                <tr>
                    <th>Subcontractor</th>
                    <th>Document Type</th>
                    <th>Expiry Date</th>
                    <th>Status</th>
                    <th>Days Until Expiry</th>
                    <th>Projects</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for doc, subcontractor, projects in expiring_docs:
        status_color, status_text, days_until = get_document_status(doc.expiry_date)
        
        # Format status with appropriate CSS class
        status_class = "expired" if days_until < 0 else "expiring"
        status_display = f'<span class="{status_class}">{status_text}</span>'
        
        # Format days until expiry
        if days_until < 0:
            days_display = f"{abs(days_until)} days overdue"
        else:
            days_display = f"{days_until} days"
        
        # Format project names
        project_names = ", ".join([p.name for p in projects]) if projects else "No projects assigned"
        
        html += f"""
                <tr>
                    <td>{subcontractor.name}</td>
                    <td>{doc.document_type}</td>
                    <td>{doc.expiry_date.strftime('%Y-%m-%d')}</td>
                    <td>{status_display}</td>
                    <td>{days_display}</td>
                    <td>{project_names}</td>
                </tr>
        """
    
    html += """
            </tbody>
        </table>
        <p style="margin-top: 20px;">
            <strong>Action Required:</strong> Please update or renew these compliance documents immediately.
        </p>
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            This is an automated notification from Site-Steward Compliance Monitoring System.
        </p>
    </body>
    </html>
    """
    
    return html


def send_email_notification(config, expiring_docs_with_details):
    """
    Send email notification for expiring documents.
    
    Requirements: 5.2, 5.5
    
    Args:
        config: Configuration object with SMTP settings
        expiring_docs_with_details: List of tuples (document, subcontractor, projects)
        
    Returns:
        Boolean indicating success or failure
    """
    if not config.SMTP_USER or not config.SMTP_PASSWORD:
        print("ERROR: SMTP credentials not configured. Skipping email notification.")
        return False
    
    if not config.ALERT_EMAIL_RECIPIENTS or config.ALERT_EMAIL_RECIPIENTS == ['']:
        print("ERROR: No email recipients configured. Skipping email notification.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'⚠️ Compliance Alert: {len(expiring_docs_with_details)} Document(s) Require Attention'
        msg['From'] = config.SMTP_FROM_EMAIL
        msg['To'] = ', '.join(config.ALERT_EMAIL_RECIPIENTS)
        
        # Create HTML body
        html_body = format_email_body(expiring_docs_with_details)
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Connect to SMTP server and send email
        print(f"Connecting to SMTP server: {config.SMTP_HOST}:{config.SMTP_PORT}")
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✓ Email notification sent successfully to: {', '.join(config.ALERT_EMAIL_RECIPIENTS)}")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to send email notification: {str(e)}")
        return False


def main():
    """
    Main function to check expiring documents and send notifications.
    
    Requirements: 5.1, 5.2, 5.5
    """
    print("=" * 80)
    print("Site-Steward Compliance Document Expiry Check")
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Load configuration
    config = get_config()
    
    # Create database session
    db_session = SessionLocal()
    
    try:
        # Get expiring documents
        print("\nQuerying compliance documents expiring within 30 days...")
        expiring_docs = get_expiring_documents(db_session)
        
        if not expiring_docs:
            print("✓ No expiring documents found. All compliance documents are valid.")
            return
        
        print(f"⚠️  Found {len(expiring_docs)} document(s) requiring attention:")
        print()
        
        # Gather details for each document
        expiring_docs_with_details = []
        
        for doc in expiring_docs:
            # Get subcontractor details
            subcontractor = db_session.query(SubcontractorORM).filter(
                SubcontractorORM.id == doc.subcontractor_id
            ).first()
            
            # Get associated projects
            projects = subcontractor.projects if subcontractor else []
            
            # Store for email
            expiring_docs_with_details.append((doc, subcontractor, projects))
            
            # Log to console
            status_color, status_text, days_until = get_document_status(doc.expiry_date)
            project_names = ", ".join([p.name for p in projects]) if projects else "No projects"
            
            print(f"  • {subcontractor.name if subcontractor else 'Unknown'}")
            print(f"    Document: {doc.document_type}")
            print(f"    Expiry: {doc.expiry_date.strftime('%Y-%m-%d')} ({status_text})")
            print(f"    Days: {days_until}")
            print(f"    Projects: {project_names}")
            print()
        
        # Send email notification
        print("Sending email notification...")
        email_sent = send_email_notification(config, expiring_docs_with_details)
        
        if email_sent:
            print("\n✓ Compliance check completed successfully.")
        else:
            print("\n⚠️  Compliance check completed with email notification failure.")
            
    except Exception as e:
        print(f"\n✗ ERROR: Compliance check failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        db_session.close()
        print("=" * 80)


if __name__ == "__main__":
    main()
