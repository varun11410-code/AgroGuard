# AgroGuard - Frontend Specification Document

Version: 1.0

Status: Approved

---

# 1. Purpose

This document defines the complete frontend design system, user experience, visual identity, layout structure, animations, components, responsiveness, and interaction behavior for AgroGuard.

This document serves as the UI/UX source of truth.

Any frontend implementation must follow this specification.

---

# 2. Design Philosophy

AgroGuard should feel:

* Modern
* Professional
* Premium
* Trustworthy
* Agriculture-focused
* AI-powered

The application should not look like:

* A college project
* A dashboard template
* A generic Bootstrap website

The visual experience should communicate:

> Modern Agriculture + Artificial Intelligence

---

# 3. Visual Theme

## Theme Name

EcoTech Glass

---

## Primary Colors

Deep Green

```css
#166534
```

---

Leaf Green

```css
#22C55E
```

---

Soft Green

```css
#DCFCE7
```

---

## Neutral Colors

Background White

```css
#F8FAFC
```

Text Dark

```css
#0F172A
```

Border Gray

```css
#E2E8F0
```

---

## Status Colors

Success

```css
#22C55E
```

Warning

```css
#F59E0B
```

Error

```css
#EF4444
```

---

# 4. Typography

## Font Family

Primary

```text
Inter
```

Fallback

```text
sans-serif
```

---

## Headings

H1

48px

Bold

---

H2

36px

Semi-Bold

---

H3

28px

Semi-Bold

---

## Body

16px

Regular

---

# 5. Design Language

## Core Style

Glassmorphism

Components should use:

* Blur
* Transparency
* Soft shadows
* Rounded corners

---

Example

```css
background:
rgba(255,255,255,0.15)

backdrop-filter:
blur(12px)
```

---

## Card Radius

```css
border-radius: 24px;
```

---

## Buttons

Rounded

Large

High contrast

---

# 6. Animation Principles

Animations must feel:

* Smooth
* Natural
* Lightweight

Not:

* Distracting
* Overused

---

Framework

Framer Motion

---

# 7. Global Background

## Main Theme

Animated Nature Background

Includes:

* Floating leaves
* Gentle movement
* Subtle gradients

---

Requirements

Must not affect performance.

Target:

60 FPS

---

# 8. Landing Page Specification

Route

```text
/
```

---

## Hero Section

Full viewport height.

Contains:

* AgroGuard Logo
* Headline
* Description
* CTA Buttons

---

Headline

Example:

```text
AI-Powered Crop Disease Detection & Agricultural Assistance
```

---

CTA Buttons

Primary

```text
Get Started
```

Secondary

```text
Learn More
```

---

## Hero Visual

3D Plant Model

OR

Animated Plant Illustration

Position:

Right side on desktop

Top section on mobile

---

## Supported Crops Section

Display:

* Tomato
* Potato

Include notice:

```text
Currently supported crops in Version 1.
```

---

## How It Works Section

Step 1

Upload Image

---

Step 2

AI Analysis

---

Step 3

Get Recommendations

---

Step 4

Download Report

---

## Features Section

Cards

* Disease Detection
* AI Assistant
* PDF Reports
* Scan History

---

## Footer

Contains:

* Copyright
* GitHub
* Contact

---

# 9. Authentication Pages

Routes

```text
/login
/register
```

---

Layout

Centered Card

Glassmorphism style

---

Fields

Login

* Email
* Password

---

Register

* Name
* Email
* Password

---

Buttons

Primary Green

---

# 10. Upload Page

Route

```text
/upload
```

---

Layout

Centered container

---

Section 1

Crop Selection

Display:

* Tomato Card
* Potato Card

Only one selectable.

---

Section 2

Image Upload

Supports:

* Click Upload
* Drag & Drop

---

Section 3

Analyze Button

Large primary button.

---

# 11. Loading Experience

After Analyze

Show multi-step loading.

---

Stage 1

```text
Uploading Image...
```

---

Stage 2

```text
Analyzing Disease...
```

---

Stage 3

```text
Generating Recommendations...
```

---

Stage 4

```text
Preparing Results...
```

---

Estimated duration display optional.

---

# 12. Results Page

Route

```text
/results/[id]
```

---

Layout

Multi-card structure.

---

Card 1

Prediction Summary

Contains:

* Disease
* Confidence Score

---

Card 2

Uploaded Image

Preview image.

---

Card 3

AI Summary

Disease explanation.

---

Card 4

Treatment Plans

---

Budget Plan

---

Standard Plan

---

Premium Plan

---

Each card contains:

* Cost Level
* Example Product
* Application Guidance
* Prevention Tips

---

Card 5

Actions

Buttons:

* Download Report
* Open AI Assistant

---

# 13. AI Assistant Widget

Position

Bottom Right

Fixed

Visible on every page.

---

Behavior

Collapsed by default.

---

On Click

Open chat window.

---

Size

Desktop

420px width

---

Mobile

Full-screen modal

---

Features

* Chat history
* Typing indicator
* Auto-scroll
* Loading animation

---

Restrictions

Guest users:

Show login prompt.

---

# 14. Profile Page

Route

```text
/profile
```

---

Sections

User Information

---

Language Preference

Options:

* English
* Hindi

---

Budget Preference

Options:

* Budget
* Standard
* Premium

---

Account Information

---

# 15. History Page

Route

```text
/history
```

---

Display

Diagnosis Cards

---

Each Card

* Crop
* Disease
* Confidence
* Date

---

Actions

* View Report
* Delete Record

---

# 16. Admin Dashboard

Route

```text
/admin
```

---

Layout

Analytics Dashboard

---

Widgets

Total Users

---

Total Scans

---

Most Common Disease

---

Recent Activity

---

Charts

Simple modern charts.

Avoid excessive complexity.

---

# 17. Mobile Responsiveness

Priority Order

1. Mobile
2. Tablet
3. Desktop

---

Breakpoints

Mobile

```css
< 768px
```

---

Tablet

```css
768px - 1024px
```

---

Desktop

```css
> 1024px
```

---

# 18. Accessibility Requirements

Every page must:

* Support keyboard navigation
* Use semantic HTML
* Include labels
* Maintain contrast ratios

---

# 19. Empty States

History Empty

```text
No scans available yet.
Analyze your first crop image.
```

---

Reports Empty

```text
No reports generated yet.
```

---

# 20. Error States

Upload Failure

```text
Unable to upload image.
Please try again.
```

---

Prediction Failure

```text
Analysis failed.
Please retry.
```

---

API Failure

```text
Something went wrong.
Please try again later.
```

---

# 21. Performance Requirements

Lighthouse Targets

Performance

90+

---

Accessibility

90+

---

Best Practices

90+

---

SEO

85+

---

# 22. Frontend Definition of Done

The frontend is complete when:

✓ Landing Page implemented

✓ Authentication implemented

✓ Upload Workflow implemented

✓ Results Page implemented

✓ AI Widget implemented

✓ History implemented

✓ Profile implemented

✓ Admin Dashboard implemented

✓ Mobile responsive

✓ Accessibility compliant

✓ Lighthouse goals achieved

✓ Matches Frontend Specification Document
