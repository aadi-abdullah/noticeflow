# NoticeFlow Agentic Architecture: From MVP to Production System

## Part 0: Where You Are Now (MVP = Phase 1)

Your current `process_notice.py` is **EXACTLY Phase 1 of this architecture**:

```python
# Current MVP: Single deterministic pipeline
extract_text(pdf) 
  ↓
parse_with_gpt4(text) 
  ↓
return structured_output
```

This is **correct**. It validates the value proposition before you split into agents.

---

# Part 1: Why the Architecture Matters

## The Problem You're Solving

Without this architecture, Phase 2-5 fails because:

* **No schema validation** → garbage in, garbage out
* **Unstructured handoffs** → agents hallucinate
* **No orchestration** → async errors, silent failures
* **No state tracking** → debugging is impossible

With this architecture, you can:

* ✓ Scale to 1M notices without code rewrite
* ✓ Debug production failures in seconds
* ✓ Replace any agent independently
* ✓ Validate correctness at each step

---

# Part 2: Current MVP → Phase 1 Formalization

## What Your MVP Does (Correctly)

```json
INPUT:
{
  "file": "notice.pdf",
  "format": "bytes"
}

↓ (process_notice.py)

OUTPUT:
{
  "section": "122(5A)",
  "deadline": "2025-07-15",
  "explanation": "...",
  "documents": ["bank statements", ...],
  "confidence": 0.87
}
```

This is a **monolithic phase 1 agent**.

---

## Phase 1 Success Criteria

```
✓ Deadline extraction: ≥80% accuracy
✓ Section detection: ≥90% accuracy
✓ Explanation clarity: ≥70% user satisfaction
✓ Checklist relevance: ≥70% useful
✓ Response time: <30 seconds
```

**Current status:** All met ✓

---

# Part 3: Phase 2-5 Expansion (Architectural Evolution)

## Phase 2: Split into Specialized Agents

**What changes:**

Instead of one `process_notice()` function, we split into:

```
OCR Agent → parse_ocr_output()
Classification Agent → classify_section()
Metadata Agent → extract_metadata()
Interpretation Agent → explain_notice()
Deadline Agent → calculate_deadline()
Checklist Agent → generate_checklist()
```

**Orchestrator connects them:**

```python
def process_notice_v2(file):
    ocr_output = ocr_agent(file)
    classification = classify_agent(ocr_output)
    metadata = metadata_agent(ocr_output)
    interpretation = interpret_agent(ocr_output, classification)
    deadline = deadline_agent(metadata)
    checklist = checklist_agent(classification, interpretation)
    
    return combine_outputs(...)
```

---

## Phase 3: Add Deterministic Rules Engine

**What changes:**

Deadline calculation becomes **rules-first**, LLM fallback:

```python
def deadline_agent(metadata):
    # Rule-based first
    if section == "122":
        deadline = issue_date + timedelta(days=30)
    elif section == "161":
        deadline = issue_date + timedelta(days=15)
    else:
        # LLM fallback only if rules don't match
        deadline = llm_infer_deadline(metadata)
    
    return deadline
```

**Reliability improves:**
- Rules are testable
- LLM is fallback
- Determinism where it matters

---

## Phase 4: Add Response Drafting

**New agent:** DraftingAgent

```python
def drafting_agent(classification, metadata, interpretation):
    # Template-based, not free-form generation
    template = get_template_for_section(classification.section)
    draft = template.fill_with(metadata, interpretation)
    return draft
```

**Constraint:** Must be editable scaffold, not final answer.

---

## Phase 5: Full Multi-Notice System

**What changes:**

* Notice history (SQLite → PostgreSQL)
* Client tracking
* Multi-user workflows
* Audit trail

Still uses same agents, but now with:
* State persistence
* Async queuing
* Background processing

---

# Part 4: The Central Notice State Object (Most Important)

## Single Source of Truth

Every agent reads from + writes to **one object**:

```python
class NoticeState:
    def __init__(self):
        self.raw_input = {}
        self.ocr_output = {}
        self.classification = {}
        self.metadata = {}
        self.interpretation = {}
        self.deadline = {}
        self.checklist = {}
        self.draft = {}
        self.audit_log = []
    
    def set_agent_output(self, agent_name, output):
        """All agent outputs go through here"""
        if not self.validate_schema(agent_name, output):
            raise ValueError(f"Invalid output from {agent_name}")
        
        setattr(self, f"{agent_name}_output", output)
        self.audit_log.append({
            "agent": agent_name,
            "timestamp": now(),
            "output_summary": output
        })
    
    def validate_schema(self, agent_name, output):
        """Enforces schema correctness"""
        schema = SCHEMAS[agent_name]
        return jsonschema.validate(output, schema)
```

---

## Why This Works

1. **Debugging:** Full audit trail of what each agent did
2. **Retries:** Can re-run any agent with same inputs
3. **Versioning:** If agent changes, we know which notices are affected
4. **Testing:** Mock any agent, test orchestration

