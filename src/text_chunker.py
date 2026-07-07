def chunk_text(text, chunk_size=800):

    paragraphs = text.split("\n\n")

    chunks = []

    current_chunk = ""

    for paragraph in paragraphs:

        if len(current_chunk) + len(paragraph) < chunk_size:

            current_chunk += paragraph + "\n\n"

        else:

            chunks.append(current_chunk)

            current_chunk = paragraph + "\n\n"

    if current_chunk:

        chunks.append(current_chunk)

    return chunks