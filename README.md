# Enterprise Expense Claim Workflow System

## Overview

The Enterprise Expense Claim Workflow System is a backend workflow management platform built using Django, Django REST Framework (DRF), and PostgreSQL.

The system enables employees to create and submit expense claims while supporting a structured enterprise approval workflow involving:

- Employees
- Reviewers
- Finance Controllers

The application also includes:

- JWT Authentication
- Role-Based Access Control (RBAC)
- Evidence Upload Management
- Duplicate Evidence Detection using SHA256 hashing
- Audit Logging
- Claim Status History Tracking
- Enterprise Workflow Lifecycle Management

---

# Technology Stack

| Technology | Purpose |
|------------|----------|
| Python 3.x | Backend Language |
| Django | Web Framework |
| Django REST Framework | REST APIs |
| PostgreSQL | Database |
| JWT (SimpleJWT) | Authentication |
| drf-spectacular | Swagger/OpenAPI Documentation |

---

# Project Architecture

enterprise_expense_system/

├── claims/

│ ├── models/

│ ├── serializers/

│ ├── services/

│ ├── selectors/

│ ├── permissions/

│ ├── views/

│ ├── migrations/

│ └── urls.py

│

├── config/

│ ├── settings.py

│ ├── urls.py

│ └── wsgi.py

│

├── manage.py

├── requirements.txt

└── README.md

---

# Core Features

## Authentication & Authorization

### JWT Authentication

The system uses JWT-based authentication with:

- Access Tokens
- Refresh Tokens

### Role-Based Access Control (RBAC)

Supported roles:

| Role | Permissions |
|------|-------------|
| EMPLOYEE | Create and submit claims |
| REVIEWER | Approve, reject, request changes |
| CONTROLLER | Finalize approved claims |

---

# Claim Workflow Lifecycle

## Supported Workflow States

- DRAFT
- SUBMITTED
- RESUBMITTED
- APPROVED
- REJECTED
- CHANGES_REQUESTED
- FINALIZED

---

# Workflow Diagram

DRAFT

↓

SUBMITTED

↓

APPROVED

↓

FINALIZED

Alternative review paths:

SUBMITTED

↓

REJECTED

SUBMITTED

↓

CHANGES_REQUESTED

↓

RESUBMITTED

---

# Evidence Management

## Features

- File upload support
- Immutable evidence storage
- SHA256 hash generation
- Duplicate evidence detection
- Fraud tracking using reuse flags

---

# Duplicate Evidence Detection

When evidence files are uploaded:

1. SHA256 hash is generated
2. Existing hashes are checked
3. Duplicate files are flagged automatically
4. Audit logs are created

This helps detect:

- Duplicate invoices
- Reused receipts
- Fraudulent submissions

---

# Audit Logging

The system maintains complete audit trails for:

- Claim creation
- Claim submission
- Approval actions
- Rejections
- Evidence uploads
- Duplicate evidence detection
- Finalization actions

---

# Status History Tracking

Every workflow transition is stored in:

ClaimStatusHistory

This ensures:

- Workflow traceability
- Historical visibility
- Enterprise audit compliance

---

# API Endpoints

## Authentication APIs

### Login

POST /auth/login/

### Refresh Token

POST /auth/refresh/

---

# Claim APIs

## Create Claim

POST /api/claims/

### Request Body

```json
{
  "amount": "500.00",
  "description": "Travel reimbursement",
  "purpose": "Client meeting"
}