from .base_agent import BaseAgent, tool

@tool
def schedule_appointment(patient_name: str, doctor_specialty: str, date: str) -> str:
    """Schedule an appointment"""
    return f"Appointment scheduled for {patient_name} with a {doctor_specialty} on {date}."

class AppointmentSchedulerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AppointmentSchedulerAgent",
            tools=[schedule_appointment],
            system_prompt="You schedule appointments for patients. Use tools to book appointments."
        )