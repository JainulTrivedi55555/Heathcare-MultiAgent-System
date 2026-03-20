import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from coordinator import HealthcareCoordinator

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MedAgent AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f8; }

[data-testid="stSidebar"] { background: #0a1628; }
[data-testid="stSidebar"] * { color: #a8bfd4 !important; }
[data-testid="stSidebar"] strong { color: #e2eaf3 !important; }

.agent-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px 14px;
    margin: 6px 0;
}
.agent-card-name { font-size: 0.82rem; font-weight: 600; color: #7dd3fc !important; }
.agent-card-desc { font-size: 0.73rem; color: #64748b !important; margin-top: 2px; line-height: 1.4; }

.page-header {
    background: linear-gradient(135deg, #0f2744 0%, #1e4080 100%);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.page-header::after {
    content: '🏥';
    position: absolute;
    right: 40px; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.12;
}
.header-tag {
    background: rgba(96,165,250,0.2);
    color: #93c5fd;
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    padding: 4px 12px; border-radius: 20px;
    border: 1px solid rgba(96,165,250,0.3);
    display: inline-block; margin-bottom: 14px;
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem; color: #ffffff;
    margin: 0 0 8px 0; line-height: 1.2;
}
.header-sub { color: rgba(255,255,255,0.55); font-size: 0.92rem; margin: 0; font-weight: 300; }

.metric-box {
    background: white; border-radius: 12px;
    padding: 20px; text-align: center;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    border-top: 3px solid #3b82f6;
}
.metric-box.orange { border-top-color: #f97316; }
.metric-box.green { border-top-color: #22c55e; }
.metric-box.red { border-top-color: #ef4444; }
.metric-num { font-size: 1.9rem; font-weight: 700; color: #1e293b; line-height: 1; margin-bottom: 6px; }
.metric-num.orange { color: #ea580c; }
.metric-num.green { color: #16a34a; }
.metric-num.red { color: #dc2626; }
.metric-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; }

.pills-wrap { margin: 0 0 24px 0; }
.pill {
    display: inline-block; background: #eff6ff;
    color: #1d4ed8; border: 1px solid #bfdbfe;
    border-radius: 20px; padding: 5px 14px;
    font-size: 0.8rem; font-weight: 500;
    margin: 3px 4px 3px 0;
}

.result-card {
    background: white; border-radius: 14px;
    margin: 16px 0; overflow: hidden;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
}
.result-card-header {
    padding: 16px 24px;
    display: flex; align-items: center; gap: 12px;
    border-bottom: 1px solid #f1f5f9;
    background: #fafbfc;
}
.step-badge {
    background: #e0e7ff; color: #4338ca;
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 1.2px; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px;
    white-space: nowrap;
}
.step-badge.green { background: #dcfce7; color: #15803d; }
.step-badge.orange { background: #fff7ed; color: #c2410c; }
.step-badge.red { background: #fee2e2; color: #b91c1c; }
.card-title { font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0; }
.result-card-body { padding: 20px 24px; color: #374151; font-size: 0.9rem; line-height: 1.8; }

.progress-wrap {
    background: white; border-radius: 12px;
    padding: 20px 24px; margin-bottom: 20px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
}
.prog-item { display: flex; align-items: center; padding: 7px 0; font-size: 0.85rem; color: #94a3b8; gap: 12px; }
.prog-item.done { color: #16a34a; font-weight: 500; }
.prog-item.active { color: #2563eb; font-weight: 600; }
.prog-dot { width: 9px; height: 9px; border-radius: 50%; background: #e2e8f0; flex-shrink: 0; }
.prog-dot.done { background: #22c55e; }
.prog-dot.active { background: #3b82f6; }

.disclaimer {
    background: #fffbeb; border: 1px solid #fde68a;
    border-radius: 10px; padding: 14px 20px;
    font-size: 0.82rem; color: #78350f; margin-top: 20px;
}

.stButton > button {
    background: #1d4ed8 !important; color: white !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 28px !important; font-weight: 600 !important;
    font-size: 0.92rem !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #1e40af !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(29,78,216,0.35) !important;
}

#MainMenu, footer, .stDeployButton { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 MedAgent AI")
    st.caption("Healthcare Multi-Agent System")
    st.divider()
    st.markdown("**Active Agents**")
    agents = [
        ("🔬", "Symptom Checker", "Analyzes symptoms, identifies diagnoses & urgency"),
        ("📚", "Medical Knowledge", "Deep-dives into each condition clinically"),
        ("💊", "Treatment Recommender", "Evidence-based treatment plans"),
        ("📅", "Appointment Scheduler", "Routes to right specialist dynamically"),
        ("📋", "Follow-Up Coordinator", "Personalized recovery & monitoring plans"),
    ]
    for icon, name, desc in agents:
        st.markdown(f"""<div class="agent-card">
            <div class="agent-card-name">{icon} {name}</div>
            <div class="agent-card-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown("**System Info**")
    st.markdown("""<div style="font-size:0.78rem;color:#64748b;line-height:2.2;">
    • <strong style="color:#94a3b8">Model:</strong> Llama 3.3 70B (Groq)<br>
    • <strong style="color:#94a3b8">Architecture:</strong> ReAct Loop<br>
    • <strong style="color:#94a3b8">Agents:</strong> 5 Specialized<br>
    • <strong style="color:#94a3b8">Tool Calls:</strong> XML-parsed
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.caption("⚠️ Not for medical diagnosis")


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="header-tag">Multi-Agent AI System</div>
    <div class="header-title">Healthcare Intelligence Platform</div>
    <p class="header-sub">5 specialized AI agents — from symptom analysis to personalized follow-up care</p>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Input
# ─────────────────────────────────────────────
col1, col2 = st.columns([1, 2])
with col1:
    patient_name = st.text_input("👤 Patient Name", placeholder="e.g. John Doe")
with col2:
    symptoms = st.text_area("🩺 Describe Symptoms",
        placeholder="e.g. High fever, severe cough, body aches and fatigue for the past 3 days...",
        height=90)

st.markdown("**Quick examples:**")
c1, c2, c3, c4 = st.columns(4)
examples = {
    "🤧 Cold / Flu": ("Alex Smith", "High fever of 102F, severe cough, body aches, runny nose and fatigue for 3 days."),
    "🤕 Migraine": ("Sarah Chen", "Severe throbbing headache on left side, nausea and sensitivity to light for 6 hours."),
    "🤢 GI Issue": ("Mike Torres", "Stomach cramping, nausea, vomiting and diarrhea for the past 24 hours."),
    "🦴 Joint Pain": ("Lisa Wong", "Swollen right knee, joint pain and morning stiffness over 30 minutes for 2 weeks."),
}
for col, (label, (name, symp)) in zip([c1, c2, c3, c4], examples.items()):
    with col:
        if st.button(label, key=label):
            st.session_state["pre_name"] = name
            st.session_state["pre_symp"] = symp
            st.rerun()

if "pre_name" in st.session_state:
    patient_name = st.session_state["pre_name"]
    symptoms = st.session_state["pre_symp"]

st.markdown("<br>", unsafe_allow_html=True)
run = st.button("🚀 Run Healthcare Analysis")


# ─────────────────────────────────────────────
# Run Pipeline
# ─────────────────────────────────────────────
if run:
    if not patient_name.strip():
        st.warning("Please enter a patient name.")
    elif not symptoms.strip():
        st.warning("Please describe the symptoms.")
    else:
        for k in ["pre_name", "pre_symp"]:
            st.session_state.pop(k, None)

        st.divider()
        st.markdown("### ⚡ Running Agent Pipeline")

        steps = [
            "🔬 Symptom Checker — analyzing symptoms...",
            "📚 Medical Knowledge — retrieving condition info...",
            "💊 Treatment Recommender — building treatment plans...",
            "📅 Appointment Scheduler — finding specialist availability...",
            "📋 Follow-Up Coordinator — creating care plan...",
        ]
        prog_ph = st.empty()

        def show_progress(current):
            html = '<div class="progress-wrap">'
            for i, s in enumerate(steps):
                cls = "done" if i < current else ("active" if i == current else "")
                icon = "✅" if i < current else ("⏳" if i == current else "○")
                html += f'<div class="prog-item {cls}"><div class="prog-dot {cls}"></div>{icon} {s}</div>'
            html += '</div>'
            prog_ph.markdown(html, unsafe_allow_html=True)

        try:
            coordinator = HealthcareCoordinator()

            show_progress(0)
            diagnosis = coordinator.symptom_agent.run(symptoms)
            urgency = coordinator._extract_urgency(diagnosis)
            diagnoses = coordinator._extract_diagnoses(diagnosis)

            show_progress(1)
            medical_knowledge = {}
            for disease in diagnoses:
                info = coordinator.knowledge_agent.run(f"Tell me about {disease} in detail.")
                medical_knowledge[disease] = info

            show_progress(2)
            treatment_plans = {}
            for disease in diagnoses:
                treatment = coordinator.treatment_agent.run(
                    f"What is the treatment plan for a patient diagnosed with {disease}?"
                )
                treatment_plans[disease] = treatment

            show_progress(3)
            primary = diagnoses[0] if diagnoses else "General consultation"
            appointment = coordinator.scheduler_agent.run(
                f"Schedule an appointment for '{patient_name}' diagnosed with '{primary}'. Urgency: '{urgency}'."
            )

            show_progress(4)
            followup = coordinator.followup_agent.run(
                f"Create a follow-up care plan for '{patient_name}' diagnosed with '{primary}'."
            )

            prog_ph.empty()

            # Metrics
            urgency_color = {"Low": "green", "Moderate": "orange", "High": "red", "Emergency": "red"}.get(urgency, "")
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""<div class="metric-box">
                    <div class="metric-num">{len(diagnoses)}</div>
                    <div class="metric-label">Possible Diagnoses</div></div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div class="metric-box {urgency_color}">
                    <div class="metric-num {urgency_color}">{urgency}</div>
                    <div class="metric-label">Urgency Level</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class="metric-box green">
                    <div class="metric-num green">5</div>
                    <div class="metric-label">Agents Completed</div></div>""", unsafe_allow_html=True)
            with m4:
                st.markdown(f"""<div class="metric-box green">
                    <div class="metric-num green">✓</div>
                    <div class="metric-label">Care Plan Ready</div></div>""", unsafe_allow_html=True)

            # Pills
            pills = "".join([f'<span class="pill">{d}</span>' for d in diagnoses])
            st.markdown(f'<div class="pills-wrap"><strong>Identified Conditions:</strong><br><br>{pills}</div>',
                        unsafe_allow_html=True)
            st.divider()

            # Step 1
            badge = {"Low": "green", "Moderate": "orange", "High": "red", "Emergency": "red"}.get(urgency, "")
            st.markdown(f"""<div class="result-card">
                <div class="result-card-header">
                    <span class="step-badge {badge}">Step 1 · Symptom Checker</span>
                    <span class="card-title">🔬 Symptom Analysis Report</span>
                </div>
                <div class="result-card-body">{diagnosis.replace(chr(10), '<br>')}</div>
            </div>""", unsafe_allow_html=True)

            # Step 2
            for disease, info in medical_knowledge.items():
                st.markdown(f"""<div class="result-card">
                    <div class="result-card-header">
                        <span class="step-badge">Step 2 · Medical Knowledge</span>
                        <span class="card-title">📚 {disease}</span>
                    </div>
                    <div class="result-card-body">{info.replace(chr(10), '<br>')}</div>
                </div>""", unsafe_allow_html=True)

            # Step 3
            for disease, treatment in treatment_plans.items():
                st.markdown(f"""<div class="result-card">
                    <div class="result-card-header">
                        <span class="step-badge orange">Step 3 · Treatment Plan</span>
                        <span class="card-title">💊 {disease}</span>
                    </div>
                    <div class="result-card-body">{treatment.replace(chr(10), '<br>')}</div>
                </div>""", unsafe_allow_html=True)

            # Step 4
            st.markdown(f"""<div class="result-card">
                <div class="result-card-header">
                    <span class="step-badge">Step 4 · Appointment Scheduler</span>
                    <span class="card-title">📅 Appointment Confirmed</span>
                </div>
                <div class="result-card-body">{appointment.replace(chr(10), '<br>')}</div>
            </div>""", unsafe_allow_html=True)

            # Step 5
            st.markdown(f"""<div class="result-card">
                <div class="result-card-header">
                    <span class="step-badge green">Step 5 · Follow-Up Coordinator</span>
                    <span class="card-title">📋 Personalized Care Plan</span>
                </div>
                <div class="result-card-body">{followup.replace(chr(10), '<br>')}</div>
            </div>""", unsafe_allow_html=True)

            # Download
            st.divider()
            report = f"""MEDAGENT AI — PATIENT REPORT
{'='*60}
Patient: {patient_name}
Symptoms: {symptoms}
Urgency: {urgency}
Diagnoses: {', '.join(diagnoses)}

SYMPTOM ANALYSIS\n{'-'*40}\n{diagnosis}

MEDICAL KNOWLEDGE\n{'-'*40}"""
            for d, info in medical_knowledge.items():
                report += f"\n{d}:\n{info}\n"
            report += f"\nTREATMENT PLANS\n{'-'*40}\n"
            for d, t in treatment_plans.items():
                report += f"\n{d}:\n{t}\n"
            report += f"\nAPPOINTMENT\n{'-'*40}\n{appointment}\n"
            report += f"\nFOLLOW-UP PLAN\n{'-'*40}\n{followup}\n"
            report += f"\n{'='*60}\nFor informational purposes only. Not a substitute for professional medical advice.\n"

            st.download_button("📥 Download Full Report (.txt)", data=report,
                file_name=f"report_{patient_name.replace(' ', '_')}.txt", mime="text/plain")

            st.markdown("""<div class="disclaimer">
            ⚠️ <strong>Medical Disclaimer:</strong> This system is for educational and informational purposes only.
            It does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare
            professional. In emergencies, call <strong>911</strong> immediately.
            </div>""", unsafe_allow_html=True)

        except Exception as e:
            prog_ph.empty()
            st.error(f"Pipeline error: {str(e)}")

else:
    st.markdown("""<div style="text-align:center;padding:4rem 2rem;color:#94a3b8;">
        <div style="font-size:3.5rem;margin-bottom:1rem;">🏥</div>
        <div style="font-size:1.3rem;font-weight:600;color:#475569;margin-bottom:8px;">Ready to analyze</div>
        <div style="font-size:0.88rem;">Enter patient name and symptoms above, then click <strong>Run Healthcare Analysis</strong></div>
    </div>""", unsafe_allow_html=True)