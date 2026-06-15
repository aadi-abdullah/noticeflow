# Production-Grade Backend Design (FastAPI)

## Part 0: Core Philosophy

**Your backend is NOT:**
- A microservice ecosystem
- A real-time distributed system
- An event-driven Kafka architecture
- An "AI platform"

**Your backend IS:**
A **stateful workflow API that runs deterministic AI pipelines**

Think: "Document processing engine + LLM orchestration layer"

Not: "AI platform"

---

# Part 1: Architecture Overview

```
                    ┌──────────────────┐
                    │   Client (UI)    │
                    │   (Streamlit)    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  FastAPI Backend │
                    │  - Routes        │
                    │  - Auth (simple) │
                    └────────┬─────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │   WORKFLOW ORCHESTRATOR (Core Engine)   │
        │ - Notice state management              │
        │ - Pipeline execution                   │
        │ - Error handling + retries             │
        └────────┬──────────────────┬────────────┘
                 │                  │
         ┌───────▼────┐      ┌──────▼────────┐
         │ AI Layer   │      │ Tools Layer   │
         │ LLM calls  │      │ - OCR         │
         │ Prompts    │      │ - Rules Eng   │
         │ Validation │      │ - Caching     │
         └────────────┘      └────────┬──────┘
                                      │
                             ┌────────▼─────────┐
                             │ PostgreSQL DB    │
                             │ - Notices        │
                             │ - Results        │
                             │ - Client history │
                             └──────────────────┘
```

---

# Part 2: Backend Tech Stack

## Core Framework
```
FastAPI       - Web framework (async-first, but we keep it simple)
Pydantic      - Schema validation (CRITICAL - every input/output validated)
SQLAlchemy    - ORM (clean DB access)
PostgreSQL    - Database (structured data only)
```

## AI/Processing
```
openai                - GPT-4o API calls
azure-document-ai     - OCR (primary)
LangSmith (optional)  - Debugging + monitoring
```

## Infrastructure
```
Redis (optional)      - State caching + job queuing (add in Phase 3)
Celery (optional)     - Async tasks (add when needed)
AWS S3 (later)        - File storage
```

---

# Part 3: Module Structure

```
noticeflow/
├── main.py                    # FastAPI app entry point
├── config.py                  # Environment config
│
├── api/
│   ├── __init__.py
│   ├── routes.py              # All HTTP endpoints
│   └── schemas.py             # Pydantic request/response schemas
│
├── core/
│   ├── __init__.py
│   ├── orchestrator.py        # MAIN: Workflow execution engine
│   ├── state.py               # NoticeState object
│   └── constants.py           # Section mappings, etc
│
├── services/
│   ├── __init__.py
│   ├── ocr_service.py         # Azure + GPT fallback
│   ├── llm_service.py         # LLM wrapper (GPT-4o calls)
│   ├── rules_engine.py        # Deterministic rules (deadlines, sections)
│   └── memory_service.py      # DB interactions
│
├── models/
│   ├── __init__.py
│   ├── notice.py              # SQLAlchemy models
│   ├── result.py
│   └── interpretation.py
│
├── utils/
│   ├── __init__.py
│   ├── logging_config.py      # Structured logging
│   ├── errors.py              # Custom exceptions
│   └── validators.py          # Schema validation helpers
│
└── tests/
    ├── __init__.py
    └── test_orchestrator.py
```

---

# Part 4: Core Module: Orchestrator

This is your **MOST IMPORTANT** module.

