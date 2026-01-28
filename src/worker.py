import os
import json
import time
import boto3
import psycopg2
from src.config import Config
from src.extractor import Extractor


def get_sqs_client():
    return boto3.client(
        "sqs",
        endpoint_url=Config.AWS_ENDPOINT_URL,
        region_name=Config.AWS_REGION
    )


def process_message(message_body):
    """Business logic: Extract data and save to Postgres."""
    data = json.loads(message_body)
    file_key = data.get("file_key")

    # 1. Get structured data (LLM or Mock)
    extractor = Extractor()
    structured_json = extractor.process_text(f"Content of {file_key}")

    # 2. Persist to Postgres
    conn = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO extractions (file_name, results) VALUES (%s, %s)",
            (file_key, json.dumps(structured_json))
        )
        conn.commit()
    conn.close()
    print(f"Successfully processed {file_key}")


def start_worker():
    sqs = get_sqs_client()
    # Get the URL for the queue name defined in your init-aws.sh
    queue_url = sqs.get_queue_url(QueueName=Config.QUEUE_NAME)["QueueUrl"]

    print(f"Worker started. Listening to {Config.QUEUE_NAME}...")

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10  # Long polling to save money/CPU
        )

        messages = response.get("Messages", [])
        for msg in messages:
            try:
                process_message(msg["Body"])
                # IMPORTANT: Delete message only after successful processing
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
            except Exception as e:
                print(f"Error processing message: {e}")

        # Small sleep to prevent tight-looping if queue is empty
        if not messages:
            time.sleep(1)


if __name__ == "__main__":
    start_worker()