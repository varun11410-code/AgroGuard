# AgroGuard 3.0 - Architecture Document

## Version

V1.0

## Status

Approved Architecture Baseline

---

# 1. Architecture Overview

## System Purpose

AgroGuard 3.0 is an AI-powered crop disease diagnosis and agricultural advisory platform.

The system combines:

* Machine Learning Disease Detection
* Conversational AI Assistance
* PDF Report Generation
* User Authentication
* Historical Record Management

into a single web application.

---

## High-Level Architecture

```text
┌──────────────────────┐
│      Frontend        │
│      Next.js         │
└──────────┬───────────┘
           │ HTTPS
           ▼
┌──────────────────────┐
│      Flask API       │
│    Backend Server    │
└──────┬─────┬─────────┘
       │     │
       │     │
       ▼     ▼
┌──────────┐ ┌──────────┐
│ML Engine │ │ AI Layer │
│Detection │ │ Gemini   │
└────┬─────┘ └────┬─────┘
     │            │
     ▼            ▼
┌──────────────────────┐
│ PostgreSQL Database  │
│      Supabase        │
└──────────────────────┘
           │
           ▼
┌──────────────────────┐
│    Cloudinary        │
│ Image Storage Layer  │
└──────────────────────┘
```

---

# 2. Technology Stack

## Frontend

### Framework

Next.js 15+

### Language

TypeScript

### Styling

Tailwind CSS

### UI Components

Shadcn/UI

### Animation

Framer Motion

### 3D Components

Three.js

### State Management

React Context API

### API Communication

Axios

---

## Backend

### Framework

Flask

### Language

Python 3.12+

### Authentication

JWT

### ORM

SQLAlchemy

### Validation

Pydantic

### Password Hashing

bcrypt

### PDF Generation

ReportLab

---

## AI Layer

### Provider

Google Gemini API

### Purpose

* Agricultural assistant
* Disease explanation
* Recommendation generation
* Report enhancement

---

## ML Layer

### Framework

TensorFlow / Keras

### Purpose

Disease classification

### Supported Classes

Tomato:

* Healthy
* Early Blight
* Late Blight

Potato:

* Late Blight

---

## Database

PostgreSQL

Hosted via Supabase

---

## Storage

Cloudinary

Purpose:

* Leaf image storage
* Temporary image retention

---

## Deployment

### Frontend

Vercel

### Backend

Render

### Database

Supabase

### Storage

Cloudinary

---

# 3. Repository Structure

```text
AgroGuard-3.0/

├── frontend/
│
├── backend/
│
├── training/
│
├── docs/
│
├── .github/
│
├── README.md
│
└── docker-compose.yml
```

---

# 4. Frontend Architecture

```text
frontend/

src/

├── app/
│   ├── page.tsx
│   ├── upload/
│   ├── results/
│   ├── history/
│   ├── profile/
│   ├── admin/
│   └── auth/
│
├── components/
│
│   ├── layout/
│   ├── navigation/
│   ├── upload/
│   ├── results/
│   ├── reports/
│   ├── chat/
│   ├── history/
│   ├── admin/
│   └── common/
│
├── services/
│
│   ├── api.ts
│   ├── auth.ts
│   ├── scan.ts
│   ├── report.ts
│   └── chat.ts
│
├── hooks/
│
├── contexts/
│
├── types/
│
├── utils/
│
└── constants/
```

---

# 5. Backend Architecture

## Clean Layered Architecture

```text
backend/

app/

├── routes/
│
├── controllers/
│
├── services/
│
├── repositories/
│
├── models/
│
├── schemas/
│
├── middleware/
│
├── config/
│
├── utils/
│
├── ai/
│
├── ml/
│
├── reports/
│
├── storage/
│
└── database/
```

---

## Responsibility Breakdown

### Routes

Receive requests.

Example:

```text
/api/scans
/api/chat
```

---

### Controllers

Handle request-response lifecycle.

---

### Services

Business logic.

Examples:

* Scan Service
* Chat Service
* Report Service

---

### Repositories

Database operations only.

No business logic.

---

### AI Module

Gemini integration.

---

### ML Module

Model loading.

Prediction execution.

Preprocessing.

---

# 6. Database Design

---

## users

```sql
users
```

| Column                | Type      |
| --------------------- | --------- |
| id                    | UUID      |
| name                  | VARCHAR   |
| email                 | VARCHAR   |
| password_hash         | TEXT      |
| role                  | ENUM      |
| language              | VARCHAR   |
| preferred_budget_tier | VARCHAR   |
| created_at            | TIMESTAMP |
| last_login_at         | TIMESTAMP |
| is_active             | BOOLEAN   |

---

## crops

```sql
crops
```

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| name       | VARCHAR   |
| supported  | BOOLEAN   |
| created_at | TIMESTAMP |

---

## scans

```sql
scans
```

| Column            | Type      |
| ----------------- | --------- |
| id                | UUID      |
| user_id           | UUID      |
| crop_id           | UUID      |
| image_url         | TEXT      |
| predicted_disease | VARCHAR   |
| confidence_score  | FLOAT     |
| selected_plan     | VARCHAR   |
| created_at        | TIMESTAMP |
| expires_at        | TIMESTAMP |

---

## reports

```sql
reports
```

