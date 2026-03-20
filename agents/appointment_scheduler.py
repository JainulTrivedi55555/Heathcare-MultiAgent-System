from datetime import datetime, timedelta
import random
from .base_agent import BaseAgent, tool

SPECIALTY_ROUTING = {
    "migraine": "Neurologist",
    "tension headache": "General Practitioner",
    "meningitis": "Emergency — Neurologist",
    "influenza": "General Practitioner",
    "common cold": "General Practitioner",
    "covid-19": "General Practitioner",
    "pneumonia": "Pulmonologist",
    "asthma": "Pulmonologist",
    "copd": "Pulmonologist",
    "gastroenteritis": "General Practitioner",
    "appendicitis": "Emergency Surgeon",
    "gerd": "Gastroenterologist",
    "gout": "Rheumatologist",
    "rheumatoid arthritis": "Rheumatologist",
    "hypertension": "Cardiologist",
    "diabetes": "Endocrinologist",
    "anemia": "Hematologist",
    "back pain": "Orthopedist or General Practitioner",
    "rash": "Dermatologist",
    "default": "General Practitioner",
}

AVAILABLE_SLOTS = ["9:00 AM", "10:30 AM", "12:00 PM", "2:00 PM", "3:30 PM", "4:45 PM"]


@tool
def schedule_appointment(patient_name: str, diagnosis: str, urgency: str = "Low") -> str:
    """
    Schedule a medical appointment based on patient name, diagnosis, and urgency level.
    Automatically routes to the appropriate specialist and finds the next available slot.
    Inputs: patient_name (str), diagnosis (str), urgency (str: Low/Moderate/High/Emergency).
    """
    # Determine urgency-based wait time
    urgency_lower = urgency.lower()
    if "emergency" in urgency_lower:
        return (
            f"⚠️ EMERGENCY ALERT for {patient_name}: "
            "Do NOT schedule a routine appointment. Call 911 or go to the nearest Emergency Room immediately."
        )
    elif "high" in urgency_lower:
        days_out = 1
    elif "moderate" in urgency_lower:
        days_out = random.randint(2, 4)
    else:
        days_out = random.randint(5, 10)

    # Route to appropriate specialist
    specialist = SPECIALTY_ROUTING.get("default")
    for condition, spec in SPECIALTY_ROUTING.items():
        if condition in diagnosis.lower():
            specialist = spec
            break

    # Generate appointment date (skip weekends)
    appt_date = datetime.today() + timedelta(days=days_out)
    while appt_date.weekday() >= 5:  # Skip Saturday (5) and Sunday (6)
        appt_date += timedelta(days=1)

    time_slot = random.choice(AVAILABLE_SLOTS)
    formatted_date = appt_date.strftime("%A, %B %d, %Y")

    return (
        f"Appointment Confirmed:\n"
        f"  Patient: {patient_name}\n"
        f"  Specialist: {specialist}\n"
        f"  Date: {formatted_date}\n"
        f"  Time: {time_slot}\n"
        f"  Reason: {diagnosis}\n"
        f"  Urgency: {urgency}\n"
        f"  Please bring your insurance card, ID, and a list of current medications."
    )


SCHEDULER_PROMPT = """
You are a medical appointment scheduling AI agent in a healthcare system.
You receive patient information and a diagnosis, then schedule an appropriate appointment.
Use the schedule_appointment tool to book the appointment.
Present the confirmed appointment details clearly, and add any preparation instructions
the patient should follow before their visit (fasting requirements, what to bring, etc.).
Always be professional, reassuring, and clear.
"""


class AppointmentSchedulerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AppointmentSchedulerAgent",
            tools=[schedule_appointment],
            system_prompt=SCHEDULER_PROMPT,
        )
