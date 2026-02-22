import requests
from typing import Any, Dict, List

from news_ingest_pipeline.config import Config

def fetch_articles(config: Config, page_size: int = 100) -> List[Dict[str, Any]]:
    params = {
        "q": config.newsapi_query,
        "apiKey": config.newsapi_key,
        "pageSize": page_size
    }

    resp = requests.get(config.newsapi_base_url, params=params, timeout=15)

    if resp.status_code != 200:
        raise RuntimeError(f"NewsAPI request failed: {resp.status_code} {resp.text}")

    payload = resp.json()
    print("totalResults:", payload.get("totalResults"))
    print("articles returned:", len(payload.get("articles", [])))

    if payload.get("status") != "ok":
        raise RuntimeError(f"NewsAPI returned error payload: {payload}")

    return payload.get("articles", [])