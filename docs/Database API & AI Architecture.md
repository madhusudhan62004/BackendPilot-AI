
# BackendPilot AI — Database, API & AI Architecture

**Version:** 0.1  
**Status:** Draft  
**Author:** Madhusudhan M  
**Last Updated:** August 2026

---

# 1. Overview

This document defines the initial database structure, API design, and AI architecture for BackendPilot AI.

The system combines:

```text
Structured Repository Knowledge
            +
Semantic Knowledge
            +
LLM Reasoning
````

---

# 2. MongoDB Design

MongoDB is the primary application database.

### Initial Collections

```text
users
projects
repositories
files
code_entities
relationships
conversations
messages
jobs
analysis_results
```

### Core Relationships

```text
User
 └── Projects
       └── Repository
             ├── Files
             ├── Code Entities
             ├── Relationships
             ├── Jobs
             └── Analysis Results

Project
 └── Conversations
       └── Messages
```

### Code Relationships

Relationships will represent connections such as:

```text
CALLS
IMPORTS
EXPOSES
USES
ACCESSES
DEPENDS_ON
TRIGGERS
```

Example:

```text
OrderController
      ↓ CALLS
OrderService
      ↓ CALLS
PaymentService
```

---

# 3. API Design

BackendPilot will initially expose REST APIs through FastAPI.

## Authentication

```http
POST /auth/register
POST /auth/login
GET  /auth/me
```

## Projects

```http
POST   /projects
GET    /projects
GET    /projects/{id}
PATCH  /projects/{id}
DELETE /projects/{id}
```

## Repositories

```http
POST   /projects/{id}/repositories/upload
POST   /projects/{id}/repositories/github
GET    /repositories/{id}
POST   /repositories/{id}/reindex
DELETE /repositories/{id}
```

## Processing

```http
GET /jobs/{job_id}
```

Repository processing will be asynchronous.

```text
Upload
  ↓
Create Job
  ↓
Background Processing
  ↓
Repository Ready
```

## System Intelligence

```http
GET  /repositories/{id}/system-map
GET  /repositories/{id}/entities
GET  /repositories/{id}/relationships
GET  /repositories/{id}/flows
POST /repositories/{id}/chat
POST /repositories/{id}/impact-analysis
```

The exact API contracts will be refined during implementation.

---

# 4. AI Architecture

BackendPilot uses three forms of repository knowledge:

```text
Structured Knowledge
        +
Relationship Knowledge
        +
Semantic Knowledge
```

---

## Structured Knowledge

Generated through deterministic code analysis.

Examples:

* Files
* Functions
* Classes
* APIs
* Imports
* Services

---

## Relationship Knowledge

Represented through the System Model / graph.

Example:

```text
OrderController
      ↓
OrderService
      ↓
PaymentService
```

Used for:

* Dependency exploration
* Flow reconstruction
* Impact analysis

---

## Semantic Knowledge

Repository content is converted into embeddings.

```text
Source Code
    ↓
Chunking
    ↓
Embedding Model
    ↓
Vector Store
```

---

# 5. RAG Pipeline

BackendPilot will use repository-aware RAG.

```text
User Question
      ↓
Query Processing
      ↓
┌─────────────────┐
│                 │
▼                 ▼
Vector Search   Graph Retrieval
│                 │
└────────┬────────┘
         ↓
   Context Builder
         ↓
        LLM
         ↓
 Answer + Sources
```

This is a **hybrid retrieval** approach.

Vector retrieval provides semantic relevance, while graph retrieval provides structural relationships.

---

# 6. Example

User asks:

> How does order creation work?

The system performs:

```text
Question
   ↓
Identify /orders API
   ↓
Graph Traversal
   ↓
Find Related Components
   ↓
Retrieve Relevant Code
   ↓
Build Context
   ↓
LLM Reasoning
   ↓
System-Level Explanation
```

Possible answer:

```text
POST /orders
     ↓
OrderController
     ↓
OrderService
     ↓
InventoryService
     ↓
PaymentService
     ↓
OrderRepository
     ↓
MongoDB
```

Relevant source files should be provided with the response.

---

# 7. Impact Analysis

Impact analysis combines graph traversal, source retrieval, and LLM reasoning.

```text
Selected Component
        ↓
Dependency Graph
        ↓
Affected Components
        ↓
Relevant Code
        ↓
LLM
        ↓
Impact Report
```

Example:

```text
PaymentService
├── OrderService
├── RefundService
├── PaymentRepository
└── Payment Tests
```

---

# 8. AI Reliability

The system should minimize hallucinations through:

* Repository-grounded retrieval
* Source references
* Structured system information
* Graph relationships
* Explicit uncertainty
* Retrieval evaluation

The system should distinguish between:

```text
Observed from Code
        vs
AI Inferred
```

---

# 9. Agent Architecture

Agents are **not part of the initial MVP**.

Initial architecture:

```text
Repository
    ↓
System Model
    ↓
RAG
    ↓
LLM
```

Later:

```text
User Request
      ↓
Agent / Planner
      ↓
Specialized Analysis
      ↓
RAG + Graph + Tools
      ↓
LLM
      ↓
Final Result
```

This keeps the initial system simpler and allows agentic capabilities to be added after the core intelligence layer is reliable.

---

# 10. Technology Stack

| Area            | Technology         |
| --------------- | ------------------ |
| Backend         | Python + FastAPI   |
| Database        | MongoDB            |
| Cache           | Redis              |
| Code Analysis   | AST / Tree-sitter  |
| Vector Store    | TBD                |
| LLM             | TBD                |
| Embeddings      | TBD                |
| Background Jobs | TBD                |
| Frontend        | React + TypeScript |
| Deployment      | Docker             |
| Version Control | Git + GitHub       |

---

# 11. Core Principle

> **Use deterministic methods to establish facts; use AI to interpret and reason over those facts.**

BackendPilot therefore follows:

```text
Repository
    ↓
Code Analysis
    ↓
System Model
    +
Semantic Index
    ↓
Hybrid Retrieval
    ↓
LLM
    ↓
System Intelligence
```

The goal is not simply to build a repository chatbot.

The goal is to build an **AI-powered system understanding layer for backend developers**.

```
```
