from .base_agent import BaseAgent, tool

@tool
def analyze_symptoms(symptoms: str) -> str:
    """Analyze symptoms and return possible diagnoses"""
    symptoms = symptoms.lower()
    if "fever" in symptoms and "cough" in symptoms:
        return "Possible diagnoses: Common Cold, Flu, COVID-19"
    elif "headache" in symptoms:
        return "Possible diagnoses: Migraine, Tension headache"
    else:
        return "Symptoms unclear, please consult a doctor."

class SymptomCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SymptomCheckerAgent",
            tools=[analyze_symptoms],
            system_prompt=(
                "You are a healthcare symptom checker. Analyze patient symptoms and suggest possible diagnoses. "
                "Use tools when needed. Respond in JSON tool_call format when calling tools."
            )
        )