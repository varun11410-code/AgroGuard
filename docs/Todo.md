# AgroGuard - Todo.md

## Project Status

Current Phase:

```text
AI Assistant Complete (Phase 9)
User Features In Progress (Phase 10)
```

---

# Development Rules

Before starting ANY task:

1. Read PRD.md
2. Read Architecture.md
3. Follow existing folder structure
4. Never introduce new frameworks without approval
5. Complete one task at a time
6. Verify acceptance criteria before moving forward

---

# PHASE 0 — Project Foundation

Goal:

Create the project skeleton and development environment.

---

## TASK 0.1

### Goal

[x] Create repository structure.

### Create

```text
frontend/
backend/
training/
docs/
.github/
```

### Acceptance Criteria

* All folders exist.
* README exists.
* Repository structure matches Architecture.md.

---

## TASK 0.2

### Goal

[x] Initialize Next.js frontend.

### Create

```text
frontend/
```

### Requirements

* TypeScript
* Tailwind CSS
* App Router

### Acceptance Criteria

* App starts successfully.
* Tailwind working.

---

## TASK 0.3

### Goal

[x] Initialize Flask backend.

### Create

```text
backend/
```

### Requirements

* Flask
* SQLAlchemy
* Flask-Migrate

### Acceptance Criteria

* Backend starts successfully.
* Health endpoint works.

---

## TASK 0.4

### Goal

[x] Create environment variable structure.

### Files

```text
frontend/.env.local

backend/.env
```

### Acceptance Criteria

Environment variables documented.

---

## TASK 0.5

### Goal

[x] Create backend folder architecture.

### Create

```text
routes/
controllers/
services/
repositories/
models/
schemas/
middleware/
config/
utils/
ai/
ml/
reports/
storage/
database/
```

### Acceptance Criteria

Folder structure matches Architecture.md.

---

# PHASE 1 — Database Setup

Goal:

Create PostgreSQL schema and database layer.

---

## TASK 1.1

### Goal

[x] Configure Supabase connection.

### Dependencies

Task 0.3

### Acceptance Criteria

Database connection successful.

---

## TASK 1.2

### Goal

[x] Create User model.

### Table

```text
users
```

### Acceptance Criteria

Migration generated successfully.

---

## TASK 1.3

### Goal

[x] Create Crop model.

### Table

```text
crops
```

### Acceptance Criteria

Migration successful.

---

## TASK 1.4

### Goal

[x] Create Scan model.

### Table

```text
scans
```

### Acceptance Criteria

Relationships working.

---

## TASK 1.5

### Goal

[x] Create Report model.

### Table

```text
reports
```

### Acceptance Criteria

Migration successful.

---

## TASK 1.6

### Goal

[x] Create ChatSession model.

### Table

```text
chat_sessions
```

### Acceptance Criteria

Migration successful.

---

## TASK 1.7

### Goal

[x] Create ChatMessage model.

### Table

```text
chat_messages
```

### Acceptance Criteria

Migration successful.

---

## TASK 1.8

### Goal

[x] Create ActivityLog model.

### Table

```text
activity_logs
```

### Acceptance Criteria

Migration successful.

---

## TASK 1.9

### Goal

[x] Seed supported crops.

### Insert

```text
Tomato
Potato
```

### Acceptance Criteria

Seed script works.

---

# PHASE 2 — Authentication

Goal:

Implement user authentication.

---

## TASK 2.1

### Goal

[x] Create registration endpoint.

### Endpoint

```http
POST /api/auth/register
```

### Acceptance Criteria

User created successfully.

---

## TASK 2.2

### Goal

[x] Implement password hashing.

### Library

bcrypt

### Acceptance Criteria

Passwords never stored in plain text.

---

## TASK 2.3

### Goal

[x] Create login endpoint.

### Endpoint

```http
POST /api/auth/login
```

### Acceptance Criteria

JWT returned.

---

## TASK 2.4

### Goal

[x] Create JWT middleware.

### Acceptance Criteria

Protected routes require token.

---

## TASK 2.5

### Goal

[x] Create current-user endpoint.

