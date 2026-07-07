# Documentation Compliance Agent

## Overview

This project is a Documentation Compliance Agent developed using Python and Flask. It compares a software requirement document (PDF) with a web application to check whether the implemented features match the documented requirements.

The application extracts requirements from the uploaded PDF, automatically logs into the target website, visits different pages, extracts UI elements, and compares them with the documentation using a Large Language Model (Groq Llama 3.3). Finally, it generates a compliance report in both HTML and JSON formats.

---

## Features

- Upload a documentation PDF
- Extract text from the PDF
- Split the document into chunks
- Generate embeddings using Sentence Transformers
- Store embeddings in a FAISS vector database
- Retrieve relevant requirements using RAG
- Automatically log into the website using Playwright
- Navigate through multiple pages after login
- Extract UI components from each page
- Compare documentation with website content using Groq LLM
- Generate HTML and JSON compliance reports

---

## Technologies Used

- Python
- Flask
- Playwright
- FAISS
- Sentence Transformers
- Groq API
- HTML/CSS

---

## Project Structure

```
documentation_compliance_agent/

│── app.py
│── config.py
│── requirements.txt
│── README.md

├── src/
│     ├── pdf_parser.py
│     ├── browser_extractor.py
│     ├── ai_compliance_analyzer.py
│     ├── page_loader.py
│     ├── report_generator.py
│     ├── requirement_extractor.py
│     ├── embeddings.py
│     ├── rag_retriever.py
│     ├── vector_store.py
│     └── ...

├── templates/

├── static/

├── uploads/

├── data/

├── reports/

└── screenshots/
```

---

## How It Works

1. Upload the documentation PDF.
2. Enter the website URL and login credentials.
3. The application extracts the document text and creates embeddings.
4. Relevant requirements are retrieved using FAISS.
5. Playwright logs into the website and visits all configured pages.
6. UI information is extracted and stored as JSON.
7. The extracted website data is compared with the documentation using Groq.
8. A compliance report is generated.

---
System Architecture

```
                    Upload PDF
                        │
                        ▼
               PDF Text Extraction
                        │
                        ▼
                 Text Chunking
                        │
                        ▼
           Sentence Transformer Embeddings
                        │
                        ▼
                FAISS Vector Database
                        │
                        ▼
            Requirement Retrieval (RAG)
                        │
                        ▼
           Playwright Browser Automation
                        │
                        ▼
           Website UI Extraction (JSON)
                        │
                        ▼
         Groq LLM Compliance Comparison
                        │
                        ▼
       HTML Report + JSON Compliance Report
## Installation

Clone the repository

```bash
git clone <repository-url>
```

Move to the project folder

```bash
cd documentation_compliance_agent
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browsers

```bash
playwright install
```

Run the project

```bash
python app.py
```

Open the application in your browser:

```
http://127.0.0.1:5000
```

---

## Output

The application generates:

- `reports/compliance_report.html`
- `reports/ai_response.json`

Screenshots of the visited pages are also saved during the analysis.

---

## Future Improvements

- Support for more document formats
- Better requirement extraction
- PDF report generation
- Support for multiple LLM providers
- Improved UI

---

## Author

Mohd Danish Turkewadi