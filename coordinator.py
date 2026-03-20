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
        Parse possible diagnoses from symptom checker output.
        Handles all Groq/Llama output formats including nested bullet lists,
        bold markdown headers, numbered lists, and inline comma-separated lists.
        """
        # Step 1: Find 'Possible Diagnoses' section and grab nested items under it
        # Handles: * **Possible Diagnoses:** followed by + Item or - Item or 1. Item
        section_match = re.search(
            r"\*{0,2}[Pp]ossible\s+[Dd]iagnos[ei]s[:\s]*\*{0,2}\s*\n((?:[ \t]*[\+\-\*•\d].*\n?)+)",
            diagnosis_text, re.IGNORECASE
        )
        if section_match:
            section = section_match.group(1)
            items = re.findall(r"[ \t]*[\+\-\*•][ \t]+(.+)|[ \t]*\d+[\.\)][ \t]+(.+)", section)
            results = []
            for a, b in items:
                val = (a or b).strip().strip("*").strip()
                if val and len(val) > 1 and not any(
                    kw in val.lower() for kw in ["urgency", "level", "moderate", "high", "low", "emergency"]
                ):
                    results.append(val)
            if results:
                return results

        # Step 2: Inline format 'Possible diagnoses: X, Y, Z'
        match = re.search(r"[Pp]ossible diagnos[ei]s[:\s]+([^\n\*]+)", diagnosis_text)
        if match:
            raw = re.sub(r"[Uu]rgency.*", "", match.group(1), flags=re.IGNORECASE)
            items = [d.strip().strip(".").strip(",").strip("*") for d in raw.split(",") if d.strip()]
            if items and "are" not in items[0].lower() and len(items[0]) < 60:
                return items

        # Step 3: Numbered list
        numbered = re.findall(r"^\d+[\.\)]\s+(.+)$", diagnosis_text, re.MULTILINE)
        if numbered:
            clean = [n.strip().strip("*") for n in numbered
                     if 2 < len(n.strip()) < 60
                     and not any(kw in n.lower() for kw in ["urgency", "moderate", "high", "low"])]
            if clean:
                return clean

        # Step 4: Flat bullet list — strict filter to exclude recommendations
        skip = ["rest", "hydrat", "consult", "monitor", "seek", "avoid", "take ",
                "fever", "symptom", "recommend", "if you", "stay", "urgency",
                "observation", "next step", "level", "report", "moderate", "high", "low"]
        bullets = re.findall(r"^[ \t]*[\+\-\*•][ \t]+(.+)$", diagnosis_text, re.MULTILINE)
        if bullets:
            clean = [b.strip().strip("*").strip() for b in bullets
                     if 2 < len(b.strip()) < 60
                     and not any(kw in b.lower() for kw in skip)]
            if clean:
                return clean

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