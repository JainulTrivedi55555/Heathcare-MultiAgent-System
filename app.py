import streamlit as st
import time
from coordinator import HealthcareCoordinator

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MedAgent AI — Healthcare Multi-Agent System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS — Clinical Precision Aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #1a1f2e;
}

/* Background */
.stApp {
    background: #f4f6fb;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0f1b2d 0%, #1a2e4a 60%, #0d2137 100%);
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #c8d8eb !important;
}
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

/* Main header */
.main-header {
    background: linear-gradient(135deg, #0f1b2d 0%, #1a3a5c 100%);
    color: white;
    padding: 2.5rem 3rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(64,196,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.main-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    font-weight: 400;
    margin: 0;
    color: white;
    letter-spacing: -0.5px;
}
.main-header p {
    font-size: 1rem;
    color: rgba(255,255,255,0.65);
    margin: 0.5rem 0 0 0;
    font-weight: 300;
}
.header-badge {
    display: inline-block;
    background: rgba(64,196,255,0.15);
    color: #40c4ff;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(64,196,255,0.3);
    margin-bottom: 1rem;
}

/* Agent pipeline cards */
.agent-step {
    background: white;
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
    border-left: 4px solid #2196F3;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: all 0.2s ease;
}
.agent-step:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transform: translateY(-1px);
}
.agent-step.urgent { border-left-color: #f44336; }
.agent-step.moderate { border-left-color: #ff9800; }
.agent-step.low { border-left-color: #4caf50; }

.step-number {
    background: #e8f4fd;
    color: #1565c0;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 0.6rem;
}
.agent-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1a1f2e;
    margin: 0.3rem 0;
}
.agent-content {
    font-size: 0.92rem;
    color: #3d4960;
    line-height: 1.7;
    margin-top: 0.6rem;
    white-space: pre-wrap;
}

/* Urgency badge */
.urgency-badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-left: 0.5rem;
}
.urgency-low { background: #e8f5e9; color: #2e7d32; }
.urgency-moderate { background: #fff3e0; color: #e65100; }
.urgency-high { background: #fce4ec; color: #c62828; }
.urgency-emergency { background: #f44336; color: white; animation: pulse 1.5s infinite; }

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.6; }
    100% { opacity: 1; }
}

/* Diagnosis pills */
.dx-pill {
    display: inline-block;
    background: #e3f2fd;
    color: #0d47a1;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 4px 14px;
    border-radius: 20px;
    margin: 3px 4px 3px 0;
    border: 1px solid #bbdefb;
}

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1565c0;
    font-family: 'DM Serif Display', serif;
}
.metric-label {
    font-size: 0.78rem;
    color: #8a94a8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
    font-weight: 500;
}

/* Progress indicator */
.progress-container {
    background: white;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.progress-step {
    display: flex;
    align-items: center;
    padding: 0.5rem 0;
    font-size: 0.88rem;
    color: #8a94a8;
}
.progress-step.active { color: #1565c0; font-weight: 600; }
.progress-step.done { color: #2e7d32; }
.step-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #dde2ed;
    margin-right: 10px;
    flex-shrink: 0;
}
.step-dot.active { background: #2196f3; }
.step-dot.done { background: #4caf50; }

/* Disclaimer */
.disclaimer {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    font-size: 0.84rem;
    color: #5d4037;
    margin-top: 1.5rem;
}

/* Sidebar agent list */
.agent-list-item {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.85) !important;
    border-left: 3px solid rgba(64,196,255,0.4);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1565c0, #1976d2);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 2rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
    width: 100%;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0d47a1, #1565c0);
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(21,101,192,0.3);
}

/* Input fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 2px solid #e8edf5;
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    transition: border 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #2196f3;
    box-shadow: 0 0 0 3px rgba(33,150,243,0.1);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 MedAgent AI")
    st.markdown("*Healthcare Multi-Agent System*")
    st.markdown("---")

    st.markdown("### 🤖 Active Agents")
    agents_info = [
        ("🔬", "Symptom Checker", "Analyzes symptoms, identifies possible diagnoses & urgency"),
        ("📚", "Medical Knowledge", "Deep-dives into each condition with clinical detail"),
        ("💊", "Treatment Recommender", "Evidence-based treatment plans per diagnosis"),
        ("📅", "Appointment Scheduler", "Routes to right specialist with dynamic scheduling"),
        ("📋", "Follow-Up Coordinator", "Personalized recovery plans & monitoring reminders"),
    ]
    for icon, name, desc in agents_info:
        st.markdown(f"""
        <div class="agent-list-item">
            <strong>{icon} {name}</strong><br>
            <span style="font-size:0.78rem;opacity:0.7">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ System Info")
    st.markdown("""
    <div style="font-size:0.82rem; opacity:0.75;">
    • <strong>Model:</strong> GPT-4o<br>
    • <strong>Architecture:</strong> ReAct Loop<br>
    • <strong>Agents:</strong> 5 Specialized<br>
    • <strong>Tool Calls:</strong> XML-parsed<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; opacity:0.5; text-align:center;">
    Built with OpenAI GPT-4o<br>
    Not for medical diagnosis
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Main Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="header-badge">Multi-Agent AI System</div>
    <h1>Healthcare Intelligence Platform</h1>
    <p>5 specialized AI agents working in concert — from symptom analysis to follow-up care</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Patient Input Form
# ─────────────────────────────────────────────
with st.container():
    col1, col2 = st.columns([1, 2])

    with col1:
        patient_name = st.text_input(
            "👤 Patient Name",
            placeholder="e.g. John Doe",
            help="Enter the patient's full name"
        )

    with col2:
        symptoms = st.text_area(
            "🩺 Describe Symptoms",
            placeholder="e.g. I have had a high fever (102°F), severe cough, body aches, and fatigue for the past 3 days. I also have a slight loss of taste.",
            height=100,
            help="Be as specific as possible — include duration, severity, and any associated symptoms"
        )

    # Example symptoms buttons
    st.markdown("**Quick examples:**")
    ex_col1, ex_col2, ex_col3, ex_col4 = st.columns(4)
    examples = {
        "🤧 Cold/Flu": ("Alex Smith", "Fever, cough, body aches, runny nose, and fatigue for 3 days."),
        "🤕 Migraine": ("Sarah Chen", "Severe throbbing headache on the left side, nausea, and sensitivity to light for 6 hours."),
        "🤢 GI Issue": ("Mike Torres", "Stomach cramping, nausea, vomiting, and diarrhea for the past 24 hours."),
        "💪 Joint Pain": ("Lisa Wong", "Swollen right knee, joint pain, and morning stiffness lasting over 30 minutes for 2 weeks."),
    }
    for col, (label, (name, symp)) in zip([ex_col1, ex_col2, ex_col3, ex_col4], examples.items()):
        with col:
            if st.button(label, key=f"ex_{label}"):
                st.session_state["ex_name"] = name
                st.session_state["ex_symp"] = symp
                st.rerun()

    # Apply example if clicked
    if "ex_name" in st.session_state:
        patient_name = st.session_state["ex_name"]
        symptoms = st.session_state["ex_symp"]

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run Healthcare Analysis", key="run")


# ─────────────────────────────────────────────
# Run Pipeline
# ─────────────────────────────────────────────
if run_btn:
    if not patient_name.strip():
        st.warning("Please enter a patient name.")
    elif not symptoms.strip():
        st.warning("Please describe the patient's symptoms.")
    else:
        # Clear previous example state
        for k in ["ex_name", "ex_symp"]:
            st.session_state.pop(k, None)

        st.markdown("---")
        st.markdown("### ⚡ Running Agent Pipeline...")

        # Progress display
        progress_placeholder = st.empty()
        steps = [
            "🔬 Symptom Checker — analyzing symptoms...",
            "📚 Medical Knowledge — retrieving condition info...",
            "💊 Treatment Recommender — building treatment plans...",
            "📅 Appointment Scheduler — finding specialist availability...",
            "📋 Follow-Up Coordinator — creating care plan...",
        ]

        def update_progress(current_step: int):
            with progress_placeholder.container():
                for i, step in enumerate(steps):
                    status = "done" if i < current_step else ("active" if i == current_step else "")
                    icon = "✅" if i < current_step else ("⏳" if i == current_step else "○")
                    st.markdown(f"""
                    <div class="progress-step {status}">
                        <div class="step-dot {status}"></div>
                        {icon} {step}
                    </div>
                    """, unsafe_allow_html=True)

        update_progress(0)

        # Monkey-patch coordinator to show live progress
        coordinator = HealthcareCoordinator()

        # Override run steps with progress updates
        results = {"error": None}
        try:
            with st.spinner(""):
                # Step 1
                update_progress(0)
                diagnosis = coordinator.symptom_agent.run(symptoms)
                urgency = coordinator._extract_urgency(diagnosis)
                diagnoses = coordinator._extract_diagnoses(diagnosis)

                # Step 2
                update_progress(1)
                medical_knowledge = {}
                for disease in diagnoses[:2]:
                    info = coordinator.knowledge_agent.run(f"Tell me about {disease} in detail.")
                    medical_knowledge[disease] = info

                # Step 3
                update_progress(2)
                treatment_plans = {}
                for disease in diagnoses[:2]:
                    treatment = coordinator.treatment_agent.run(
                        f"What is the treatment plan for a patient diagnosed with {disease}?"
                    )
                    treatment_plans[disease] = treatment

                # Step 4
                update_progress(3)
                primary = diagnoses[0] if diagnoses else "General consultation"
                appointment = coordinator.scheduler_agent.run(
                    f"Schedule an appointment for '{patient_name}' diagnosed with '{primary}'. Urgency: '{urgency}'."
                )

                # Step 5
                update_progress(4)
                followup = coordinator.followup_agent.run(
                    f"Create a follow-up care plan for '{patient_name}' diagnosed with '{primary}'."
                )

                results = {
                    "patient_name": patient_name,
                    "symptoms": symptoms,
                    "symptom_analysis": diagnosis,
                    "urgency": urgency,
                    "diagnoses": diagnoses,
                    "medical_knowledge": medical_knowledge,
                    "treatment_plans": treatment_plans,
                    "appointment": appointment,
                    "followup": followup,
                    "error": None,
                }

        except Exception as e:
            results["error"] = str(e)
            st.error(f"Pipeline error: {e}")

        progress_placeholder.empty()

        if not results.get("error"):
            # ── Summary Metrics ──────────────────────────────────────────
            st.markdown("---")
            st.markdown("### 📊 Analysis Summary")

            urgency_color = {
                "Low": "#4caf50", "Moderate": "#ff9800",
                "High": "#f44336", "Emergency": "#b71c1c"
            }.get(results["urgency"], "#2196f3")

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(results['diagnoses'])}</div>
                    <div class="metric-label">Possible Diagnoses</div>
                </div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{urgency_color}">{results['urgency']}</div>
                    <div class="metric-label">Urgency Level</div>
                </div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">5</div>
                    <div class="metric-label">Agents Completed</div>
                </div>""", unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">✓</div>
                    <div class="metric-label">Care Plan Ready</div>
                </div>""", unsafe_allow_html=True)

            # ── Diagnoses Pills ──────────────────────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            pills_html = "".join([f'<span class="dx-pill">{d}</span>' for d in results["diagnoses"]])
            st.markdown(f"**Possible Diagnoses:** {pills_html}", unsafe_allow_html=True)

            st.markdown("---")

            # ── Step 1: Symptom Analysis ─────────────────────────────────
            urgency_class = results["urgency"].lower()
            st.markdown(f"""
            <div class="agent-step {urgency_class}">
                <div class="step-number">Step 1 · Symptom Checker</div>
                <div class="agent-title">🔬 Symptom Analysis Report</div>
                <div class="agent-content">{results['symptom_analysis']}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Step 2: Medical Knowledge ────────────────────────────────
            for disease, info in results["medical_knowledge"].items():
                st.markdown(f"""
                <div class="agent-step">
                    <div class="step-number">Step 2 · Medical Knowledge</div>
                    <div class="agent-title">📚 {disease}</div>
                    <div class="agent-content">{info}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Step 3: Treatment Plans ──────────────────────────────────
            for disease, treatment in results["treatment_plans"].items():
                st.markdown(f"""
                <div class="agent-step">
                    <div class="step-number">Step 3 · Treatment Plan</div>
                    <div class="agent-title">💊 Treatment: {disease}</div>
                    <div class="agent-content">{treatment}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Step 4: Appointment ──────────────────────────────────────
            st.markdown(f"""
            <div class="agent-step">
                <div class="step-number">Step 4 · Appointment Scheduler</div>
                <div class="agent-title">📅 Appointment Confirmed</div>
                <div class="agent-content">{results['appointment']}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Step 5: Follow-Up ────────────────────────────────────────
            st.markdown(f"""
            <div class="agent-step low">
                <div class="step-number">Step 5 · Follow-Up Coordinator</div>
                <div class="agent-title">📋 Personalized Care Plan</div>
                <div class="agent-content">{results['followup']}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Download Report ──────────────────────────────────────────
            st.markdown("---")
            report_text = f"""HEALTHCARE MULTI-AGENT SYSTEM — PATIENT REPORT
{'='*60}
Patient: {results['patient_name']}
Symptoms: {results['symptoms']}
Urgency: {results['urgency']}
Diagnoses: {', '.join(results['diagnoses'])}

SYMPTOM ANALYSIS
{'-'*40}
{results['symptom_analysis']}

MEDICAL KNOWLEDGE
{'-'*40}
"""
            for disease, info in results["medical_knowledge"].items():
                report_text += f"\n{disease}:\n{info}\n"

            report_text += f"\nTREATMENT PLANS\n{'-'*40}\n"
            for disease, treatment in results["treatment_plans"].items():
                report_text += f"\n{disease}:\n{treatment}\n"

            report_text += f"\nAPPOINTMENT\n{'-'*40}\n{results['appointment']}\n"
            report_text += f"\nFOLLOW-UP PLAN\n{'-'*40}\n{results['followup']}\n"
            report_text += f"\n{'='*60}\nDISCLAIMER: For informational purposes only. Not a substitute for professional medical advice.\n"

            st.download_button(
                label="📥 Download Full Report (.txt)",
                data=report_text,
                file_name=f"medical_report_{patient_name.replace(' ', '_')}.txt",
                mime="text/plain",
            )

            # Disclaimer
            st.markdown("""
            <div class="disclaimer">
            ⚠️ <strong>Medical Disclaimer:</strong> This system is for educational and informational purposes only. 
            It does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare 
            professional for medical concerns. In case of emergency, call <strong>911</strong> immediately.
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Empty state
# ─────────────────────────────────────────────
elif not run_btn:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 2rem; color: #8a94a8;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🏥</div>
        <div style="font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: #3d4960; margin-bottom: 0.5rem;">
            Ready to analyze
        </div>
        <div style="font-size: 0.9rem;">
            Enter a patient name and describe their symptoms above, then click <strong>Run Healthcare Analysis</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
