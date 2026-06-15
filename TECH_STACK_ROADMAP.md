# NoticeFlow Technology Stack & Implementation Roadmap

## Part 0: Current State vs. Recommended Stack

### What You Have Right Now (MVP)
```
Frontend:    Streamlit (perfect for MVP)
Backend:     process_notice.py (Python functions)
OCR:         Azure fallback to GPT Vision
LLM:         GPT-4o
DB:          None (stateless)
Hosting:     Streamlit Cloud
```

**Status:** ✅ Correct for Phase 1 validation

---

### Recommended Path Forward

```
Phase 1 (Now):    Keep as-is (Streamlit)
Phase 2:          Add FastAPI backend + PostgreSQL
Phase 3:          Scale to Next.js frontend
Phase 4+:         Add vector DB + advanced RAG
```

---

# Part 1: Why This Stack (The Real Reasoning)

## The Constraint Matrix

| Need | Tool | Why NOT Others |
|------|------|---------|
| **Fast iteration** | Python | Node.js is verbose for AI orchestration |
| **LLM integration** | FastAPI | Django is bloated; Flask is too minimal |
| **Structured JSON handling** | FastAPI | Perfect async support for LLM calls |
| **Quick validation** | Streamlit | Web framework adds 2+ weeks of work |
| **Scalable frontend** | Next.js | Vue/Svelte harder to find engineers; Streamlit has limits |
| **Data reliability** | PostgreSQL | MongoDB loses you referential integrity |
| **Debuggability** | Python everywhere | Microservices hide behavior |

---

## What You're Really Optimizing For

```
Phase 1-2: Speed of building
  → Python monolith beats microservices

Phase 2-3: Iteration on LLM behavior
  → LangSmith + OpenAI logs beats Datadog

Phase 3-4: Correctness first
  → PostgreSQL + structured outputs beats NoSQL

Phase 4+: Only then scale
  → Vector DB for similar case retrieval
```

---

# Part 2: Exact Stack by Phase

## Phase 1 (MVP - Current)

```yaml
Frontend:
  Framework: Streamlit
  Deployment: Streamlit Cloud (free tier)
  
Backend:
  Language: Python 3.11
  Framework: None (direct functions)
  Structure: process_notice.py
  
Processing:
  OCR: Azure Document Intelligence + GPT-4o Vision
  LLM: OpenAI GPT-4o
  
Storage:
  Database: None (stateless)
  Files: Memory (uploaded file)
  
Deployment:
  Server: Streamlit Cloud
  Cost: Free
```

**Total development time:** 1 week ✓

---

## Phase 2 (Add Persistence + Backend)

```yaml
Frontend:
  Framework: Streamlit (no change)
  Deployment: Streamlit Cloud
  
Backend:
  Language: Python 3.11
  Framework: FastAPI
  Structure:
    ├─ app.py (routes)
    ├─ orchestrator.py (workflow)
    ├─ agents/ (extraction, classification, etc)
    ├─ schemas.py (JSON validation)
    └─ models.py (DB models)
  
Processing:
  OCR: Azure Document Intelligence + GPT-4o Vision
  LLM: GPT-4o (with fallback to Claude)
  Logging: LangSmith (debugging)
  
Storage:
  Database: PostgreSQL
  Migrations: Alembic
  Vector DB: None yet
  Files: AWS S3 (or Supabase)
  
Deployment:
  Backend: Render.com (or Railway)
  Database: Render Postgres
  Cost: $50-100/month
```

**Total development time:** 2-3 weeks

---

## Phase 3 (Scale Frontend + Orchestration)

```yaml
Frontend:
  Framework: Next.js 14 (React)
  Styling: TailwindCSS
  State: React Query
  Auth: NextAuth.js (later)
  Deployment: Vercel
  
Backend:
  Framework: FastAPI (enhanced)
  Structure:
    ├─ api/
    │  ├─ notices/
    │  ├─ clients/
    │  └─ results/
    ├─ orchestrator/
    ├─ agents/
    ├─ schemas/
    └─ observability/
  Async: Celery (optional)
  
Processing:
  OCR: Azure Document Intelligence
  LLM: GPT-4o + Claude (role-based routing)
  Retrieval: SQLAlchemy ORM + vector search
  
Storage:
  Database: PostgreSQL
  Vector DB: pgvector (built-in to Postgres)
  Files: AWS S3
  Cache: Redis (optional)
  
Monitoring:
  Logging: LangSmith + Sentry
  Metrics: Prometheus (optional)
  
Deployment:
  Frontend: Vercel
  Backend: AWS ECS or Railway
  Database: AWS RDS
  Cost: $200-400/month
```

