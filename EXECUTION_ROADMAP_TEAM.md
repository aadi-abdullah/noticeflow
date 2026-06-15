# NoticeFlow Execution Roadmap & Team Formation

## Part 0: The Execution Reality

This is not a "startup building" document.

This is a **"shipping workflow system under time pressure with domain validation"** document.

The difference:
- **Startup mindset:** How do we build a team? How do we raise money? How do we scale?
- **Shipping mindset:** How do we prove this works with real CAs in 4 weeks?

You need the second one.

---

# Part 1: Minimum Viable Team (MVT) - What You Actually Need

## 1.1 Role 1: You (Founder / Technical Lead)

### What You Own
- System design + architecture
- Backend (FastAPI Phase 2+)
- LLM prompt engineering
- OCR orchestration
- LangSmith setup (debugging)
- Deployment + DevOps

### Why This Can't Be Outsourced Early
If you don't understand every part of the pipeline, you can't debug when it breaks. And it **will** break.

### Time Commitment
- Phase 1: 40-50 hrs/week (shipping MVP)
- Phase 2: 30-40 hrs/week (backend + DB)
- Phase 3+: 20-30 hrs/week (if team grows)

**Reality check:** Can you commit this for 12 weeks? If not, product won't happen.

---

## 1.2 Role 2: Frontend/UX Builder (Contractor or Hire)

### What They Own
- Streamlit UI (Phase 1)
- Next.js frontend (Phase 3+)
- User feedback on interface
- Mobile responsiveness

### NOT What They Own
- Business logic
- LLM integration
- Deadline calculations
- Checklist generation

### Skill Requirements
- Can ship working UI in <1 week
- Understands "trust-building" UX (clean, professional, not trendy)
- Quick iteration based on feedback

### Time Commitment
- Phase 1: 10-15 hrs/week (UI polish)
- Phase 2: 5-10 hrs/week (backend integration)
- Phase 3: 20-30 hrs/week (Next.js build)

### How to Find
- Post on Upwork: "Need React/Next.js engineer for tax workflow product"
- Budget: $30-50/hr (freelancer) or $80-120k/year (hire)

---

## 1.3 Role 3: Domain Advisor (NOT Full-Time)

### What They Own
- Validate every extraction
- Correct wrong checklists
- Confirm real-world workflows
- Prevent hallucinations

### NOT What They Own
- Product decisions
- Code
- Infrastructure

### Who This Is
- Senior CA from 5-50 person firm (someone with real FBR notice handling)
- NOT a law firm partner (too disconnected from real work)
- NOT someone who "knows tax" but hasn't handled notices

### Time Commitment
- Phase 1: 3-5 hrs/week (review outputs)
- Phase 2: 2-3 hrs/week (validate KB)
- Phase 3+: 1-2 hrs/week (edge cases)

### Compensation
- Early: 0.5-1% equity (no money upfront)
- Later: $500-1000/month retainer once revenue exists

### How to Find
- Personal network (best)
- LinkedIn: Search "Chartered Accountant" + "tax" + "notice"
- Reach out: "We're building a tool for notice handling. Need a CA advisor to validate outputs."

**Critical:** This is the most important hire. Get this wrong = product dies.

---

## 1.4 (Optional) Role 4: Data/Research Support (Part-Time)

### Only After Phase 2 When You Have
- 50+ real notices
- Enough data to see patterns
- Time to build KB

### What They Do
- Organize notice dataset
- Tag attributes
- Research section mappings

### Time: 5-10 hrs/week

---

# Part 2: Team Decision Tree

### RIGHT NOW (Week 0)

```
Can you (founder) do:
  - Python backend?
  - LLM orchestration?
  - Deployment?

NO → Find co-founder (STOP, recruit first)
YES → Continue

Do you know a CA/tax consultant personally?

NO → Recruit domain advisor first (1-2 weeks)
YES → Ask them to advise (confirm commitment)

Can you build Streamlit UI yourself?

YES → Do it (save money)
NO → Hire frontend person (this week)
```

---

# Part 3: Exact Weekly Roadmap (12 Weeks to Product-Market Signal)

## Week 0 (This Week): Setup

