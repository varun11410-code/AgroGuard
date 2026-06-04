# AgroGuard - AI Agent Rules

Version: 1.0

Status: Mandatory

Applies To:
- Cursor
- Claude Sonnet
- GitHub Copilot
- Gemini
- ChatGPT
- Any Future AI Coding Agent

---

# 1. Purpose

This document defines the development rules that all AI coding agents must follow while working on AgroGuard.

The goal is to maintain:

- Architecture consistency
- Code quality
- Security
- Scalability
- Maintainability

AI agents must follow this document before generating or modifying code.

---

# 2. Required Reading Order

Before starting any task, read:

1. PRD.md
2. Architecture.md
3. Todo.md
4. AI_AGENT_RULES.md

Never skip this order.

---

# 3. Architecture Authority

Architecture.md is the single source of truth.

If generated code conflicts with Architecture.md:

Architecture.md always wins.

Do not redesign architecture without explicit approval.

---

# 4. Development Principles

Always prioritize:

1. Readability
2. Maintainability
3. Security
4. Scalability
5. Simplicity

Never prioritize clever code over readable code.

---

# 5. Allowed Technologies

Frontend

- Next.js
- TypeScript
- Tailwind CSS
- Shadcn/UI
- Framer Motion
- Three.js

Backend

- Flask
- SQLAlchemy
- Pydantic
- JWT
- bcrypt

Database

- PostgreSQL

Storage

- Cloudinary

AI

- Gemini API

Do not introduce additional frameworks without approval.

---

# 6. Forbidden Actions

Never:

- Change folder structure
- Introduce new frameworks
- Rename database tables
- Change API contracts
- Remove security checks
- Store passwords in plain text
- Hardcode secrets
- Commit API keys

Without explicit approval.

---

# 7. Code Quality Standards

All code must be:

- Typed
- Modular
- Reusable
- Documented

Avoid:

- Massive files
- Massive functions
- Deep nesting

---

# 8. File Size Limits

Frontend Components

Maximum:

300 lines

Backend Files

Maximum:

400 lines

Services

Maximum:

300 lines

If exceeded:

Refactor into smaller modules.

---

# 9. Function Size Limits

Maximum:

50 lines per function

Preferred:

20–30 lines

If a function becomes too large:

Extract helper functions.

---

# 10. Naming Conventions

---

## Frontend

Components

Use:

PascalCase

Examples:

- UploadCard
- ChatWidget
- TreatmentPlanCard

---

Hooks

Use:

camelCase

Examples:

- useAuth
- useScanHistory

---

Files

Use:

PascalCase for components

Example:

UploadCard.tsx

---

## Backend

Files

Use:

snake_case

Examples:

scan_service.py
chat_controller.py

---

Classes

Use:

PascalCase

Examples:

ScanService
ChatService

---

Functions

Use:

snake_case

Examples:

generate_report()
predict_disease()

---

# 11. Frontend Rules

---

## Component Design

Components must be:

- Small
- Reusable
- Focused on one responsibility

Avoid:

God Components

---

## Styling

Use:

Tailwind only

Do not:

- Use inline styles
- Create custom CSS files

Unless absolutely necessary.

---

## State Management

Use:

- React Context
- Local State

Do not add Redux.

---

## API Calls

All API calls must go through:

```text
src/services/
```

Never call APIs directly inside UI components.

# 12. Backend Rules
## Layer Responsibilities

Routes

Receive requests only.

Controllers

Handle request-response lifecycle.

Services

Business logic only.

Repositories

Database operations only.

Never mix responsibilities.

Example

## BAD

Route performs SQL queries.

## GOOD

Route
→ Controller
→ Service
→ Repository

# 13. Database Rules

Never perform raw SQL unless necessary.

Use SQLAlchemy ORM.

All tables must:

Use UUID primary keys
Have timestamps where appropriate
# 14. API Standards

All API responses must follow:

Success:

{
  "success": true,
  "data": {}
}

Error:

{
  "success": false,
  "message": "Description"
}

Never return inconsistent response formats.

# 15. Error Handling

Every endpoint must:

Validate input
Catch exceptions
Return safe errors

Never expose:

Stack traces
Secrets
Internal implementation details
# 16. Security Rules
## Authentication

Use JWT.

Never trust frontend authentication state.

Always validate tokens server-side.

## Passwords

Always hash using bcrypt.

Never store plaintext passwords.

## File Uploads

Validate:

MIME type
File size
Extension

Reject invalid uploads.

## Environment Variables

Store all secrets in:

.env

Never hardcode:

API Keys
Database URLs
JWT Secrets
# 17. AI Integration Rules

Gemini must be wrapped inside:

ai/

Create abstraction layer:

AIProvider

Future providers should be replaceable without modifying business logic.

## Prompt Management

Do not hardcode prompts inside routes.

Store prompts separately.

# 18. ML Integration Rules

Model loading must happen once.

Do not:

Reload model per request.

Use singleton pattern.

# 19. Logging Rules

Always log:

Login
Upload
Prediction
Report Download
Chat Usage
Errors

Never log:

Passwords
Tokens
Secrets
# 20. Documentation Rules

Every major module must include:

Purpose
Inputs
Outputs

Complex functions require docstrings.

# 21. Testing Rules

Before marking a task complete:

Verify:

No TypeScript errors
No Python errors
Build passes
API endpoint works
# 22. Git Rules

Commit messages must follow:

feat:
fix:
refactor:
docs:
test:
chore:

Examples:

feat: add disease prediction endpoint

fix: resolve image upload validation

refactor: split scan service into modules

# 23. Performance Rules

Avoid:

Duplicate API calls
Unnecessary rerenders
Repeated model loading

Optimize for:

Mobile users
Slow networks
# 24. Accessibility Rules

All UI must:

Be keyboard accessible
Have proper labels
Use semantic HTML
# 25. Mobile First Requirement

Primary target:

Mobile Devices

Priority Order:

Mobile
Tablet
Desktop

All pages must be responsive.

# 26. Completion Rule

A task is complete only when:

Acceptance criteria satisfied
No build errors
No lint errors
No architecture violations

If uncertain:

Do not assume.

Ask for clarification.