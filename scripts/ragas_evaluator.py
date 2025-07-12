from ragas.metrics import faithfulness
from ragas import evaluate
from datasets import Dataset
from pymongo import MongoClient
from typing import List, Dict, Optional
from scripts.config import get_logger

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
        logger.info("Preparing dataset for RAGAS evaluation...")
        dataset = Dataset.from_dict({
            "question": [question],
            "answer": [generated_answer],
            "contexts": [[context]]  # still expects list inside dataset
        })

        logger.info("Running faithfulness evaluation...")
        result = evaluate(dataset, metrics=[faithfulness])
        metrics = result.to_pandas().to_dict("records")[0]
        logger.info(f"Evaluation complete: {metrics['faithfulness']}")
        return {"faithfulness": metrics['faithfulness']}

    except Exception as e:
        logger.error(f"Metric evaluation failed: {e}")
        return {"faithfulness": 0.0}

def store_chat_metrics(
    question: str,
    generated_answer: str,
    context: str,
    metrics: Dict[str, float],
    db_name: str = "diagnosify",
    collection_name: str = "chat_history"
):
    """
    Stores evaluated RAG metrics and chat data in MongoDB.
    """
    try:
        logger.info("Connecting to MongoDB...")
        client = MongoClient("mongodb://localhost:27017")
        db = client[db_name]
        collection = db[collection_name]

        document = {
            "question": question,
            "generated_answer": generated_answer,
            "retrieved_context": context,
            "faithfulness_score": metrics.get("faithfulness", 0.0),
        }

        result = collection.insert_one(document)
        logger.info(f"Chat and metric stored successfully. Doc ID: {result.inserted_id}")

    except Exception as e:
        logger.error(f"Error while saving chat metrics to DB: {e}")

def evaluate_and_store(
    question: str,
    generated_answer: str,
    context: str,
):
    """
    End-to-end evaluation and logging to DB.
    """
    logger.info("Starting full RAG logging pipeline...")
    metrics = evaluate_rag_metrics(question, generated_answer, context)
    store_chat_metrics(question, generated_answer, context, metrics)

# 🧪 Example usage
if __name__ == "__main__":
    evaluate_and_store(
        question="What abnormalities are found in the report?",
        generated_answer="The report mentions increased cardiothoracic ratio and mild pleural effusion.",
        context="There is blunting of the left costophrenic angle and cardiothoracic ratio is increased."
    )