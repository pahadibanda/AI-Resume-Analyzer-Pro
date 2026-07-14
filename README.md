# 🤖 AI Resume Analyzer Pro

An AI-powered Resume Analyzer that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) and job descriptions. It calculates ATS compatibility, matches resumes with Job Descriptions, identifies skill gaps, recommends career paths, generates custom interview questions, and exports a professionally formatted PDF intelligence report.

---

## 🔗 Live Demo

👉 **[Launch AI Resume Analyzer Pro on Streamlit Cloud](https://pahadibanda-ai-resume-analyzer.streamlit.app)**

---

## ✨ Key Features

* **📊 ATS Compatibility Scoring:** Detailed multi-factor ATS calculator assessing layout structure, contact details, standard headings, and skill alignment.
* **🎯 JD Match Analysis:** Compares your resume directly with a target Job Description to compute a compatibility percentage.
* **🧠 Skill Gap Detection:** Highlights matching skills and lists critical missing skills in clean, color-coded grids.
* **💼 Recommended Career Roles:** Recommends alternative job titles based on your detected skill taxonomy.
* **🎤 AI Interview Preparation:** Generates mock interview questions categorized by difficulty levels (Easy, Medium, Hard).
* **📄 Premium PDF Reports:** Download clean, minimalist, professionally designed reports (built using ReportLab) summarizing all insights and scoring gauges.
* **🛡️ Built-in Privacy & Security:** 
  * Strict file upload checks (MIME verification, double extension blocks, 10MB limit).
  * **Zero-persistence temporary file processing** — uploaded documents are parsed in memory and instantly deleted from the disk.

---

## 🛠️ Tech Stack

* **Frontend & Orchestration:** Python, Streamlit
* **AI Engine:** LangChain, Groq API (`llama-3.3-70b-versatile` model)
* **Document Extraction:** PDFPlumber
* **Report Engine:** ReportLab (custom page templates, column layouts, custom canvas flowables)
* **Styling & Particle FX:** Vanilla CSS, HTML5, tsParticles

---

## ⚙️ Installation & Local Setup

Clone the repository and install the dependencies to run the project locally:

```bash
# Clone the repository
git clone https://github.com/pahadibanda/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```

---

## 🔑 Environment Variables Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

*Note: The `.env` file is configured in `.gitignore` and is ignored by Git to prevent your API credentials from being committed to GitHub.*

For **Streamlit Cloud Deployment**, navigate to your App Dashboard ➔ **Settings** ➔ **Secrets**, and paste:

```toml
GROQ_API_KEY="your_groq_api_key"
```

---

## 👨‍💻 Author

**Rajat Rangra**

* **GitHub:** [pahadibanda](https://github.com/pahadibanda)
* **LinkedIn:** [Rajat Rangra on LinkedIn](https://www.linkedin.com/in/rajatrangra/)
* **Portfolio:** [Rajat's Portfolio Website](https://rajat-portfolio-kappa.vercel.app/)

---

## ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub!
