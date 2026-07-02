import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content