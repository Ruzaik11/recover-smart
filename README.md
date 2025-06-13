# Recover Smart – Backend API

**Capstone Project – Fanshawe College (2023–2024)**  
Recover Smart is a Django-based backend system designed to support post-surgery recovery tracking for patients and healthcare professionals.

---

## 🧠 Overview

This backend service provides secure API endpoints to manage patients, clinicians, recovery plans, and symptom tracking. Built with Django and Django REST Framework, it enables structured, data-driven recovery support.

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **Django 4.x**
- **Django REST Framework**
- **PostgreSQL**
- **Docker & Docker Compose**

---

## 🔐 Key Features

- **User Authentication & Roles**  
  Supports login for patients and clinicians with JWT-based authentication.

- **Patient Management**  
  Create, update, and assign recovery plans to patients.

- **Daily Check-ins**  
  Endpoints for submitting recovery surveys (e.g., pain levels, mobility).

- **Clinician Dashboard APIs**  
  Access aggregated data and recent check-in logs.

- **Secure REST API**  
  Built using DRF with token-based permissions and input validation.

---

## 🚀 Getting Started

### Prerequisites

- Docker + Docker Compose
- Git

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/recover-smart-backend.git
cd recover-smart-backend

# Build and run the containers
docker-compose up --build

# API will be available at http://localhost:8000/api/