**Total development time:** 4-6 weeks

---

## Phase 4+ (Enterprise Features)

```yaml
Frontend:
  Framework: Next.js + TypeScript
  UI: Design system (shadcn/ui)
  Mobile: React Native (later)
  
Backend:
  Framework: FastAPI + async workers
  Structure: Full microservices ready (but not doing it yet)
  
Processing:
  LLM: Multi-model orchestration
  RAG: Vector search + similarity
  
Storage:
  Database: PostgreSQL + read replicas
  Vector: Pinecone or Weaviate (scale-out)
  
Deployment:
  Infrastructure: Kubernetes (now justified)
  Cost: $1000+/month
```

---

# Part 3: Technology Decisions (Current MVP)

## 3.1 Frontend: Streamlit ✅

### Why It's Perfect for Phase 1
- ✅ Zero frontend engineering
- ✅ Deploy in 2 minutes
- ✅ Built-in file upload
- ✅ Automatic mobile responsive
- ✅ Easy to iterate
- ✅ Free tier covers MVP

### When to Replace (Phase 3)
```
IF:
  - ≥100 active users
  OR user base > 3 firms
  OR need user authentication
  OR need multi-page dashboard

THEN:
  - Build Next.js frontend
  - Keep Streamlit for admin tools (optional)
```

### Migration Path
```
Streamlit (MVP) → Next.js (Phase 3)
  ↓
Same FastAPI backend
  ↓
No business logic changes
```

---

## 3.2 Backend: FastAPI (Phase 2) ✅

### Current State
Your `process_notice.py` is perfect phase 1.

### Phase 2 Evolution

```python
# Phase 1 (now): process_notice.py
def process_notice(uploaded_file):
    text = extract_ocr(uploaded_file)
    result = parse_with_gpt4(text)
    return result

# Phase 2: FastAPI backend
from fastapi import FastAPI, UploadFile, File
from orchestrator import run_notice_pipeline

app = FastAPI()

@app.post("/api/notices/process")
async def process_notice(file: UploadFile = File(...)):
    result = await run_notice_pipeline(file)
    return result

@app.get("/api/notices/{notice_id}")
async def get_notice(notice_id: str):
    return db.query(Notice).filter(Notice.id == notice_id).first()
```

### Why FastAPI (Not Django, Flask, etc.)

| Aspect | FastAPI | Django | Flask | Node |
|--------|---------|--------|-------|------|
| LLM async | ✅ Native | ⚠ Complex | ⚠ Complex | ⚠ JS semantics |
| JSON handling | ✅ Perfect | ✅ Good | ⚠ Manual | ⚠ Verbose |
| Type hints | ✅ Built-in | ⚠ Optional | ✗ No | ✗ No |
| Startup speed | ✅ Fast | ⚠ Slow | ✅ Fast | ✅ Fast |
| AI pipeline code | ✅ Clean | ⚠ ORM heavy | ✅ Simple | ⚠ Callback hell |
| Team hiring | ✅ Easy | ✅ Easy | ⚠ Many variations | ✅ Easy |

---

## 3.3 OCR: Hybrid Strategy ✅

### Current (MVP)
```python
def extract_ocr(file):
    try:
        # Primary: Azure Document Intelligence
        return azure_extract(file)
    except:
        try:
            # Fallback 1: PyPDF2
            return pdf_extract(file)
        except:
            # Fallback 2: GPT-4o Vision
            return gpt_vision_extract(file)
```

**Status:** ✅ Correct, keep as-is

### Cost Optimization
```
Azure: $2-5 per 1000 pages (cheapest at scale)
GPT Vision: $0.03 per image
PyPDF2: Free

Strategy:
- 90% uses Azure (cheapest for good scans)
- 10% falls back to vision (only for bad scans)
- Expected cost: $0.002 per notice
```

