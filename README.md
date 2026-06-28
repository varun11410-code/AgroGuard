<div align="center">

# 🌿 AgroGuard

### AI-Powered Crop Disease Diagnosis & Agricultural Advisory Platform

<p align="center">
  <img src="./docs/assets/banner.png" alt="AgroGuard Banner" width="100%">
</p>

Detect crop diseases from a single leaf photo, get AI-explained treatment plans, and download a professional diagnosis report — in under a minute.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Frontend](https://img.shields.io/badge/Frontend-Next.js%2015-black)](#)
[![Backend](https://img.shields.io/badge/Backend-Flask-lightgrey)](#)
[![ML](https://img.shields.io/badge/ML-TensorFlow%20%7C%20Scikit--Learn-orange)](#)
[![Deployment](https://img.shields.io/badge/Deployed-Vercel%20%7C%20Hugging%20Face-blue)](#)
[![Status](https://img.shields.io/badge/Status-V1%20Released-success)](#)

</div>

---

<p align="center">
  <a href="https://agro-guard-xi.vercel.app/">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-Visit_AgroGuard-success?style=for-the-badge" />
  </a>
  <a href="https://huggingface.co/spaces/Varun11410/AgroGuard-backend">
    <img src="https://img.shields.io/badge/API-Backend-blue?style=for-the-badge" />
  </a>
  <a href="https://github.com/varun11410-code/AgroGuard">
    <img src="https://img.shields.io/badge/Source_Code-GitHub-black?style=for-the-badge" />
  </a>
</p>

> 🚀 **Live Application:** https://agro-guard-xi.vercel.app

> 📡 **Backend API:** https://huggingface.co/spaces/Varun11410/AgroGuard-backend

> 📖 **Project Documentation:** See `/docs` directory.

---

## 📖 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [System Architecture Overview](#-system-architecture-overview)
4. [Technology Stack](#-technology-stack)
5. [Project Structure](#-project-structure)
6. [Installation Guide](#-installation-guide)
7. [Deployment](#-deployment)
8. [Application Workflow](#-application-workflow)
9. [Security Features](#-security-features)
10. [Performance & Scalability](#-performance--scalability)
11. [Screenshots](#-screenshots)
12. [Future Enhancements](#-future-enhancements)
13. [Contributors](#-contributors)
14. [License](#-license)
15. [Acknowledgements](#-acknowledgements)
16. [Contact](#-contact)

---

## 🌱 Project Overview

**AgroGuard** is a full-stack, AI-assisted agricultural advisory platform that helps farmers identify crop diseases directly from leaf images and receive actionable, AI-generated guidance on treatment and prevention.

Rather than functioning as a standalone image classifier, AgroGuard is built as an **end-to-end advisory experience**: disease detection, treatment recommendations, downloadable PDF reports, and a context-aware conversational assistant — all wrapped in a secure, role-based, production-oriented web application.

The project currently supports disease detection for:

| Crop | Supported Classes |
|---|---|
| 🍅 **Tomato** | Healthy, Early Blight, Late Blight |
| 🥔 **Potato** | Healthy, Early Blight, Late Blight |

> **Transparency Notice:** AgroGuard V1 currently supports disease detection for **Tomato and Potato only**. This limitation is intentionally surfaced across the Landing Page, Upload Page, and documentation to set accurate expectations for users.

AgroGuard was built as a production-oriented portfolio project, designed to demonstrate full-stack engineering, applied machine learning, AI system integration, and product thinking — while still delivering genuine value to real farmers.

---

# 🚀 Feature Showcase

| Feature | Description |
|----------|-------------|
| 🧠 **AI Agricultural Assistant** | Context-aware AI assistant powered by a provider-agnostic architecture supporting Groq and Google Gemini. |
| 🔬 **Hybrid ML Disease Detection** | CLAHE → Wavelet → ResNet101 + DenseNet201 → Feature Fusion → SVM classification pipeline for accurate disease diagnosis. |
| 📄 **Professional PDF Reports** | Generate downloadable diagnosis reports containing disease details, treatment plans, prevention tips, and AI explanations. |
| 💬 **Diagnosis-Aware Chat** | Continue the conversation after a prediction with AI that already understands the detected crop and disease. |
| 📊 **Admin Analytics Dashboard** | Platform analytics, user management, scan history, reports, and activity logs from one centralized dashboard. |
| ☁️ **Production Cloud Architecture** | Frontend on Vercel, backend containerized, PostgreSQL on Supabase, Cloudinary image storage, fully production-ready deployment. |
| 🔒 **Secure Authentication** | JWT authentication, bcrypt password hashing, RBAC, protected APIs, validation, and secure error handling. |
| 📱 **Responsive Modern UI** | EcoTech Glass design system with Framer Motion animations and mobile-first responsive experience. |

<p align="center">
  <img src="./docs/assets/features.png" alt="AgroGuard Features" width="90%">
</p>
---

## ✨ Key Features

### 🧠 AI Features
- **Provider-Agnostic AI Layer** — A vendor-independent `AIProvider` abstraction supporting **Groq** (default) and **Google Gemini** (supported), swappable via environment configuration with zero business-logic changes.
- **General Agriculture Assistant (Mode A)** — Available to authenticated users for general crop care, farming best practices, and agriculture Q&A.
- **Diagnosis-Aware Assistant (Mode B)** — Automatically activated after a diagnosis, injected with crop type, disease, and confidence score to give contextual explanations and treatment guidance.
- **AI-Generated Treatment Plans** — Budget, Standard, and Premium recommendation tiers, each with example products, application guidance, and prevention tips.
- **Graceful AI Degradation** — Provider timeouts, retries, and unified exception handling ensure the app stays usable even when an AI provider is unavailable.

### 🔬 Machine Learning
- **Hybrid Disease Classification Pipeline**: CLAHE enhancement → Wavelet Transform → ResNet101 + DenseNet201 feature extraction → Feature Fusion → StandardScaler → Mutual Information feature selection → SVM classification.
- **Deterministic Risk Calculator** — Risk level is computed by backend business logic from the model's confidence score, never by the LLM — eliminating AI hallucination in clinical-style outputs.
- **Unsupported Input Handling** — Inputs outside the supported crop/disease scope bypass AI enrichment entirely and return a clean fallback response instead of a hallucinated explanation.

### 🔐 Authentication & Security
- JWT-based authentication with **bcrypt** password hashing.
- Role-based access control (**Guest**, **User**, **Admin**).
- Protected API routes and token-based session management with logout/token revocation.
- Full input validation and file upload validation (type & size).

### 📄 Report Generation
- On-demand **PDF report generation** (ReportLab) containing crop, disease, confidence score, AI summary, treatment plans, prevention tips, and timestamp.
- **Metadata-only persistence** — PDF binaries are never stored; reports are dynamically reconstructed from structured metadata on each download request.
- Graceful image-placeholder fallback if a source image has expired or been deleted.

### 🛡️ Administration
- Admin-only dashboard with platform-wide analytics: total users, total diagnoses, popular diseases, and user/scan growth trends.
- User, scan, and report management modules with pagination.
- Dedicated activity log center for system-wide audit visibility.

### 🎨 User Experience
- Mobile-first, responsive design across the entire application.
- **EcoTech Glass** design theme — green-toned, nature-inspired glassmorphism aesthetic.
- Animated UI built with Framer Motion and an interactive Three.js landing section.
- Guided upload-to-results flow with a transparent loading sequence (uploading → analyzing → generating insights).

### 🚀 Deployment
- Frontend deployed on **Vercel**.
- Backend containerized and deployed via **Hugging Face Spaces (Docker)**.
- Managed PostgreSQL database via **Supabase**.
- Image storage and CDN delivery via **Cloudinary**.

### 📊 Logging & Monitoring
- Structured activity logging across key system events: `LOGIN`, `REGISTER`, `UPLOAD`, `PREDICTION`, `REPORT_GENERATION`, `REPORT_DOWNLOAD`, `CHAT_MESSAGE`, `ERROR`.
- Centralized error handling with user-friendly messaging and backend-side failure logging.

---

## 🏗️ System Architecture

<p align="center">
  <img src="./docs/assets/architecture.png" alt="AgroGuard Architecture" width="100%">
</p>

AgroGuard follows a modular, layered architecture that separates presentation, business logic, AI orchestration, machine learning inference, persistence, and cloud services. This design keeps components loosely coupled, improves maintainability, and allows future AI providers, ML models, or storage services to be integrated with minimal changes to the existing codebase.

**Key architectural decisions:**

- **Clean layered backend** — Requests flow through Routes → Controllers → Services (business logic) → Repositories (data access only), keeping business rules decoupled from persistence.
- **Provider-agnostic AI module** — A dedicated `ai/` layer (provider interface, factory, and isolated prompt builders) ensures no business logic is coupled to a specific AI vendor.
- **Metadata-only storage strategy** — Raw image binaries live in Cloudinary; PostgreSQL stores only structured metadata (URLs, predictions, report data), keeping the database lightweight and queries fast.
- **Guest vs. Authenticated isolation** — Guest images never touch persistent storage (processed in browser memory as Base64); authenticated user images are stored in Cloudinary under a scheduled 180-day retention policy.

---

# 📊 Project Highlights

| Category | Details |
|----------|----------|
| 🏗️ Architecture | Layered Architecture (Routes → Controllers → Services → Repositories) |
| 🧠 AI Providers | Groq (Default), Google Gemini (Supported) |
| 🔬 ML Pipeline | CLAHE → Wavelet → ResNet101 → DenseNet201 → Feature Fusion → SVM |
| 🌱 Supported Crops | Tomato & Potato |
| 🦠 Disease Classes | Healthy, Early Blight, Late Blight |
| 📄 Report Engine | Dynamic PDF Generation (ReportLab) |
| ☁️ Cloud Services | Vercel, Hugging Face Spaces, Supabase, Cloudinary |
| 🔒 Authentication | JWT + bcrypt + RBAC |
| 📱 Frontend | Next.js 15 + TypeScript + Tailwind CSS |
| ⚙️ Backend | Flask + SQLAlchemy + PostgreSQL |
| 🤖 AI Features | Diagnosis Explanation, Treatment Plans, Context-Aware Chat |
| 📈 Deployment | Production Ready |

<p align="center">
  <img src="./docs/assets/highlights.png" width="95%">
</p>

---

# 🔄 End-to-End Workflow

<p align="center">
  <img src="./docs/assets/workflow.png" alt="AgroGuard Workflow" width="100%">
</p>

The workflow below illustrates how a leaf image moves through AgroGuard—from upload and disease prediction to AI-powered recommendations, report generation, and historical record management.

---

## 🛠️ Technology Stack

### Frontend
| Technology | Purpose |
|---|---|
| Next.js 15+ | React framework / App Router |
| TypeScript | Type-safe application code |
| Tailwind CSS | Utility-first styling |
| Shadcn/UI | Accessible component library |
| Framer Motion | Animation & transitions |
| Three.js | 3D landing page visuals |
| React Context API | State management |
| Axios | API communication |

### Backend
| Technology | Purpose |
|---|---|
| Flask | Python web framework |
| Python 3.12+ | Core backend language |
| SQLAlchemy | ORM / database modeling |
| Pydantic | Request/response validation |
| Flask-Migrate | Database migrations |

### Database
| Technology | Purpose |
|---|---|
| PostgreSQL | Relational data store |
| Supabase | Managed Postgres hosting |

### AI
| Technology | Purpose |
|---|---|
| Groq API | Default AI provider (fast inference) |
| Google Gemini API | Supported alternative provider |
| Custom `AIProvider` abstraction | Vendor-agnostic AI integration layer |

### Machine Learning
| Technology | Purpose |
|---|---|
| TensorFlow / Keras | Deep feature extraction (ResNet101, DenseNet201) |
| Scikit-Learn | SVM classification, feature scaling & selection |

### Authentication
| Technology | Purpose |
|---|---|
| JWT | Stateless session authentication |
| bcrypt | Password hashing |

### Storage
| Technology | Purpose |
|---|---|
| Cloudinary | Image hosting & CDN delivery |

### Deployment
| Technology | Purpose |
|---|---|
| Vercel | Frontend hosting |
| Hugging Face Spaces (Docker) | Backend hosting |
| Supabase | Production database hosting |
| Cloudinary | Production image storage |

### Dev Tools
| Technology | Purpose |
|---|---|
| Git / GitHub | Version control |
| Docker | Backend containerization |
| ESLint / Prettier | Frontend code quality |

---

# 🔌 REST API Overview

AgroGuard exposes a modular REST API following a resource-oriented design. Protected endpoints require JWT authentication, while public endpoints remain accessible to guest users where appropriate.

| Module | Endpoint Prefix | Authentication |
|----------|----------------|----------------|
| 🔐 Authentication | `/api/auth/*` | Public / JWT |
| 🌱 Disease Detection | `/api/scan/*` | Guest / JWT |
| 💬 AI Chat | `/api/chat/*` | JWT |
| 📄 Reports | `/api/report/*` | JWT |
| 📚 Scan History | `/api/history/*` | JWT |
| 👤 User Profile | `/api/profile/*` | JWT |
| 🛡️ Admin Dashboard | `/api/admin/*` | Admin |
| ❤️ Health Check | `/api/health` | Public |

### Authentication Flow

```text
Register/Login
        │
        ▼
Receive JWT Token
        │
        ▼
Store Securely
        │
        ▼
Attach Authorization Header
        │
        ▼
Access Protected Endpoints
```

**Security Features**

- JWT Authentication
- Role-Based Access Control (RBAC)
- bcrypt Password Hashing
- Input Validation via Pydantic
- Secure Error Handling
- Protected Admin Routes
- Request Validation
- File Upload Validation

<p align="center">
  <img src="./docs/assets/api-overview.png" alt="REST API Overview" width="100%">
</p>

---

# 🔬 Machine Learning Pipeline

AgroGuard uses a **hybrid deep learning and classical machine learning pipeline** rather than relying on a single convolutional neural network. The workflow combines image preprocessing, feature engineering, deep feature extraction, feature fusion, dimensionality reduction, and Support Vector Machine (SVM) classification to improve robustness and generalization.

| Stage | Technique |
|--------|-----------|
| 📷 Image Input | Uploaded Tomato/Potato Leaf |
| 🎨 Contrast Enhancement | CLAHE |
| 🌊 Texture Enhancement | Wavelet Transform |
| 🧠 Deep Feature Extraction | ResNet101 |
| 🧠 Deep Feature Extraction | DenseNet201 |
| 🔗 Feature Fusion | Concatenate CNN Features |
| 📊 Feature Selection | Mutual Information |
| ⚖️ Feature Scaling | StandardScaler |
| 🤖 Classification | Support Vector Machine (SVM) |
| 📈 Output | Disease Prediction + Confidence |

This hybrid approach combines the representational power of deep convolutional neural networks with the strong decision boundaries of Support Vector Machines, producing reliable predictions while maintaining a modular and extensible inference pipeline.

<p align="center">
  <img src="./docs/assets/ml-pipeline.png" alt="Machine Learning Pipeline" width="100%">
</p>

---

## 📁 Project Structure

```text
AgroGuard/
├── frontend/                  # Next.js application
│   └── src/
│       ├── app/                # App Router pages
│       │   ├── upload/         # Crop selection & image upload flow
│       │   ├── results/        # Diagnosis results & treatment plans
│       │   ├── history/        # Scan & report history
│       │   ├── profile/        # User preferences
│       │   ├── admin/          # Admin dashboard
│       │   └── auth/           # Login & registration
│       ├── components/         # Reusable UI building blocks
│       │   ├── layout/ navigation/ upload/
│       │   ├── results/ reports/ chat/
│       │   └── history/ admin/ common/
│       ├── services/            # API client modules (api, auth, scan, report, chat)
│       ├── hooks/                # Custom React hooks
│       ├── contexts/             # Global state providers
│       ├── types/                # Shared TypeScript types
│       └── utils/ constants/     # Helpers & static config
│
├── backend/                   # Flask application
│   └── app/
│       ├── routes/             # API route definitions
│       ├── controllers/        # Request/response handling
│       ├── services/           # Business logic (scan, chat, report)
│       ├── repositories/       # Database access layer
│       ├── models/             # SQLAlchemy ORM models
│       ├── schemas/            # Pydantic validation schemas
│       ├── middleware/         # Auth & role-based guards
│       ├── ai/                  # Provider-agnostic AI module
│       │   ├── providers/         # base.py, groq_provider.py, gemini_provider.py
│       │   ├── prompts/            # diagnosis_prompt.py, chatbot_prompt.py
│       │   └── provider_factory.py
│       ├── ml/                  # Model loading, preprocessing, inference
│       ├── reports/              # PDF generation logic
│       ├── storage/              # Cloudinary integration
│       └── database/             # DB session & config
│
├── training/                  # ML model training notebooks/scripts
├── docs/                       # Architecture & project documentation
├── .github/                    # CI/CD & repository configuration
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Installation Guide

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.12+
- PostgreSQL instance (or a free [Supabase](https://supabase.com) project)
- A [Cloudinary](https://cloudinary.com) account
- A [Groq API key](https://groq.com) (and optionally a Gemini API key)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/AgroGuard.git
cd AgroGuard
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Variables

**Backend (`backend/.env`)**
```env
# Required
AI_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=postgresql://user:password@host:port/dbname
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret

# Optional
GEMINI_API_KEY=your_gemini_api_key
GROQ_MODEL=llama-3.1-8b-instant
GEMINI_MODEL=gemini-1.5-flash
```

**Frontend (`frontend/.env.local`)**
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

> 🔒 Never commit `.env` files. All secrets must be supplied via environment variables only.

### 5. Database Migration
```bash
cd backend
flask db upgrade
```

### 6. Run Locally

**Backend:**
```bash
cd backend
flask run
```

**Frontend:**
```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`, with the API served from `http://localhost:5000`.

---

## ☁️ Deployment

AgroGuard follows a decoupled deployment model:

| Layer | Platform |
|---|---|
| Frontend | **Vercel** — automatic builds from the `frontend/` directory |
| Backend | **Hugging Face Spaces (Docker)** — containerized Flask API |
| Database | **Supabase** — managed PostgreSQL |
| Storage | **Cloudinary** — image hosting & CDN |

The frontend communicates with the backend exclusively over HTTPS via the `NEXT_PUBLIC_API_URL` environment variable, allowing each layer to be deployed, scaled, and redeployed independently.

---

## 🔄 Application Workflow

**Guest Flow**
```
Landing Page → Upload Page → Select Crop → Upload Image → Analyze → View Results → Download Report
```

**Authenticated User Flow**
```
Landing Page → Login → Upload Image → Analyze → View Results → Open AI Assistant → Ask Questions → Download Report → View History
```

1. The user selects a supported crop (Tomato or Potato) and uploads a leaf image.
2. The image is validated, then passed through the hybrid ML pipeline for disease classification.
3. A deterministic risk level is calculated from the model's confidence score.
4. For supported predictions, the AI layer enriches the result with a plain-language summary and tiered treatment recommendations.
5. The user can open the AI Assistant to ask follow-up questions in the context of their diagnosis (authenticated users only).
6. A PDF report can be generated and downloaded at any time, containing the full diagnosis and treatment details.
7. Authenticated users can revisit past scans and reports from their history pages.

---

## 🔒 Security Features

- **Password Security:** All passwords are hashed with bcrypt — never stored in plaintext.
- **Authentication:** Stateless JWT-based sessions with logout/token revocation support.
- **Authorization:** Role-based access control distinguishing Guest, User, and Admin permissions across all protected routes (`/api/scans`, `/api/history`, `/api/profile`, `/api/chat`, `/api/admin`).
- **Input Validation:** All API inputs are validated via Pydantic schemas.
- **Upload Validation:** File type and size are strictly validated before processing.
- **Rate Limiting:** Enforced on sensitive endpoints, including daily guest diagnosis limits.
- **Secrets Management:** All credentials and API keys are supplied exclusively through environment variables — never hardcoded.
- **Secure Error Handling:** Errors are logged server-side while user-facing messages remain generic and safe.

---

## ⚡ Performance & Scalability

- Prediction responses target **under 10 seconds** end-to-end.
- Non-AI API responses target **under 2 seconds**.
- **Metadata-only persistence** keeps the database lightweight — raw images live in Cloudinary, not PostgreSQL.
- **Provider-agnostic AI architecture** allows new AI vendors to be added by implementing a single interface and registering it in a factory — with no changes to business logic.
- **Mobile-first design** ensures consistent performance across the smartphone-first farmer user base.
- Architecture explicitly supports future expansion — new crops, new disease classes, new ML models, and new AI providers — through configuration and modular additions rather than structural rewrites.

---

# 📸 Application Gallery

## 🏠 Landing Page

<p align="center">
<img src="./docs/assets/screenshots/landing.png" width="95%">
</p>

---

## 📤 Image Upload

<p align="center">
<img src="./docs/assets/screenshots/upload.png" width="95%">
</p>

---

## ⚙️ AI Analysis Pipeline

<p align="center">
<img src="./docs/assets/screenshots/analysis.png" width="95%">
</p>

---

## 🔬 Diagnosis Results

<p align="center">
<img src="./docs/assets/screenshots/results.png" width="95%">
</p>

---

## 💬 Diagnosis-Aware AI Assistant

<p align="center">
<img src="./docs/assets/screenshots/chat.png" width="95%">
</p>

---

## 📄 PDF Report Generation

<p align="center">
<img src="./docs/assets/screenshots/report.png" width="95%">
</p>

---

## 🕒 Scan History

<p align="center">
<img src="./docs/assets/screenshots/history.png" width="95%">
</p>

---

## 🛡️ Admin Dashboard

<p align="center">
<img src="./docs/assets/screenshots/admin.png" width="95%">
</p>

---

## 🗺️ Project Roadmap

### ✅ Completed (V1.0)

- [x] User Authentication & Authorization
- [x] Hybrid CNN + SVM Disease Classification
- [x] AI-Powered Agricultural Assistant
- [x] Context-Aware Diagnosis Chat
- [x] AI-Generated Treatment Recommendations
- [x] PDF Report Generation
- [x] Scan History
- [x] Report History
- [x] User Profile & Preferences
- [x] Admin Dashboard
- [x] Activity Logging
- [x] Cloudinary Image Storage
- [x] Provider-Agnostic AI Architecture
- [x] Responsive Mobile-First UI
- [x] Production Deployment

---

### 🚀 Planned (V1.1)

- [ ] Google OAuth Authentication
- [ ] Support for Additional Crops
- [ ] Additional Disease Classes
- [ ] Improved Recommendation Engine
- [ ] Enhanced Admin Analytics

---

### 🌍 Future Vision (V2.0)

- [ ] Weather Integration
- [ ] Seasonal Crop Advisory
- [ ] Multi-language Support
- [ ] Expert Consultation Module
- [ ] Agricultural Knowledge Base
- [ ] Offline Mobile Support

---

## 👥 Contributors

### Varun Kumar Sinha — *Lead Developer*
Responsible for:
- System Architecture
- Backend Development
- AI Integration
- Machine Learning Integration
- Authentication & Security
- Database Design
- API Development
- Deployment
- Testing
- Project Management

### Rakshita Srivastava — *Frontend Design & Project Contributor*
Contributed to:
- Frontend UI/UX Design
- Debugging Assistance
- Testing
- Feature Discussions
- Design Feedback

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgements

- The open-source communities behind Next.js, Flask, TensorFlow, and Scikit-Learn.
- Groq and Google Gemini for AI inference capabilities powering the advisory assistant.
- Supabase, Cloudinary, Vercel, and Hugging Face Spaces for infrastructure that made production deployment possible.

---

## 📬 Contact

**Varun Kumar Sinha**

- GitHub: https://github.com/varun11410-code
- LinkedIn: https://www.linkedin.com/in/varunkumarsinha
- Email: sinhavarun99@gmail.com