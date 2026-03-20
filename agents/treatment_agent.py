from .base_agent import BaseAgent, tool

TREATMENT_DATABASE = {
    "influenza": {
        "medications": ["Oseltamivir (Tamiflu) — antiviral, most effective within 48hrs of onset", "Acetaminophen or Ibuprofen for fever/pain"],
        "home_care": ["Rest for 5–7 days", "Stay well hydrated (water, broth, electrolytes)", "Use a humidifier to ease congestion", "Isolate to prevent spreading"],
        "when_to_see_doctor": "If fever exceeds 103°F (39.4°C), breathing difficulty, or symptoms worsen after day 5.",
        "specialist": "General Practitioner",
        "prevention": "Annual flu vaccine. Hand hygiene. Avoid touching face.",
    },
    "common cold": {
        "medications": ["Decongestants (pseudoephedrine)", "Antihistamines for runny nose", "Throat lozenges", "Saline nasal spray"],
        "home_care": ["Rest and sleep", "Hot fluids (tea, soup)", "Honey and lemon for sore throat", "Steam inhalation"],
        "when_to_see_doctor": "If symptoms last >10 days, high fever, or difficulty breathing.",
        "specialist": "General Practitioner",
        "prevention": "Handwashing, avoiding close contact with infected individuals.",
    },
    "covid-19": {
        "medications": ["Antivirals (Paxlovid) for high-risk patients — consult doctor", "OTC fever reducers (Acetaminophen)", "Rest and supportive care for mild cases"],
        "home_care": ["Isolate for at least 5 days", "Monitor oxygen levels with a pulse oximeter", "Rest and hydration", "Monitor for worsening symptoms"],
        "when_to_see_doctor": "Difficulty breathing, persistent chest pain, confusion, inability to stay awake, bluish lips.",
        "specialist": "General Practitioner or Pulmonologist for severe cases",
        "prevention": "Vaccination, masking in crowded spaces, hand hygiene, ventilation.",
    },
    "migraine": {
        "medications": ["Triptans (Sumatriptan) — migraine-specific", "NSAIDs (Ibuprofen, Naproxen)", "Anti-nausea medication (Metoclopramide)", "Preventive: Topiramate, Propranolol"],
        "home_care": ["Dark, quiet room", "Cold or warm compress on head/neck", "Stay hydrated", "Identify and avoid triggers (caffeine, stress, certain foods)"],
        "when_to_see_doctor": "First-ever severe headache, headache with fever/stiff neck, or neurological symptoms.",
        "specialist": "Neurologist",
        "prevention": "Regular sleep, stress management, trigger avoidance, prophylactic medication.",
    },
    "gastroenteritis": {
        "medications": ["ORS (Oral Rehydration Salts) — most critical", "Loperamide (Imodium) for diarrhea in adults", "Antiemetics for severe vomiting (Ondansetron)"],
        "home_care": ["BRAT diet (Bananas, Rice, Applesauce, Toast)", "Small frequent sips of clear fluids", "Avoid dairy, fatty, spicy foods", "Rest"],
        "when_to_see_doctor": "Signs of dehydration (no urination >8hrs, sunken eyes), blood in stool, high fever.",
        "specialist": "General Practitioner or Gastroenterologist",
        "prevention": "Handwashing, safe food handling, avoid contaminated water.",
    },
    "hypertension": {
        "medications": ["ACE inhibitors (Lisinopril)", "Calcium channel blockers (Amlodipine)", "Diuretics (Hydrochlorothiazide)", "ARBs (Losartan) — as prescribed by physician"],
        "home_care": ["DASH diet (low sodium, rich in fruits/vegetables)", "Regular aerobic exercise (30 min/day)", "Limit alcohol", "Quit smoking", "Stress reduction (meditation, yoga)"],
        "when_to_see_doctor": "BP consistently above 140/90 mmHg. Hypertensive crisis (>180/120): Emergency.",
        "specialist": "Cardiologist",
        "prevention": "Healthy diet, regular exercise, weight management, limit salt and alcohol.",
    },
    "asthma": {
        "medications": ["Rescue inhaler (Albuterol/Salbutamol) for acute attacks", "Inhaled corticosteroids (Fluticasone) for long-term control", "Leukotriene modifiers (Montelukast)"],
        "home_care": ["Identify and avoid triggers (dust, pollen, smoke, cold air)", "Keep home clean and dust-free", "Use air purifiers", "Follow asthma action plan"],
        "when_to_see_doctor": "Worsening symptoms despite medication, >2 rescue inhaler uses per week, nighttime symptoms.",
        "specialist": "Pulmonologist or Allergist",
        "prevention": "Allergen control, flu vaccination, regular check-ups.",
    },
    "default": {
        "medications": ["Consult a licensed physician for appropriate medications."],
        "home_care": ["Rest and stay hydrated", "Monitor symptoms and track changes", "Avoid self-medicating without professional guidance"],
        "when_to_see_doctor": "If symptoms persist more than 3–5 days or worsen significantly.",
        "specialist": "General Practitioner (for initial evaluation)",
        "prevention": "Maintain healthy lifestyle: balanced diet, regular exercise, adequate sleep.",
    },
}


@tool
def get_treatment_plan(diagnosis: str) -> str:
    """
    Retrieve a structured treatment plan for a given diagnosis.
    Input: diagnosis name as a string.
    Returns: recommended medications, home care instructions, when to see a doctor, and specialist referral.
    """
    # Match diagnosis to database
    diagnosis_lower = diagnosis.lower().strip()
    matched_key = None
    for key in TREATMENT_DATABASE:
        if key in diagnosis_lower or diagnosis_lower in key:
            matched_key = key
            break

    plan = TREATMENT_DATABASE.get(matched_key, TREATMENT_DATABASE["default"])

    medications = "\n  • ".join(plan["medications"])
    home_care = "\n  • ".join(plan["home_care"])

    return (
        f"Treatment Plan for: {diagnosis}\n"
        f"\nMedications:\n  • {medications}"
        f"\nHome Care:\n  • {home_care}"
        f"\nWhen to See a Doctor: {plan['when_to_see_doctor']}"
        f"\nRecommended Specialist: {plan['specialist']}"
        f"\nPrevention: {plan['prevention']}"
    )


TREATMENT_PROMPT = """
You are a treatment recommendation specialist AI agent in a healthcare system.
You receive a diagnosis and provide structured, actionable treatment guidance.
Use the get_treatment_plan tool to retrieve recommended treatments.
Then present a clear, empathetic, and organized treatment summary including:
- Medication options (remind user to consult doctor before starting)
- Home care and lifestyle recommendations
- Warning signs that require immediate medical attention
- Which type of specialist to see
- Prevention tips

Always remind the patient this is informational and not a substitute for professional medical advice.
Be empathetic and supportive in your tone.
"""


class TreatmentRecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TreatmentRecommendationAgent",
            tools=[get_treatment_plan],
            system_prompt=TREATMENT_PROMPT,
        )
