# AgroGuard - Product Requirements Document (PRD)

## 1. Product Overview

* **Product Name:** AgroGuard
* **Product Type:** AI-Powered Crop Disease Diagnosis and Agricultural Advisory Platform
(Disease detection is performed using a hybrid machine learning pipeline combining deep feature extraction and SVM classification.

Generative AI (via a provider-agnostic layer) is used exclusively for post-prediction enrichment, including treatment recommendations, preventive advice, PDF report generation context, and chatbot assistance.)
* **Version:** V1 (Portfolio & Production-Oriented Release)
* **Project Goal:** * AgroGuard is a modern web application that helps farmers identify crop diseases from leaf images and receive AI-powered agricultural guidance.
* *Primary Goal:* Demonstrate strong software engineering, machine learning, AI integration, and product design skills through a polished, production-oriented application suitable for portfolio and recruiter evaluation.
* *Secondary Goal:* Provide practical value to real users by offering disease diagnosis, treatment recommendations, and agricultural assistance.



---

## 2. Vision Statement

To create a professional AI-powered agricultural assistant that combines machine learning disease detection with conversational AI to help farmers make informed crop management decisions. Rather than functioning as a simple image classifier, AgroGuard should provide an end-to-end advisory experience including diagnosis, recommendations, reporting, and contextual AI support.

---

## 3. Problem Statement

**Many farmers struggle to:**

* Identify crop diseases accurately.
* Access timely agricultural guidance.
* Understand treatment options.
* Compare treatment approaches based on budget.
* Maintain records of disease diagnoses.

**Existing solutions are often:**

* Difficult to use.
* Not farmer-friendly.
* Focused only on prediction.
* Lacking conversational assistance.

AgroGuard addresses these issues through a unified AI-assisted workflow.

---

## 4. Target Users

### Primary Persona: Farmer

* **Profile:**
* Works with agricultural crops.
* Uses smartphones more frequently than desktops.
* Has agricultural knowledge but limited technical expertise.
* Requires quick and actionable recommendations.


* **Goals:**
* Identify diseases quickly.
* Understand treatment options.
* Receive recommendations in simple language.
* Access reports for future reference.



### Secondary Persona: Recruiter / Evaluator

* **Profile:**
* Software engineering recruiter.
* Technical interviewer.
* Faculty evaluator.
* Industry mentor.


* **Goals:**
* Evaluate software engineering skills.
* Evaluate AI integration skills.
* Evaluate system design abilities.
* Evaluate product thinking.



---

## 5. Supported Scope (V1)

**Supported Crops:**

* **Tomato:** Healthy, Early Blight, Late Blight
* **Potato:** Late Blight

> **Transparency Requirement:**
> The application must clearly communicate that AgroGuard currently supports Tomato and Potato disease detection only. This notice should appear on the Landing Page, Upload Page, Documentation, and GitHub README.

---

## 6. Success Metrics

### Technical Success

* Application deploys successfully.
* All APIs function correctly.
* Authentication works reliably.
* Disease prediction pipeline works end-to-end.
* PDF generation works correctly.
* AI assistant responds successfully.

### Product Success

* User can complete diagnosis within 60 seconds.
* User can download a report after diagnosis.
* User can understand treatment recommendations.
* User can continue discussion with the AI assistant.

### Portfolio Success

* A recruiter should be able to experience the Landing Page, Upload Image, Disease Detection, AI Consultation, and PDF Report Generation within a few minutes.

---

## 7. Core Features

### F1. Disease Detection

* **Description:** Users upload crop leaf images and receive disease predictions.
* **Inputs:** Crop Type, Leaf Image
* **Outputs:** Disease Name, Confidence Score, AI Summary
* **Acceptance Criteria:** * Upload validation works.
* Prediction returned successfully.
* Confidence displayed.
* Results page generated.



### F2. Crop Selection

* **Description:** User must select a crop before uploading an image.
* **Supported Options:** Tomato, Potato
* **Acceptance Criteria:** Crop selection is required; unsupported crops are blocked.

### F3. AI Agricultural Assistant

* **Description:** Context-aware chatbot powered by a provider-agnostic AI layer.
* **Mode A: General Agriculture Assistant** (Available to authenticated users)
* Capabilities: Agriculture questions, disease questions, crop care guidance, farming best practices.


