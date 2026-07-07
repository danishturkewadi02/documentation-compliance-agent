import fitz


def extract_pdf_text(pdf_path):

    try:

        document = fitz.open(pdf_path)

        extracted_text = ""

        for page in document:

            text = page.get_text()

            extracted_text += text + "\n"

        document.close()

        return extracted_text

    except Exception as e:

        print("PDF Parsing Error:", e)

        return None