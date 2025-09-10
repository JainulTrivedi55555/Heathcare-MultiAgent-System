from .base_agent import BaseAgent, tool

@tool
def get_disease_info(disease: str) -> str:
    """Return information about a disease"""
    info_db = {
        "Common Cold": "A viral infection of your nose and throat.",
        "Flu": "A contagious respiratory illness caused by influenza viruses.",
        "COVID-19": "A respiratory illness caused by the SARS-CoV-2 virus.",
        "Migraine": "A headache of varying intensity, often accompanied by nausea."
    }
    return info_db.get(disease, "Information not found.")

class MedicalKnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MedicalKnowledgeAgent",
            tools=[get_disease_info],
            system_prompt="You provide detailed medical information about diseases. Use tools to fetch info."
        )