# 📄 Smart PDF Reader & Intelligence Suite

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_red.svg)](https://smartpdfreader.streamlit.app)

An interactive AI-powered document analysis application built with **Streamlit** and high-speed **Groq LPU** inference. Upload any PDF document to extract executive summaries, perform skimming/scanning analyses, and automatically generate interactive multiple-choice quizzes.

---

## ✨ Features

* **📝 Executive Summary:** Generates structured document overviews highlighting objectives, main themes, and core takeaways.
* **🔍 Skimming Analysis:** Extracts major section headings, central arguments, and bullet points for fast scanning.
* **🎯 Scanning Extraction:** Locates and pulls out specific metrics, key dates, technical terminology, and definitions.
* **❓ Interactive Quiz Mode:** Auto-generates customized multiple-choice quizzes complete with real-time scoring and answer explanations.

---

## 🛠️ Project Structure

```text
smart_pdf_reader/
│
├── app.py                   # Main Streamlit application entry point
├── requirements.txt         # Required Python packages
├── README.md                # Project documentation
│
└── utils/
    ├── pdf_processor.py     # PDF text extraction utilities
    ├── groq_client.py       # API connection and generation prompts
    └── quiz_engine.py       # Quiz generation and JSON parsing logic

```

---

## 🚀 Local Setup Instructions

### 1. Prerequisites

Ensure you have **Python 3.10 or higher** installed on your machine.

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/smart_pdf_reader.git
cd smart_pdf_reader

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Local Secrets

Create a `.streamlit` folder in the root directory and add a `secrets.toml` file inside it:

```bash
mkdir .streamlit
touch .streamlit/secrets.toml

```

Add your **Groq API Key** to `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"

```

### 5. Run the Application

```bash
streamlit run app.py

```

---

## ☁️ Deployment on Streamlit Cloud

1. Push your repository to **GitHub** (ensure `.streamlit/secrets.toml` is in `.gitignore`).
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app**, select your repository, branch, and set `app.py` as the main file path.
4. Go to **Advanced settings...** -> **Secrets** and paste:
```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"

```


5. Click **Deploy**.

---

## ⚡ Tech Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io/)
* **LLM Engine:** [Groq LPU API](https://groq.com/)
* **PDF Parsing:** `pypdf`
* **Language:** Python 3.10+
