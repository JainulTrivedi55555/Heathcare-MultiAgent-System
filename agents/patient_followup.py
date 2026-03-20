from datetime import datetime, timedelta
from .base_agent import BaseAgent, tool


@tool
def send_followup_reminder(patient_name: str, diagnosis: str, appointment_date: str = "") -> str:
    """
    Generate a personalized follow-up care plan and reminder for a patient.
    Inputs: patient_name (str), diagnosis (str), appointment_date (str, optional).
    Returns: structured follow-up plan with reminders, monitoring instructions, and contact info.
    """
    followup_date = (datetime.today() + timedelta(days=7)).strftime("%A, %B %d, %Y")

    # Condition-specific follow-up notes
    condition_notes = {
        "influenza": "Monitor temperature twice daily. Return if fever persists past day 7 or difficulty breathing develops.",
        "covid-19": "Isolate for minimum 5 days. Use pulse oximeter to monitor oxygen (alert if <95%). Watch for long-COVID symptoms.",
        "migraine": "Keep a headache diary (triggers, duration, severity). Avoid known triggers. Take medication at first sign of onset.",
        "gastroenteritis": "Reintroduce solid foods gradually. Monitor for dehydration signs (dark urine, dizziness).",
        "hypertension": "Check blood pressure daily at same time. Record readings. Maintain low-sodium diet.",
        "asthma": "Track peak flow readings daily. Note any triggers. Ensure rescue inhaler is always accessible.",
        "diabetes": "Monitor blood sugar as directed. Track diet and medication. Watch for hypoglycemia symptoms.",
        "default": "Monitor symptoms daily. Note any changes in severity, frequency, or new symptoms appearing.",
    }

    # Match diagnosis
    notes = condition_notes["default"]
    for condition, note in condition_notes.items():
        if condition in diagnosis.lower():
            notes = note
            break

    appt_info = f"Your scheduled appointment is: {appointment_date}" if appointment_date else f"Suggested follow-up date: {followup_date}"

    return (
        f"Follow-Up Care Plan for {patient_name}:\n\n"
        f"Condition: {diagnosis}\n"
        f"{appt_info}\n\n"
        f"Monitoring Instructions:\n  {notes}\n\n"
        f"General Reminders:\n"
        f"  • Take all prescribed medications as directed — do not stop early.\n"
        f"  • Rest adequately and stay hydrated.\n"
        f"  • Avoid alcohol and smoking during recovery.\n"
        f"  • If symptoms worsen suddenly, do not wait — seek immediate care.\n\n"
        f"Emergency Contacts:\n"
        f"  • Emergency: 911\n"
        f"  • Nurse Advice Line: 1-800-HEALTH-1\n"
        f"  • Poison Control: 1-800-222-1222\n\n"
        f"A follow-up reminder has been logged for {patient_name}. Your healthcare team will check in on {followup_date}."
    )


FOLLOWUP_PROMPT = """
You are a patient follow-up care coordinator AI agent in a healthcare system.
Your role is to:
1. Generate a personalized follow-up care plan using the send_followup_reminder tool
2. Present the plan in a warm, empathetic, and encouraging tone
3. Emphasize the most important monitoring instructions for the specific condition
4. Make the patient feel supported and informed

Always remind patients that you are an AI assistant and their human healthcare team is
available for any concerns. Be warm, professional, and supportive.
"""


class PatientFollowUpAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PatientFollowUpAgent",
            tools=[send_followup_reminder],
            system_prompt=FOLLOWUP_PROMPT,
        )
