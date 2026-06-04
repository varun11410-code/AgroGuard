# AgroGuard - Security & Access Control Document

Version: 1.0

Status: Approved

---

# 1. Purpose

This document defines the security architecture, access control policies, authentication rules, authorization rules, data protection standards, and operational security requirements for AgroGuard.

The goal is to ensure:

* User data protection
* Secure authentication
* Secure file handling
* Secure AI integration
* Secure administration
* Portfolio-level production readiness

---

# 2. Security Objectives

AgroGuard must protect:

1. User Accounts
2. User Credentials
3. Uploaded Images
4. Scan History
5. Generated Reports
6. AI Conversations
7. Admin Resources
8. Application Infrastructure

Security should follow:

* Least Privilege Principle
* Defense in Depth
* Secure by Default
* Privacy First

---

# 3. User Roles

## Guest User

Unauthenticated visitor.

Permissions:

* View Landing Page
* Upload Leaf Image
* Perform Disease Detection
* Download Generated Report

Restrictions:

* Cannot use AI Assistant
* Cannot access History
* Cannot access Profile
* Cannot access Admin Resources

---

## Authenticated User

Registered user.

Permissions:

* Disease Detection
* AI Assistant
* Scan History
* Report History
* Profile Management
* Preference Management

Restrictions:

* Cannot access Admin Dashboard
* Cannot access Other Users' Data
* Cannot access System Logs

---

## Admin

System administrator.

Permissions:

* Dashboard Analytics
* User Statistics
* Activity Logs
* System Monitoring

Restrictions:

* Cannot access user passwords
* Cannot retrieve password hashes
* Cannot access infrastructure secrets

---

# 4. Authentication Policy

## Authentication Method

JWT (JSON Web Token)

Authentication Flow:

User Login
↓
Credential Validation
↓
JWT Generation
↓
Protected API Access

---

## Password Requirements

Minimum:

* 8 characters

Recommended:

* Uppercase letter
* Lowercase letter
* Number
* Special character

---

## Password Storage

Passwords must:

* Never be stored in plaintext
* Always be hashed

Algorithm:

bcrypt

---

## JWT Security Rules

Tokens must:

* Be signed
* Have expiration time
* Be validated on every protected request

Never trust frontend authentication state.

All authorization decisions must be verified server-side.

---

# 5. Authorization Model

## Access Control Type

Role-Based Access Control (RBAC)

Roles:

* USER
* ADMIN

---

## Route Protection Matrix

| Route           | Guest | User | Admin |
| --------------- | ----- | ---- | ----- |
| Landing Page    | Yes   | Yes  | Yes   |
| Upload Image    | Yes   | Yes  | Yes   |
| Scan Result     | Yes   | Yes  | Yes   |
| AI Assistant    | No    | Yes  | Yes   |
| History         | No    | Yes  | Yes   |
| Profile         | No    | Yes  | Yes   |
| Admin Dashboard | No    | No   | Yes   |
| Activity Logs   | No    | No   | Yes   |

---

# 6. File Upload Security

## Accepted Formats

Allowed:

* JPG
* JPEG
* PNG

Rejected:

* GIF
* SVG
* Executables
* Scripts

---

## Validation Requirements

Validate:

* MIME Type
* File Extension
* File Size

Validation must occur:

1. Frontend
2. Backend

Backend validation is mandatory.

---

## File Size Limit

Recommended:

10 MB Maximum

---

## File Naming

Never trust uploaded filenames.

Generate secure unique names.

Example:

scan_4f7a8c9d.jpg

---

# 7. Image Storage Security

Storage Provider:

Cloudinary

---

## Guest Images

Workflow:

Upload
↓
Analyze
↓
Delete

No permanent storage.

---

## Authenticated User Images

Workflow:

Upload
↓
Store
↓
Link to Scan
↓
Retention Policy
↓
Automatic Deletion

---

## Retention Period

180 Days

After expiration:

* Image removed
* Storage reference deleted

