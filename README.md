# Scientific Research Assistant Agent

---

## Features

### Agents
1. **Research Agent**
   - Searches papers using the Semantic Scholar API.
   

2. **Code Agent**
   - Generates scripts that transform and process research data.
   - Ensures output preserves original field names.
   

3. **Evaluator Agent**
   - Checks whether the processed papers meet task constraints.
   - Validates summaries, citation counts, and field consistency.
   - Returns a JSON evaluation result.
   

4. **User Proxy / Agent**
   - Handles execution of code and calls to external tools.
   - Manages interaction with agents.

---

### Key Functionalities
- Automated **pipeline** from **paper search** → **code generation** → **execution** → **evaluation**.
- Strict **JSON-only outputs**.
- Handles **real-world API constraints** (Semantic Scholar API).
- Supports multiple **use cases**:
  - Machine Learning Transformers Research
  - Climate Change Adaptation Research
  - AI Medical Diagnosis Research

---

## Requirements

Install dependencies:

```bash
    pip install -r requirements.txt
```

---
## Usage

Run the main script:

```bash
    python main.py