### Day 1-2: Team Recruitment
```
☐ Confirm domain advisor availability (email/call)
☐ Post for frontend person (Upwork)
☐ Get 3-5 applications
☐ Interview + hire top candidate
```

### Day 3-4: Data Collection
```
☐ Contact 5-10 CAs you know
☐ Ask: "Can you send me 2-3 tax notices (anonymized)?"
☐ Explain: "Testing AI system for notice handling"
☐ Collect into shared folder
```

### Day 5: Infrastructure
```
☐ Confirm API keys (OpenAI, Azure)
☐ Test Streamlit Cloud deployment
☐ Set up GitHub repo for tracking
☐ Create Trello board (or notion)
```

### Output: Domain advisor confirmed, 5-10 notices collected, frontend person hired

---

## Week 1-2: Phase 1 MVP (Thin Prototype)

### What to Build
```
✓ Upload notice (PDF/image)
✓ Extract text (Azure + fallback)
✓ Classify section (GPT-4o)
✓ Extract deadline
✓ Plain explanation
✓ Document checklist
✓ Display results (60-second end-to-end)
```

### What NOT to Build
```
✗ User authentication
✗ History tracking
✗ Dashboards
✗ Email notifications
✗ Advanced features
```

### Acceptance Criteria
```
☐ Process 10 collected notices
☐ Domain advisor reviews outputs
☐ Domain advisor says: "This is 70% correct"
  (not 100%, 70% is enough for MVP)
☐ Outputs are human-readable (not AI gibberish)
☐ No crashes on bad inputs
```

### Deliverables
```
1. app.py (Streamlit - likely you already have this)
2. process_notice.py (LLM pipeline - likely you already have this)
3. requirements.txt
4. README (how to run)
5. 10 annotated test cases (for evaluation)
```

### Team Work Split
```
You:         Process_notice.py + orchestration (40 hrs)
Frontend:    Streamlit UI polish (15 hrs)
CA advisor:  Review outputs + corrections (5 hrs)
```

### Success Signal
```
✓ IF domain advisor says outputs are usable
  → Move to Week 3

✗ IF domain advisor says "this is wrong"
  → Debug for 2-3 days, iterate
  → Don't move forward until fixed
```

---

## Week 3-4: Phase 2 Real User Testing

### What to Do
```
1. Deploy MVP to Streamlit Cloud
2. Get 3-5 CAs to use it live (30-min screen-share sessions)
3. Watch them use it
4. Collect feedback
```

### Exact Script for User Testing
```
"Here's a tool that converts tax notices to checklists.
 Try it on one of your recent notices.
 I'll watch silently and take notes."

[User uploads notice, system processes, shows results]

"Does this help?"
"Would you use this on your next notice?"
"What's wrong or confusing?"
```

### Metrics to Capture
```
□ Deadline extraction accuracy (vs actual notice)
□ Section detected correctly? (Y/N)
□ Checklist useful? (Y/N/Partially)
□ Response time acceptable? (<30 sec)
□ Would re-use? (Y/N)

Target:
  ≥3/5 users say "yes" to re-use
  ≥80% deadline accuracy
  ≥70% think checklist is useful
```

### Decision Gate (End of Week 4)
```
IF metrics met:
  ✓ Proceed to Phase 3 (backend + persistence)
  
IF metrics NOT met:
  ✗ Debug for 3-5 days
  ✗ Focus on biggest complaint
  ✗ Re-test with 2 users
  ✗ Then decide: iterate or pivot
```

### What Happens If It Fails?
```
Common failures:
  1. "Deadline is always wrong"
    → Fix: Improve section-deadline rules mapping
    
  2. "Checklist is generic"
    → Fix: Add more allegation-specific rules
    
  3. "Explanation is confusing"
    → Fix: Refine system prompt, simplify language
    
  4. "Takes too long"
    → Fix: Optimize OCR pipeline, reduce LLM calls
```

**Do NOT move forward until root cause is fixed.**

---

## Week 5-8: Phase 3 MVP Productization (Add Persistence)

### What to Build
```
✓ FastAPI backend
✓ PostgreSQL database
✓ Save notices per client
✓ Show case history
✓ Re-upload interface
```

