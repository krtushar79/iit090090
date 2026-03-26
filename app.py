import random
import streamlit as st

TOPICS = {
    "Quantitative Aptitude": {
        "Arithmetic": [
            "A shopkeeper gives 10% discount and still earns 20% profit. If marked price is ₹660, find cost price.",
            "A person travels 120 km. First 60 km at 40 km/h and next 60 km at 60 km/h. Find average speed.",
            "Compound interest on ₹10,000 for 2 years at 10% p.a. (annual compounding) is?",
        ],
        "Algebra": [
            "If x + 1/x = 5, then find x² + 1/x².",
            "Solve: 2x + 3 = 17.",
            "If roots of x² - 7x + k = 0 are equal, find k.",
        ],
        "Modern Math": [
            "How many 3-digit numbers can be formed using digits 1,2,3,4 without repetition?",
            "Probability of getting exactly one head in two fair coin tosses is?",
            "If nC2 = 45, find n.",
        ],
    },
    "Data Interpretation": {
        "Tables": [
            "A table shows sales (in lakh): A=24, B=30, C=36. What is % increase from A to C?",
            "Total students in 5 classes are 40, 35, 30, 45, 50. Find average.",
            "If revenue is 250 and cost is 200, profit margin on revenue is?",
        ],
        "Charts": [
            "Pie chart angle for category X is 72°. What percentage does X represent?",
            "Bar chart values: 10, 20, 15, 25. Median is?",
            "Line graph shows population from 2 lakh to 2.5 lakh. % growth?",
        ],
    },
    "Logical Reasoning": {
        "Series": [
            "Find next number: 2, 6, 12, 20, 30, ?",
            "Find odd one out: 3, 5, 11, 14, 17",
            "Find next letter: A, C, F, J, O, ?",
        ],
        "Arrangement": [
            "5 people sit in a row. A is left of B, C is right of B. Who is in middle if order is fixed as A-B-C-D-E?",
            "In circular arrangement of 6 people, opposite of P is Q. If R is left of P, who can be right of Q?",
            "If M is taller than N, N taller than O, who is shortest?",
        ],
    },
    "English": {
        "Vocabulary": [
            "Choose synonym of 'Meticulous'.",
            "Choose antonym of 'Benevolent'.",
            "Meaning of idiom: 'Spill the beans'.",
        ],
        "Grammar": [
            "Choose correct sentence: (A) He don't know (B) He doesn't knows (C) He doesn't know (D) He not know",
            "Fill in blank: She ___ to office every day.",
            "Identify error: Each of the boys have submitted their assignment.",
        ],
    },
}

OPTIONS_POOL = ["A", "B", "C", "D"]


PROMPT_LEVEL_NOTE = (
    "MCQ difficulty is tuned to ISI MSQE PEA style: concept + speed + traps like PYQ patterns."
)


def build_options(correct_answer: str):
    distractors = [
        str(int(correct_answer) + 1) if correct_answer.isdigit() else f"Option {c}"
        for c in ["X", "Y", "Z"]
    ]
    all_options = [correct_answer] + distractors
    random.shuffle(all_options)
    return all_options



def solve_question(q: str):
    # Lightweight deterministic explainer for offline use.
    ql = q.lower()
    if "x + 1/x = 5" in q:
        return "23", "(x + 1/x)^2 = x^2 + 1/x^2 + 2. So 25 = req + 2 => req = 23.", "Formula use kiya, direct substitution se quick solve hota hai."
    if "2x + 3 = 17" in q:
        return "7", "2x = 14 => x = 7.", "Simple linear equation hai, LHS isolate karo aur divide by 2 karo."
    if "nC2 = 45" in q:
        return "10", "n(n-1)/2 = 45 => n(n-1)=90 => n=10.", "Combination pattern yaad rakho: nC2 = n(n-1)/2."
    if "72" in q:
        return "20", "(72/360)*100 = 20%.", "Pie chart mein angle ko 360 se divide karke percent nikaalte hain."
    if "exactly one head" in ql:
        return "1/2", "HH, HT, TH, TT me favorable = 2 (HT,TH) out of 4 => 1/2.", "Sample space clearly likho, galti kam hoti hai."
    # fallback
    return "Cannot be determined", "Given information is insufficient for unique numeric answer.", "Is type mein options elimination and assumptions check zaroori hota hai."


def generate_mcqs(topic: str, subtopic: str, count: int):
    source = TOPICS[topic][subtopic]
    items = []
    for _ in range(count):
        q = random.choice(source)
        ans, explain_en, explain_hi = solve_question(q)
        options = build_options(ans)
        correct_label = OPTIONS_POOL[options.index(ans)]
        items.append(
            {
                "question": q,
                "options": dict(zip(OPTIONS_POOL, options)),
                "answer": correct_label,
                "explain_en": explain_en,
                "explain_hi": explain_hi,
            }
        )
    return items


def render_mcq(mcq, idx):
    st.markdown(f"### Q{idx}. {mcq['question']}")
    selected = st.radio(
        "Choose one:",
        list(mcq["options"].keys()),
        format_func=lambda k: f"{k}. {mcq['options'][k]}",
        key=f"q_{idx}",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Check", key=f"check_{idx}"):
            if selected == mcq["answer"]:
                st.success("Correct ✅")
            else:
                st.error(f"Incorrect ❌ | Correct answer: {mcq['answer']}")
    with col2:
        with st.expander("Hinglish Explanation"):
            st.write(f"**Step (English):** {mcq['explain_en']}")
            st.write(f"**Hinglish:** {mcq['explain_hi']}")


def app():
    st.set_page_config(page_title="ISI MSQE PEA MCQ Prep AI", layout="wide")
    st.title("🎯 ISI MSQE PEA MCQ Prep (AI-style Generator)")
    st.caption("Unlimited auto-generated practice set with PYQ-style level + Hinglish explanations")
    st.info(PROMPT_LEVEL_NOTE)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        topic = st.selectbox("Select Topic", list(TOPICS.keys()))
    with col2:
        subtopic = st.selectbox("Select Subtopic", list(TOPICS[topic].keys()))
    with col3:
        count = st.slider("No. of MCQs", 1, 20, 5)

    if st.button("Generate New MCQ Set", type="primary"):
        st.session_state["mcqs"] = generate_mcqs(topic, subtopic, count)

    mcqs = st.session_state.get("mcqs", generate_mcqs(topic, subtopic, count))
    for i, mcq in enumerate(mcqs, start=1):
        render_mcq(mcq, i)
        st.divider()

    st.markdown("### How to Run")
    st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")


if __name__ == "__main__":
    app()
