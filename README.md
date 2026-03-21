# MedAgent — AI Healthcare Multi-Agent System

A multi-agent AI system that takes a patient's symptoms and runs them through 5 specialized agents in sequence — from diagnosis to a personalized follow-up care plan. Available as both a CLI tool and a Streamlit web app.

> ⚠️ For informational purposes only. Not a substitute for professional medical advice.

---

## How it works

When you enter a patient's name and symptoms, the coordinator kicks off a sequential pipeline:

1. **Symptom Checker** — analyzes symptoms and identifies possible diagnoses with an urgency level (Low / Moderate / High / Emergency)
2. **Medical Knowledge** — pulls detailed info on each identified condition (what it is, duration, contagiousness, complications)
3. **Treatment Recommender** — gives a treatment plan for each diagnosis including medications, home care, and when to see a doctor
4. **Appointment Scheduler** — routes the patient to the right specialist and books a slot based on urgency
5. **Follow-Up Coordinator** — generates a personalized recovery and monitoring plan

Each agent runs on a **ReAct loop** (Reasoning + Acting) — the LLM reasons about the task, optionally calls a tool via `<tool_call>` XML tags, observes the result, and produces a final answer. All powered by **Llama 3.3 70B** via the Groq API.

---

## Stack

Python · Groq API (Llama 3.3 70B) · Streamlit · python-dotenv

---

## Setup

**1. Clone and install**
```bash
git clone https://github.com/JainulTrivedi55555/MedAgent-AI-Healthcare-MultiAgent-System.git
cd MedAgent-AI-Healthcare-MultiAgent-System
pip install -r requirements.txt
```

**2. Add your Groq API key**
```bash
cp .env.example .env
# Open .env and set your GROQ_API_KEY
```

**3. Run**

Streamlit web app:
```bash
streamlit run app.py
```

Or the CLI:
```bash
python main.py
```

---

## Project layout

```
├── app.py                        # Streamlit web UI
├── main.py                       # CLI entry point
├── coordinator.py                # Orchestrates all 5 agents sequentially
├── requirements.txt
├── .env.example
│
├── agents/
│   ├── base_agent.py             # ReAct loop + Groq LLM integration
│   ├── symptom_checker.py        # Diagnoses symptoms, assigns urgency
│   ├── medical_knowledge.py      # Condition info from internal disease DB
│   ├── treatment_agent.py        # Medication + home care recommendations
│   ├── appointment_scheduler.py  # Specialist routing + slot booking
│   └── patient_followup.py       # Recovery monitoring + reminders
│
└── .devcontainer/
    └── devcontainer.json
```