### What NOT to Build Yet
```
✗ Multi-user/authentication
✗ Advanced dashboard
✗ Email notifications
✗ Compliance checking
```

### Database Schema (Minimal)
```sql
notices:
  - id
  - user_id (just a name for now)
  - raw_notice (PDF path)
  - ocr_text
  - extracted_json
  - created_at

results:
  - id
  - notice_id
  - deadline
  - explanation
  - checklist
  - created_at
```

### Team Work Split
```
You:         FastAPI backend + DB integration (35 hrs)
Frontend:    Update Streamlit to call API (10 hrs)
CA advisor:  Validate new outputs (3 hrs)
```

### Acceptance Criteria
```
☐ Can upload notice → save to DB
☐ Can retrieve past notices
☐ Results match Phase 1 outputs (no regression)
☐ Domain advisor approves accuracy
☐ 3-5 CAs test + give thumbs up
```

### Success Signal
```
✓ At least 1 CA has used system twice (without you asking)
  → Move to Phase 4
```

---

## Week 9-12: Phase 4 Retention Layer (Make It Sticky)

### What to Build
```
✓ Client-specific workflows
✓ Document tracking (which docs collected)
✓ Simple dashboard
✓ Re-upload for same client
```

### What NOT to Build Yet
```
✗ Multi-user authentication
✗ Draft response generation
✗ Team collaboration
✗ Integrations
```

### Success Signal
```
✓ 60%+ of users upload 2+ notices
✓ CAs mention recommending to colleagues
✓ Average response time < 3 days (for CA to collect docs)
```

### Decision Gate (End of Week 12)
```
IF retention exists:
  ✓ You have product-market signal
  ✓ Proceed to Phase 5 (expansion + scaling)
  
IF retention doesn't exist:
  ✗ Product doesn't solve real problem
  ✗ Kill or pivot
```

---

# Part 4: Critical Milestones (DO NOT SKIP)

## Milestone 1: First Correct Extraction (Week 1)
```
✓ Take one real notice from your CA advisor
✓ System extracts:
    - Section correctly
    - Deadline correctly
    - Allegation category correctly
✓ CA says: "Yes, that's accurate"

What this proves: Core logic works
```

---

## Milestone 2: Checklist Accepted Without Correction (Week 2)
```
✓ System generates document checklist
✓ CA reviewer says: "Yes, this is what I'd ask for"
✓ CA does NOT suggest missing items

What this proves: Knowledge base is sound
```

---

## Milestone 3: User Says "I'd Use This Again" (Week 4)
```
✓ After real user testing
✓ At least 3/5 users say: "I would use this on my next notice"

What this proves: Solves real workflow pain
```

---

## Milestone 4: Second Usage Without Prompting (Week 12)
```
✓ CA uses system again, without you asking
✓ Uploads a different notice
✓ Uses output in real workflow

What this proves: PRODUCT VALIDATION
```

---

# Part 5: Weekly Standup Template (Discipline)

Every Friday, fill this out:

```markdown
# Week X Standup

## Completed
- [x] Task 1
- [x] Task 2
- [x] Task 3

## Blockers
- [ ] Issue 1 (impact: progress)
- [ ] Issue 2 (impact: progress)

## Metrics
- Notices tested: N
- CA feedback score: X/10
- Deadline accuracy: Y%
- "Would re-use" rate: Z%

## Next Week
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Decision Needed?
- [ ] Keep going
- [ ] Iterate on X
- [ ] Pivot to Y
```

Share with your team every Friday. **This forces accountability.**

---

# Part 6: What Kills Most Products (Recognize These Early)

## 🔴 Red Flag 1: Scope Creep

```
Week 1: "Let's add authentication"
Week 2: "Let's add draft generation"
Week 3: "Let's add team collaboration"

→ By Week 12, you're nowhere

RULE: Do not build features that don't directly
      improve notice handling accuracy.
```

---

## 🔴 Red Flag 2: No Domain Advisor Feedback

```
You build for 4 weeks in isolation
You show domain advisor (finally)
Domain advisor says: "This is wrong"

Too late. You've built wrong thing.

RULE: Show domain advisor every 2-3 days.
```

---

## 🔴 Red Flag 3: No Real User Testing

