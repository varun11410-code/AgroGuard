# AgroGuard - Architecture Document

## Version

V1.0

## Status

Approved Architecture Baseline

---

# 1. Architecture Overview

## System Purpose

AgroGuard is an AI-powered crop disease diagnosis and agricultural advisory platform.

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
│Detection │ │AIProvider│
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

Groq (Default) / Google Gemini API (Supported)

### Components

* AIProviderFactory (Dynamic provider resolution)
* AIProvider (Interface for transport)
* Prompts (Dedicated prompt engineering layer)

### Purpose

* Agricultural assistant
* Disease explanation
* Recommendation generation
* Report enhancement

---

## ML Layer

### Frameworks:
TensorFlow / Keras
Scikit-Learn

### Purpose:
Hybrid Disease Classification Pipeline

### Pipeline:
Leaf Image
↓
CLAHE Enhancement
↓
Wavelet Transform
↓
ResNet101 Feature Extraction
↓
DenseNet201 Feature Extraction
↓
Feature Fusion
↓
StandardScaler Transformation
↓
Mutual Information Feature Selection
↓
SVM Classification

### Supported Classes

Tomato:

* Healthy
* Early Blight
* Late Blight

Potato:

* Healthy
* Early Blight
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

Hugging Face Spaces (Docker)

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
│   ├── providers/
│   │   ├── base.py
│   │   ├── gemini_provider.py
│   │   └── groq_provider.py
│   ├── prompts/
│   │   ├── diagnosis_prompt.py
│   │   └── chatbot_prompt.py
│   ├── provider_factory.py
│   ├── interfaces.py
│   └── exceptions.py
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

Provider-agnostic AI integration (Groq, Gemini).

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
Image Upload
      │
      ▼
ML Prediction
      │
      ▼
Support Detection
      │
      ▼
Deterministic Risk Calculator
      │
      ▼
AI Enrichment (supported predictions only)
      │
      ▼
Persistence
      │
      ▼
Frontend
```

Risk Level is calculated deterministically by backend business logic based on the model's confidence score.
The AI Provider never generates the Risk Level.
Unsupported predictions bypass AI enrichment entirely to prevent hallucinated disease explanations.

---

## Model Service

Responsibilities:

• Load SVM model at startup
• Load StandardScaler artifact
• Load feature selection indices
• Initialize ResNet101 feature extractor
• Initialize DenseNet201 feature extractor
• Perform preprocessing
• Perform feature extraction
• Perform feature fusion
• Apply feature scaling
• Apply feature selection
• Perform SVM inference
• Return prediction and confidence score

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

## Provider Architecture

AgroGuard uses a provider-agnostic AI architecture. Business logic must never depend directly on a concrete provider.

```text
AIProvider (Interface)
      │
      ▼
AIProviderFactory (Singleton cache & resolver)
      │
      ▼
GroqProvider (Concrete implementation)
```

### Components

* **Provider Abstraction:** `AIProvider` interface defines the standard contract for all AI integrations.
* **Singleton Provider Caching & Registration:** `AIProviderFactory` serves as the single entry point. It instantiates the requested provider based on environment variables, caching it as a singleton to reuse client sessions. 
* **Concrete Providers:** (e.g., `GroqProvider`). Contain transport logic only. They do not build prompts. Gemini is available as an optional legacy provider but is not tightly coupled.
* **Prompt Builders:** A dedicated layer containing prompt engineering to inject contextual disease data safely. Kept strictly separate from transport logic.
* **Structured JSON Contract:** Providers must normalize their output into a single internal unified JSON contract before returning it. The rest of AgroGuard (e.g., `AIEnrichmentService`, `ChatOrchestrator`) does not know which provider produced the response.
* **Future Provider Extensibility:** Adding a new provider requires only implementing the `AIProvider` interface and registering it in the factory. No business logic changes are needed.

## AI Error Handling

The AI layer implements a robust error handling strategy focusing on:
* **Provider Timeout Strategy:** Explicit timeouts for external AI provider calls.
* **Retry Strategy:** Configurable retries for transient provider failures.
* **Unified Exception Handling:** Translating provider-specific errors into unified application exceptions.
* **Graceful Degradation:** Fallbacks and user-friendly messaging when AI services are unavailable.

---

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

# 10. Storage & Report Architecture

## Storage Architecture (Metadata-Only)

AgroGuard uses a strictly metadata-only persistence strategy for images and reports. 

### Authenticated Users
```text
Image → Cloudinary → image_url → PostgreSQL
```
The raw binary is sent to Cloudinary, and only the secure URL is saved in the database.
Includes **Rollback Protection** (if DB commit fails, the Cloudinary asset is automatically orphaned and cleaned up).

### Guest Users
```text
Image → Browser Memory → Base64 → PDF
```
No Cloudinary upload. No Database record. The image stays in browser memory as a Base64 string and is streamed directly to the PDF generator.

---

## Report Generation Architecture

### Active Report Generation

```text
Prediction
      │
      ▼
Generate PDF
      │
      ▼
Persist Report Metadata
```

### Historical Report Generation

```text
Report Metadata
      │
      ▼
Scan Metadata
      │
      ▼
Cloudinary Retrieval
      │
      ▼
PDF Regeneration
      │
      ▼
