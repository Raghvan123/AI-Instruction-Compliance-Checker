import streamlit as st
from compliance_engine import compute_final_score

st.set_page_config(page_title="Instruction Compliance Checker", layout="wide")

st.title("AI-Based Instruction Compliance Checker")
st.markdown("---")

instruction = st.text_area("Enter Instruction")
response = st.text_area("Enter Response")

if st.button("Evaluate"):

    if instruction.strip() == "" or response.strip() == "":
        st.warning("Please enter both instruction and response.")
    else:
        results = compute_final_score(instruction, response)

        st.markdown("## Evaluation Dashboard")

        # Metrics in Columns
        col1, col2, col3 = st.columns(3)

        col1.metric("Semantic Similarity", round(results['semantic'], 3))
        col2.metric("Auxiliary Score", round(results['auxiliary'], 3))
        col3.metric("Constraint Score", round(results['constraint'], 3))

        st.markdown("---")

        # Big Final Score
        st.markdown("### Final Compliance Score")

        score = results['final_score']
        st.progress(score / 100)

        if score >= 85:
            st.success(f"{results['grade']} — {score}/100")
        elif score >= 70:
            st.info(f"{results['grade']} — {score}/100")
        elif score >= 50:
            st.warning(f"{results['grade']} — {score}/100")
        else:
            st.error(f"{results['grade']} — {score}/100")

        # Expandable Explanation
        with st.expander("🔎 View Detailed Explanation"):
            for point in results["explanation"]:
                st.write(f"- {point}")