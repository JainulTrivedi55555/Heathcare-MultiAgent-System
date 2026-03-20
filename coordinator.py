import re
import logging
from typing import Dict, Any
from agents.symptom_checker import SymptomCheckerAgent
from agents.medical_knowledge import MedicalKnowledgeAgent
from agents.treatment_agent import TreatmentRecommendationAgent
from agents.appointment_scheduler import AppointmentSchedulerAgent
from agents.patient_followup import PatientFollowUpAgent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [Coordinator] %(levelname)s: %(message)s")
logger = logging.getLogger("HealthcareCoordinator")


class HealthcareCoordinator:
    """
    Orchestrates 5 specialized AI agents in a sequential healthcare workflow:
    1. SymptomCheckerAgent     — Analyzes symptoms → returns diagnosis + urgency
    2. MedicalKnowledgeAgent   — Deep dives into each diagnosis
    3. TreatmentRecommendationAgent — Provides treatment plans
    4. AppointmentSchedulerAgent    — Books appropriate specialist appointment
    5. PatientFollowUpAgent         — Creates a personalized follow-up care plan
    """

    def __init__(self):
        logger.info("Initializing Healthcare Multi-Agent System...")
        self.symptom_agent = SymptomCheckerAgent()
        self.knowledge_agent = MedicalKnowledgeAgent()
        self.treatment_agent = TreatmentRecommendationAgent()
        self.scheduler_agent = AppointmentSchedulerAgent()
        self.followup_agent = PatientFollowUpAgent()
        logger.info("All 5 agents initialized successfully.")

    def _extract_urgency(self, diagnosis_text: str) -> str:
        """Extract urgency level from symptom checker output."""
        text_lower = diagnosis_text.lower()
        if "emergency" in text_lower:
            return "Emergency"
        elif "high" in text_lower:
            return "High"
        elif "moderate" in text_lower:
            return "Moderate"
        return "Low"

    def _extract_diagnoses(self, diagnosis_text: str) -> list:
        """
        Parse ALL possible diagnoses from symptom checker output.
        Handles multiple LLM output formats without capping results.
        Filters out non-diagnosis bullets (recommendations, observations etc.)
        """
        # Step 1: Try to isolate diagnosis section first, then extract from it
        # This prevents picking up recommendation bullets as diagnoses
        section_patterns = [
            r"[Pp]ossible [Dd]iagnos[ei]s[:\s]*\*?\*?\n((?:[\-\*•\d].*\n?)+)",
            r"\*\*[Pp]ossible [Dd]iagnos[ei]s[:\s]*\*\*\n((?:[\-\*•\d].*\n?)+)",
            r"diagnoses are[:\s]*\n((?:[\-\*•\d].*\n?)+)",
        ]
        for pattern in section_patterns:
            match = re.search(pattern, diagnosis_text, re.IGNORECASE)
            if match:
                section = match.group(1)
                items = re.findall(r"^[\-\*•]\s+(.+)$|^\d+[\.\)]\s+(.+)$", section, re.MULTILINE)
                results = [(a or b).strip() for a, b in items if (a or b).strip()]
                if results:
                    return results

        # Step 2: Inline format 'Possible diagnoses: X, Y, Z'
        match = re.search(r"[Pp]ossible diagnos[ei]s[:\s]+([^\n]+)", diagnosis_text)
        if match:
            raw = match.group(1)
            raw = re.sub(r"[Uu]rgency.*", "", raw, flags=re.IGNORECASE)
            items = [d.strip().strip(".").strip(",") for d in raw.split(",") if d.strip()]
            if items and "are" not in items[0].lower() and len(items[0]) < 50:
                return items

        # Step 3: Numbered list anywhere in text
        numbered = re.findall(r"^\d+[\.\)]\s+(.+)$", diagnosis_text, re.MULTILINE)
        if numbered:
            diagnoses = [n.strip() for n in numbered if len(n.strip()) < 60]
            if diagnoses:
                return diagnoses

        # Step 4: Bullet list — filter out recommendation/observation sentences
        # Diagnoses are short condition names, not full sentences
        skip_keywords = ["rest", "hydrat", "consult", "monitor", "seek", "avoid",
                         "take", "fever present", "symptom", "recommend", "if you"]
        bullets = re.findall(r"^[\-\*•]\s+(.+)$", diagnosis_text, re.MULTILINE)
        if bullets:
            diagnoses = [
                b.strip() for b in bullets
                if len(b.strip()) < 50
                and not any(kw in b.lower() for kw in skip_keywords)
            ]
            if diagnoses:
                return diagnoses

        return ["General condition — consult a doctor"]

    def handle_patient(self, patient_name: str, symptoms: str) -> Dict[str, Any]:
        """
        Main entry point. Runs the full multi-agent pipeline.
        Returns a structured dict with all agent outputs for use by CLI or Streamlit UI.
        """
        results: Dict[str, Any] = {
            "patient_name": patient_name,
            "symptoms": symptoms,
            "symptom_analysis": "",
            "urgency": "Low",
            "diagnoses": [],
            "medical_knowledge": {},
            "treatment_plans": {},
            "appointment": "",
            "followup": "",
            "error": None,
        }

        try:
            # ── Step 1: Symptom Analysis ──────────────────────────────────────
            logger.info(f"[Step 1] Running SymptomCheckerAgent for {patient_name}...")
            diagnosis = self.symptom_agent.run(symptoms)
            results["symptom_analysis"] = diagnosis
            results["urgency"] = self._extract_urgency(diagnosis)
            results["diagnoses"] = self._extract_diagnoses(diagnosis)
            logger.info(f"Diagnoses found: {results['diagnoses']}")

            # ── Step 2: Medical Knowledge (ALL diagnoses) ────────────────────
            for disease in results["diagnoses"]:
                logger.info(f"[Step 2] Running MedicalKnowledgeAgent for: {disease}")
                info = self.knowledge_agent.run(f"Tell me about {disease} in detail.")
                results["medical_knowledge"][disease] = info

            # ── Step 3: Treatment Recommendations (ALL diagnoses) ─────────────
            for disease in results["diagnoses"]:
                logger.info(f"[Step 3] Running TreatmentRecommendationAgent for: {disease}")
                treatment = self.treatment_agent.run(
                    f"What is the treatment plan for a patient diagnosed with {disease}?"
                )
                results["treatment_plans"][disease] = treatment

            # ── Step 4: Appointment Scheduling ────────────────────────────────
            logger.info(f"[Step 4] Running AppointmentSchedulerAgent for {patient_name}...")
            primary_diagnosis = top_diagnoses[0] if top_diagnoses else "General consultation"
            appointment = self.scheduler_agent.run(
                f"Schedule an appointment for patient '{patient_name}' diagnosed with '{primary_diagnosis}'. "
                f"Urgency level is '{results['urgency']}'."
            )
            results["appointment"] = appointment

            # ── Step 5: Follow-Up Plan ─────────────────────────────────────────
            logger.info(f"[Step 5] Running PatientFollowUpAgent for {patient_name}...")
            followup = self.followup_agent.run(
                f"Create a follow-up care plan for patient '{patient_name}' "
                f"diagnosed with '{primary_diagnosis}'."
            )
            results["followup"] = followup

            logger.info("✅ Multi-agent pipeline completed successfully.")

        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            results["error"] = str(e)

        return results

    def print_results(self, results: Dict[str, Any]) -> None:
        """Pretty-print results to the console (for CLI usage)."""
        sep = "─" * 60
        print(f"\n{'═' * 60}")
        print(f"  HEALTHCARE MULTI-AGENT SYSTEM — PATIENT REPORT")
        print(f"{'═' * 60}")
        print(f"Patient: {results['patient_name']}")
        print(f"Reported Symptoms: {results['symptoms']}")
        print(f"Urgency Level: {results['urgency']}")

        print(f"\n{sep}")
        print("STEP 1 — SYMPTOM ANALYSIS")
        print(sep)
        print(results["symptom_analysis"])

        for disease, info in results["medical_knowledge"].items():
            print(f"\n{sep}")
            print(f"STEP 2 — MEDICAL KNOWLEDGE: {disease.upper()}")
            print(sep)
            print(info)

        for disease, treatment in results["treatment_plans"].items():
            print(f"\n{sep}")
            print(f"STEP 3 — TREATMENT PLAN: {disease.upper()}")
            print(sep)
            print(treatment)

        print(f"\n{sep}")
        print("STEP 4 — APPOINTMENT SCHEDULED")
        print(sep)
        print(results["appointment"])

        print(f"\n{sep}")
        print("STEP 5 — FOLLOW-UP CARE PLAN")
        print(sep)
        print(results["followup"])

        if results.get("error"):
            print(f"\n⚠️ Error during pipeline: {results['error']}")

        print(f"\n{'═' * 60}")
        print("⚠️  DISCLAIMER: This system is for informational purposes only.")
        print("    Always consult a licensed healthcare professional.")
        print(f"{'═' * 60}\n")