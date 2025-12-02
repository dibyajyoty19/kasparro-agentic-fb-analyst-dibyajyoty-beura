# Kasparro — Agentic Facebook Performance Analyst

A multi-agent, autonomous system designed to diagnose Facebook Ads performance, explain **why ROAS changed over time**, and generate **creative recommendations** to improve low-CTR campaigns.  
Built as part of the **Kasparro Applied AI Engineer Assignment**.

---

## 🚀 Quick Start

```bash
python -V  #should be >= 3.10

#Create and activate virtual environment
python -m venv .venv
#Windows
.venv\Scripts\activate
#macOS / Linux
#source .venv/bin/activate

pip install -r requirements.txt

#Run analysis
python run.py "Analyze ROAS drop"

### V2 Improvements

- Added structured JSON-based logging with RunLogger
- Introduced retry logic for resilient workflow execution (LLM/data operations)
- Added strict schema validation with early failure
- Added edge-case tests (zero rows, missing columns)
- Improved evaluator with evidence richness (baseline vs recent ROAS)
- Added Makefile for simple developer experience (setup/run/test)
- Added detailed report generation with call-to-action insights
- Added per-agent execution logging and timing-based observability

make setup
make run
make test
python run.py "Analyze ROAS drop"


