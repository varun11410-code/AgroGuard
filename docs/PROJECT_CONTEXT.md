# AgroGuard - Project Context

Version: 1.0

Status: Active Project Context

---

# Project Overview

AgroGuard is an AI-powered crop disease diagnosis and agricultural advisory web application.

The platform combines:

* Machine Learning Disease Detection
* AI Agricultural Assistant
* PDF Report Generation
* User Authentication
* Scan History Management

into a single modern web application.

This project is being developed as a production-oriented portfolio project intended to demonstrate full-stack development, machine learning integration, AI integration, system design, security practices, and product thinking.

---

# Core Product Goal

Help farmers identify crop diseases from leaf images and receive actionable agricultural guidance through an AI-assisted workflow.

Primary Goal:

* Showcase software engineering and AI skills to recruiters.

Secondary Goal:

* Provide practical value to real users.

---

# Target Users

Primary Users:

* Farmers

Characteristics:

* Agricultural knowledge
* Limited technical expertise
* Mobile-first usage

---

Secondary Users:

* Recruiters
* Technical Interviewers
* Faculty Evaluators

---

# Current Scope (V1)

Supported Crops:

1. Tomato
2. Potato

---

Supported Disease Classes:

Tomato:

* Healthy
* Early Blight
* Late Blight

Potato:

* Late Blight

---

Important:

The application must clearly communicate that only these crops and disease classes are supported in V1.

No unsupported crop predictions should be implied.

---

# User Roles

Guest

Can:

* Upload image
* Analyze disease
* Download report

Cannot:

* Access AI Assistant
* Save history
* Access profile

---

User

Can:

* Disease detection
* AI Assistant
* Scan history
* Report history
* Profile management

---

Admin

Can:

* Dashboard analytics
* Activity logs
* System monitoring

---

# Core Features

1. Disease Detection
2. AI Agricultural Assistant
3. Treatment Recommendations
4. PDF Reports
5. Scan History
6. Profile Management
7. Admin Dashboard

---

# AI Assistant Scope

Provider:

Google Gemini API

Mode 1:

General agricultural assistant.

Mode 2:

Diagnosis-aware assistant.

Receives context:

* Crop
* Disease
* Confidence Score
* Selected Treatment Plan

The assistant provides guidance only.

It does NOT provide guaranteed outcomes or professional agricultural certification.

---

# Technology Stack

Frontend:

* Next.js
* TypeScript
* Tailwind CSS
* Shadcn/UI
* Framer Motion
* Three.js

Backend:

* Flask
* SQLAlchemy
* JWT
* bcrypt

Database:

* PostgreSQL (Supabase)

Storage:

* Cloudinary

AI:

* Gemini API

ML:

* TensorFlow/Keras

Deployment:

* Vercel
* Render
* Supabase
* Cloudinary

---

# Design Theme

Theme Name:

EcoTech Glass

Visual Style:

* Green-themed
* Nature-inspired
* Glassmorphism
* Modern
* Premium

Primary Colors:

* Deep Green
* Leaf Green
* Soft Green

User experience should feel:

Modern Agriculture + Artificial Intelligence

---

# Architecture Principles

1. Mobile First
2. API First
3. Modular Design
4. Separation of Concerns
5. Security by Default
6. Future Extensibility

Architecture.md is the source of truth.

---

# Security Rules

Passwords:

* Always bcrypt hashed

Authentication:

* JWT

Uploads:

* Validate file type
* Validate size

Secrets:

* Environment variables only

Never hardcode:

* API Keys
* Secrets
* Tokens

---

# AI Development Rules

Before implementing any feature:

1. Read PRD.md
2. Read Architecture.md
3. Read AI_AGENT_RULES.md

Always follow existing architecture.

Never introduce new frameworks or redesign architecture without approval.

---

# Current Development Status

Planning Phase Complete

Completed Documents:

✓ PRD.md

✓ Architecture.md

✓ Todo.md

✓ AI_AGENT_RULES.md

✓ SECURITY_AND_ACCESS_CONTROL.md

✓ FRONTEND_SPECIFICATION.md

✓ PROJECT_CONTEXT.md

Development Progress:

Not Started

Current Objective:

Begin implementation according to Todo.md Phase 0.

---

# Success Criteria

A recruiter should be able to:

Landing Page
↓
Upload Leaf Image
↓
Receive Disease Prediction
↓
Open AI Assistant
↓
Download PDF Report
↓
View Scan History

within a few minutes and clearly understand the technical depth of the project.

This user journey is the primary demonstration flow of AgroGuard.
