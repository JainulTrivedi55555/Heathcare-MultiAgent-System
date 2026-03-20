from .base_agent import BaseAgent, tool


@tool
def analyze_symptoms(symptoms: str) -> str:
    """
    Analyze patient symptoms and return a list of possible diagnoses with urgency levels.
    Input: a string describing the patient's symptoms.
    """
    symptoms_lower = symptoms.lower()

    # Urgency rules — checked first
    if any(kw in symptoms_lower for kw in ["chest pain", "crushing", "heart attack", "can't breathe", "stroke", "unconscious"]):
        return (
            "URGENT — Possible diagnoses: Myocardial Infarction (Heart Attack), Pulmonary Embolism, Stroke. "
            "Urgency: EMERGENCY. Recommend immediate 911 / ER visit."
        )

    # Respiratory
    if "fever" in symptoms_lower and ("cough" in symptoms_lower or "shortness of breath" in symptoms_lower):
        if "loss of taste" in symptoms_lower or "loss of smell" in symptoms_lower:
            return "Possible diagnoses: COVID-19, Influenza. Urgency: Moderate. Recommend testing and isolation."
        return "Possible diagnoses: Influenza, Common Cold, COVID-19, Pneumonia. Urgency: Moderate."

    if "cough" in symptoms_lower and "night sweat" in symptoms_lower and "weight loss" in symptoms_lower:
        return "Possible diagnoses: Tuberculosis, Lymphoma. Urgency: High. Recommend chest X-ray and CBC."

    if "cough" in symptoms_lower and "wheez" in symptoms_lower:
        return "Possible diagnoses: Asthma, COPD, Bronchitis. Urgency: Moderate."

    # Neurological
    if "headache" in symptoms_lower and "stiff neck" in symptoms_lower and "fever" in symptoms_lower:
        return "Possible diagnoses: Meningitis, Encephalitis. Urgency: HIGH — Seek immediate care."

    if "headache" in symptoms_lower and ("nausea" in symptoms_lower or "light sensitive" in symptoms_lower or "vomit" in symptoms_lower):
        return "Possible diagnoses: Migraine, Tension Headache, Cluster Headache. Urgency: Low-Moderate."

    if "headache" in symptoms_lower:
        return "Possible diagnoses: Tension Headache, Migraine, Sinusitis, Hypertension. Urgency: Low."

    # Gastrointestinal
    if "abdominal pain" in symptoms_lower or "stomach pain" in symptoms_lower:
        if "right side" in symptoms_lower or "lower right" in symptoms_lower:
            return "Possible diagnoses: Appendicitis. Urgency: HIGH — Seek immediate evaluation."
        if "diarrhea" in symptoms_lower or "vomiting" in symptoms_lower:
            return "Possible diagnoses: Gastroenteritis, Food Poisoning, IBS. Urgency: Moderate."
        return "Possible diagnoses: IBS, Gastritis, Peptic Ulcer, GERD. Urgency: Low-Moderate."

    if "nausea" in symptoms_lower and "vomiting" in symptoms_lower:
        return "Possible diagnoses: Gastroenteritis, Food Poisoning, Appendicitis. Urgency: Moderate."

    # Musculoskeletal
    if "joint pain" in symptoms_lower or "swollen joint" in symptoms_lower:
        if "fever" in symptoms_lower:
            return "Possible diagnoses: Septic Arthritis, Rheumatoid Arthritis, Gout. Urgency: Moderate-High."
        return "Possible diagnoses: Osteoarthritis, Gout, Rheumatoid Arthritis. Urgency: Low."

    if "back pain" in symptoms_lower:
        return "Possible diagnoses: Muscle Strain, Herniated Disc, Kidney Stones, Sciatica. Urgency: Low-Moderate."

    # Dermatological
    if "rash" in symptoms_lower:
        if "fever" in symptoms_lower:
            return "Possible diagnoses: Viral Exanthem, Meningococcemia, Drug Reaction. Urgency: Moderate-High."
        return "Possible diagnoses: Contact Dermatitis, Eczema, Psoriasis, Allergic Reaction. Urgency: Low."

    # Fatigue / General
    if "fatigue" in symptoms_lower or "tired" in symptoms_lower:
        if "weight loss" in symptoms_lower:
            return "Possible diagnoses: Thyroid Disorder, Diabetes, Anemia, Malignancy. Urgency: Moderate."
        return "Possible diagnoses: Anemia, Hypothyroidism, Depression, Sleep Disorder. Urgency: Low."

    return (
        "Symptoms are non-specific. Possible diagnoses: Viral Infection, Stress-related condition, Nutritional Deficiency. "
        "Urgency: Low. Recommend consulting a General Practitioner for detailed evaluation."
    )


SYMPTOM_CHECKER_PROMPT = """
You are an expert AI symptom checker for a healthcare multi-agent system.
Your role is to:
1. Carefully review the patient's reported symptoms
2. Use the analyze_symptoms tool to get a structured list of possible diagnoses
3. Return a clear, structured report including:
   - Possible diagnoses (list)
   - Urgency level (Low / Moderate / High / Emergency)
   - Key observations
   - Recommended next steps

Always remind the patient that this is not a substitute for professional medical advice.
Format your response clearly. Do not use excessive medical jargon.
"""


class SymptomCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SymptomCheckerAgent",
            tools=[analyze_symptoms],
            system_prompt=SYMPTOM_CHECKER_PROMPT,
        )
