def chunk_text(pages, chunk_size=500, overlap=100):

    chunks = []

    for page_data in pages:

        page_number = page_data["page"]

        text = page_data["text"]

        # Split by paragraph boundaries
        paragraphs = text.split("\n\n")

        current_chunk = ""

        for para in paragraphs:

            para = para.strip()

            if not para:
                continue

            # If paragraph fits in current chunk
            if len(current_chunk) + len(para) <= chunk_size:

                current_chunk += para + "\n\n"

            else:

                # Save current chunk
                chunks.append(
                    {
                        "page": page_number,
                        "text": current_chunk.strip()
                    }
                )

                # Create overlap
                overlap_text = current_chunk[-overlap:]

                # Start new chunk
                current_chunk = overlap_text + para + "\n\n"

        # Save remaining chunk
        if current_chunk.strip():

            chunks.append(
                {
                    "page": page_number,
                    "text": current_chunk.strip()
                }
            )

    return chunks