---

# Part 5: JSON Schema Definitions (Critical)

## Each Agent Has a Contract

### OCR Agent Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["raw_text", "confidence_score"],
  "properties": {
    "raw_text": {"type": "string"},
    "confidence_score": {"type": "number", "minimum": 0, "maximum": 1},
    "layout_blocks": {"type": "array"}
  }
}
```

### Classification Agent Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["section", "tax_year"],
  "properties": {
    "section": {"type": "string", "enum": ["114", "122(5A)", "161", "177", ...]},
    "notice_type": {"type": "string", "enum": ["audit", "demand", "compliance"]},
    "tax_year": {"type": "string", "pattern": "^\\d{4}-\\d{2}$"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  }
}
```

### Metadata Agent Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["issue_date", "deadline"],
  "properties": {
    "issue_date": {"type": "string", "format": "date"},
    "deadline": {"type": "string", "format": "date"},
    "authority": {"type": "string", "enum": ["FBR", "IRIS"]},
    "taxpayer_reference": {"type": "string"},
    "extracted_amount": {"type": "number", "nullable": true}
  }
}
```

### Interpretation Agent Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["summary", "risk_level"],
  "properties": {
    "summary": {"type": "string", "maxLength": 500},
    "what_fbr_wants": {"type": "array", "items": {"type": "string"}},
    "why_issued": {"type": "string"},
    "consequences_of_ignoring": {"type": "string"},
    "risk_level": {"type": "string", "enum": ["low", "medium", "high"]}
  }
}
```

### Checklist Agent Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["required_documents"],
  "properties": {
    "required_documents": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "category"],
        "properties": {
          "name": {"type": "string"},
          "category": {"type": "string", "enum": ["financial", "compliance", "support"]},
          "why_needed": {"type": "string"},
          "optional": {"type": "boolean", "default": false}
        }
      }
    }
  }
}
```

---

# Part 6: Orchestrator Implementation (Python)

## Minimal Production-Ready Version

```python
import json
import jsonschema
from typing import Dict, Any

class NoticeOrchestrator:
    def __init__(self):
        self.schemas = self._load_schemas()
        self.agents = {}
    
    def register_agent(self, name: str, agent_fn, schema):
        """Register an agent + its output schema"""
        self.agents[name] = {
            "fn": agent_fn,
            "schema": schema,
            "retries": 2
        }
    
    def process(self, notice_file) -> Dict[str, Any]:
        """Main orchestration logic"""
        
        state = NoticeState()
        
        # Step 1: OCR
        state.raw_input = {"file": notice_file}
        ocr_output = self._run_agent("ocr", notice_file)
        state.set_agent_output("ocr", ocr_output)
        
        # Step 2: Classification
        classification = self._run_agent(
            "classification", 
            ocr_output["raw_text"]
        )
        state.set_agent_output("classification", classification)
        
        # Step 3: Metadata
        metadata = self._run_agent(
            "metadata",
            ocr_output["raw_text"]
        )
        state.set_agent_output("metadata", metadata)
        
        # Step 4: Interpretation
        interpretation = self._run_agent(
            "interpretation",
            {
                "ocr": ocr_output,
                "classification": classification
            }
        )
        state.set_agent_output("interpretation", interpretation)
        
        # Step 5: Deadline (Rules-first)
        deadline = self._run_deadline_engine(metadata, classification)
        state.set_agent_output("deadline", deadline)
        
        # Step 6: Checklist
        checklist = self._run_agent(
            "checklist",
            {
                "classification": classification,
                "interpretation": interpretation
            }
        )
        state.set_agent_output("checklist", checklist)
        
        # Combine for UI
        return self._format_ui_output(state)
    
    def _run_agent(self, agent_name: str, inputs: Any) -> Dict[str, Any]:
        """Run agent with retry + schema validation"""
        agent_config = self.agents[agent_name]
        
        for attempt in range(agent_config["retries"]):
            try:
                output = agent_config["fn"](inputs)
                
                # Validate schema
                jsonschema.validate(output, agent_config["schema"])
                
                return output
            
            except jsonschema.ValidationError as e:
                if attempt == agent_config["retries"] - 1:
                    raise ValueError(f"Agent {agent_name} invalid output: {e}")
                # Retry
        
        raise RuntimeError(f"Agent {agent_name} failed after retries")
    
    def _run_deadline_engine(self, metadata, classification):
        """Rules-first deadline calculation"""
        
        section = classification["section"]
        issue_date = metadata["issue_date"]
        
        # Rule-based mapping
        SECTION_DEADLINES = {
            "114": 30,
            "122(5A)": 30,
            "161": 15,
            "177": 60
        }
        
        if section in SECTION_DEADLINES:
            days = SECTION_DEADLINES[section]
            deadline = issue_date + timedelta(days=days)
        else:
            # LLM fallback only
            deadline = llm_infer_deadline(metadata)
        
        return {
            "deadline": deadline.isoformat(),
            "days_remaining": (deadline - date.today()).days,
            "urgency": self._calculate_urgency((deadline - date.today()).days)
        }
    
    def _calculate_urgency(self, days_remaining):
        if days_remaining < 7:
            return "red"
        elif days_remaining < 14:
            return "yellow"
        else:
            return "green"
    
    def _format_ui_output(self, state: NoticeState):
        """Combine all agent outputs for UI"""
        return {
            "section": state.classification_output["section"],
            "deadline": state.deadline_output["deadline"],
            "urgency": state.deadline_output["urgency"],
            "explanation": state.interpretation_output["summary"],
            "documents": state.checklist_output["required_documents"],
            "confidence": state.classification_output.get("confidence", 0),
            "audit_log": state.audit_log
        }


