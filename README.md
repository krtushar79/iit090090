# ISI MSQE PEA MCQ Prep App

A Streamlit-based AI-style practice app for **ISI MSQE PEA MCQ entrance preparation** with:

- Unlimited MCQ set generation
- PYQ-like level feel (concept + speed + trap pattern)
- Hinglish explanations for each question
- Instant answer checking

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- This starter is deterministic/offline and does not require paid API keys.
- You can later plug in OpenAI/LLM APIs for richer true-generative question diversity.
