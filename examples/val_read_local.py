from mardata_entryana import DataEntry
from typedframe import TypedDataFrame
import pandas as pd


class DataInput(TypedDataFrame):
    schema = {
        "customer_id": int,
        "name": str,
        "dni": int,
        "email": str,
        "phone": str,
        # "code": str,
    }

    optional = {
        "code": str,
    }


def add_ingestion_timestamp(
    df: pd.DataFrame, contract_dataset: TypedDataFrame = None
) -> pd.DataFrame:
    """
    Add ingestion timestamp to the DataFrame.
    """
    df["ingestion_timestamp"] = pd.Timestamp.now()

    return df


de_etl = DataEntry(provider="local", config={"contract_definition": DataInput})

df = de_etl.read(
    ".\\local\\data\\customer.csv",
    validation=True,
    header=True,
    post_transformations=[add_ingestion_timestamp],
)

print(df.head())

report_df = de_etl.validate(df, schema_csv_path="./local/schema.csv", validation=True)

print(report_df.head())

de_etl.write(
    df, dest="./local/output/customer_out.parquet.snappy", mode="overwrite", header=True
)

print(df.head())
