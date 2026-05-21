"""Data Analyzer Agent — statistics, anomalies, insights."""
from ..services.mimo_client import MiMoClient

SYSTEM = """You are a data analysis expert. Analyze the dataset and provide:

1. **Overview**: Row count, column count, data types
2. **Statistics**: Key metrics (mean, median, min, max for numeric columns)
3. **Patterns**: Notable trends, correlations, distributions
4. **Anomalies**: Outliers, missing data, suspicious values
5. **Insights**: 3-5 actionable insights from this data
6. **Visualization**: Suggest 2-3 chart types that would best represent this data

Respond in structured markdown."""


class DataAnalyzer:
    """Analyzes CSV/JSON data — statistics, anomalies, visualization suggestions."""

    def __init__(self, client: MiMoClient):
        self.client = client
        self.name = "data_analyzer"

    async def analyze(self, content: str, filename: str) -> dict:
        prompt = f"Data file: {filename}\n\n{content[:8000]}"
        result = await self.client.analyze(SYSTEM, prompt)
        return {
            "agent": self.name,
            "filename": filename,
            "analysis": result["content"],
            "tokens_used": result["tokens_used"],
            "model": result["model"],
        }
