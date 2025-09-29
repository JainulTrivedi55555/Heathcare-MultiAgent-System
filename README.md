## HEALTHCARE MULTI AGENT SYSTEMS

Overview:
This project is a Healthcare Multi-Agent System that simulates a collaborative AI environment where multiple specialized agents work together to analyze patient symptoms, provide a diagnosis, and recommend treatment plans. The system leverages OpenAI’s GPT models to process natural language inputs and generate meaningful healthcare insights.

Features

•	Multi-Agent Architecture: Different agents specialize in symptom analysis and treatment recommendation.

•	Natural Language Processing: Uses GPT models to understand and generate human-like medical advice.

•	Coordinator: Orchestrates communication between agents to provide a seamless workflow.

•	Extensible Design: Easily add more agents or improve existing ones.

Components
1. Coordinator

•	Acts as the central controller.

•	Receives patient information (name and symptoms).

•	Sends symptoms to the Symptom Agent.

•	Receives diagnosis and forwards it to the Treatment Agent.

•	Collects treatment recommendations and outputs the final result.

2. Symptom Agent

•	Analyzes patient symptoms.

•	Generates a medical diagnosis using GPT.

3. Treatment Agent

•	Receives diagnosis.

•	Suggests treatment plans or next steps using GPT.

4. Base Agent

•	Provides shared functionality for API calls to OpenAI.

•	Used as a parent class for Symptom and Treatment agents.

How It Works

1.	Patient Input: The system receives patient details and symptoms.

2.	Symptom Analysis: The Coordinator sends symptoms to the Symptom Agent, which returns a diagnosis.

3.	Treatment Recommendation: The diagnosis is sent to the Treatment Agent, which returns treatment advice.

4.	Output: The Coordinator outputs the diagnosis and treatment plan.

Example Usage: 

Input:
from coordinator import Coordinator

coordinator = Coordinator()

patient_name = "John Doe"

patient_symptoms = "I have fever and cough for 3 days."

coordinator.handle_patient(patient_name, patient_symptoms)

Output: 
Patient: John Doe reports symptoms: I have fever and cough for 3 days.

Diagnosis: The patient likely has a viral respiratory infection such as the common cold or flu.

Treatment: Recommend rest, hydration, over-the-counter fever reducers, and monitoring symptoms. If symptoms worsen, consult a healthcare professional.



Project Structure: 

healthcare-multi-agent-system/

│

├── agents/

│   ├── base_agent.py          # Base class for agents with OpenAI API calls

│   ├── symptom_agent.py       # Symptom analysis agent

│   └── treatment_agent.py     # Treatment recommendation agent

│

├── coordinator.py             # Orchestrates agent communication

├── main.py                   # Entry point to run the system

├── test_openai.py            # Simple script to test OpenAI API key

└── README.md                 # Project documentation




Setup Instructions: 

1. Clone the repository:

git clone https://github.com/JainulTrivedi55555/Heathcare-MultiAgent-System.git

cd healthcare-multi-agent-system

3. Install dependencies:

Make sure you have Python 3.8+ installed.

pip install -r requirements.txt

4. Set your OpenAI API key:

On Windows (Command Prompt):

setx OPENAI_API_KEY "your-api-key"

On macOS/Linux:

export OPENAI_API_KEY="your-api-key"

4. Run the system:

python main.py



Notes:

Ensure your OpenAI API key has sufficient quota.

The system currently uses GPT-4o model; you can change the model in the agent code if needed.

This is a prototype and should not replace professional medical advice.
