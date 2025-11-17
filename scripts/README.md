# Scripts Directory

This directory contains utility scripts for the Site-Steward MVP.

## Scripts

### 1. check_expiry.py

Monitors compliance documents and sends email alerts for documents that are expired or expiring within 30 days.

### 2. verify_seed_data.py

Verifies that the database seed data was loaded correctly after initialization.

---

## Compliance Check Script (check_expiry.py)

### Overview

The `check_expiry.py` script monitors compliance documents and sends email alerts for documents that are expired or expiring within 30 days.

## Requirements

- Python 3.7+
- PostgreSQL database with compliance documents
- SMTP server credentials for sending emails

## Configuration

The script uses environment variables for configuration. Set these in your `.env` file:

```bash
# Database Configuration
DATABASE_URL=postgresql://admin:password@localhost:5432/sitesteward

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@sitesteward.com
ALERT_EMAIL_RECIPIENTS=admin@example.com,manager@example.com
```

### Gmail Configuration

If using Gmail:
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password as `SMTP_PASSWORD`

## Usage

### Manual Execution

Run the script manually:

```bash
python scripts/check_expiry.py
```

### Scheduled Execution (Cron)

To run the script daily at 8:00 AM, add this to your crontab:

```bash
# Edit crontab
crontab -e

# Add this line
0 8 * * * cd /path/to/project && /usr/bin/python3 scripts/check_expiry.py >> /var/log/compliance_check.log 2>&1
```

### Windows Task Scheduler

On Windows, use Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 8:00 AM
4. Set action: Start a program
   - Program: `python`
   - Arguments: `scripts/check_expiry.py`
   - Start in: `C:\path\to\project`

## Output

The script outputs:
- Console logs showing found documents
- Email notifications to configured recipients
- Exit code 0 on success, 1 on failure

### Example Output

```
================================================================================
Site-Steward Compliance Document Expiry Check
Execution Time: 2024-11-17 08:00:00
================================================================================

Querying compliance documents expiring within 30 days...
⚠️  Found 2 document(s) requiring attention:

  • ABC Construction
    Document: Insurance Certificate
    Expiry: 2024-11-12 (EXPIRED)
    Days: -5
    Projects: Downtown Tower

  • XYZ Electrical
    Document: Safety Certification
    Expiry: 2024-12-05 (EXPIRING SOON)
    Days: 18
    Projects: Downtown Tower, Harbor Bridge

Sending email notification...
Connecting to SMTP server: smtp.gmail.com:587
✓ Email notification sent successfully to: admin@example.com, manager@example.com

✓ Compliance check completed successfully.
================================================================================
```

## Email Format

The email notification includes:
- Subject: "⚠️ Compliance Alert: X Document(s) Require Attention"
- HTML table with:
  - Subcontractor name
  - Document type
  - Expiry date
  - Status (EXPIRED or EXPIRING SOON)
  - Days until expiry
  - Associated projects

## Compliance Rules

- **RED Status**: Document is expired OR expiring within 30 days
- **GREEN Status**: Document is valid for more than 30 days

## Testing

Run the unit tests:

```bash
python test_check_expiry.py
```

## Troubleshooting

### Database Connection Failed

- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database user has read permissions

### Email Not Sending

- Verify SMTP credentials are correct
- Check firewall allows outbound connections on port 587
- For Gmail, ensure App Password is used (not regular password)
- Verify `ALERT_EMAIL_RECIPIENTS` is set

### No Documents Found

- Check if compliance documents exist in database
- Verify expiry dates are set correctly
- Run query manually to confirm data exists

## Requirements Mapping

This script implements the following requirements:

- **Requirement 5.1**: Query compliance documents expiring within 30 days
- **Requirement 5.2**: Send email notifications for expiring documents
- **Requirement 5.3**: Mark documents as RED if expired or expiring within 30 days
- **Requirement 5.4**: Mark documents as GREEN if valid for more than 30 days
- **Requirement 5.5**: Log notification results


---

## Database Verification Script (verify_seed_data.py)

### Overview

The `verify_seed_data.py` script verifies that the database seed data was loaded correctly after initialization.

### Usage

#### Using Make (Recommended)

```bash
make verify-db
```

#### Manual Execution

```bash
python scripts/verify_seed_data.py
```

#### Docker Execution

```bash
docker-compose exec api python scripts/verify_seed_data.py
```

### What It Checks

The script verifies the following seed data:

- **Users**: 2 users (admin and foreman)
- **Projects**: 2 sample projects
- **Assets**: 3 sample assets
- **Subcontractors**: 2 sample subcontractors
- **Compliance Documents**: 3 sample documents
- **Asset History**: 1 sample history record

### Example Output

```
Verifying seed data...

✓ Users: 2 found
  - admin (admin)
  - foreman (foreman)

✓ Projects: 2 found
  - Downtown Office Building (123 Main St, City)
  - Residential Complex Phase 2 (456 Oak Ave, Town)

✓ Assets: 3 found
  - Excavator CAT 320 (Heavy Equipment) - Downtown Office Building
  - Generator 50kW (Power Equipment) - Downtown Office Building
  - Scaffolding Set A (Safety Equipment) - Unassigned

✓ Subcontractors: 2 found
  - ABC Electrical Services (contact@abcelectrical.com)
  - XYZ Plumbing Co (info@xyzplumbing.com)

✓ Compliance Documents: 3 found
  - Liability Insurance for ABC Electrical Services (expires: 2024-12-31)
  - Safety Certification for ABC Electrical Services (expires: 2024-12-01)
  - Liability Insurance for XYZ Plumbing Co (expires: 2025-02-15)

✓ Asset History: 1 records found

==================================================
Verification Summary:
==================================================
✓ Users: 2 (expected: 2)
✓ Projects: 2 (expected: 2)
✓ Assets: 3 (expected: 3)
✓ Subcontractors: 2 (expected: 2)
✓ Compliance Documents: 3 (expected: 3)
✓ Asset History: 1 (expected: 1)

==================================================
✓ All seed data verified successfully!

Default credentials:
  Admin - username: admin, password: admin123
  Foreman - username: foreman, password: foreman123
```

### Exit Codes

- **0**: All seed data verified successfully
- **1**: Some seed data is missing or verification failed

### When to Use

Run this script after:
- Initial database setup with `make seed-db`
- Database reset or migration
- Troubleshooting login or data issues

### Troubleshooting

#### Database Connection Failed

- Ensure PostgreSQL is running: `docker-compose ps db`
- Check `DATABASE_URL` in `.env`
- Restart database: `docker-compose restart db`

#### Missing Seed Data

If verification fails, re-run the seed script:

```bash
make seed-db
```

Or reset the database completely:

```bash
# WARNING: This deletes all data!
docker-compose down -v
docker-compose up -d
make seed-db
```
