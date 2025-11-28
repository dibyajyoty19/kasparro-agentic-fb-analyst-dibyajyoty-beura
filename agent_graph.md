# Agent Graph — Kasparro Agentic Facebook Performance Analyst

##  System Overview
This multi-agent system autonomously analyzes Facebook Ads performance, identifies ROAS changes, evaluates hypotheses, and suggests improved creative messaging.

---

##  Agent Responsibilities

| Agent | Role / Function |
|--------|----------------|
| **Planner Agent** | Breaks user query into subtasks + workflow |
| **Data Agent** | Loads dataset and generates performance summaries |
| **Insight Agent** | Creates hypotheses explaining ROAS changes |
| **Evaluator Agent** | Validates hypotheses using numeric evidence |
| **Creative Agent** | Generates new creative ideas for low-CTR campaigns |

---

##  Agent-to-Agent Communication Flow

```text
User Query (e.g., "Analyze ROAS drop")

           │
           ▼
     🧠 Planner Agent
           │
           ├─ T1: Data request → 📊 Data Agent
           │                     │
           │                     └── Data Summary:
           │                         - ROAS trends
           │                         - CTR distribution
           │                         - Low CTR campaigns
           │
           ├─ T2: Insight generation → 💡 Insight Agent
           │                           │
           │                           └── Hypotheses (audience fatigue, creative decline, targeting mismatch)
           │
           ├─ T3: Validation → 📐 Evaluator Agent
           │                     │
           │                     └── Validated hypotheses
           │                         - is_supported
           │                         - evidence numbers
           │                         - confidence score
           │
           └─ T4: Creative guidance → 🎨 Creative Agent
                                     │
                                     └── Recommendations:
                                         - Headlines
                                         - Messaging variants
                                         - Call-to-action ideas

           ▼
     📦 Orchestrator Packs Outputs
           │
           ├── insights.json
           ├── creatives.json
           ├── report.md
           └── logs/
