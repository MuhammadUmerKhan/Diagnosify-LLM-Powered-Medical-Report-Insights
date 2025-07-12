import streamlit as st, os
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

logger = get_logger(__name__)

st.set_page_config(page_title="Medical Report Analyzer", page_icon="🩺", layout="wide")
apply_custom_css()

class MedicalChatbot:
    """Handles conversational queries about medical reports."""
    def __init__(self):
        self.llm = configure_llm()
        self.embedding_model = configure_embedding_model()
        self.uploaded_files = [f for f in st.session_state.get("uploaded_files", []) if f.name.lower().endswith('.pdf')]

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
                logger.info(f"Removed temporary file: {file_path}")

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
                    "You are a friendly Medical Report Assistant 🤗, helping patients understand their reports with clarity. "
                    "Answer based solely on the provided report, using simple language and a supportive tone. "
                    "For normal results, use a cheerful tone 🎉. For concerning results, be gentle and encouraging 💪. "
                    "If information is missing, note it kindly 🙏. Use emojis for engagement.\n\n"
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
            logger.error(f"Error setting up QA chain: {e}")
            return None

    @enable_chat_history
    def main(self):
        """Main function for the Assistant page."""
        st.header("💬 Medical Report Chatbot 🌡️")
        st.markdown("<p style='color:#00ff99'>Ask questions about your medical report!</p>", unsafe_allow_html=True)

        st.sidebar.title("🤖 Chatbot Page Overview")
        st.sidebar.markdown(
           "<p style='color:#00ff99'>This page allows you to ask questions about your uploaded medical reports (PDFs only). The AI chatbot uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers based on the report content, with a conversational history for follow-up questions.</p>",
            unsafe_allow_html=True
        )
        
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
                response = result["answer"]
                st.write(response)
                print_qa(MedicalChatbot, user_query, response)

if __name__ == "__main__":
    MedicalChatbot().main()