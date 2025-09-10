from .base_agent import BaseAgent, tool

@tool
def send_followup_reminder(patient_name: str) -> str:
    """Send follow-up reminder to patient"""
    return f"Reminder sent to {patient_name} for follow-up consultation."

class PatientFollowUpAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PatientFollowUpAgent",
            tools=[send_followup_reminder],
            system_prompt="You send follow-up reminders to patients. Use tools to send reminders."
        )