---

## 3.4 LLM: GPT-4o (Primary) ✅

### Current (MVP)
```python
def parse_with_gpt4(text):
    return client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": FBR_SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )
```

**Status:** ✅ Correct

### Phase 2: Add Claude Fallback

```python
def parse_notice(text):
    try:
        # Primary: GPT-4o (fastest for extraction)
        return gpt_parse(text)
    except:
        # Fallback: Claude (longer context, different strength)
        return claude_parse(text)

def draft_response(context):
    # Claude better for drafting (Phase 4)
    return claude_draft(context)
```

### Cost Analysis
```
GPT-4o:     $0.15 per 1000 input tokens
Claude:     $0.003 per 1000 input tokens
GPT-4o mini: $0.05 per 1000 input tokens

Strategy:
- Use GPT-4o for extraction (best performance)
- Use GPT-4o-mini for simple classification (cheaper)
- Reserve Claude for drafting (different style needed)

Expected cost per notice:
- Input tokens: ~2000 (notice text)
- Output tokens: ~500 (structured response)
- Total: ~$0.35/notice
```

---

## 3.5 Database: PostgreSQL (Phase 2)

### Phase 1: None ✓
(Stateless is correct for MVP)

### Phase 2: PostgreSQL

```sql
-- Core tables

CREATE TABLE notices (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255),
  raw_text TEXT,
  extracted_json JSONB,
  section VARCHAR(20),
  deadline DATE,
  created_at TIMESTAMP
);

CREATE TABLE clients (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255),
  name VARCHAR(255),
  tax_id VARCHAR(20),
  created_at TIMESTAMP
);

CREATE TABLE notice_results (
  id UUID PRIMARY KEY,
  notice_id UUID REFERENCES notices(id),
  explanation TEXT,
  checklist JSONB,
  deadline_urgency VARCHAR(20),
  created_at TIMESTAMP
);

CREATE TABLE failure_cases (
  id UUID PRIMARY KEY,
  notice_id UUID REFERENCES notices(id),
  failure_type VARCHAR(100),
  created_at TIMESTAMP
);
```

### Why PostgreSQL
- ✅ Structured relational data (references matter)
- ✅ Built-in vector support (Phase 3+)
- ✅ JSONB for flexible extraction results
- ✅ Excellent with Python ORMs
- ✅ Standard across industry (easy hiring)

---

## 3.6 Deployment: Streamlit Cloud (Phase 1) → Render (Phase 2)

### Phase 1 (Now)
```
Streamlit Cloud (free tier)
- Automatic deploys from GitHub
- No backend needed
- 1GB RAM (enough for MVP)
```

### Phase 2 (After validation)
```
Frontend:    Streamlit Cloud (unchanged)
Backend:     Render.com
Database:    Render Postgres
Files:       AWS S3 (free tier)

Total cost: ~$50-70/month
```

### Phase 3 (Scale)
```
Frontend:    Vercel (Next.js)
Backend:     AWS ECS or Railway
Database:    AWS RDS
Files:       AWS S3
Vector DB:   pgvector in Postgres

Total cost: ~$200-400/month
```

---

# Part 4: Avoiding Common Mistakes

## ❌ Mistake 1: Microservices Too Early

```
WRONG (Phase 2):
├─ ocr-service
├─ classification-service
├─ extraction-service
└─ checklist-service

RIGHT (Phase 2):
Single FastAPI app with:
├─ /api/notices/process
├─ /api/results/{id}
└─ /api/checklists/{id}
```

**When to split:** Only when single server gets >80% CPU

---

## ❌ Mistake 2: Complex Orchestration Too Early

```
WRONG (Phase 2):
Use Temporal / Airflow / Kafka

RIGHT (Phase 2):
def orchestrate(file):
    ocr_text = extract_ocr(file)
    classification = classify(ocr_text)
    deadline = extract_deadline(ocr_text)
    checklist = generate_checklist(classification)
    return combine(...)
```

**When to add queuing:** When request takes >30 seconds

---

## ❌ Mistake 3: NoSQL for Structured Data