```python
# core/orchestrator.py

from typing import Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class NoticeState:
    """Single object carrying all notice processing state"""
    
    def __init__(self, notice_id: str):
        self.notice_id = notice_id
        self.created_at = datetime.now()
        
        # Raw inputs
        self.raw_file_path = None
        self.ocr_text = ""
        
        # Agent outputs
        self.classification = {}
        self.metadata = {}
        self.interpretation = {}
        self.checklist = {}
        
        # Metadata
        self.workflow_plan = []
        self.confidence_scores = {}
        self.errors = []
        self.human_review_needed = False
        self.human_review_reason = None
    
    def to_dict(self):
        return {
            "notice_id": self.notice_id,
            "classification": self.classification,
            "metadata": self.metadata,
            "interpretation": self.interpretation,
            "checklist": self.checklist,
            "human_review_needed": self.human_review_needed,
            "errors": self.errors,
        }


class WorkflowOrchestrator:
    """Main pipeline executor - deterministic workflow engine"""
    
    def __init__(self, ocr_service, llm_service, rules_engine, memory_service):
        self.ocr_service = ocr_service
        self.llm_service = llm_service
        self.rules_engine = rules_engine
        self.memory_service = memory_service
    
    def process_notice(self, file_path: str, notice_id: str) -> NoticeState:
        """Main entry point - orchestrates entire pipeline"""
        
        state = NoticeState(notice_id)
        state.raw_file_path = file_path
        
        try:
            # Step 1: OCR
            logger.info(f"[{notice_id}] Step 1: OCR extraction")
            state.ocr_text = self._extract_ocr(file_path)
            if not state.ocr_text:
                raise ValueError("OCR failed - no text extracted")
            
            # Step 2: Planning
            logger.info(f"[{notice_id}] Step 2: Planning workflow")
            plan = self.llm_service.get_workflow_plan(state.ocr_text)
            state.workflow_plan = plan.get("steps", [])
            
            # Step 3: Classification
            logger.info(f"[{notice_id}] Step 3: Classification")
            state.classification = self._classify_notice(state.ocr_text)
            self._validate_schema("classification", state.classification)
            
            # Step 4: Extraction
            logger.info(f"[{notice_id}] Step 4: Extraction")
            state.metadata = self._extract_metadata(
                ocr_text=state.ocr_text,
                section=state.classification.get("section")
            )
            self._validate_schema("extraction", state.metadata)
            
            # Step 5: Interpretation
            logger.info(f"[{notice_id}] Step 5: Interpretation")
            state.interpretation = self._interpret_notice(
                ocr_text=state.ocr_text,
                section=state.classification.get("section"),
                metadata=state.metadata
            )
            self._validate_schema("interpretation", state.interpretation)
            
            # Step 6: Checklist
            logger.info(f"[{notice_id}] Step 6: Checklist generation")
            state.checklist = self._generate_checklist(
                section=state.classification.get("section"),
                interpretation=state.interpretation
            )
            self._validate_schema("checklist", state.checklist)
            
            # Step 7: Guardrails + Flagging
            logger.info(f"[{notice_id}] Step 7: Applying guardrails")
            self._apply_guardrails(state)
            
            # Step 8: Store
            logger.info(f"[{notice_id}] Step 8: Storing result")
            self.memory_service.store_result(state)
            
            logger.info(f"[{notice_id}] ✓ COMPLETE")
            return state
            
        except Exception as e:
            logger.error(f"[{notice_id}] ✗ FAILED: {str(e)}")
            state.errors.append({
                "step": "unknown",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            state.human_review_needed = True
            return state
    
    def _extract_ocr(self, file_path: str) -> str:
        """Multi-fallback OCR strategy"""
        try:
            # Primary: Azure
            return self.ocr_service.extract_azure(file_path)
        except Exception as e:
            logger.warning(f"Azure OCR failed: {e}")
            try:
                # Fallback: GPT-4o Vision
                return self.ocr_service.extract_gpt4o_vision(file_path)
            except Exception as e2:
                logger.warning(f"GPT vision failed: {e2}")
                # Fallback: Simple PDF
                return self.ocr_service.extract_pypdf(file_path)
    
    def _classify_notice(self, ocr_text: str) -> dict:
        """Call LLM Classification Agent"""
        result = self.llm_service.classify_notice(ocr_text)
        return result
    
    def _extract_metadata(self, ocr_text: str, section: str) -> dict:
        """Call LLM Extraction Agent"""
        result = self.llm_service.extract_metadata(ocr_text, section)
        
        # Enhance with deterministic rules
        if section.startswith("122"):
            result["deadline"] = self.rules_engine.calculate_deadline(
                section=section,
                issue_date=result.get("notice_date")
            )
        
        return result
    
    def _interpret_notice(self, ocr_text: str, section: str, metadata: dict) -> dict:
        """Call LLM Interpretation Agent"""
        result = self.llm_service.interpret_notice(
            ocr_text=ocr_text,
            section=section,
            metadata=metadata
        )
        return result
    
    def _generate_checklist(self, section: str, interpretation: dict) -> dict:
        """Call LLM Checklist Agent"""
        result = self.llm_service.generate_checklist(
            section=section,
            interpretation=interpretation
        )
        return result
    
    def _validate_schema(self, step_name: str, output: dict) -> None:
        """CRITICAL: Validate every agent output"""
        from core.schemas import SCHEMAS
        
        schema = SCHEMAS.get(step_name)
        if not schema:
            logger.warning(f"No schema defined for {step_name}")
            return
        
        import jsonschema
        try:
            jsonschema.validate(output, schema)
        except jsonschema.ValidationError as e:
            raise ValueError(f"Schema validation failed for {step_name}: {e.message}")
    
    def _apply_guardrails(self, state: NoticeState) -> None:
        """Apply safety + legal guardrails"""
        
        # Rule 1: Check deadline is future date
        deadline = state.metadata.get("deadline")
        if deadline and deadline < datetime.now().date():
            state.human_review_needed = True
            state.human_review_reason = "Deadline in past - extraction error"
        
        # Rule 2: Check confidence scores
        for step, score in state.confidence_scores.items():
            if score < 0.7:
                state.human_review_needed = True
                state.human_review_reason = f"Low confidence in {step}: {score}"
        
        # Rule 3: No legal certainty claims
        summary = state.interpretation.get("summary", "").lower()
        if any(word in summary for word in ["definitely", "certainly", "must"]):
            state.interpretation["summary"] = state.interpretation["summary"] \
                .replace("definitely", "likely") \
                .replace("certainly", "likely")
```

