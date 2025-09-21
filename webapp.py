# import streamlit as st
# from pdfextractor import text_extractor
# import google.generativeai as genai
# import os 

# # Configure trhe model 
# key = os.getenv('GOOGLE_API_KEY')
# genai.configure(api_key= key)
# model = genai.GenerativeModel('gemini-2.5-flash-lite')
# resume_text = job_desc = None

# # upload resume 
# st.sidebar.title(":orange[Upload your resume (pdf only)]")

# file = st.sidebar.file_uploader('Resume', type=['pdf'])
# if file:
#         resume_text = text_extractor(file)
#         # st.write(resume_text)
        
# # let define the main page 
# st.title(":orange[Skill Match] :blue[AI Assistant skill matching tool]")
# st.markdown("#### This application will match your resume and the job description . It will create a detailed report on the match")
# tips = ''' Follow these steps to proceed:
# 1. Upload your resume (pdf only).
# 2. Copy and past the job description for which you are applying for.
# 3. Click the button and see the magic 
# '''

# st.write(tips)

# job_desc=st.text_area("Copy and Paste the Job Description here",max_chars=10000)

# prompt=f'''
# Assume you are expert in skill matching and creating profiles.
# Match the following resume with the job description provided by the user.
# Resume: {resume_text}
# Job_Description: {job_desc}

# Your output should be as follows:
# * Give a brief description of the applicant in 3-5 lines.
# * Give a range of expected ATS score along with the matching and non matching keywords.
# * Give the chances of getting sorlisted for this position in percentage.
# * perform SWOT analysis and discuss each and everything in bullets points
# * Suggest what all improvement can be made in resume in order get better ats and increase percentage of getting shortlisted.
# * Also create two customised resumes as per the job description provided and increase percentage of getting shortlisted.
# * prepare one page resume in such a way that can be copied and converted in word and can be converted to pdf.
# * use bullet points and table wherever required 
# '''

# button = st.button('Click')
# if button:
#     if resume_text and job_desc:
#         response = model.generate_content(prompt)
#         st.write(response.text)
#     else:
#         st.write("Please Upload your resume")



import streamlit as st
from pdfextractor import text_extractor
import google.generativeai as genai
import os

# =========================
# Configure Gemini AI
# =========================
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Skill Match AI",
    page_icon="🤖",
    layout="wide"
)

# =========================
# Styling
# =========================
st.markdown("""
    <style>
        body { font-family: "Segoe UI", sans-serif; }
        .main-header { text-align: center; padding: 1rem; }
        .feature-card {
            background: #E6DADA;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            color: #000;
            transition: all 0.3s ease;
        }
        .feature-card:hover { transform: translateY(-4px); box-shadow: 0 6px 16px rgba(0,0,0,0.15); }
        .feature-card h3 { margin-bottom: 0.5rem; color: #000; }
        .footer { text-align: center; margin-top: 2rem; font-size: 13px; color: gray; }
    </style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown("""
<div class="main-header">
    <h1>🤖 Skill Match AI</h1>
    <p>Analyze your resume against any job description in seconds</p>
</div>
""", unsafe_allow_html=True)

# =========================
# Sidebar: Upload Resume
# =========================
with st.sidebar:
    st.subheader("📄 Upload Resume")
    file = st.file_uploader("Choose your resume (PDF)", type=["pdf"])
    if file:
        try:
            st.session_state.resume_text = text_extractor(file)
            st.success("Resume uploaded successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# =========================
# Feature Highlights
# =========================
st.subheader("✨ Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="feature-card"><h3>🎯 ATS Score</h3><p>Check keyword matches & ATS compatibility</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="feature-card"><h3>📊 SWOT</h3><p>Get strengths, weaknesses, opportunities, threats</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="feature-card"><h3>📝 Optimization</h3><p>Actionable resume improvement tips</p></div>""", unsafe_allow_html=True)

# =========================
# Job Description Input
# =========================
st.markdown("""
<div style="background: #E6DADA; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); margin-top: 1rem; margin-bottom: 1rem;">
    <h3 style="color: #000; text-align: center;">📋 Paste Job Description</h3>
    <p style="color: gray; text-align: center; font-size: 14px;">Provide the complete job description for accurate resume analysis</p>
</div>
""", unsafe_allow_html=True)

job_desc = st.text_area(
    "",
    height=250,
    placeholder="📝 Paste the full job description here...\n\nInclude:\n• Job title and company\n• Required skills\n• Job responsibilities\n• Experience requirements",
)

# =========================
# Generate Report Button
# =========================
if st.button("🚀 Generate Report", use_container_width=True):
    if file and job_desc.strip():
        st.info("🔍 Analyzing resume and job description...")

        prompt = f"""
        Assume you are expert in skill matching and creating profiles.
        Match the following resume with the job description provided by the user.
        Resume: {st.session_state.resume_text}
        Job_Description: {job_desc}

        Your output should be as follows:
        * Give a brief description of the applicant in 3-5 lines.
        * Give a range of expected ATS score along with the matching and non matching keywords.
        * Give the chances of getting shortlisted for this position in percentage.
        * Perform SWOT analysis and discuss each point in bullet points.
        * Suggest all improvements that can be made in the resume to improve ATS score and increase chances of being shortlisted.
        * Create two customized resumes per the job description to increase chances of getting shortlisted.
        * Prepare a one-page resume in a copyable format for Word/PDF.
        * Use bullet points and tables wherever required.
        """

        try:
            response = model.generate_content(prompt)
            st.markdown("### 📝 AI Skill Match Report")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
    else:
        st.warning("Please upload a resume and paste a job description.")

# =========================
# Footer
# =========================
st.markdown("""
<div class="footer">
    <p>Built with ❤️ using Streamlit + Gemini AI</p>
</div>
""", unsafe_allow_html=True)
