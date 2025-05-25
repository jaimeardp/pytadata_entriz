import boto3
import pandas as pd
from pathlib import Path
import sys
from moto import mock_aws  # Changed this line

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pytadata_entriz.providers import aws as backend  # Ensure this is correctly located


def test_aws_write_roundtrip(tmp_path):
    df = pd.DataFrame({"a": [1]})
    with mock_aws():  # Changed this line
        # It's good practice to specify the region when creating clients,
        # even with moto, to mirror real AWS behavior.
        s3_client = boto3.client(
            "s3", region_name="us-east-1"
        )  # Or your preferred region
        s3_client.create_bucket(Bucket="bucket-name")
        # If your 'backend.write' uses its own boto3 client, ensure it's created *inside* the mock_aws context.
        backend.write(
            df,
            dest="s3://bucket-name/x/",
            mode="overwrite",
            partition_cols=None,
            dtype=None,
        )
