Upwork Proposal Assistant
Overview
The Upwork Proposal Assistant is a Streamlit-based web application designed to help freelancers craft compelling and highly relevant proposals for Upwork job posts. By leveraging the power of Google's Gemini AI model, it analyzes job descriptions and your freelancer profile/summary to generate tailored proposals, assess match percentages, suggest improvements, highlight key selling points, and more.

Features
This application provides the following functionalities:

Generate New Proposal: Crafts a unique and persuasive proposal based on the Upwork job post and your freelancer profile.

Analyze Proposal Match (%): Acts as an ATS scanner, providing a percentage match, identifying missing keywords, and offering final thoughts on alignment.

Improve Existing Proposal: Offers actionable advice and suggestions to enhance your proposal's effectiveness and alignment with job requirements.

Highlight Key Selling Points: Extracts and emphasizes your most significant achievements and relevant skills from your profile in the context of the job post.

Identify Transferable Skills: Pinpoints versatile skills from your profile that can be effectively applied to the job role, even if not explicitly mentioned.

Assess Bid Suitability: Provides an overall assessment of your fit for the project, including potential challenges, advantages, and a recommended bid range/rating.

Setup and Installation
Follow these steps to get the Upwork Proposal Assistant up and running on your local machine.

1. Clone the Repository (or save the code)
If you have the code in a file, save it as app.py. If it's part of a Git repository, clone it:

git clone <repository_url>
cd <repository_directory>

2. Create a Virtual Environment (Recommended)
It's good practice to use a virtual environment to manage dependencies:

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install Dependencies
Install the required Python libraries using the requirements.txt file provided:

pip install -r requirements.txt

4. Obtain a Google Gemini API Key
Go to the Google AI Studio and create a new API key.

Copy your API key.

5. Configure Environment Variables
Create a file named .env in the same directory as your app.py file and add your Gemini API key to it:

GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"

Replace "YOUR_GEMINI_API_KEY_HERE" with the actual API key you obtained.

6. Run the Streamlit Application
Once all dependencies are installed and your API key is configured, run the application from your terminal:

streamlit run app.py

This command will open the application in your default web browser.

How to Use
Paste Upwork Job Post: Copy the full job description from Upwork and paste it into the "Upwork Job Post" text area.

Paste Your Freelancer Profile/Summary: Provide a summary of your relevant skills, experience, and achievements, or even an existing draft of a proposal, in the "Your Freelancer Profile/Summary" text area.

Choose an Action: Click on any of the buttons under "Choose an action:" to get the desired analysis or generate a proposal.

View Results: The results will be displayed in the "Proposal Analysis / Generation Result" area below the buttons.

Future Enhancements
Multi-page PDF Support: Extend pdf2image functionality to process entire PDF resumes/portfolios.

Save/Load Proposals: Implement functionality to save generated proposals or analyses for later review.

User Authentication: For a more personalized experience, integrate user authentication to store profiles and job posts.

Advanced Filtering/Search: Allow users to search through past analyses or proposals.

Integration with Upwork API: (Requires Upwork API access) Potentially automate job post fetching or proposal submission.

Customizable Prompts: Allow users to modify or create their own prompts for more