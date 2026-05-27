import streamlit as st
import pickle
import os

from retriever import retrieve_relevant_chunks
from llm import generate_answer
from pdf_processor import process_pdf

st.set_page_config(page_title="PDF RAG Chatbot")

st.title("📄 Native PDF RAG Chatbot")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)

# Process PDF
if uploaded_file:

    # Save uploaded PDF temporarily
    pdf_path = os.path.join("data", uploaded_file.name)

    os.makedirs("data", exist_ok=True)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    # Process PDF only once
    if not os.path.exists("faiss_index.pkl"):

        with st.spinner("Processing PDF..."):

            index, chunks = process_pdf(pdf_path)

            # Save index
            with open("faiss_index.pkl", "wb") as f:
                pickle.dump(index, f)

            # Save chunks
            with open("chunks.pkl", "wb") as f:
                pickle.dump(chunks, f)

    # Load index
    with open("faiss_index.pkl", "rb") as f:
        index = pickle.load(f)

    # Load chunks
    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    st.success("PDF processed successfully!")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User question
    question = st.chat_input("Ask a question from the PDF")

    if question:

        # Store user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Show user message
        with st.chat_message("user"):
            st.markdown(question)

        # Retrieve relevant chunks
        retrieved_chunks = retrieve_relevant_chunks(
            question,
            index,
            chunks
        )

        # Create context
        context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)

        # Generate answer
        answer = generate_answer(
            context,
            question
        )

        # FIX: initialize citations
        citations = ""

        # Add citations
        for chunk in retrieved_chunks:
            citations += (
                f"\nPage {chunk['page']}:\n"
                f"{chunk['text'][:300]}...\n"
            )

        final_response = answer + citations

        # Store assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": final_response
            }
        )

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(final_response)

else:
    st.info("Please upload a PDF file.")