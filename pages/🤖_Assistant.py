import streamlit as st
import os
import uuid
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from scripts.utils import enable_chat_history, display_msg, print_qa, configure_llm, configure_embedding_model, apply_custom_css
from scripts.config import get_logger
from scripts.streaming import StreamHandler
from scripts.config import TEMP_DIR
from scripts.ragas_evaluator import evaluate_and_store

logger = get_logger(__name__)

st.set_page_config(page_title="Medical Report Chatbot", page_icon="🩺", layout="wide")
apply_custom_css()

class MedicalChatbot:
    """Handles conversational queries about medical reports."""
    def __init__(self):
        self.llm = configure_llm()
        self.embedding_model = configure_embedding_model()
        self.uploaded_files = [f for f in st.session_state.get("uploaded_files", []) if f.name.lower().endswith('.pdf')]
        # Initialize user_id if not already set
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
            logger.info(f"✅ Assigned new user_id: {st.session_state.user_id}")

    def save_file(self, file):
        """Save uploaded file temporarily."""
        os.makedirs(TEMP_DIR, exist_ok=True)
        file_path = os.path.join(TEMP_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        return file_path

    def setup_qa_chain(self):
        """Set up the conversational QA chain with FAISS retriever."""
        try:
            docs = []
            for file in self.uploaded_files:
                file_path = self.save_file(file)
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
                os.unlink(file_path)
                logger.info(f"✅ Removed temporary file: {file_path}")

            if not docs:
                raise ValueError("No valid PDF documents extracted.")

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            vector_db = FAISS.from_documents(splits, self.embedding_model)
            retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})
            memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True)
            system_prompt = PromptTemplate(
                input_variables=["context", "question", "chat_history"],
                template=(
                    "You are a kind Medical Assistant 🤗. Explain the report in clear, simple terms based only on the context. "
                    "Use 🎉 for normal findings and 💪 for concerns. If data is missing, respond gently 🙏. Use emojis for empathy.\n\n"
                    "Context: {context}\nChat History: {chat_history}\nQuestion: {question}\nAnswer:"
                )
            )
            return ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=memory,
                return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": system_prompt}
            )
        except Exception as e:
            logger.error(f"❌ Error setting up QA chain: {e}")
            return None

    @enable_chat_history
    def main(self):
        """Main function for the chat page."""
        st.header("💬 Medical Report Chatbot 🌡️")
        st.markdown("<p style='color:#00ff99'>Ask questions about your medical report!</p>", unsafe_allow_html=True)

        st.sidebar.title("🤖 Medical Report Analyzer")
        st.sidebar.markdown(
            "<p style='color:#00ff99'>Use this page to chat with your medical reports or navigate to RAGAS Evaluation to view your chat history and metrics.</p>",
            unsafe_allow_html=True
        )

        # Sidebar for RAGAS evaluation
        st.sidebar.subheader("RAGAS Evaluation")
        enable_ragas = st.sidebar.checkbox("Enable RAGAS Evaluation", value=False)
        if enable_ragas:
            openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
            if openai_api_key:
                openai_api_key = openai_api_key.strip()
                if openai_api_key.startswith("sk-"):
                    os.environ["OPENAI_API_KEY"] = openai_api_key
                    logger.info("✅ OpenAI API key set successfully.")
                    st.session_state.enable_ragas = True
                else:
                    st.sidebar.error("Invalid API key format. It should start with 'sk-'.")
                    logger.info("❌ Wrong OpenAI API key.")
                    st.session_state.enable_ragas = False
            else:
                st.sidebar.warning("Please provide a valid OpenAI API key to enable RAGAS evaluation.")
                st.session_state.enable_ragas = False
        else:
            st.session_state.enable_ragas = False

        if not self.uploaded_files:
            st.error("❌ Upload a PDF report on the Home page first.")
            return

        user_query = st.chat_input(placeholder="🔎 Ask about your report")
        if user_query:
            qa_chain = self.setup_qa_chain()
            if not qa_chain:
                st.error("❌ Failed to set up retrieval system.")
                return

            display_msg(user_query, "user")
            with st.chat_message("assistant", avatar="🤖"):
                st_cb = StreamHandler(st.empty())
                result = qa_chain.invoke({"question": user_query}, {"callbacks": [st_cb]})
                retrieved_docs = result.get("source_documents", [])
                retrieved_contexts = [doc.page_content for doc in retrieved_docs]
                combined_context = " ".join(retrieved_contexts) if retrieved_contexts else ""
                response = result["answer"]
                st.write(response)
                print_qa(MedicalChatbot, user_query, response)

                # RAGAS evaluation and storage
                if st.session_state.get("enable_ragas", False) and "OPENAI_API_KEY" in os.environ:
                    try:
                        evaluate_and_store(
                            question=user_query,
                            generated_answer=response,
                            context=combined_context,
                            user_id=st.session_state.user_id
                        )
                    except Exception as e:
                        if "AuthenticationError" in str(e) or "invalid_api_key" in str(e).lower():
                            logger.error(f"❌ OpenAI API authentication failed: {e}")
                            st.error("❌ Authentication failed. Please check your OpenAI API key.")
                        else:
                            logger.error(f"❌ Error during RAGAS evaluation: {e}")
                            st.error("❌ Failed to evaluate and store metrics.")

if __name__ == "__main__":
    MedicalChatbot().main()