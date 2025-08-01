
import pandas as pd

def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)

def infer_schema(df: pd.DataFrame) -> dict:
    return {col: str(dtype) for col, dtype in df.dtypes.items()}