```
WRONG:
MongoDB for notices (flexible schema)

RIGHT:
PostgreSQL with JSONB columns
- Relational integrity
- Easy JOIN queries
- Better for audit trails
```

---

## ❌ Mistake 4: RAG Before You Have Data

```
WRONG (Phase 1):
Dump tax law PDFs into Pinecone

RIGHT:
Phase 1-2: Build knowledge base with rules
Phase 3: Add vector retrieval for similar cases
```

---

# Part 5: Implementation Checklist

## Phase 1 (MVP - Current)
```
✅ Streamlit UI
✅ OCR pipeline (Azure + fallback)
✅ GPT-4o extraction
✅ Structured JSON output
✅ Error handling
✅ Deployment to Streamlit Cloud
✅ Beta testing with CAs
```

## Phase 2 (Add Persistence - Week 3-4)
```
☐ Create FastAPI project
☐ Set up PostgreSQL schema
☐ Migrate process_notice.py to FastAPI
☐ Add database saving logic
☐ Implement audit trail
☐ Add failure case logging
☐ Deploy to Render
☐ Connect Streamlit frontend to FastAPI backend
☐ Test end-to-end
```

## Phase 3 (Scale Frontend - Week 5-6)
```
☐ Start Next.js project
☐ Build upload interface (mirror Streamlit)
☐ Add results dashboard
☐ Implement client tracking
☐ Add user authentication (NextAuth)
☐ Deploy to Vercel
☐ Migrate users from Streamlit
```

## Phase 4 (Advanced Features - Month 3+)
```
☐ Add vector embeddings
☐ Build similar case retrieval
☐ Create response template library
☐ Implement draft generation
☐ Add compliance checker
```

---

# Part 6: Architecture Diagram (What You're Building)

```
Phase 1 (Now)
═════════════
┌──────────┐
│Streamlit │──→ process_notice.py
│   UI     │    (GPT-4o + Azure OCR)
└──────────┘

Phase 2
═════════════
┌──────────┐
│Streamlit │
│   UI     │    ┌──────────┐
└──────────┘───→│FastAPI   │
               │Backend   │──→ PostgreSQL
               └──────────┘
               
Phase 3
═════════════
┌──────────┐
│ Next.js  │
│   UI     │    ┌──────────┐
└──────────┘───→│FastAPI   │──→ PostgreSQL
               │Backend   │──→ pgvector
               └──────────┘
```

---

# Part 7: Cost Evolution

| Phase | Frontend | Backend | Database | LLM | Total |
|-------|----------|---------|----------|-----|-------|
| 1 | Free | Free | Free | $20-50 | $20-50 |
| 2 | Free | $20 | $10 | $20-50 | $50-80 |
| 3 | $20 | $50 | $30 | $50-100 | $150-200 |
| 4+ | $50 | $100+ | $100+ | $100+ | $350+ |

---

# Part 8: Technology Decisions Summary

| Component | Phase 1 | Phase 2 | Phase 3+ |
|-----------|---------|---------|----------|
| Frontend | Streamlit | Streamlit | Next.js |
| Backend | Python functions | FastAPI | FastAPI (scaled) |
| Database | None | PostgreSQL | PostgreSQL + pgvector |
| OCR | Azure + GPT Vision | Azure + GPT Vision | Azure + GPT Vision |
| LLM | GPT-4o | GPT-4o + Claude | Multi-model routing |
| Deployment | Streamlit Cloud | Render | AWS/GCP |
| Vector DB | N/A | N/A | pgvector |
| Monitoring | Logs | LangSmith + Sentry | Full observability |

---

# Part 9: The Real Question

```
Phase 1 (MVP): DONE ✓
Phase 2 (Backend + DB): START THIS WEEK
Phase 3 (Frontend scale): START WEEK 5-6
Phase 4+ (Advanced): ONLY IF USERS DEMAND IT
```

---

**What's your next move?**

A) Deploy Phase 1, collect data, then plan Phase 2
B) Start building Phase 2 FastAPI backend now (parallel to beta)
C) Wait for Phase 1 validation before planning Phase 2

Most founders choose A (validate first). But B (parallel) saves 1-2 weeks if MVP succeeds.

Which fits your timeline?
