News Ingest Pipeline

Overview
This project implements a news ingestion pipeline.

It pulls articles from the NewsAPI Everything endpoint.
It transforms and validates each article.
It sends each article as a JSON record to an AWS Kinesis Data Stream.

The goal is to produce a working, minimal pipeline that demonstrates API integration, data transformation, and Kinesis streaming.

Architecture
	1.	NewsAPI Everything endpoint
	2.	Python ingestion service
	3.	AWS Kinesis Data Stream

Flow
Poll NewsAPI -> Normalize article -> Generate article_id -> Send to Kinesis

Normalization and Cleaning Applied
- Converts null or missing fields to empty strings.
- Trims leading and trailing whitespace from all text fields.
- Ensures published_at always has a valid ISO 8601 UTC timestamp.
- Truncates content to a maximum configured length to prevent oversized records.
- Generates a unique article_id using uuid4().

Output Schema
Each article sent to Kinesis has the following structure:

{
“article_id”: “3f8e5c2a-7b91-4d8a-a2f3-5c0b7e6f9d12”,
“source_name”: “Gizmodo.com”,
“title”: “Major Bitcoin Miner Sells $305 Million Worth of Crypto to Fund Pivot to AI”,
“content”: “Over the weekend, bitcoin miner Cango sold 4,451 bitcoin for around $305 million…”,
“url”: “https://gizmodo.com/major-bitcoin-miner-sells-305-million-worth-of-crypto-to-fund-pivot-to-ai-2000720078”,
“author”: “Kyle Torpey”,
“published_at”: “2026-02-10T16:10:27Z”,
“ingested_at”: “2026-02-22T22:15:10Z”
}

article_id is generated using uuid4().
It is a random 128-bit UUID displayed as 36 characters including hyphens.

Requirements
	•	Python 3.9 or higher
	•	AWS account
	•	AWS Kinesis Data Stream created
	•	NewsAPI API key

Project Structure
isentia-news-ingest-pipeline/
README.md
requirements.txt
Dockerfile
.env
src/
news_ingest_pipeline/
init.py
main.py
config.py
newsapi_client.py
models.py
kinesis_writer.py

Environment Variables
Required:
NEWSAPI_KEY=your_newsapi_key
NEWSAPI_QUERY=bitcoin
AWS_REGION=ap-southeast-1
KINESIS_STREAM_NAME=your_stream_name

Setup Instructions
1.	Clone repository
git clone <repo_url>
cd isentia-news-ingest-pipeline

2.	Create virtual environment
python3 -m venv venv
source venv/bin/activate

3.	Install dependencies
pip install -r requirements.txt

4.	Configure environment
Create a .env file in the root directory and add required variables.
	
5.	Configure AWS credentials

Option 1
aws configure

Option 2
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

Running the Application
Because the project uses the src layout, set PYTHONPATH before running:

export PYTHONPATH=src
python3 -m news_ingest_pipeline.main

The application will:
	•	Fetch articles from NewsAPI
	•	Transform and normalize fields
	•	Generate a UUID article_id
	•	Send records to Kinesis
	•	Log results

Docker Usage
Build image:
docker build -t news-ingest-pipeline .

Run container:
docker run –rm 
-e NEWSAPI_KEY=your_key 
-e NEWSAPI_QUERY=bitcoin 
-e AWS_REGION=ap-southeast-1 
-e KINESIS_STREAM_NAME=your_stream 
-e AWS_ACCESS_KEY_ID=your_key 
-e AWS_SECRET_ACCESS_KEY=your_secret 
news-ingest-pipeline

Kinesis Integration
The application uses boto3 to send records to AWS Kinesis.

Each article is sent as one JSON record using PutRecord or PutRecords.
PartitionKey uses article_id.

Kinesis limits:
	•	Max record size: 1 MB
	•	Max 500 records per PutRecords call

Implementation Notes
	•	article_id is randomly generated using uuid4().
	•	Content is truncated if it exceeds the configured maximum length.
	•	Null fields are normalized to safe defaults.
	•	Pydantic validates the article schema.

Testing Strategy
Basic validation:
	•	Confirm API fetch works.
	•	Confirm JSON transformation matches required schema.
	•	Confirm records appear in Kinesis Data Viewer.

Production Considerations
	•	Add checkpointing to avoid reprocessing.
	•	Add structured logging.
	•	Add retry logic with backoff.
	•	Add metrics and monitoring.
	•	Add CI pipeline.