from .base_agent import BaseAgent, tool

DISEASE_DATABASE = {
    # Respiratory
    "Common Cold": {
        "description": "A viral upper respiratory tract infection primarily caused by rhinoviruses.",
        "symptoms": "Runny nose, sore throat, sneezing, mild fever, congestion.",
        "duration": "7–10 days",
        "contagious": "Yes — spreads via droplets and surface contact.",
        "complications": "Sinusitis, ear infection (in children).",
    },
    "Influenza": {
        "description": "A highly contagious respiratory illness caused by influenza A or B viruses.",
        "symptoms": "High fever, chills, muscle aches, fatigue, dry cough, headache.",
        "duration": "1–2 weeks",
        "contagious": "Yes — highly contagious 1 day before and up to 5–7 days after onset.",
        "complications": "Pneumonia, hospitalization, death in high-risk groups.",
    },
    "COVID-19": {
        "description": "A respiratory illness caused by the SARS-CoV-2 coronavirus.",
        "symptoms": "Fever, cough, shortness of breath, loss of taste/smell, fatigue, body aches.",
        "duration": "Mild: 1–2 weeks. Severe cases may be longer.",
        "contagious": "Yes — airborne and droplet transmission.",
        "complications": "Long COVID, pneumonia, organ damage, death in vulnerable populations.",
    },
    "Pneumonia": {
        "description": "Infection that inflames air sacs in one or both lungs, which may fill with fluid.",
        "symptoms": "Cough with phlegm, fever, chills, difficulty breathing, chest pain.",
        "duration": "2–4 weeks with treatment",
        "contagious": "Bacterial form can be; viral form usually contagious.",
        "complications": "Sepsis, respiratory failure, pleural effusion.",
    },
    "Asthma": {
        "description": "A chronic condition where the airways narrow and swell, making breathing difficult.",
        "symptoms": "Wheezing, shortness of breath, chest tightness, coughing (especially at night).",
        "duration": "Chronic — managed with medication.",
        "contagious": "No.",
        "complications": "Severe asthma attacks, respiratory failure.",
    },
    # Neurological
    "Migraine": {
        "description": "A neurological condition causing intense, recurring headaches often with nausea and light sensitivity.",
        "symptoms": "Throbbing head pain (usually one-sided), nausea, vomiting, sensitivity to light/sound.",
        "duration": "4–72 hours per episode.",
        "contagious": "No.",
        "complications": "Chronic migraine, medication overuse headache, stroke (rare).",
    },
    "Tension Headache": {
        "description": "The most common type of headache, caused by muscle tension in the head and neck.",
        "symptoms": "Dull, aching head pain, pressure around forehead, tenderness in scalp/neck.",
        "duration": "30 minutes to several hours.",
        "contagious": "No.",
        "complications": "Chronic daily headache if frequent.",
    },
    "Meningitis": {
        "description": "Inflammation of the membranes surrounding the brain and spinal cord.",
        "symptoms": "Sudden severe headache, stiff neck, high fever, sensitivity to light, nausea.",
        "duration": "Bacterial: life-threatening if untreated. Viral: resolves in 1–2 weeks.",
        "contagious": "Bacterial form is contagious via respiratory droplets.",
        "complications": "Brain damage, hearing loss, septicemia, death.",
    },
    # Gastrointestinal
    "Gastroenteritis": {
        "description": "Inflammation of the stomach and intestines, typically caused by viral or bacterial infection.",
        "symptoms": "Nausea, vomiting, diarrhea, stomach cramps, mild fever.",
        "duration": "1–3 days (viral); up to 10 days (bacterial).",
        "contagious": "Yes — via contaminated food/water or person-to-person contact.",
        "complications": "Dehydration, especially dangerous in infants and elderly.",
    },
    "Appendicitis": {
        "description": "Inflammation of the appendix requiring urgent surgical treatment.",
        "symptoms": "Sudden pain near navel moving to lower right abdomen, nausea, fever, vomiting.",
        "duration": "Urgent — can rupture within 24–72 hours without treatment.",
        "contagious": "No.",
        "complications": "Ruptured appendix, peritonitis, sepsis — life-threatening.",
    },
    "GERD": {
        "description": "Gastroesophageal Reflux Disease — chronic acid reflux damaging the esophagus.",
        "symptoms": "Heartburn, regurgitation, difficulty swallowing, chest discomfort.",
        "duration": "Chronic — managed with lifestyle changes and medication.",
        "contagious": "No.",
        "complications": "Esophagitis, Barrett's esophagus, esophageal cancer (rare).",
    },
    # Musculoskeletal
    "Gout": {
        "description": "A form of inflammatory arthritis caused by excess uric acid crystallizing in joints.",
        "symptoms": "Sudden, severe joint pain (often big toe), swelling, redness, warmth.",
        "duration": "Acute attacks: 3–10 days. Chronic without treatment.",
        "contagious": "No.",
        "complications": "Kidney stones, tophi (uric acid deposits), joint damage.",
    },
    "Rheumatoid Arthritis": {
        "description": "A chronic autoimmune disease causing joint inflammation and damage.",
        "symptoms": "Joint pain, swelling, stiffness (especially morning), fatigue, fever.",
        "duration": "Chronic — managed with DMARDs and biologics.",
        "contagious": "No.",
        "complications": "Joint deformity, cardiovascular disease, lung problems.",
    },
    # General
    "Diabetes Type 2": {
        "description": "A metabolic condition where the body doesn't use insulin properly, leading to high blood sugar.",
        "symptoms": "Frequent urination, increased thirst, fatigue, blurred vision, slow-healing wounds.",
        "duration": "Chronic — managed with diet, exercise, and medication.",
        "contagious": "No.",
        "complications": "Neuropathy, retinopathy, kidney disease, cardiovascular disease.",
    },
    "Hypertension": {
        "description": "High blood pressure — a chronic condition where blood pressure in arteries is persistently elevated.",
        "symptoms": "Often no symptoms ('silent killer'). Severe: headache, vision changes, chest pain.",
        "duration": "Chronic — managed with lifestyle and medication.",
        "contagious": "No.",
        "complications": "Stroke, heart attack, heart failure, kidney disease.",
    },
    "Anemia": {
        "description": "A condition where you lack enough healthy red blood cells to carry oxygen to tissues.",
        "symptoms": "Fatigue, weakness, pale skin, shortness of breath, dizziness, cold hands/feet.",
        "duration": "Depends on cause. Iron deficiency: weeks to months with treatment.",
        "contagious": "No.",
        "complications": "Heart problems, complications during pregnancy, growth issues in children.",
    },
}