### Endpoint

```http
GET /api/auth/me
```

### Acceptance Criteria

Returns authenticated user.

---

## TASK 2.6

### Goal

[x] Implement role middleware.

### Roles

```text
USER
ADMIN
```

### Acceptance Criteria

Admin routes protected.

---

## TASK 2.7

### Goal

[x] Implement logout endpoint.

### Endpoint

POST /api/auth/logout

### Requirements

• Invalidate refresh token
• Support token revocation/blacklisting

### Acceptance Criteria

User logout invalidates future refresh attempts.

# PHASE 3 — Frontend Foundation

Goal:

Create reusable UI system.

---

## TASK 3.1

[x] Install Shadcn/UI.

---

## TASK 3.2

[x] Create theme configuration.

---

## TASK 3.3

[x] Create Navbar component.

---

## TASK 3.4

[x] Create Footer component.

---

## TASK 3.5

[x] Create reusable Button component.

---

## TASK 3.6

[x] Create reusable Card component.

---

## TASK 3.7

[x] Create loading animation component.

---

## TASK 3.8

[x] Create route protection system.

---

# PHASE 4 — Landing Page

Goal:

Build recruiter-facing landing page.

---

## TASK 4.1

[x] Create Hero Section.

### Includes

* [x] Product Title
* [x] CTA Buttons

---

## TASK 4.2

[x] Create animated 3D plant section.

---

## TASK 4.3

[x] Create "How It Works" section.

---

## TASK 4.4

[x] Create supported crops section.

---

## TASK 4.5

[x] Create AI Assistant preview section.

---

## TASK 4.6

[x] Implement mobile responsiveness.

---

## TASK 4.7

[x] Optimize landing page performance.

---

# PHASE 5 — Upload Workflow

Goal:

Implement disease detection workflow.

---

## TASK 5.1

[x] Create crop selection cards.

### Options

* Tomato
* Potato

---

## TASK 5.2

[x] Create drag-and-drop uploader.

---

## TASK 5.3

[x] Implement file validation.

### Validate

* Type
* Size

---

## TASK 5.4

[x] Connect upload endpoint.

---

## TASK 5.5

[x] Create analysis loading sequence.

### Steps

```text
Uploading Image
Analyzing Disease
Generating Insights
```

---

## TASK 5.6

[x] Display prediction results.

---

## TASK 5.7: Assemble Upload Workflow Page

[x] Create app/upload/page.tsx
[x] Integrate Crop Selection Cards
[x] Integrate Drag-and-Drop Uploader
[x] Connect validation states
[x] Add Analyze button
[x] Connect loading sequence navigation
---

# PHASE 6 — ML Integration

Goal:

Integrate trained disease model.

---

## TASK 6.1

[x] Create model loader service.

---

## TASK 6.2

[x] Implement image preprocessing.

---

## TASK 6.3

[x] Implement prediction service.

---

## TASK 6.4

[x] Return confidence score.

---

## TASK 6.5

[x] Connect Flask API to model.

---

## TASK 6.6

[x] Handle unsupported predictions.

---

# PHASE 7 — Results Page

Goal:

Build diagnosis experience.

---

## TASK 7.1

[x] Create disease result card.

---

## TASK 7.2

[x] Create confidence display.

---

## TASK 7.3

[x] Create uploaded image preview.

---

## TASK 7.4

[x] Create AI summary section.

---

## TASK 7.5

[x] Create treatment plan cards.

### Plans

* Budget
* Standard
* Premium

---

## TASK 7.6

[x] Implement plan selection.

---

## TASK 7.7

[x] Save selected plan.

---

# PHASE 8 — PDF Reports

Goal:

Generate downloadable reports.

---

## TASK 8.1

[x] Create PDF template.

---

## TASK 8.2

[x] Create report generation service.

---

## TASK 8.3

[x] Create report endpoint.

---

## TASK 8.4

[x] Implement report download.

---

## TASK 8.5

[x] Store report metadata (Deferred to Phase 10)
    - Re-evaluated by Principal Engineer.
    - Cannot be implemented without `scan_id` (foreign key constraint).
    - Formally moved to Phase 10 (User Features) to align with PRD F9 guest workflow and architecture retention policies.