| Column         | Type      |
| -------------- | --------- |
| id             | UUID      |
| scan_id        | UUID      |
| generated_at   | TIMESTAMP |
| report_version | VARCHAR   |
| summary        | TEXT      |

---

## chat_sessions

```sql
chat_sessions
```

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| user_id    | UUID      |
| scan_id    | UUID      |
| created_at | TIMESTAMP |
| expires_at | TIMESTAMP |

---

## chat_messages

```sql
chat_messages
```

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| session_id | UUID      |
| role       | VARCHAR   |
| message    | TEXT      |
| created_at | TIMESTAMP |

---

## activity_logs

```sql
activity_logs
```

| Column        | Type      |
| ------------- | --------- |
| id            | UUID      |
| user_id       | UUID      |
| activity_type | VARCHAR   |
| metadata      | JSON      |
| timestamp     | TIMESTAMP |

---

# 7. Authentication Architecture

## Login Flow

```text
User Login
      │
      ▼
Validate Credentials
      │
      ▼
Generate JWT
      │
      ▼
Return Access Token
      │
      ▼
Protected Routes
```

---

## Protected Endpoints

```text
/api/scans
/api/history
/api/profile
/api/chat
/api/admin
```

---

## Roles

### USER

Access:

* Scan
* History
* Reports
* AI Assistant

---

### ADMIN

Access:

* Analytics
* Activity Logs
* User Statistics

---

# 8. Disease Detection Architecture

## Flow

```text
Upload Image
      │
      ▼
Validate File
      │
      ▼
Cloudinary Upload
      │
      ▼
Preprocessing
      │
      ▼
Model Inference
      │
      ▼
Prediction
      │
      ▼
Results
```

---

## Model Service

Responsibilities:

* Load model at startup
* Perform inference
* Return prediction
* Return confidence score

---

## Response Format

```json
{
  "crop": "Tomato",
  "disease": "Early Blight",
  "confidence": 0.89
}
```

---

# 9. AI Architecture

## Context-Aware Assistant

---

### Mode A

General Agriculture Assistant

Available before diagnosis.

---

### Mode B

Diagnosis-Aware Assistant

Receives:

```json
{
  "crop": "Tomato",
  "disease": "Early Blight",
  "confidence": 0.89
}
```

---

## Prompt Context Injection

System Context:

```text
Crop
Disease
Confidence
Selected Treatment Plan
```

Inserted automatically.

---

## AI Safety Constraints

Assistant must:

* Avoid definitive medical claims.
* Avoid guaranteeing treatment outcomes.
* Explain limitations.
* Encourage local agricultural consultation when needed.

---

# 10. Report Generation Architecture

## Generation Trigger

```text
Result Page
      │
Download Report
      │
Generate PDF
      │
Download
```

---

## Report Contents

* User Information
* Crop
* Disease
* Confidence
* AI Summary
* Treatment Plans
* Prevention Measures
* Timestamp

---

## Storage Strategy

Store metadata only.

PDF generated dynamically.

No permanent PDF storage.

---

# 11. Image Retention Policy

## Guest Users

```text
Upload
↓
Predict
↓
Delete Image
```

---

## Registered Users

```text
Upload
↓
Store Image
↓
Store Scan
↓
Auto Delete After Retention Period
```

---

Retention Duration

```text
180 Days
```

---

# 12. API Contracts

---

## Authentication

```http
POST /api/auth/register
```

```http
POST /api/auth/login
```

```http
POST /api/auth/logout
```

```http
GET /api/auth/me
```

---

## Scans

```http
POST /api/scans
```

Create scan.

---

```http
GET /api/scans
```

History.

---

```http
GET /api/scans/{id}
```

Single scan.

---

```http
DELETE /api/scans/{id}
```

Delete scan.

---

## Reports

```http
POST /api/reports/{scanId}
```

Generate report.

---

```http
GET /api/reports/{id}
```

Fetch metadata.

---

```http
GET /api/reports/{id}/download
```

Download PDF.

---

## Chat

```http
POST /api/chat
```

Send message.

---

```http
GET /api/chat/session
```

Current session.

---

## Admin

```http
GET /api/admin/stats
```

Dashboard statistics.

---

```http
GET /api/admin/logs
```

Activity logs.

---

# 13. Logging Strategy

Log Events:

```text
LOGIN

REGISTER

UPLOAD

PREDICTION

REPORT_GENERATION

REPORT_DOWNLOAD

CHAT_MESSAGE

ERROR
```

---

# 14. Environment Variables

## Frontend

```env
NEXT_PUBLIC_API_URL=
```

---

## Backend

```env
DATABASE_URL=

JWT_SECRET_KEY=

GEMINI_API_KEY=

CLOUDINARY_CLOUD_NAME=

CLOUDINARY_API_KEY=

CLOUDINARY_API_SECRET=
```

---

# 15. Scalability Strategy

The architecture must support future additions without major redesign.

Future expansions:

* New Crops
* New Diseases
* New Models
* Additional AI Providers
* Mobile Application

The current architecture should require only configuration and module additions rather than structural rewrites.

---

# 16. Architecture Principles

1. Separation of Concerns
2. Modular Design
3. API-First Development
4. Mobile-First Frontend
5. Secure by Default
6. Future Extensibility
7. AI Provider Independence
8. Minimal Vendor Lock-In
9. Maintainable Folder Structure
10. Production-Oriented Development