* **Mode B: Diagnosis-Aware Assistant** (Activated after disease detection)
* Context Received: Crop Type, Disease, Confidence Score.
* Capabilities: Explain diagnosis, suggest treatments, suggest prevention measures, generate crop care advice.



> **Limitations:** Recommendations are informational only. The system must prominently display: *"Recommendations are AI-generated guidance and should not replace professional agricultural consultation."*

### F4. Treatment Recommendations

* **Description:** Generate multiple treatment approaches.
* **Categories:**
* *Budget Plan:* Low-cost treatment approach.
* *Standard Plan:* Balanced treatment approach.
* *Premium Plan:* Comprehensive treatment approach.


* **Recommendation Structure:** Each recommendation should include Treatment Category, Example Product, Application Guidance, and Prevention Tips.

### F5. PDF Report Generation

* **Description:** Generate downloadable diagnosis reports.
* **Report Contents:** Crop Name, Disease Name, Confidence Score, AI Summary, Treatment Recommendations, Prevention Suggestions, Timestamp.
* **Acceptance Criteria:** PDF downloads successfully, and information matches the diagnosis.

### F6. User Authentication

* **User Registration:** Name, Email, Password
* **User Login:** Email, Password
* **Security:** Password hashing, JWT authentication, Protected routes

### F7. User History

* Authenticated users can access:
* **Scan History:** Previous Diagnoses, Disease Results, Dates
* **Report History:** Previously Generated Reports



### F8. User Preferences

* Users can configure Language and Preferred Budget Tier.
* **Available Budget Tiers:** Budget, Standard, Premium

### F9. Guest Access

* **Guests may:** Upload image, Analyze disease, Download report.
* **Guests may NOT:** Use AI Assistant, Save history, Save reports.
* **Guest Limits:** Daily diagnosis limits should be enforced.

### F10. Admin Dashboard

* **Description:** Admin-only functionality.
* **Features:** Total Users, Total Diagnoses, Popular Diseases, Recent Activity Logs.

---

## 8. Non-Functional Requirements

* **Performance:**
* Prediction response under 10 seconds.
* API response under 2 seconds excluding AI calls.
* Mobile-first design.


* **Security:**
* JWT Authentication & Password hashing.
* Input and File upload validation.
* Role-based access control.


* **Scalability:**
* Architecture should support additional crops, diseases, and AI providers without major redesign.


* **Reliability:**
* Graceful API error handling.
* Logging of failures.
* User-friendly error messages.



---

## 9. User Journey

### Guest Flow

`Landing Page` → `Upload Page` → `Select Crop` → `Upload Image` → `Analyze` → `View Results` → `Download Report`

### Authenticated User Flow

`Landing Page` → `Login` → `Upload Image` → `Analyze` → `View Results` → `Open AI Assistant` → `Ask Questions` → `Download Report` → `View History`

---

## 10. Data Retention Policy

* **Guest Users:** Uploaded images deleted after analysis. No history retained.
* **Authenticated Users:** Images retained temporarily. Automatic deletion after retention period.
* *Recommended retention period:* **180 Days**



---

## 11. Out of Scope (V1)

The following features are intentionally excluded:

* Mobile Application
* Drone Integration & Satellite Imagery
* Weather Forecasting
* Marketplace Features (Fertilizer E-Commerce, Expert Consultation Marketplace)
* Real-Time Disease Monitoring
* Multi-Crop Disease Expansion Beyond Current Dataset
* Voice Assistant
* Offline Mode

---

## 12. Future Roadmap

* **V1.1:** Google OAuth, Additional Crops, Additional Diseases
* **V1.2:** Multilingual Expansion, Advanced Analytics, Improved Recommendation Engine
* **V2.0:** Weather Integration, Seasonal Crop Advisory, Expert Consultation Module, Advanced Agricultural Knowledge Base

---

## 13. Definition of Done

AgroGuard V1 is considered complete when the following are operational and implemented:

* [x] Frontend deployed.
* [x] Backend deployed.
* [x] Disease prediction operational.
* [x] Authentication operational.
* [x] AI assistant operational.
* [x] Report generation operational.
* [x] Scan history operational.
* [x] Admin dashboard operational.
* [x] Security validations implemented.
* [x] End-to-end workflow demonstrated successfully.