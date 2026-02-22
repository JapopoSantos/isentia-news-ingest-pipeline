import json
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from news_ingest_pipeline.config import Config


class KinesisWriter:
    def __init__(self, config: Config) -> None:
        self.stream_name = config.kinesis_stream_name
        self.client = boto3.client("kinesis", region_name=config.aws_region)

    def send_one(self, record: Dict[str, Any], partition_key: str) -> str:
        try:
            resp = self.client.put_record(
                StreamName=self.stream_name,
                Data=json.dumps(record).encode("utf-8"),
                PartitionKey=partition_key,
            )
            return resp["SequenceNumber"]
        except (ClientError, BotoCoreError) as e:
            raise RuntimeError(f"Kinesis put_record failed: {e}") from e