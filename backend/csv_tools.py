#csv_tool.py
import pandas as pd
import io
from typing import Optional
 
 
class CSVManager:
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.filename: str = ""
 
    def load_csv(self, content: bytes, filename: str) -> str:
        self.df = pd.read_csv(io.BytesIO(content))
        self.filename = filename
        return self.get_info()
 
    def get_info(self) -> str:
        if self.df is None:
            return "No CSV file has been loaded yet."
 
        info = [
            f"Dataset: {self.filename}",
            f"Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns",
            f"Columns: {list(self.df.columns)}",
            "\nData Types:\n" + str(self.df.dtypes),
            "\nMissing Values:\n" + str(self.df.isnull().sum()),
            "\nFirst 3 rows:\n" + self.df.head(3).to_string()
        ]
        return "\n".join(info)
 
    def describe(self) -> str:
        if self.df is None:
            return "No CSV file has been loaded yet."
        return self.df.describe(include="all").to_string()
 
    def query(self, expression: str) -> str:
        """
        Run a simple pandas expression.
        Example: df[df['Survived'] == 1]['Age'].mean()
        """
        if self.df is None:
            return "No CSV file has been loaded yet."
 
        try:
            local_dict = {"df": self.df, "pd": pd}
            result = eval(expression, {"__builtins__": {}}, local_dict)
            return str(result)
        except Exception as e:
            return f"Error while running query: {str(e)}"