---

# Part 5: API Routes

```python
# api/routes.py

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import uuid

router = APIRouter()

class UploadNoticeRequest(BaseModel):
    client_id: str

class NoticeResponse(BaseModel):
    notice_id: str
    section: str
    deadline: str
    summary: str
    checklist: list
    human_review_needed: bool

@router.post("/notices/upload")
async def upload_notice(file: UploadFile, client_id: str):
    """Upload and store a notice"""
    notice_id = str(uuid.uuid4())
    
    # Save file
    file_path = f"/uploads/{notice_id}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Store in DB (metadata only)
    memory_service.create_notice(notice_id, client_id, file_path)
    
    return {
        "notice_id": notice_id,
        "status": "uploaded"
    }

@router.post("/notices/{notice_id}/process")
async def process_notice(notice_id: str):
    """Main pipeline execution endpoint"""
    
    # Get notice from DB
    notice = memory_service.get_notice(notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    # Run orchestrator
    state = orchestrator.process_notice(
        file_path=notice.file_path,
        notice_id=notice_id
    )
    
    return NoticeResponse(
        notice_id=state.notice_id,
        section=state.classification.get("section"),
        deadline=str(state.metadata.get("deadline")),
        summary=state.interpretation.get("summary"),
        checklist=state.checklist.get("required_documents"),
        human_review_needed=state.human_review_needed
    )

@router.get("/notices/{notice_id}")
async def get_notice_result(notice_id: str):
    """Retrieve full result for a notice"""
    result = memory_service.get_result(notice_id)
    return result.to_dict() if result else {"error": "Not found"}

@router.get("/clients/{client_id}/notices")
async def list_client_notices(client_id: str):
    """List all notices for a client"""
    notices = memory_service.list_notices_by_client(client_id)
    return notices
```

---

# Part 6: Service Layer (Dependency Injection)

```python
# services/llm_service.py

import openai
from tenacity import retry, stop_after_attempt

class LLMService:
    """Wrapper around all LLM calls - single point of control"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    @retry(stop=stop_after_attempt(3))
    def classify_notice(self, ocr_text: str) -> dict:
        """Classification Agent"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "system",
                "content": "You are a tax notice classifier...",
                "user": f"Classify this notice:\n{ocr_text}"
            }],
            temperature=0.2,  # Low temp for consistency
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    @retry(stop=stop_after_attempt(3))
    def extract_metadata(self, ocr_text: str, section: str) -> dict:
        """Extraction Agent"""
        # Similar pattern
        pass
```

---

# Part 7: PostgreSQL Schema

```sql
-- notices table
CREATE TABLE notices (
    id UUID PRIMARY KEY,
    client_id VARCHAR(255),
    file_path VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- extracted_results table
CREATE TABLE extracted_results (
    id UUID PRIMARY KEY,
    notice_id UUID REFERENCES notices(id),
    classification_json JSONB,
    metadata_json JSONB,
    interpretation_json JSONB,
    checklist_json JSONB,
    human_review_needed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- error_log table
CREATE TABLE error_log (
    id UUID PRIMARY KEY,
    notice_id UUID REFERENCES notices(id),
    step VARCHAR(50),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

# Part 8: Error Handling Pattern

```python
# core/errors.py

class NoticeProcessingError(Exception):
    """Base exception for notice processing"""
    pass

class OCRError(NoticeProcessingError):
    """OCR extraction failed"""
    pass

class LLMError(NoticeProcessingError):
    """LLM call failed"""
    pass

class SchemaValidationError(NoticeProcessingError):
    """Output didn't match schema"""
    pass

