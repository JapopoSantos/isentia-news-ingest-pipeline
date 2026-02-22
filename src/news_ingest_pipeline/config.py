import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self) -> None:
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.newsapi_query = os.getenv("NEWSAPI_QUERY")
        self.aws_region = os.getenv("AWS_REGION")
        self.kinesis_stream_name = os.getenv("KINESIS_STREAM_NAME")

        self.newsapi_base_url = os.getenv(
            "NEWSAPI_BASE_URL",
            "https://newsapi.org/v2/everything"
        )

        self._validate()

    def _validate(self) -> None:
        missing = []

        if not self.newsapi_key:
            missing.append("NEWSAPI_KEY")
        if not self.newsapi_query:
            missing.append("NEWSAPI_QUERY")
        if not self.aws_region:
            missing.append("AWS_REGION")
        if not self.kinesis_stream_name:
            missing.append("KINESIS_STREAM_NAME")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")