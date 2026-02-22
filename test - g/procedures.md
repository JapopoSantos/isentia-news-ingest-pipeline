Step by step procedure to build it (simplest working path)

Step 1. Create the repo and structure
	1.	Create a new git repo folder.
	2.	Create the folder structure shown above.
	3.	Add README.md, requirements.txt, Dockerfile, and .env.example.

Step 2. Create AWS Kinesis stream
	1.	In AWS console, open Kinesis Data Streams.
	2.	Create a stream, for example: aurora-news
	3.	Choose on-demand capacity for simplest setup, or provisioned with 1 shard.
	4.	Note the AWS region and stream name. You will use both in env vars.

Step 3. Get NewsAPI key and define your query
	1.	Create a NewsAPI account and get an API key.
	2.	Decide your initial query string, for example: “finance OR markets” or “bitcoin”.

Step 4. Implement config loading
	1.	In config.py, load env vars (python-dotenv for local).
	2.	Validate required vars exist. Fail fast with a clear error.

Step 5. Implement NewsAPI fetch
	1.	In newsapi_client.py, call the Everything endpoint with:
	•	q (query)
	•	language
	•	sortBy
	•	pageSize
	2.	Handle HTTP errors and NewsAPI error payloads.
	3.	Keep the last seen publishedAt or a rolling time window, so you do not re-pull too much.

Step 6. Implement schema and cleaning
	1.	In models.py define an Article model with the required fields.
	2.	Normalize:
	•	source_name from source.name
	•	url from url
	•	published_at to ISO string
	•	ingested_at as now UTC ISO string
	3.	Generate article_id:
	•	sha256(url + published_at) is simple and stable.
	4.	Truncate content if huge.

Step 7. Implement Kinesis writer
	1.	In kinesis_writer.py create a boto3 Kinesis client.
	2.	Send records using PutRecords in batches (up to 500).
	3.	Use PartitionKey:
	•	article_id is simplest, or source_name.
	4.	Add retry with tenacity for transient AWS errors.

Step 8. Implement main polling loop
	1.	In main.py:
	•	load config
	•	loop forever:
	•	fetch articles
	•	transform and validate
	•	write to Kinesis
	•	sleep POLL_INTERVAL_SECONDS
	2.	Log counts: fetched, valid, sent, failed.
	3.	Keep a small in-memory set of article_ids seen in this run to reduce duplicates.

Step 9. Add Dockerfile
	1.	Use python:3.11-slim or python:3.12-slim.
	2.	Copy requirements.txt, install, copy src, set PYTHONPATH, run module.

Step 10. Quick verification
Local smoke test
	1.	Export env vars or use .env.
	2.	Run the script.
	3.	Confirm logs show successful PutRecords.

Kinesis verification
	1.	In AWS console, open your stream.
	2.	Use Data Viewer in console, or a small consumer script, to confirm records arrive and look correct JSON.

Docker smoke test
	1.	Build image.
	2.	Run container with env vars.
	3.	Confirm logs show successful sends.

What is the output goal (high level sample)

Each article becomes one JSON record written to Kinesis. Example:

{
“article_id”: “8b1f2d1f9d3a6b7f3b0d8d7c4c2d3b0f6a9e1c2b3d4e5f60718293a4b5c6d”,
“source_name”: “Reuters”,
“title”: “Example headline”,
“content”: “Cleaned article content text. Possibly truncated.”,
“url”: “https://example.com/news/article”,
“author”: “Jane Doe”,
“published_at”: “2026-02-22T01:23:45Z”,
“ingested_at”: “2026-02-22T09:10:00Z”
}
