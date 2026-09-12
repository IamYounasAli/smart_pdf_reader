import streamlit as st
from utils.pdf_processor import extract_text_from_pdf
from utils.groq_client import generate_analysis
from utils.quiz_engine import generate_quiz

st.set_page_config(
    page_title="PDF Intelligence Suite",
    page_icon="📄",
    layout="wide"
)

# Initialize Session States
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "skimming" not in st.session_state:
    st.session_state.skimming = None
if "scanning" not in st.session_state:
    st.session_state.scanning = None
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# Sidebar Configuration
with st.sidebar:
    st.title("📄 PDF Reader & Analyzer")
    st.markdown("Powered by **Groq LPU** & **Streamlit**")
    
    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
    user_description = st.text_area(
        "Document Context / Goals", 
        placeholder="e.g., Medical journal, focus on findings and methodology..."
    )

    if uploaded_file and st.button("Process Document", type="primary"):
        with st.spinner("Extracting text from PDF..."):
            try:
                st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
                # Reset analysis cache on new file upload
                st.session_state.summary = None
                st.session_state.skimming = None
                st.session_state.scanning = None
                st.session_state.quiz_data = None
                st.session_state.user_answers = {}
                st.success("PDF processed successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

# Main Layout
if not st.session_state.pdf_text:
    st.info("👈 Please upload a PDF and click 'Process Document' in the sidebar to begin.")
else:
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Executive Summary", "🔍 Skimming", "🎯 Scanning", "❓ Quiz Mode"])
    
    # Executive Summary Tab
    with tab1:
        st.header("Executive Summary")
        if not st.session_state.summary:
            if st.button("Generate Summary"):
                with st.spinner("Generating summary via Groq..."):
                    st.session_state.summary = generate_analysis(
                        st.session_state.pdf_text, user_description, "summary"
                    )
        if st.session_state.summary:
            st.markdown(st.session_state.summary)

    # Skimming Tab
    with tab2:
        st.header("Skimming Overview (Key Concepts & Headings)")
        if not st.session_state.skimming:
            if st.button("Generate Skimming Analysis"):
                with st.spinner("Extracting core arguments..."):
                    st.session_state.skimming = generate_analysis(
                        st.session_state.pdf_text, user_description, "skimming"
                    )
        if st.session_state.skimming:
            st.markdown(st.session_state.skimming)

    # Scanning Tab
    with tab3:
        st.header("Scanning Details (Metrics, Dates & Terminology)")
        if not st.session_state.scanning:
            if st.button("Generate Scanning Extraction"):
                with st.spinner("Locating specific data points..."):
                    st.session_state.scanning = generate_analysis(
                        st.session_state.pdf_text, user_description, "scanning"
                    )
        if st.session_state.scanning:
            st.markdown(st.session_state.scanning)

    # Quiz Tab
    with tab4:
        st.header("Interactive Quiz")
        if not st.session_state.quiz_data:
            num_q = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
            if st.button("Generate Quiz"):
                with st.spinner("Creating quiz questions..."):
                    try:
                        st.session_state.quiz_data = generate_quiz(
                            st.session_state.pdf_text, user_description, num_q
                        )
                    except Exception as e:
                        st.error(f"Failed to generate quiz: {e}")
        
        if st.session_state.quiz_data:
            with st.form("quiz_form"):
                for idx, q in enumerate(st.session_state.quiz_data):
                    st.subheader(f"Q{idx+1}: {q['question']}")
                    st.session_state.user_answers[idx] = st.radio(
                        "Select your answer:",
                        q["options"],
                        key=f"q_{idx}"
                    )
                    st.divider()
                
                submitted = st.form_submit_button("Submit Answers")
                if submitted:
                    score = 0
                    total = len(st.session_state.quiz_data)
                    st.header("Results")
                    for idx, q in enumerate(st.session_state.quiz_data):
                        user_ans = st.session_state.user_answers.get(idx)
                        correct_ans = q["answer"]
                        if user_ans == correct_ans:
                            score += 1
                            st.success(f"**Q{idx+1}: Correct!** ({user_ans})")
                        else:
                            st.error(f"**Q{idx+1}: Incorrect.** Your answer: {user_ans} | Correct answer: {correct_ans}")
                        st.caption(f"*Explanation:* {q.get('explanation', 'N/A')}")
                    
                    st.metric("Final Score", f"{score} / {total}", f"{int((score/total)*100)}%")