---

# PHASE 9 — AI Assistant

Goal:

Implement context-aware chatbot.

---

## TASK 9.1

[x] Configure Gemini API.

---

## TASK 9.2

[x] Create AI provider service.

---

## TASK 9.3

[x] Create chat session service.

---

## TASK 9.4

[x] Create chat message service.

---

## TASK 9.5

[x] Inject disease context.

### Context

```text
Crop
Disease
Confidence
Selected Plan
```

---

## TASK 9.6

[x] Build floating chat widget.

---

## TASK 9.7

[x] Restrict chatbot to authenticated users.

---

## TASK 9.8

[x] Store session messages.

---

# PHASE 10 — User Features

Goal:

Implement user dashboard functionality.

---

## TASK 10.1

[x] Create profile page.

---

## TASK 10.2

Implement language preference.

---

## TASK 10.3

Implement budget preference.

---

## TASK 10.4

Create scan history page.

---

## TASK 10.5

Create report history page.

---

## TASK 10.5b

Store report metadata.
- **Dependencies required:** Scan Persistence, User History, Authentication, Report Ownership.
- Must tie into `POST /api/reports/generate` when the user is authenticated.

---

## TASK 10.6

Implement scan deletion.

---

# PHASE 11 — Admin Dashboard

Goal:

Implement administration features.

---

## TASK 11.1

Create admin dashboard layout.

---

## TASK 11.2

Display user count.

---

## TASK 11.3

Display scan count.

---

## TASK 11.4

Display popular diseases.

---

## TASK 11.5

Display activity logs.

---

## TASK 11.6

Protect admin routes.

---

# PHASE 12 — Storage Layer

Goal:

Configure Cloudinary integration.

---

## TASK 12.1

Create Cloudinary service.

---

## TASK 12.2

Upload scan images.

---

## TASK 12.3

Retrieve image URLs.

---

## TASK 12.4

Implement image deletion.

---

## TASK 12.5

Implement 180-day cleanup policy.

---

# PHASE 13 — Security

Goal:

Production-grade security.

---

## TASK 13.1

Validate all API inputs.

---

## TASK 13.2

Implement upload security checks.

---

## TASK 13.3

Implement rate limiting.

---

## TASK 13.4

Implement guest scan limits.

---

## TASK 13.5

Hide sensitive environment variables.

---

## TASK 13.6

Implement secure error handling.

---

# PHASE 14 — Logging

Goal:

Activity monitoring.

---

## TASK 14.1

Log registrations.

---

## TASK 14.2

Log logins.

---

## TASK 14.3

Log uploads.

---

## TASK 14.4

Log predictions.

---

## TASK 14.5

Log report downloads.

---

## TASK 14.6

Log AI interactions.

---

## TASK 14.7

Log application errors.

---

# PHASE 15 — Deployment

Goal:

Deploy production version.

---

## TASK 15.1

Deploy frontend to Vercel.

---

## TASK 15.2

Deploy backend to Render.

---

## TASK 15.3

Configure Supabase production DB.

---

## TASK 15.4

Configure Cloudinary production storage.

---

## TASK 15.5

Configure environment variables.

---

## TASK 15.6

Perform production smoke testing.

---

# PHASE 16 — Final Review

Goal:

Prepare portfolio-ready release.

---

## TASK 16.1

Create README.md.

---

## TASK 16.2

Add architecture diagrams.

---

## TASK 16.3

Capture screenshots.

---

## TASK 16.4

Record demo video.

---

## TASK 16.5

Perform recruiter walkthrough test.

### Workflow

```text
Landing Page
↓
Upload Image
↓
Diagnosis
↓
AI Assistant
↓
PDF Report
↓
History
```

---

## TASK 16.6

Create Release v1.0

### Definition of Done

* Frontend deployed
* Backend deployed
* Database deployed
* ML working
* AI working
* Reports working
* Authentication working
* Admin dashboard working
* Security checks completed
* Documentation complete
