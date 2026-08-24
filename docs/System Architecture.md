
# BackendPilot AI — System Architecture

**Version:** 0.1  
**Status:** Draft  
**Author:** Madhusudhan M  
**Last Updated:** August 2026

---

# 1. Architecture Overview

BackendPilot AI follows a **modular monolith architecture** initially.

The system is built around the principle:

> **Deterministic analysis builds the system model; AI reasons over that model.**

High-level flow:

```text
Frontend
    ↓
FastAPI Backend
    ↓
Repository Processing
    ↓
Code Analysis
    ↓
System Model
    ↓
┌─────────────────┬─────────────────┐
│                 │                 │
MongoDB       Vector Store       System Graph
│                 │                 │
└─────────────────┬─────────────────┘
                  ↓
             AI / RAG Layer
                  ↓
                 LLM
                  ↓
        System-Level Intelligence
````

---

# 2. Major Components

## Frontend

Responsible for:

* Dashboard
* System Map
* Flow Explorer
* Dependency Explorer
* AI Assistant
* Impact Analysis

Initial technology: **React + TypeScript**

---

## FastAPI Backend

Acts as the main application layer.

Major modules:

```text
auth
projects
repositories
analysis
system_model
search
ai
conversations
jobs
```

---

## Repository Processing

Responsible for converting a repository into structured information.

```text
Repository
    ↓
Extraction
    ↓
File Discovery
    ↓
Filtering
    ↓
Parsing
    ↓
Entity Extraction
    ↓
Relationship Extraction
```

---

## Code Analysis

Uses AST/parser-based analysis wherever possible.

The system extracts:

* Functions
* Classes
* Imports
* APIs
* Services
* Dependencies
* Database interactions

This provides reliable structural information without unnecessarily relying on an LLM.

---

## System Model

The core knowledge representation of BackendPilot.

Example:

```text
POST /orders
      ↓
OrderController
      ↓
OrderService
   ┌──┴──────┐
   ↓         ↓
Payment   Inventory
Service   Service
      ↓
   MongoDB
```

The System Model enables:

* Dependency exploration
* Flow reconstruction
* Architecture visualization
* Impact analysis

---

## MongoDB

Primary application and repository database.

Potential data:

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

---

## Vector Store

Stores embeddings for semantic retrieval.

```text
Code
 ↓
Chunks
 ↓
Embeddings
 ↓
Vector Store
```

Used by the RAG layer to find semantically relevant repository content.

The exact vector technology will be decided during implementation.

---

## AI / RAG Layer

Combines structured and semantic knowledge.

```text
User Question
      ↓
Vector Retrieval + Graph Retrieval
      ↓
Context Builder
      ↓
LLM
      ↓
Answer + Source References
```

RAG is treated as an **AI capability**, not the entire product.

---

## Redis

Used where fast temporary storage or caching is useful.

Potential uses:

* Response caching
* Job state
* Frequently accessed results
* Temporary processing state

---

## Background Workers

Long-running repository operations should run asynchronously.

```text
Upload Repository
      ↓
Create Job
      ↓
Background Worker
      ↓
Parse
      ↓
Analyze
      ↓
Index
      ↓
System Ready
```

---

# 3. Complete Data Flow

```text
                Repository
                    ↓
             Repository Parser
                    ↓
             AST / Code Analysis
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
     Code Entities       Relationships
          │                   │
          └─────────┬─────────┘
                    ↓
              System Model
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
      MongoDB            Vector Store
          │                   │
          └─────────┬─────────┘
                    ↓
               RAG / Retrieval
                    ↓
                   LLM
                    ↓
          System-Level Answer
```

---

# 4. Key Architecture Principle

BackendPilot should **not** follow:

```text
ZIP → LLM → Chat
```

Instead:

```text
Repository
    ↓
Deterministic Analysis
    ↓
Persistent System Model
    +
Semantic Knowledge
    ↓
AI Reasoning
```

The system therefore separates:

**Facts** → determined through code analysis

**Relationships** → represented through the system model

**Meaning & Reasoning** → handled by AI

---

# 5. Initial Technology Stack

| Layer            | Technology         |
| ---------------- | ------------------ |
| Frontend         | React + TypeScript |
| Backend          | Python + FastAPI   |
| Database         | MongoDB            |
| Cache            | Redis              |
| Code Analysis    | AST / Tree-sitter  |
| Vector Store     | TBD                |
| LLM              | TBD                |
| Embeddings       | TBD                |
| Background Jobs  | TBD                |
| Containerization | Docker             |
| Version Control  | Git + GitHub       |

---

# 6. Architecture Evolution

### V0.1

```text
React → FastAPI → MongoDB → Repository Parser
```

### V0.2

```text
System Model
     +
Vector Search
     ↓
RAG
     ↓
LLM
```

### V0.3+

```text
Redis
+
Background Workers
+
Evaluation
+
Observability
```

### V1.0+

```text
System Intelligence
+
Agentic Workflows
+
Runtime Analysis
```

The architecture will evolve based on actual implementation findings rather than introducing unnecessary complexity upfront.
