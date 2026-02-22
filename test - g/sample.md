This is what you typically receive from NewsAPI Everything endpoint.

Sample raw response from NewsAPI

{
“status”: “ok”,
“totalResults”: 2,
“articles”: [
{
“source”: {
“id”: “reuters”,
“name”: “Reuters”
},
“author”: “John Smith”,
“title”: “Bitcoin rises above $60,000”,
“description”: “Bitcoin climbed on renewed ETF optimism.”,
“url”: “https://www.reuters.com/markets/bitcoin-rises-60000”,
“urlToImage”: “https://images.reuters.com/bitcoin.jpg”,
“publishedAt”: “2026-02-22T01:23:45Z”,
“content”: “Bitcoin surged on Friday as investors reacted to fresh ETF signals…”
},
{
“source”: {
“id”: null,
“name”: “TechCrunch”
},
“author”: null,
“title”: “AI startup raises $50M”,
“description”: “Funding round led by major VC.”,
“url”: “https://techcrunch.com/2026/02/22/ai-startup-raises”,
“urlToImage”: null,
“publishedAt”: “2026-02-22T02:00:00Z”,
“content”: “An AI startup announced a $50M Series B round today…”
}
]
}

Important points:
	•	Nested source object
	•	Fields you do not need such as description and urlToImage
	•	author may be null
	•	content may contain trailing markers like “[+123 chars]”

Now this is what your pipeline should send to Kinesis.

Sample transformed output per article

Record 1

{
“article_id”: “a1c3f8d7b0e4c6f19d2e5a7b8c9d0e11223344556677889900aabbccddeeff11”,
“source_name”: “Reuters”,
“title”: “Bitcoin rises above $60,000”,
“content”: “Bitcoin surged on Friday as investors reacted to fresh ETF signals…”,
“url”: “https://www.reuters.com/markets/bitcoin-rises-60000”,
“author”: “John Smith”,
“published_at”: “2026-02-22T01:23:45Z”,
“ingested_at”: “2026-02-22T09:15:10Z”
}

Record 2

{
“article_id”: “bb72a5e0f9d3c4b1e6a8f0d1c2b3a49876543210ffeeddccbbaa998877665544”,
“source_name”: “TechCrunch”,
“title”: “AI startup raises $50M”,
“content”: “An AI startup announced a $50M Series B round today…”,
“url”: “https://techcrunch.com/2026/02/22/ai-startup-raises”,
“author”: “”,
“published_at”: “2026-02-22T02:00:00Z”,
“ingested_at”: “2026-02-22T09:15:10Z”
}

What changed from before to after
	1.	source.name → source_name
You flatten the nested structure.
	2.	Remove unused fields
description and urlToImage are removed.
	3.	Normalize null values
author null becomes empty string.
	4.	Add article_id
Deterministic hash of url + publishedAt.
Example logic:
sha256(url + publishedAt)
	5.	Add ingested_at
Current UTC timestamp when your pipeline processed the article.
	6.	Keep consistent naming
publishedAt → published_at
	7.	One Kinesis record per article
You send each transformed JSON as one record.