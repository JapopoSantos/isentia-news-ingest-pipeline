News Ingest Pipeline

Overview
This project implements a simple news ingestion pipeline.

It pulls articles from the NewsAPI Everything endpoint on a fixed interval.
It transforms and validates each article.
It sends each article as a JSON record to an AWS Kinesis Data Stream.

The goal is to produce a working, minimal, production-style pipeline that demonstrates API integration, data transformation, and Kinesis streaming.

Architecture
	1.	NewsAPI Everything endpoint
	2.	Python ingestion service
	3.	AWS Kinesis Data Stream

Flow:

Poll NewsAPI → Normalize article → Generate article_id → Send to Kinesis → Repeat

Output Schema

Each article sent to Kinesis has the following structure:

{
“article_id”: “sha256(url + published_at)”,
“source_name”: “Reuters”,
“title”: “Example headline”,
“content”: “Cleaned article content”,
“url”: “https://example.com/news/article”,
“author”: “John Doe”,
“published_at”: “2026-02-22T01:23:45Z”,
“ingested_at”: “2026-02-22T09:15:10Z”
}

article_id is generated deterministically using SHA-256 on url + published_at to avoid duplicates.

Requirements
	•	Python 3.11 or higher
	•	AWS account
	•	AWS Kinesis Data Stream created
	•	NewsAPI API key

Project Structure

ISENTIA - NEWS INGEST PIPELINE/
README.md
requirements.txt
Dockerfile
.env.example
src/
news_ingest_pipeline/
init.py
main.py
config.py
newsapi_client.py
models.py
kinesis_writer.py
utils.py

Environment Variables

Required:

NEWSAPI_KEY=your_newsapi_key
NEWSAPI_QUERY=bitcoin
AWS_REGION=ap-southeast-1
KINESIS_STREAM_NAME=your_stream_name

Optional:

POLL_INTERVAL_SECONDS=60
NEWSAPI_PAGE_SIZE=50
NEWSAPI_LANGUAGE=en
NEWSAPI_SORT_BY=publishedAt
LOG_LEVEL=INFO

Setup Instructions
	1.	Clone repository

git clone 
cd news-ingest-pipeline
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
Export environment variables:

export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

Running the Application

Run locally:

python -m news_ingest_pipeline.main

The application will:
	•	Poll NewsAPI
	•	Transform articles
	•	Send records to Kinesis
	•	Log results
	•	Sleep for POLL_INTERVAL_SECONDS
	•	Repeat

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

Each article is sent as one JSON record using PutRecords or PutRecord.

PartitionKey uses article_id to ensure stable shard distribution.

Kinesis limits:
	•	Max record size: 1 MB
	•	Max 500 records per PutRecords call

Implementation Notes
	•	Deterministic article_id prevents duplicates.
	•	Content may be truncated to avoid size issues.
	•	Null fields are normalized.
	•	Errors from AWS are retried.
	•	Logging captures success and failure counts.

Testing Strategy

Basic validation:
	•	Confirm API fetch works.
	•	Confirm JSON transformation matches schema.
	•	Confirm records appear in Kinesis Data Viewer.

Optional unit tests can validate:
	•	article_id generation
	•	Data transformation logic

Production Considerations
	•	Add persistent checkpointing to avoid reprocessing.
	•	Add structured logging.
	•	Add metrics.
	•	Add dead-letter handling for failed records.
	•	Add CI pipeline.
