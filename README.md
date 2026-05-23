# Enterprise Expense Claim Workflow System

## Overview

The Enterprise Expense Claim Workflow System is a backend workflow management platform built using Django, Django REST Framework (DRF), PostgreSQL, and JWT Authentication.

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
- Optimistic Concurrency Handling
- Database Indexing
- Pagination Support
- Celery-ready Asynchronous Processing
- Fraud Detection Support

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
| Celery | Background Task Processing |
| Redis | Celery Broker / Async Queue |

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

│ ├── tasks/

│ ├── validators/

│ ├── compliance/

│ ├── migrations/

│ └── urls.py

│

├── config/

│ ├── settings.py

│ ├── celery.py

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

# Employee / Reviewer / Controller Responsibilities

## Employee

Employees can:

- Create claims
- View own claims
- Upload evidence
- Submit claims
- Resubmit claims after requested changes

Employees cannot:

- Approve claims
- Reject claims
- Finalize claims

---

## Reviewer

Reviewers can:

- Approve claims
- Reject claims
- Request changes

Reviewers cannot:

- Create claims
- Submit claims
- Finalize claims

---

## Controller

Controllers can:

- Finalize approved claims

Controllers cannot:

- Create claims
- Approve claims
- Reject claims

---

# Evidence Management

## Features

- File upload support
- Immutable evidence storage
- SHA256 hash generation
- Duplicate evidence detection
- Fraud tracking using reuse flags

---

# High-Volume Evidence Processing

Evidence uploads are processed using chunk-based SHA256 hashing instead of loading entire files into memory.

Benefits:

- Reduced memory consumption
- Better handling of large uploads
- Improved concurrency support
- Scalable upload processing

Duplicate evidence detection is designed using asynchronous processing concepts to prevent expensive fraud-analysis operations from blocking upload requests.

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

# Scalability & Production-Oriented Features

The system architecture was designed with enterprise scalability and maintainability considerations.

Implemented scalability-focused improvements include:

- Database indexing for optimized query performance
- Optimistic concurrency/version handling
- Transaction-safe workflow execution
- Pagination support for large datasets
- Chunk-based file hashing for memory-efficient uploads
- Asynchronous duplicate evidence analysis using Celery-ready architecture
- Modular service-layer architecture for future horizontal scaling
- Audit-safe immutable evidence storage
- Reusable selectors for centralized query optimization

These improvements help support high-volume enterprise workflows and large-scale claim processing systems.

---

# Concurrency Handling

The system includes optimistic concurrency handling using version-based workflow updates.

This prevents:

- Multiple reviewers modifying the same claim simultaneously
- Workflow race conditions
- Lost updates during concurrent operations

Workflow transitions are executed using transactional database operations for consistency and reliability.

---

# Asynchronous Processing

The architecture includes Celery-ready asynchronous task integration for scalable background processing.

Example use cases:

- Duplicate evidence analysis
- Fraud detection workflows
- Notification systems
- Compliance checks
- Heavy audit processing

This prevents long-running operations from increasing API response latency under high concurrency.

---

# Database Optimizations

Implemented database optimizations include:

- Indexed claim status lookups
- Indexed employee-based filtering
- Indexed audit log queries
- Indexed evidence hash lookups
- Indexed workflow history retrieval
- Indexed fraud/reuse tracking

These optimizations improve query performance for large-scale enterprise workloads.

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