```
You think system is good
You deploy
Real CAs use it
"This doesn't help at all"

RULE: Get real CAs testing by Week 3.
      Do not spend 8 weeks perfecting
      before you know if it works.
```

---

## 🔴 Red Flag 4: Metrics Aren't Clear

```
Week 4: "How are we doing?"
Team: "Umm, pretty good I think?"

→ You have no idea if you're winning

RULE: Every week, measure:
  - Deadline accuracy %
  - Checklist usefulness (Y/N)
  - Would re-use %
  - Response time (seconds)
```

---

# Part 7: Decision Tree at Each Gate

## After Week 2 (MVP Built)

```
Domain advisor review:
  
  "Outputs are 70%+ correct"?
    → YES: Show to CAs in Week 3
    → NO: Debug for 2-3 days, try again
    
    NO progress after 3 days?
    → Kill this direction, pivot
```

---

## After Week 4 (Real User Testing)

```
Did 3/5+ CAs say "I'd re-use this"?
  
  → YES: Build Phase 3 (persistence)
  → NO: What was the complaint?
  
    "Deadlines wrong": Fix section-deadline rules
    "Checklist generic": Add more rules
    "Takes too long": Optimize OCR
    "Not worth my time": Product doesn't solve problem
                         → KILL
```

---

## After Week 8 (Persistence Built)

```
Did at least 1 CA use it twice?
  
  → YES: Build Phase 4 (retention)
  → NO: Why didn't they come back?
        - Was extraction wrong?
        - Was checklist not helpful?
        - Did they just forget?
        
  Ask them directly. Fix the reason.
```

---

## After Week 12 (Retention Features)

```
Do 60%+ of users have 2+ notices?
  
  → YES: You have product-market signal
         → Plan Phase 5 (scaling)
         
  → NO: Product doesn't create habit
        → Kill or significantly pivot
```

---

# Part 8: The Accountability Contract

Print this out. Sign it. Put it on your wall.

```
I commit to:

[ ] Deploy MVP by end of Week 2
[ ] Get real CA feedback by end of Week 3
[ ] Have decision on "continue or iterate" by end of Week 4
[ ] Have persistence layer built by end of Week 8
[ ] Know if product has retention by end of Week 12

I will NOT:
[ ] Build features before validating core workflow
[ ] Spend >2 weeks optimizing before user testing
[ ] Hire extra people before product works
[ ] Pivot without data
[ ] Accept mediocre domain advisor input

If I break these promises:
[ ] Stop work immediately
[ ] Identify what went wrong
[ ] Fix it or kill the project

Signature: _______________
Date: _______________
```

---

# Part 9: How to Know You're Actually Winning

```
Week 2:  Domain advisor says outputs are usable
Week 4:  3+ CAs would re-use
Week 8:  System persists data, no bugs
Week 12: Users coming back without prompting

If ALL of these happen: You have product.
If ANY fails: Fix or kill.
```

---

# Part 10: Final Execution Rule

> Do not ask "is this architecturally perfect?"
> Ask instead: "Did a CA use this to handle a real notice faster?"

If YES: Keep building.
If NO: Stop, debug, iterate.

Architecture can be fixed. Wrong product cannot.

---

# IMMEDIATE ACTIONS (Next 3 Days)

## Day 1
```
☐ Email 3 CAs you know: "Need feedback on tax tool"
☐ Post on Upwork: "Need Streamlit/React developer"
☐ Check OpenAI/Azure credits are sufficient for 100 notices
```

## Day 2
```
☐ Interview 3 frontend candidates
☐ Hire top candidate (or commit to doing UI yourself)
☐ Confirm domain advisor (email + call)
☐ Collect 5-10 notices from CAs (anonymized)
```

## Day 3
```
☐ Set up GitHub + Trello board
☐ Create shared folder for test notices
☐ Schedule weekly standup (Friday 5pm)
☐ Write down your 12-week milestones
☐ Post this roadmap in your workspace
```

---

**You now have a 12-week path to knowing if this works.**

Execute this exactly.

When you hit Week 4 decision gate, you'll know within 1 week if you should continue or kill.

No guessing. No "someday". Just data.

Go.