Download
```

---

## Report Contents

* User Information
* Crop
* Disease
* Confidence
* AI Summary
* Treatment Plans (modern structure support)
* Prevention Measures
* Timestamp

---

## Storage Strategy Details

* **Metadata-Only Persistence:** We store metadata (disease, summary, treatment JSON) in PostgreSQL. PDF binaries are never permanently stored.
* **Historical Reconstruction:** Reports are reconstructed dynamically from metadata upon download request.
* **Image Placeholders:** If a Cloudinary image is deleted or expired, the PDF generator gracefully falls back to an image placeholder without crashing.
* **Legacy Compatibility:** Handles both legacy string-based recommendations and modern structured treatment plans.

---

# 11. Image Retention Policy

## Guest Users

* **Browser-only:** Images are loaded directly into browser memory (Base64).
* **Never uploaded:** Images never touch Cloudinary or PostgreSQL.

---

## Registered Users

* **Cloudinary:** Uploaded securely to isolated folders.
* **Cleanup & Scheduled Deletion:** Automated lifecycle rules periodically purge expired scans (180 days).
* **Graceful Degradation:** If an image is deleted (via manual user deletion or scheduled cleanup), historical scans and reports still render properly utilizing graceful fallbacks.

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

# 14. Environment Configuration

## Frontend

```env
NEXT_PUBLIC_API_URL= # Required: Points to the Flask backend URL.
```

---

## Backend

Every environment variable required for production orchestration.

### Required Variables
* `AI_PROVIDER`: Defines the active provider (e.g., `groq`). Determines provider selection at runtime.
* `GROQ_API_KEY`: Required for Groq AI enrichment and chatbot.
* `JWT_SECRET_KEY`: Used for authentication and session management.
* `DATABASE_URL`: Connection string for PostgreSQL (Supabase).
* `CLOUDINARY_CLOUD_NAME`: Target cloud environment.
* `CLOUDINARY_API_KEY`: Storage upload authentication.
* `CLOUDINARY_API_SECRET`: Storage API access token.

### Optional Variables
* `GEMINI_API_KEY`: Included for backward compatibility if fallback/legacy provider is needed.
* `GROQ_MODEL` / `GEMINI_MODEL`: Specifies the target LLM model.

This configuration architecture allows seamless future extensibility by simply injecting new provider keys without redeploying code logic.

---

# 15. Scalability Strategy

The architecture must support future additions without major redesign.

Future expansions:

* New Crops
* New Diseases
* New Models
* Additional AI Providers (Adding a new provider requires: Implementing the `AIProvider` interface, Registering the provider in the factory, Configuring environment variables. No business logic changes are needed.)
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

---

# 17. Phase 12 & 12.A Migration Decisions

This section records major architectural migrations to serve as a historical reference for future maintainers.

## Phase 12

* **Metadata-only persistence:** 
  * *Previous:* Binary blobs stored directly or tightly coupled local files.
  * *New:* Raw binaries are hosted externally; database only records `image_url`.
  * *Reason & Benefits:* Offloads bandwidth, reduces DB footprint, improves query speeds.
* **Cloudinary integration:** 
  * *Previous:* Local file storage.
  * *New:* Direct stream uploads to Cloudinary.
  * *Reason & Benefits:* Professional CDN delivery and automatic image optimization.
* **Guest image isolation:** 
  * *Previous:* Guest uploads saved locally.
  * *New:* Guest uploads are kept entirely in Base64 browser memory.
  * *Reason & Benefits:* Prevents tenant storage exhaustion and eliminates orphaned guest files.
* **Cleanup strategy:** 
  * *Previous:* Manual DB cleanup without external syncing.
  * *New:* Cascading deletion that proactively deletes Cloudinary assets before purging DB records, including rollback safeguards.
  * *Reason & Benefits:* Zero orphaned data.

## Phase 12.A

* **AIProvider abstraction:**
  * *Previous:* Hardcoded Gemini SDK calls scattered across services.
  * *New:* `AIProvider` interface and `ProviderFactory` singleton.
  * *Reason & Benefits:* True vendor independence and zero-downtime provider swapping.
* **Prompt builder extraction:**
  * *Previous:* Prompts built directly inside controllers/services.
  * *New:* Dedicated `prompts/` module.
  * *Reason & Benefits:* Separation of concerns; easier tuning of LLM behavior.
* **Groq migration:**
  * *Previous:* Gemini as sole provider.
  * *New:* Groq `llama-3.1-8b-instant` as default provider.
  * *Reason & Benefits:* Dramatically faster response times for real-time AI UX.
* **Deterministic Risk Calculator:**
  * *Previous:* LLM asked to guess Risk Level.
  * *New:* Backend utility calculates Risk deterministically based on ML confidence.
  * *Reason & Benefits:* Eliminates AI hallucination and ensures mathematical consistency.
* **Unified Report Payload:**
  * *Previous:* Ad-hoc schema with legacy string-based recommendations.
  * *New:* Structured JSON contract (`treatment_plans` array) universally mapped.
  * *Reason & Benefits:* Predictable PDF rendering and UI cards.
* **Prediction UX improvements:**
  * *Previous:* Unsupported inputs threw ambiguous errors or triggered confused LLM responses.
  * *New:* Unsupported inputs bypass AI completely and return clean fallback UI.
  * *Reason & Benefits:* Vastly improves user trust and interface stability.
