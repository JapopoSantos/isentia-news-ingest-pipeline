from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

from pydantic import BaseModel, Field


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Article(BaseModel):
    article_id: str
    source_name: str
    title: str
    content: str
    url: str
    author: str = ""
    published_at: str
    ingested_at: str = Field(default_factory=_utc_now_iso)

    @classmethod
    def from_newsapi(cls, raw: Dict[str, Any], *, max_content_chars: int = 50_000) -> "Article":
        source = raw.get("source") or {}
        source_name = (source.get("name") or "").strip()

        title = (raw.get("title") or "").strip()
        url = (raw.get("url") or "").strip()
        author = (raw.get("author") or "").strip()
        published_at = (raw.get("publishedAt") or "").strip()

        content = (raw.get("content") or "").strip()
        if len(content) > max_content_chars:
            content = content[:max_content_chars]

        if not published_at:
            published_at = _utc_now_iso()

        article_id = str(uuid4())

        return cls(
            article_id=article_id,
            source_name=source_name,
            title=title,
            content=content,
            url=url,
            author=author,
            published_at=published_at,
        )