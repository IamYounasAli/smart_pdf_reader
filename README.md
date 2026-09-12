# Groq & Streamlit PDF Reader & Quiz Generator

A high-performance AI PDF reader that generates Executive Summaries, Skimming overviews, Scanning detail extractions, and interactive Multiple-Choice Quizzes using Groq LPUs.

## Setup Instructions

1. **Unzip the file and navigate to the folder:**
   ```bash
   cd pdf_reader_app
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Rename `.env.example` to `.env` and insert your Groq API Key:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key
   ```
   *(Alternatively, you can enter the API key directly in the Streamlit web interface sidebar)*.

5. **Run the Application:**
   ```bash
   streamlit run app.py
   ```
