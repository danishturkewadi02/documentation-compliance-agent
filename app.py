from flask import (
    Flask,
    render_template,
    request,
    send_file,
    send_from_directory
)
import webbrowser
import os
import json
import faiss
from src.pdf_report_generator import generate_pdf
from src.pdf_parser import extract_pdf_text
from src.text_chunker import chunk_text
from src.embeddings import create_embeddings
from src.vector_store import create_faiss_index
from src.rag_retriever import retrieve_relevant_chunks
from src.requirement_extractor import extract_requirements
from src.report_generator import generate_html
from src.browser_extractor import open_website
from src.page_loader import load_pages
from src.ai_compliance_analyzer import analyze as ai_analyze
from flask import send_file
print("=" * 60)
print("RUNNING APP.PY")
print(__file__)
print("=" * 60)
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_route():

    # -----------------------------
    # 1. Read form data
    # -----------------------------

    pdf = request.files["pdf_file"]

    website_url = request.form["url"]
    email = request.form["email"]
    password = request.form["password"]

    # -----------------------------
    # 2. Save uploaded PDF
    # -----------------------------
    if pdf.filename == "":
        return render_template(
        "index.html",
        result="Please select a PDF file."
     )
    pdf_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        pdf.filename
    )

    pdf.save(pdf_path)

    print("\n========== PDF ==========\n")

    print("PDF Saved :", pdf_path)

    # -----------------------------
    # 3. Extract PDF text
    # -----------------------------

    pdf_text = extract_pdf_text(pdf_path)

    with open(
        "data/extracted_text.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(pdf_text)

    print("PDF text extracted")

    # -----------------------------
    # 4. Chunk PDF
    # -----------------------------

    chunks = chunk_text(pdf_text)

    with open(
        "data/chunks.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=4
        )

    print("Chunks created :", len(chunks))

    # -----------------------------
    # 5. Embeddings
    # -----------------------------

    embeddings = create_embeddings(chunks)

    print("Embeddings :", len(embeddings))

    # -----------------------------
    # 6. Create FAISS
    # -----------------------------

    index = create_faiss_index(embeddings)

    faiss.write_index(
        index,
        "data/vector_index.faiss"
    )

    print("FAISS vectors :", index.ntotal)

    # -----------------------------
    # 7. Retrieve documentation
    # -----------------------------

    query = "What should login page contain?"

    retrieved_chunks = retrieve_relevant_chunks(query)

    requirements = []

    for chunk in retrieved_chunks:

        requirements.extend(
            extract_requirements(chunk)
        )
    requirements = list(dict.fromkeys(requirements))
    print("\n========== REQUIREMENTS ==========\n")

    for req in requirements:
        print("-", req)

    # -----------------------------
    # 8. Crawl website
    # -----------------------------

    print("\n========== WEBSITE ==========\n")

    open_website(
        website_url,
        email,
        password
    )

    # -----------------------------
    # 9. Load extracted pages
    # -----------------------------

    pages = load_pages()

    print(
        "\nPages Extracted :",
        len(pages)
    )

    # -----------------------------
    # 10. AI Analysis
    # -----------------------------
    print("Calling AI Analyzer...")
    print(ai_analyze)
    print("\n========== AI ANALYSIS ==========\n")

    try:
        ai_response = ai_analyze(requirements, pages)

    except Exception as e:

        print("AI Error:", e)

        return render_template(
        "index.html",
        result="AI analysis failed. Please try again later or check your Groq quota."
        )

    print(
    json.dumps(
        ai_response,
        indent=4,
        ensure_ascii=False
    )
    )

    # Save raw AI response

   
    generate_html(
    ai_response,
    pdf.filename
    )
    generate_pdf(ai_response)
    with open(
    "reports/ai_response.json",
    "w",
    encoding="utf-8"
    ) as file:

        json.dump(
        ai_response,
        file,
        indent=4,
        ensure_ascii=False
        )
    report_path = os.path.abspath("reports/compliance_report.html")
    ##webbrowser.open("file://" + report_path)
    print("\nAI report saved successfully")

    return render_template(
    "report.html")
@app.route("/download-report")
def download_report():

    return send_file(
        "reports/compliance_report.pdf",
        as_attachment=True
    )
@app.route("/view-report")
def view_report():

    return send_file(
        "reports/compliance_report.html"
    )
@app.route("/download-json")
def download_json():

    return send_file(
        "reports/ai_response.json",
        as_attachment=True
    )
@app.route("/screenshots/<path:filename>")
def screenshots(filename):

    return send_from_directory(
        "reports/screenshots",
        filename
    )
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )