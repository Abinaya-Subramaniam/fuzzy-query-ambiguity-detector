import streamlit as st
from nlp_utils import preprocess_query, calculate_features, get_detailed_analysis
from ambiguity import fuzzy_system

st.set_page_config(
    page_title="Fuzzy Ambiguity Detector",
    layout="centered"
)

st.title("Fuzzy Logic Ambiguity Detector")
st.markdown("Detect query ambiguity for better LLM responses")

query = st.text_area(
    "**Enter your query:**",
    value="How do they do things?",
    height=100,
    placeholder="Type your question here..."
)

if st.button("Analyze with Fuzzy Logic", type="primary") or query:
    tokens = preprocess_query(query)
    features = calculate_features(query, tokens)
    
    ambiguity_score = fuzzy_system.compute_ambiguity(
        features['length'],
        features['vague_ratio'],
        features['specificity'],
        features['question_clarity']
    )
    
    analysis = get_detailed_analysis(query, tokens, features)
    
    st.markdown("---")
    
    if ambiguity_score < 30:
        color = "green"
        status = " Clear"
        suggestion = "Direct answer"
    elif ambiguity_score < 60:
        color = "orange"
        status = " Moderate"
        suggestion = "Ask for clarification"
    else:
        color = "red"
        status = " Ambiguous"
        suggestion = "Requires clarification"
    
    st.markdown(f"### Ambiguity Score: **{ambiguity_score:.1f}/100**")
    
    if color == "green":
        st.progress(ambiguity_score/100, text=f"{status} - {suggestion}")
    elif color == "orange":
        st.progress(ambiguity_score/100, text=f"{status} - {suggestion}")
    else:
        st.progress(ambiguity_score/100, text=f"{status} - {suggestion}")
    
    st.markdown("### LLM Response Strategy")
    
    if ambiguity_score < 30:
        st.success("**Direct Answer Approach**")
        st.write("The query is clear and specific. LLM can provide a direct, comprehensive answer.")
        st.code(f"User asked: '{query}'\nLLM: Provide a detailed, accurate answer.")
    
    elif ambiguity_score < 60:
        st.warning("**Clarification-First Approach**")
        st.write("The query has some ambiguity. LLM should ask clarifying questions before answering.")
        st.code(f"""User asked: '{query}'
LLM: "I'd like to give you the best answer. Could you clarify what you mean?""")

    else:
        st.error("**Clarification-Required Approach**")
        st.write("The query is too ambiguous. LLM must ask for specific clarification.")
        st.code(f"""User asked: '{query}'
LLM: "To help you effectively, I need some clarification on what you're asking.""")

st.caption("Simple fuzzy logic system for detecting query ambiguity")