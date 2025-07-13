from ragas.metrics import faithfulness
from ragas import evaluate
from datasets import Dataset
from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
from scripts.config import get_logger, get_mongo_uri

# Logger setup
logger = get_logger(__name__)

def evaluate_rag_metrics(
    question: str,
    generated_answer: str,
    context: str,
) -> Optional[Dict[str, float]]:
    """
    Evaluates the faithfulness metric using RAGAS for a single Q&A-context set.
    """
    try:
        logger.info("♻ Preparing dataset for RAGAS evaluation...")
        dataset = Dataset.from_dict({
            "question": [question],
            "answer": [generated_answer],
            "contexts": [[context]]
        })
        logger.info("♻ Running faithfulness evaluation...")
        result = evaluate(dataset, metrics=[faithfulness])
        metrics = result.to_pandas().to_dict("records")[0]
        logger.info(f"✅ Evaluation complete: {metrics}")
        return {"faithfulness": metrics['faithfulness']}
    except Exception as e:
        logger.error(f"❌ Metric evaluation failed: {e}")
        return {"faithfulness": 0.0}

def store_chat_metrics(
    question: str,
    generated_answer: str,
    context: str,
    metrics: Dict[str, float],
    user_id: str,
    db_name: str = "diagnosify",
    collection_name: str = "chat_history"
):
    """
    Stores evaluated RAG metrics and chat data in MongoDB Atlas with user_id.
    """
    try:
        logger.info("♻ Connecting to MongoDB Atlas...")
        client = MongoClient(get_mongo_uri())
        db = client[db_name]
        collection = db[collection_name]
        document = {
            "user_id": user_id,
            "question": question,
            "generated_answer": generated_answer,
            "retrieved_context": context,
            "faithfulness_score": metrics.get("faithfulness", 0.0),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        result = collection.insert_one(document)
        client.close()
        logger.info(f"✅ Chat and metric stored successfully. Doc ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"❌ Error while saving chat metrics to DB: {e}")

def evaluate_and_store(
    question: str,
    generated_answer: str,
    context: str,
    user_id: str
):
    """
    End-to-end evaluation and logging to DB with user_id.
    """
    logger.info("♻ Starting full RAGAS logging pipeline...")
    metrics = evaluate_rag_metrics(question, generated_answer, context)
    store_chat_metrics(question, generated_answer, context, metrics, user_id)

def get_user_chat_history(user_id: str, db_name: str = "diagnosify", collection_name: str = "chat_history") -> List[Dict]:
    """
    Retrieves chat history for a specific user from MongoDB Atlas.
    
    Args:
        user_id (str): The unique identifier for the user.
        db_name (str): Name of the MongoDB database.
        collection_name (str): Name of the MongoDB collection.
    
    Returns:
        List[Dict]: List of chat documents for the user.
    """
    try:
        logger.info(f"♻ Retrieving chat history for user_id: {user_id}")
        client = MongoClient(get_mongo_uri())
        db = client[db_name]
        collection = db[collection_name]
        chats = list(collection.find({"user_id": user_id}))
        client.close()
        logger.info(f"✅ Retrieved {len(chats)} chats for user_id: {user_id}")
        return chats
    except Exception as e:
        logger.error(f"❌ Error retrieving chat history for user_id {user_id}: {e}")
        return []

# 🧪 Example usage
if __name__ == "__main__":
    evaluate_and_store(
        question="What abnormalities are found in the report?",
        generated_answer="The report mentions increased cardiothoracic ratio and mild pleural effusion.",
        context="There is blunting of the left costophrenic angle and cardiothoracic ratio is increased.",
        user_id="test_user_123"
    )