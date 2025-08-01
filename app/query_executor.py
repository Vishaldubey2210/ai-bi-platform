
import sqlite3
import pandas as pd

def run_sql_on_csv(df: pd.DataFrame, sql_query: str) -> pd.DataFrame or str:
    try:
        conn = sqlite3.connect(":memory:")
        df.to_sql("data", conn, index=False, if_exists="replace")

        result_df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return result_df
    except Exception as e:
        return f"⚠️ SQL Execution Error: {str(e)}"
