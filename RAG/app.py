import streamlit as st
import pickle
import os

from retriever import retrieve_relevant_chunks
from llm import generate_answer
from pdf_processor import process_pdf

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Native PDF RAG Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_pdf" not in st.session_state:
    st.session_state.processed_pdf = None

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

header {visibility:hidden;}
footer {visibility:hidden;}

.block-container{
    max-width:1200px;
    padding-top:1.5rem;
}

.main-title{
    font-size:34px;
    font-weight:700;
    margin-bottom:0;
}

.sub-title{
    color:#9ca3af;
    font-size:15px;
    margin-bottom:20px;
}

.info-card{
    border:1px solid #31333F;
    border-radius:12px;
    padding:15px;
    margin-top:10px;
}

div[data-testid="stChatMessage"]{
    border:1px solid #31333F;
    border-radius:12px;
    padding:14px;
    margin-bottom:12px;
}

.source-box{
    border-left:4px solid #22c55e;
    padding-left:12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<div class='main-title'>
📄 Native PDF RAG Chatbot
</div>

<div class='sub-title'>
Ask questions based only on the content of your uploaded PDF.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("📂 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type="pdf"
    )

    st.markdown("---")

    if uploaded_file:

        st.success("✅ PDF Loaded")

        st.markdown(f"""
<div class="info-card">

<b>Current Document</b>

<br><br>

📄 {uploaded_file.name}

</div>
""", unsafe_allow_html=True)

    else:

        st.info("Upload a PDF to begin.")

    st.markdown("---")

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()
        # ---------------------------------------------------
# MAIN APPLICATION
# ---------------------------------------------------

if uploaded_file:

    os.makedirs("data", exist_ok=True)

    pdf_path = os.path.join("data", uploaded_file.name)

    # Save uploaded PDF
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process only once for each uploaded PDF
    if st.session_state.processed_pdf != uploaded_file.name:

        with st.spinner("📄 Processing PDF..."):

            index, chunks = process_pdf(pdf_path)

            with open("faiss_index.pkl", "wb") as f:
                pickle.dump(index, f)

            with open("chunks.pkl", "wb") as f:
                pickle.dump(chunks, f)

        st.session_state.processed_pdf = uploaded_file.name
        st.session_state.messages = []

        st.success("✅ PDF processed successfully!")

    # Load saved files

    with open("faiss_index.pkl", "rb") as f:
        index = pickle.load(f)

    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    # ---------------------------------------------------
    # PDF STATUS
    # ---------------------------------------------------

    left, right = st.columns([4, 1])

    with left:

        st.success("🟢 Ready to answer questions")

    with right:

        st.metric(
            label="Chunks",
            value=len(chunks)
        )

    st.divider()

    # ---------------------------------------------------
    # CHAT HISTORY
    # ---------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ---------------------------------------------------
    # CHAT INPUT
    # ---------------------------------------------------

    question = st.chat_input(
        "Ask a question about your PDF..."
    )
    # ---------------------------------------------------
# GENERATE ANSWER
# ---------------------------------------------------

    if question:

        # ----------------------------
        # Show User Message
        # ----------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # ----------------------------
        # Assistant Response
        # ----------------------------

        with st.chat_message("assistant"):

            answer_placeholder = st.empty()

            with st.spinner("🤖 Thinking..."):

                retrieved_chunks = retrieve_relevant_chunks(
                    question,
                    index,
                    chunks
                )

                context = "\n\n".join(
                    chunk["text"]
                    for chunk in retrieved_chunks
                )

                answer = generate_answer(
                    context,
                    question
                )

            answer_placeholder.markdown(answer)

            # Save assistant reply
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            # ----------------------------
            # Source Citations
            # ----------------------------

            if retrieved_chunks:

                st.markdown("#### 📖 Sources")

                for chunk in retrieved_chunks:

                    with st.expander(
                        f"📄 Page {chunk['page']}"
                    ):

                        st.markdown(
                            f"""
<div class="source-box">

{chunk["text"]}

</div>
                            """,
                            unsafe_allow_html=True
                        )
                        # ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

else:

    st.markdown("<br>", unsafe_allow_html=True)

    st.info("📄 Upload a PDF from the left sidebar to begin.")

    st.markdown("### Try asking questions like:")

    st.markdown("""
- Summarize this document.
- What are the key findings?
- Explain the main concepts.
- What is the conclusion?
- List the important points.
""")