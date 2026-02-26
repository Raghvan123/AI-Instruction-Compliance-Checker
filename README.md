AI-Based Instruction Compliance Checker

Project Overview
This project is an AI-based system that evaluates whether a response correctly follows a given instruction.

It uses a hybrid evaluation model combining:
• Semantic similarity analysis
• Keyword overlap scoring
• Structural constraint validation
• Weighted final compliance scoring
The system provides a compliance score (0–100), grade classification, and detailed explanation.
_________________________________________________________________________________________________________________________________________________

Methodology
The evaluation consists of three components:

1 Semantic Similarity
Uses Sentence-BERT embeddings to measure meaning similarity between instruction and response.

2 Auxiliary Score
Checks keyword relevance and length adequacy.

3 Constraint Score
Validates structural constraints such as:
• Number of items required
• Format constraints
• Specific conditions mentioned in instruction
Final score is computed using a weighted formula.
_________________________________________________________________________________________________________________________________________________

Features
• Interactive Streamlit dashboard
• Real-time compliance evaluation
• Detailed explanation output
• Grade classification system
• Clean and minimalist UI
_________________________________________________________________________________________________________________________________________________

Project Structure
AI-Instruction-Compliance-Checker/
│
├── app.py
├── compliance_engine.py
├── requirements.txt
├── README.md
_________________________________________________________________________________________________________________________________________________

Installation
Clone the repository:

git clone https://github.com/yourusername/AI-Instruction-Compliance-Checker.git
cd AI-Instruction-Compliance-Checker

Install dependencies:

pip install -r requirements.txt

Run the app:

streamlit run app.py
_________________________________________________________________________________________________________________________________________________

Applications
• AI response evaluation
• Chatbot monitoring
• NLP research
• Academic grading assistance
• Instruction-following validation systems
_________________________________________________________________________________________________________________________________________________

Future Improvements
• LLM-based contextual evaluation
• Dataset benchmarking
• Web API deployment
• Enhanced constraint extraction
_________________________________________________________________________________________________________________________________________________

Author
Raghvan
Msc CS / Somaiya Vidyavihar University
2025