---

# 8. Data Protection Policy

## Stored User Data

Allowed:

* Name
* Email
* Preferences
* Scan History
* Report Metadata

---

## Prohibited Data

Do NOT store:

* Plaintext Passwords
* API Keys
* Tokens
* Credit Card Data
* Government IDs

---

# 9. Database Security

## Access Principle

Application access only.

Direct public database access prohibited.

---

## ORM Usage

Use SQLAlchemy ORM.

Avoid raw SQL.

---

## Injection Prevention

All database interactions must:

* Use ORM
* Use parameterized queries

Never build SQL queries using string concatenation.

---

# 10. API Security

## Input Validation

Every endpoint must validate:

* Required fields
* Data type
* Length constraints

---

## Response Standard

Success:

{
"success": true,
"data": {}
}

Error:

{
"success": false,
"message": "Error Description"
}

---

## Error Disclosure

Never expose:

* Stack traces
* Internal paths
* Database structure
* Secrets

Return safe error messages only.

---

# 11. AI Security

Provider:

Google Gemini API

---

## API Key Protection

Gemini API keys must:

* Be stored in environment variables
* Never be exposed to frontend
* Never be committed to Git

---

## Prompt Injection Protection

User input must never be treated as trusted system instructions.

The system prompt must remain protected.

---

## AI Limitations Notice

Users must be informed:

"Recommendations are AI-generated guidance and should not replace professional agricultural consultation."

---

# 12. Chat Security

## Access Policy

Only authenticated users may use AI Assistant.

---

## Session Ownership

Users may only access their own chat sessions.

---

## Session Lifecycle

Session Created
↓
User Active
↓
Session Ends
↓
Automatic Cleanup

---

# 13. Rate Limiting

Purpose:

Prevent abuse.

---

## Guest Users

Recommended:

* 10 scans/day

---

## Authenticated Users

Recommended:

* 50 scans/day

---

## AI Requests

Recommended:

* 30 AI requests/day

---

# 14. Admin Security

## Protected Resources

* Dashboard
* Statistics
* Activity Logs

---

## Admin Verification

Every admin endpoint must verify:

* Valid JWT
* Admin Role

Both checks required.

---

# 15. Logging Policy

## Log Events

Log:

* Login
* Registration
* Upload
* Prediction
* Report Download
* Chat Usage
* Errors

---

## Never Log

* Passwords
* Tokens
* API Keys
* Secrets

---

# 16. Environment Variable Security

Store secrets only in:

.env

Examples:

DATABASE_URL

JWT_SECRET_KEY

GEMINI_API_KEY

CLOUDINARY_API_KEY

CLOUDINARY_API_SECRET

---

## Git Protection

Never commit:

.env

Add to:

.gitignore

Mandatory.

---

# 17. Transport Security

All production communication must use HTTPS.

Applies to:

* Frontend
* Backend
* API Calls
* Authentication

---

# 18. Dependency Security

Before every release:

* Update dependencies
* Check known vulnerabilities
* Remove unused packages

---

# 19. Incident Response

If suspicious activity is detected:

1. Log incident
2. Restrict access if required
3. Review activity logs
4. Rotate compromised credentials
5. Redeploy updated configuration

---

# 20. Security Checklist

Before Release:

✓ Password hashing implemented

✓ JWT authentication implemented

✓ Role authorization implemented

✓ Upload validation implemented

✓ Rate limiting implemented

✓ HTTPS enabled

✓ Environment variables secured

✓ Admin routes protected

✓ Input validation completed

✓ Error handling completed

✓ Logging implemented

✓ Retention policy implemented

✓ AI keys protected

---

# 21. Security Definition of Done

AgroGuard is considered security-ready when:

* Authentication works securely
* Authorization is enforced
* Uploads are validated
* Secrets are protected
* Admin resources are protected
* Logs are implemented
* Retention policy is active
* No critical vulnerabilities are present
* Production deployment uses HTTPS
* Security checklist passes completely
