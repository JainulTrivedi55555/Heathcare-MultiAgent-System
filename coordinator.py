from agents.symptom_checker import SymptomCheckerAgent
from agents.medical_knowledge import MedicalKnowledgeAgent
from agents.appointment_scheduler import AppointmentSchedulerAgent
from agents.patient_followup import PatientFollowUpAgent

class HealthcareCoordinator:
    def __init__(self):
        self.symptom_agent = SymptomCheckerAgent()
        self.knowledge_agent = MedicalKnowledgeAgent()
        self.scheduler_agent = AppointmentSchedulerAgent()
        self.followup_agent = PatientFollowUpAgent()

    def handle_patient(self, patient_name: str, symptoms: str):
        print(f"Patient: {patient_name} reports symptoms: {symptoms}\n")

        diagnosis = self.symptom_agent.run(symptoms)
        print(f"SymptomCheckerAgent:\n{diagnosis}\n")

        diseases = []
        for line in diagnosis.splitlines():
            if "Possible diagnoses:" in line:
                diseases = [d.strip() for d in line.split(":")[1].split(",")]
                break

        for disease in diseases:
            info = self.knowledge_agent.run(f"Tell me about {disease}.")
            print(f"MedicalKnowledgeAgent info on {disease}:\n{info}\n")

        appointment = self.scheduler_agent.run(
            f"Schedule appointment for {patient_name} with General Practitioner on 2024-07-01."
        )
        print(f"AppointmentSchedulerAgent:\n{appointment}\n")

        reminder = self.followup_agent.run(f"Send follow-up reminder to {patient_name}.")
        print(f"PatientFollowUpAgent:\n{reminder}\n")