# Usage in orchestrator:

try:
    state.classification = self._classify_notice(state.ocr_text)
except LLMError as e:
    logger.error(f"Classification failed: {e}")
    state.human_review_needed = True
    # Don't crash - continue
except SchemaValidationError as e:
    logger.error(f"Schema validation: {e}")
    # Retry with correction prompt
    state.classification = self._classify_notice_with_correction(state.ocr_text)
```

---

# Part 9: Logging Strategy (CRITICAL)

```python
# utils/logging_config.py

import logging
import json

class StructuredLogger:
    """Log every LLM interaction for debugging"""
    
    def log_llm_call(self, agent_name: str, prompt: str, response: str):
        """Log LLM interaction"""
        log_entry = {
            "type": "llm_call",
            "agent": agent_name,
            "prompt_length": len(prompt),
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        logger.info(json.dumps(log_entry))
    
    def log_llm_failure(self, agent_name: str, error: str):
        """Log LLM failure"""
        log_entry = {
            "type": "llm_failure",
            "agent": agent_name,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        logger.error(json.dumps(log_entry))
```

**Why log everything?**
- Debugging hallucinations requires seeing exact prompts
- Performance monitoring (which agents are slow?)
- Data collection (train better models later)

---

# Part 10: Workflow Execution Patterns

## Pattern A: Synchronous (MVP)

```python
# Simple, blocking
@app.post("/process")
async def process(file: UploadFile):
    state = orchestrator.process_notice(file.filename)
    return state.to_dict()
```

Pros: Simple, debuggable
Cons: Slow if API has many requests

---

## Pattern B: Async + Polling (Phase 3)

```python
# Upload returns immediately
@app.post("/upload")
async def upload(file: UploadFile):
    job_id = queue_job(file)
    return {"job_id": job_id}

# Client polls for results
@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    status = cache.get(job_id)
    return {"status": status, "ready": status == "complete"}
```

---

# Part 11: Testing Strategy

```python
# tests/test_orchestrator.py

def test_happy_path():
    """Test complete successful pipeline"""
    state = orchestrator.process_notice("test_notice.pdf", "test_id")
    
    assert state.classification["section"] is not None
    assert state.metadata["deadline"] is not None
    assert len(state.checklist["required_documents"]) > 0
    assert not state.human_review_needed

def test_ocr_fallback():
    """Test OCR fallback chain"""
    # Make Azure fail
    # Expect GPT vision to be called
    # Expect fallback to PyPDF
    pass

def test_schema_validation():
    """Test that invalid LLM output is caught"""
    # Mock LLM returning invalid JSON
    # Expect validation error + retry
    pass
```

---

# Part 12: Deployment Architecture

## Local (Development)
```
FastAPI (dev server) → PostgreSQL (local) → File storage (local)
```

## Render.com (MVP)
```
FastAPI (Render) → PostgreSQL (Render) → File storage (local or R2)
```

## AWS (Production)
```
FastAPI (ECS) → PostgreSQL (RDS) → File storage (S3)
```

---

# Part 13: What NOT to Do

❌ **DON'T:**
- Build microservices yet (all in one FastAPI)
- Use message queues early (synchronous is fine)
- Add Kubernetes (Render or AWS ECS is enough)
- Mix AI logic into routes (keep in services)
- Skip logging (you'll regret it)
- Assume LLM outputs are correct (validate everything)

✅ **DO:**
- Keep orchestrator simple + deterministic
- Validate every output
- Log every LLM call
- Have clear service boundaries
- Test error cases
- Make it debuggable first, optimized second

---

# Part 14: MVP Backend Checklist

```
Phase 2 Backend (5-8 weeks):

[ ] FastAPI setup + routes
[ ] Pydantic schemas for all inputs/outputs
[ ] SQLAlchemy models + migrations
[ ] PostgreSQL local setup
[ ] Orchestrator core logic
[ ] LLM service wrapper
[ ] OCR service (Azure + fallback)
[ ] Rules engine (deadlines, sections)
[ ] Memory service (DB interactions)
[ ] Structured logging
[ ] Error handling + retry logic
[ ] Local testing
[ ] Deploy to Render
[ ] Integration with Streamlit frontend
[ ] Test with 5 real notices
```

---

# Part 15: One-Line System Definition

> **A FastAPI-based deterministic workflow engine that orchestrates OCR + LLM + rules engine to convert tax notices into structured compliance actions, with full audit trail and schema validation at every step.**

This is your production backend.

It's simple. It's traceable. It works.

