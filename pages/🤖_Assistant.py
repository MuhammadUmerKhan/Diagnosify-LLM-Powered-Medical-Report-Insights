import streamlit as st, os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from src.utils import enable_chat_history, display_msg, print_qa, configure_llm, configure_vector_embeddings
from src.streaming import StreamHandler
from src.logger import get_logger
from src.config import TEMP_DIR

logger = get_logger(__name__)

st.set_page_config(page_title="Medical Report Analyzer", page_icon="🩺", layout="wide")

# Custom CSS
st.markdown("""
<style>
.stApp { 
    color: #00ff99; 
    background: #000000; 
    font-family: 'Arial', sans-serif;
}
.card { 
    background: linear-gradient(135deg, #1c2526, #2e2e2e); 
    border-radius: 15px; 
    padding: 20px; 
    margin-bottom: 20px; 
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7); 
    border: 2px solid #00e5ff;
}
.stButton>button { 
    background: #ff00ff; 
    color: #ffd700; 
    border-radius: 10px; 
    padding: 12px 24px; 
    border: none; 
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.8); 
    font-size: 16px; 
    font-weight: bold;
}
.stButton>button:hover { 
    background: #cc00cc; 
    box-shadow: 0 0 25px rgba(255, 0, 255, 1); 
    transform: scale(1.1); 
    color: #ffffff;
}
h1, h2, h3 { 
    color: #ffd700; 
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
}
.warning { color: #ff5252; font-weight: bold; }
.critical { color: #ff5252; font-weight: bold; }
.borderline { color: #ffca28; font-weight: bold; }
.normal { color: #00ff99; font-weight: bold; }
.stDataFrame { background: #1c2526; border-radius: 10px; padding: 10px; }
.dataframe th { background: #ff00ff !important; color: #ffd700 !important; font-weight: bold !important; }
.dataframe tr:nth-child(even) { background: #2e2e2e; }
.dataframe tr:nth-child(odd) { background: #1c2526; }
.dataframe td { color: #00ff99; }
.bullet-point { 
    margin-left: 20px; 
    color: #00e5ff; 
    font-size: 16px; 
    line-height: 1.6;
}
.chat-message { 
    padding: 10px; 
    margin-bottom: 10px; 
    border-radius: 10px;
}
.chat-message.user { background: #ff00ff; color: #ffd700; }
.chat-message.bot { background: #2e2e2e; color: #00ff99; }
.stSidebar { 
    background: #1c2526; 
    color: #00e5ff;
}
.stSidebar h3 { color: #ffd700; }
.stSidebar p { color: #00ff99; }
.stSelectbox label { color: #ffd700; }
.stSelectbox div[data-baseweb="select"] { background: #2e2e2e; color: #00ff99; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🤖 Chatbot Page Overview")
st.sidebar.markdown("""
<p style='color:#00ff99'>This page allows you to ask questions about your uploaded medical reports (PDFs only). The AI chatbot uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers based on the report content, with a conversational history for follow-up questions.</p>
""", unsafe_allow_html=True)

# st.sidebar.subheader("📤 Chatbot Settings")
configure_llm()

st.header("💬 Medical Diagnosis Chatbot 🌡️")
st.markdown("<p style='color:#00ff99; font-size: 18px;'>Ask questions about your medical report! 📋</p>", unsafe_allow_html=True)

class MedicalChatbot:
    def __init__(self):
        self.llm = configure_llm()
        self.embedding_model = configure_vector_embeddings()
        # Filter for PDFs only
        self.uploaded_files = [f for f in st.session_state.get("uploaded_files", []) if f.name.lower().endswith('.pdf')]

    def save_file(self, file):
        os.makedirs(TEMP_DIR, exist_ok=True)
        file_path = os.path.join(TEMP_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        return file_path

    def setup_qa_chain(self):
        try:
            docs = []
            for file in self.uploaded_files:
                file_path = self.save_file(file)
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
                os.unlink(file_path)
                logger.info(f"✅ Removed temporary file: {file_path}")

            if not docs:
                raise Exception("❌ No valid PDF documents extracted.")

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            vector_db = FAISS.from_documents(splits, self.embedding_model)
            retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})
            memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True)
            system_prompt = PromptTemplate(
                input_variables=["context", "question", "chat_history"],
                template=(
                    "You are a friendly and empathetic Medical Report Document Assistant 🤗, here to help patients understand their medical reports with care and clarity. Provide accurate, detailed, and well-structured answers based solely on the provided medical report documents 📄. Use a warm, supportive tone and simple language, avoiding complex medical jargon—explain terms clearly when needed 🌟.\n\n"
                    "Adjust your tone based on the report's findings: \n"
                    "- For normal results, use a cheerful and reassuring tone to celebrate good health 🎉 (e.g., 'Everything looks perfect!').\n"
                    "- For concerning or critical results, adopt a gentle, cautious, and hopeful tone to provide clarity while offering encouragement 💪 (e.g., 'This needs attention, but with the right steps, we can manage it!').\n"
                    "- If information is missing, kindly note it and offer general, helpful guidance 🙏.\n\n"
                    "Incorporate emojis to make answers clear, engaging, and emotionally supportive 😊.\n\n"
                    "Context: {context}\n\n"
                    "Chat History: {chat_history}\n\n"
                    "User Question: {question}\n\n"
                    "Answer:"
                )
            )
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=memory,
                return_source_documents=True,
                verbose=False,
                combine_docs_chain_kwargs={"prompt": system_prompt}
            )
            return qa_chain
        except Exception as e:
            logger.error(f"❌ Error setting up QA chain: {e}")
            return None

    @enable_chat_history
    def main(self):
        if not self.uploaded_files:
            st.error("❌ Please upload a PDF medical report using the Home page sidebar to start analyzing! 🚀")
            st.stop()

        user_query = st.chat_input(placeholder="🔎 Ask something about your medical report!")
        if user_query:
            qa_chain = self.setup_qa_chain()
            if qa_chain is None:
                st.error("❌ Failed to set up retrieval system. Please try again.")
                return

            display_msg(user_query, "user")
            with st.chat_message("assistant", avatar="🤖"):
                st_cb = StreamHandler(st.empty())
                result = qa_chain.invoke({"question": user_query}, {"callbacks": [st_cb]})
                response = result["answer"]
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
                print_qa(MedicalChatbot, user_query, response)

if __name__ == "__main__":
    obj = MedicalChatbot()
    obj.main()