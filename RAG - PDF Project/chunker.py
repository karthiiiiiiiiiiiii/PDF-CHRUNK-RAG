import re


def split_long_text(text, chunk_size, overlap):
    """
    Split long text into smaller chunks at sentence boundaries.
    """

    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        if len(current_chunk) + len(sentence) <= chunk_size:

            current_chunk += sentence + " "

        else:

            if current_chunk.strip():

                chunks.append(current_chunk.strip())

            overlap_text = current_chunk[-overlap:]

            current_chunk = overlap_text + " " + sentence

    if current_chunk.strip():

        chunks.append(current_chunk.strip())

    return chunks


def chunk_text(pages, chunk_size=500, overlap=100):

    chunks = []

    current_chunk = ""
    current_pages = []

    for page_data in pages:

        page_number = page_data["page"]
        text = page_data["text"]

        # Normalize line endings
        text = text.replace("\r", "")

        # Split into logical blocks
        blocks = re.split(r"\n\s*\n", text)

        for block in blocks:

            block = block.strip()

            if not block:
                continue

            lines = block.split("\n")

            first_line = lines[0].strip()

            # Detect headings
            is_heading = (
                len(lines) == 1
                and len(first_line) < 80
                and (
                    first_line.isupper()
                    or first_line.endswith(":")
                )
            )

            # Detect bullet or numbered lists
            is_list = any(
                re.match(r"^(\-|\*|•|\d+\.)\s+", line.strip())
                for line in lines
            )

            block_text = "\n".join(lines)

            # Start a new chunk if heading appears
            if is_heading and current_chunk.strip():

                chunks.append({
                    "page": current_pages[0],
                    "text": current_chunk.strip()
                })

                current_chunk = ""
                current_pages = []

            # If block fits
            if len(current_chunk) + len(block_text) <= chunk_size:

                current_chunk += block_text + "\n\n"

                if page_number not in current_pages:
                    current_pages.append(page_number)

            else:

                # Save previous chunk
                if current_chunk.strip():

                    chunks.append({
                        "page": current_pages[0],
                        "text": current_chunk.strip()
                    })

                overlap_text = current_chunk[-overlap:]

                current_chunk = overlap_text + "\n\n" + block_text + "\n\n"

                current_pages = [page_number]

            # Split oversized paragraphs
            if len(current_chunk) > chunk_size * 1.5:

                long_chunks = split_long_text(
                    current_chunk,
                    chunk_size,
                    overlap
                )

                for chunk in long_chunks[:-1]:

                    chunks.append({
                        "page": current_pages[0],
                        "text": chunk
                    })

                current_chunk = long_chunks[-1]

    if current_chunk.strip():

        chunks.append({
            "page": current_pages[0],
            "text": current_chunk.strip()
        })

    return chunks