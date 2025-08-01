# main.py
import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


from app.firebase_auth import signup_user, login_user
from app.query_executor import run_sql_on_csv
from app.llm_utils import ask_llm, query_llm  # ✅ Import both
from app.pdf_generator import generate_pdf

# Set title
st.set_page_config(page_title="AI BI Platform", layout="wide")
st.title("AI BI Platform")

# -------------------- AUTH SECTION --------------------
auth_option = st.sidebar.radio("Choose Option:", ("Login", "Signup"))

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if auth_option == "Signup":
    if st.sidebar.button("Create Account"):
        result = signup_user(email, password)
        if isinstance(result, dict):
            st.success("✅ Signup successful! Please login.")
        else:
            st.error(f" {result}")
else:
    if st.sidebar.button("Login"):
        result = login_user(email, password)
        if isinstance(result, dict):
            st.success("✅ Login successful!")
            st.session_state['user'] = result
        else:
            st.error(f"❌ {result}")

# Prevent non-logged-in users from continuing

if "user" not in st.session_state:
 
    st.stop()

# -------------------- CSV UPLOAD --------------------
st.subheader("📁 Upload CSV File")
uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df)

    # -------------------- AI MODE SELECTION --------------------
    st.subheader("💬 Ask a Question")
    question_mode = st.radio("Choose how you want AI to answer:", ["Generate SQL", "Answer Directly"])

    question = st.text_input("Ask your question about the data:")

    if question:
        with st.spinner("🧠 Thinking..."):
            try:
                schema = df.dtypes.astype(str).to_dict()

                if question_mode == "Generate SQL":
                    sql_query = ask_llm(question, schema)
                    st.code(sql_query, language="sql")

                    result = run_sql_on_csv(df, sql_query)

                    if isinstance(result, pd.DataFrame):
                        st.success("✅ Query executed successfully!")
                        st.dataframe(result)

                        # -------------------- PDF DOWNLOAD --------------------
                        pdf_file_path = generate_pdf(question, sql_query, result)
                        with open(pdf_file_path, "rb") as f:
                            st.download_button(
                                label="📄 Download Q&A as PDF",
                                data=f,
                                file_name="query_report.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.error(f"❌ Error: {result}")

                else:  # Answer Directly
                    answer = query_llm(question)
                    st.success("✅ AI Response:")
                    st.markdown(f"**{answer}**")

            except Exception as e:
                st.error(f"❌ Failed: {str(e)}")

else:
    st.info("👆 Please upload a CSV file to get started.")
