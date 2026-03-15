description: Autonomous documentation synchronization and intelligence layer for all code changes.
priority: critical
scope: global
---

# DOCUMENTATION INTELLIGENCE SYSTEM

This is a global rule system responsible for maintaining **living documentation** across the entire repository.

The system automatically detects structural changes in the codebase and ensures all documentation stays synchronized.

---

# CORE PHILOSOPHY

Code and documentation must evolve together.

Any change in code that is not reflected in documentation is considered an **incomplete task**.

Documentation must always represent the **current architecture of the system**.

---

# CHANGE DETECTION ENGINE

Whenever a task modifies the repository, the system must detect:

### Structural Changes

New files created  
Files deleted  
Files renamed  
Folder structure changes

### Logic Changes

New feature implementation  
New strategy/scraper added  
New service/module introduced  
API behavior changes  
Dependency changes

### Architecture Changes

New subsystem introduced  
Database schema modified  
New integrations added  
New external services connected

---

# DOCUMENTATION UPDATE ENGINE

After detecting a change, update the relevant documentation.

---

# README UPDATE RULES

Update README when:

New feature added  
New module added  
New dependency introduced  
Installation process changed  
Environment variables changed  
Usage instructions changed  

README must contain:
Project Overview
Features
Installation
Usage
Configuration
Architecture Overview


---

# ARCHITECTURE DOCUMENTATION

File:


docs/ARCHITECTURE.md


Update when:

New service created  
New module introduced  
Data flow changed  
System responsibilities changed  

Architecture documentation must include:


System Components
Module Responsibilities
Service Architecture
Data Flow
Dependency Graph
---

# STRATEGY DOCUMENTATION

File:


docs/STRATEGIES.md


Update when:

New strategy added  
New scraper implemented  

Example:


src/strategies/flipkart.py


Documentation format:


Strategy Name
Supported Platform
Input Parameters
Returned Data
Limitations
Example Usage


---

# API DOCUMENTATION

File:


docs/API.md


Update when:

New endpoint added  
Response format changed  
Request parameters changed  

Documentation must contain:


Endpoint
Method
Parameters
Response Schema
Example Response


---

# CHANGELOG AUTOMATION

File:


CHANGELOG.md


Every update must be recorded.

Format:

[DATE]
Added

New feature

Updated

Modified behavior

Fixed

Bug fixes

Removed

Deprecated features


---

# ARCHITECTURE INTELLIGENCE

If a new module is detected inside:


src/services
src/strategies
src/controllers
src/utils


The system must automatically update architecture documentation.

---

# STRATEGY AUTO DETECTION

If a file is added inside:


src/strategies/


Example:


src/strategies/flipkart.py


Then:

Automatically append strategy details into


docs/STRATEGIES.md


---

# API AUTO DETECTION

If files change inside:


src/routes
src/controllers
src/api


Then update:


docs/API.md


---

# DOCUMENTATION CONSISTENCY CHECK

Before completing any task verify:


[ ] README updated
[ ] CHANGELOG updated
[ ] Architecture docs updated
[ ] API docs updated (if needed)
[ ] Strategy docs updated (if needed)


If any item is missing, the task is incomplete.

---

# AGENT INTEGRATION

This system applies to **all agents**:


backend-specialist
frontend-specialist
mobile-developer
devops-engineer
database-architect
performance-optimizer
security-auditor
test-engineer
orchestrator


Agents cannot finish a task until documentation synchronization is complete.

---

# AUTOMATIC EXECUTION FLOW

Whenever code changes occur:


Detect change
↓
Classify change
↓
Identify affected documentation
↓
Update documentation
↓
Verify consistency
↓
Complete task


---

# FAILURE CONDITION

If documentation does not reflect code changes, the task must be marked as **incomplete**.

---

# RESULT

The repository always maintains **accurate and living documentation** that reflects the real system architecture.