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
        """Parse possible diagnoses from symptom checker output."""
        for line in diagnosis_text.splitlines():
            if "possible diagnoses:" in line.lower():
                raw = line.split(":", 1)[1]
                # Remove urgency info and clean up
                raw = re.sub(r"urgency.*", "", raw, flags=re.IGNORECASE)
                return [d.strip().strip(".") for d in raw.split(",") if d.strip()]
        # Fallback: look for comma-separated list in full text
        matches = re.findall(r"Possible diagnoses?[:\s]+([^\n.]+)", diagnosis_text, re.IGNORECASE)
        if matches:
            return [d.strip() for d in matches[0].split(",")]
        return ["General condition — see doctor"]

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

            # ── Step 2: Medical Knowledge (top 2 diagnoses) ───────────────────
            top_diagnoses = results["diagnoses"][:2]
            for disease in top_diagnoses:
                logger.info(f"[Step 2] Running MedicalKnowledgeAgent for: {disease}")
                info = self.knowledge_agent.run(f"Tell me about {disease} in detail.")
                results["medical_knowledge"][disease] = info

            # ── Step 3: Treatment Recommendations (top 2 diagnoses) ───────────
            for disease in top_diagnoses:
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
