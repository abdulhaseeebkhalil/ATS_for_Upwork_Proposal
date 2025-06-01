from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image # Keep this in case user wants to upload proposal PDFs later, though not used in initial version
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input_text, freelancer_profile, prompt_role):
    """
    Sends the job post, freelancer profile, and a specific prompt role to the Gemini model
    to generate a response.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    # For text-based inputs, we send them as a list of text parts.
    # The prompt_role defines the persona and task for the model.
    response = model.generate_content([prompt_role,
                                       f"Upwork Job Post:\n{input_text}",
                                       f"Freelancer Profile/Summary:\n{freelancer_profile}"])
    return response.text

# --- Streamlit Application UI ---
st.set_page_config(page_title="Upwork Proposal Assistant", layout="centered")

# Custom CSS for a cleaner look and feel, inspired by the sketch
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Inter', sans-serif;
    }
    .stTextArea label {
        font-weight: bold;
        color: #333;
    }
    .stButton > button {
        background-color: #2196F3;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 1em;
        margin: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        width: 100%; /* Make buttons fill their column */
    }
    .stButton > button:hover {
        background-color: #1976D2;
        color: white;  /* Ensuring text stays white on hover */
        transform: translateY(-2px);
        box-shadow: 3px 3px 8px rgba(0,0,0,0.3);
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    .stTextInput label {
        font-weight: bold;
        color: #333;
    }
    .response-area {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
    }
    .response-header {
        font-size: 1.8em;
        color: #333;
        margin-bottom: 15px;
        text-align: center;
    }
    /* Layout for buttons to mimic sketch */
    .st-emotion-cache-1c7y2qn { /* This targets the container for columns */
        gap: 1rem; /* Adjust gap between columns */
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">Upwork Proposal Assistant</h1>', unsafe_allow_html=True)

# Input Fields
job_post_text = st.text_area("Upwork Job Post: (Paste the full job description here)", key="job_input", height=200)
freelancer_profile_text = st.text_area("Your Freelancer Profile/Summary: (Paste your relevant skills, experience, or existing proposal draft here)", key="profile_input", height=150)

# --- Prompts for different functionalities ---
# Note: These prompts are designed to be general and can be adapted further for specific nuances.

PROMPT_GENERATE_PROPOSAL = """
You are an expert Upwork proposal writer. Your task is to craft a compelling and tailored proposal for the provided Upwork Job Post, leveraging the information from the Freelancer Profile/Summary. Focus on highlighting relevant skills, experience, and a clear call to action. Ensure the tone is professional, persuasive, and concise, typically fitting within a standard Upwork proposal length.
"""

PROMPT_ANALYZE_MATCH_PERCENTAGE = """
You are an Upwork ATS (Applicant Tracking System) scanner. Your task is to evaluate the provided Proposal (which is generated from the Freelancer Profile/Summary) against the Upwork Job Post. Give me the percentage of match.
First, the output should come as a percentage (e.g., "75% Match").
Then, list "Keywords Missing" from the proposal that are present in the job post.
Lastly, provide "Final Thoughts" on the proposal's overall alignment and areas for quick improvement.
"""

PROMPT_IMPROVE_PROPOSAL = """
You are a seasoned Upwork Career Coach and proposal strategist. Your task is to analyze the provided Proposal (from the Freelancer Profile/Summary) against the Upwork Job Post. Suggest specific improvements, rephrasing, or additional points the freelancer should focus on to better align with the job requirements and stand out. Highlight areas where the proposal excels and where there is room for improvement. Provide actionable advice.
"""

PROMPT_HIGHLIGHT_SELLING_POINTS = """
You are a professional Upwork Profile Analyst. Your task is to extract and highlight the most significant selling points and achievements from the Freelancer Profile/Summary in the context of the Upwork Job Post. Focus on accomplishments that align strongly with the job and showcase measurable impacts relevant to the client's needs.
"""

PROMPT_IDENTIFY_TRANSFERABLE_SKILLS = """
You are an Upwork Talent Scout specializing in skill identification. Your task is to identify transferable skills from the Freelancer Profile/Summary that can be applied effectively to the specified Upwork Job Post. Highlight skills that are versatile and demonstrate adaptability to the job's requirements, even if not explicitly stated in the job post.
"""

PROMPT_ASSESS_BID_SUITABILITY = """
You are an experienced Upwork Business Advisor. Your task is to analyze the Freelancer Profile/Summary against the Upwork Job Post to determine the overall suitability for bidding on this project. Provide a detailed assessment of the fit, including potential challenges and advantages. Conclude with a recommendation for the bid range (e.g., 'Low', 'Medium', 'High' based on fit and complexity) and a rating out of 10 that reflects the overall fit of the freelancer for the role.
"""

# --- Buttons based on the sketch and functionalities ---
st.markdown("---")
st.markdown("### Choose an action:")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    submit_generate = st.button("Generate New Proposal")
with col2:
    submit_match = st.button("Analyze Proposal Match (%)")
with col3:
    submit_improve = st.button("Improve Existing Proposal")
with col4:
    submit_selling_points = st.button("Highlight Key Selling Points")
with col5:
    submit_transferable = st.button("Identify Transferable Skills")
with col6:
    submit_bid_suitability = st.button("Assess Bid Suitability")

# --- Response Display Area ---
st.markdown('<div class="response-area">', unsafe_allow_html=True)
st.markdown('<h3 class="response-header">Proposal Analysis / Generation Result</h3>', unsafe_allow_html=True)
response_placeholder = st.empty() # Placeholder for the response text area
st.markdown('</div>', unsafe_allow_html=True)


# --- Logic for button clicks ---
if submit_generate:
    if job_post_text and freelancer_profile_text:
        with st.spinner("Generating proposal..."):
            response = get_gemini_response(job_post_text, freelancer_profile_text, PROMPT_GENERATE_PROPOSAL)
            response_placeholder.text_area("Generated Proposal:", value=response, height=400, key="generated_proposal")
    else:
        st.error("Please provide both the Upwork Job Post and your Freelancer Profile/Summary to generate a proposal.")

elif submit_match:
    if job_post_text and freelancer_profile_text:
        with st.spinner("Analyzing match percentage..."):
            response = get_gemini_response(job_post_text, freelancer_profile_text, PROMPT_ANALYZE_MATCH_PERCENTAGE)
            response_placeholder.text_area("Proposal Match Analysis:", value=response, height=300, key="match_analysis")
    else:
        st.error("Please provide both the Upwork Job Post and your Freelancer Profile/Summary to analyze the match.")

elif submit_improve:
    if job_post_text and freelancer_profile_text:
        with st.spinner("Suggesting improvements..."):
            response = get_gemini_response(job_post_text, freelancer_profile_text, PROMPT_IMPROVE_PROPOSAL)
            response_placeholder.text_area("Proposal Improvement Suggestions:", value=response, height=300, key="improve_suggestions")
    else:
        st.error("Please provide both the Upwork Job Post and your Freelancer Profile/Summary to get improvement suggestions.")

elif submit_selling_points:
    if job_post_text and freelancer_profile_text:
        with st.spinner("Highlighting selling points..."):
            response = get_gemini_response(job_post_text, freelancer_profile_text, PROMPT_HIGHLIGHT_SELLING_POINTS)
            response_placeholder.text_area("Key Selling Points:", value=response, height=300, key="selling_points")
    else:
        st.error("Please provide both the Upwork Job Post and your Freelancer Profile/Summary to highlight selling points.")

elif submit_transferable:
    if job_post_text and freelancer_profile_text:
        with st.spinner("Identifying transferable skills..."):
            response = get_gemini_response(job_post_text, freelancer_profile_text, PROMPT_IDENTIFY_TRANSFERABLE_SKILLS)
            response_placeholder.text_area("Transferable Skills:", value=response, height=300, key="transferable_skills")
    else:
        st.error("Please provide both the Upwork Job Post and your Freelancer Profile/Summary to identify transferable skills.")

elif submit_bid_suitability:
    if job_post_text and freelancer_profile_text:
        with st.spinner("Assessing bid suitability..."):
            response = get_gemini_response(job_post_text, freelancer_profile_text, PROMPT_ASSESS_BID_SUITABILITY)
            response_placeholder.text_area("Bid Suitability Assessment:", value=response, height=300, key="bid_suitability")
    else:
        st.error("Please provide both the Upwork Job Post and your Freelancer Profile/Summary to assess bid suitability.")