@tool
def get_disease_info(disease: str) -> str:
    """
    Retrieve structured medical information about a specific disease or condition.
    Input: disease name as a string.
    Returns: description, symptoms, duration, contagiousness, and potential complications.
    """
    # Case-insensitive lookup
    for key, info in DISEASE_DATABASE.items():
        if key.lower() == disease.lower() or disease.lower() in key.lower():
            return (
                f"**{key}**\n"
                f"Description: {info['description']}\n"
                f"Symptoms: {info['symptoms']}\n"
                f"Duration: {info['duration']}\n"
                f"Contagious: {info['contagious']}\n"
                f"Potential Complications: {info['complications']}"
            )
    return (
        f"Detailed information for '{disease}' is not in the local database. "
        "Please consult a medical professional or peer-reviewed sources like Mayo Clinic or WebMD."
    )


MEDICAL_KNOWLEDGE_PROMPT = """
You are a medical knowledge specialist AI agent in a healthcare system.
Your role is to provide clear, accurate, patient-friendly information about diseases and conditions.
Use the get_disease_info tool to retrieve structured information.
Then present the findings in a readable, organized format covering:
- What the condition is
- Key symptoms to watch for
- How long it typically lasts
- Whether it's contagious
- Potential complications if untreated

Always recommend consulting a licensed healthcare provider for personalized medical advice.
"""


class MedicalKnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MedicalKnowledgeAgent",
            tools=[get_disease_info],
            system_prompt=MEDICAL_KNOWLEDGE_PROMPT,
        )