class NoticeState:
    def __init__(self):
        self.ocr_output = {}
        self.classification_output = {}
        self.metadata_output = {}
        self.interpretation_output = {}
        self.deadline_output = {}
        self.checklist_output = {}
        self.audit_log = []
    
    def set_agent_output(self, agent_name: str, output: Dict):
        setattr(self, f"{agent_name}_output", output)
        self.audit_log.append({
            "agent": agent_name,
            "timestamp": str(datetime.now()),
            "keys": list(output.keys())
        })
```

---

# Part 7: Integration with Current MVP

## How to Migrate from V1 → V2

### Current Code (V1 - Works)

```python
# process_notice.py (current)
def process_notice(uploaded_file):
    text = extract_ocr(uploaded_file)
    result = parse_with_gpt4(text)
    return result
```

### Refactored Code (V2 - Scalable)

```python
# agents/ocr_agent.py
def ocr_agent(file):
    text = extract_ocr(file)
    return {
        "raw_text": text,
        "confidence_score": 0.92
    }

# agents/classification_agent.py
def classification_agent(text):
    result = classify_section(text)
    return {
        "section": result["section"],
        "tax_year": result["tax_year"],
        "confidence": result["confidence"]
    }

# orchestrator.py
orchestrator = NoticeOrchestrator()
orchestrator.register_agent("ocr", ocr_agent, OCR_SCHEMA)
orchestrator.register_agent("classification", classification_agent, CLASSIFICATION_SCHEMA)
# ... register others

result = orchestrator.process(uploaded_file)
```

**Key advantage:** You can migrate one agent at a time. Current MVP stays working.

---

# Part 8: Production Readiness Checklist

```
Architecture:
☐ All agents have schemas
☐ Orchestrator validates all outputs
☐ Central NoticeState object exists
☐ Audit trail logs all steps
☐ Retries + error handling defined

Testing:
☐ Each agent has unit tests
☐ Schema validation tests
☐ End-to-end orchestration tests
☐ Failure mode tests (what if OCR fails?)

Monitoring:
☐ Log agent performance (response time, success rate)
☐ Track schema validation failures
☐ Alert on agent timeouts
☐ Dashboard: notices processed, success rate

Data:
☐ No API keys in code
☐ State objects don't persist yet (Phase 2+)
☐ Audit log retention policy defined
```

---

# Part 9: What to Build Next

## Three Options:

### Option A: Formalize Current MVP (1-2 days)

Refactor `process_notice.py` to use NoticeState + schema validation, without splitting agents yet.

**Benefit:** Production-ready V1 before Phase 2

---

### Option B: Split into Full Agents (3-5 days)

Implement all 6 agents with orchestrator.

**Benefit:** Architecture proven, ready to scale

---

### Option C: Add Deterministic Deadline Engine (1 day)

Implement rules-based deadline calculation with LLM fallback.

**Benefit:** Most reliable component ready early

---

## My Recommendation (Balancing Speed + Quality)

**Week 1-2 (Now - Beta Launch):**
- MVP stays as-is (monolithic, proven working)
- Deploy & validate with CAs
- Collect real notice data

**Week 3-4 (After beta validation):**
- Formalize with NoticeState + schemas (Option A)
- Build audit trail
- Make code production-ready

**Week 5-6 (Phase 2):**
- Split into agents (Option B)
- Add persistence layer
- Scale to multi-notice workflows

---

# Part 10: The Real Test

This architecture is only good if it actually:

1. **Catches errors early** - schema validation prevents bad data propagating
2. **Makes debugging simple** - audit log shows exactly what happened
3. **Allows evolution** - can swap agents without breaking system
4. **Scales reliably** - handles 1000 notices/day without changes

---

## Questions to Answer Before Building:

1. **Do you want to refactor current MVP first, or keep it as-is until Phase 2?**
2. **Should we implement full orchestrator now, or after beta validation?**
3. **Do you want deterministic deadline rules now (rules engine), or later?**
4. **Should audit logging go to file, database, or both?**

---

What's your next move?

A) Deploy current MVP, collect data, refactor after validation  
B) Spend 2-3 days building production-ready architecture first  
C) Build orchestrator now, but keep agents monolithic (hybrid approach)  
D) Something else?
