import ollama


def generate_answer(context, question):

    prompt = f"""
You are a PDF Question Answering Assistant.

Answer ONLY from the provided context.

Rules:
1. Do not use outside knowledge.
2. If the answer is not present in the context, say:
   "Information not found in the PDF."
3. Keep the answer concise and accurate.
4. Mention relevant source content when possible.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]