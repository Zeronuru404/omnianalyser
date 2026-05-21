"""Document Analyzer Agent — summarize, extract, Q&A."""
from ..services.mimo_client import MiMoClient

SYSTEM = """You are a document analysis expert. Analyze the document and provide:

1. **Summary**: 3-5 sentence overview
2. **Key Points**: Bullet list of main ideas (5-8 points)
3. **Entities**: Names, dates, numbers, organizations mentioned
4. **Sentiment**: Overall tone (positive/negative/neutral) with confidence
5. **Questions**: 3 insightful questions someone might ask about this document

Respond in structured markdown."""


class DocAnalyzer:
    """Analyzes text documents — summarize, extract key points, detect sentiment."""

    def __init__(self, client: MiMoClient):
        self.client = client
        self.name = "doc_analyzer"

    async def analyze(self, content: str, filename: str) -> dict:
        prompt = f"Document: {filename}\n\n{content[:8000]}"
        result = await self.client.analyze(SYSTEM, prompt)
        return {
            "agent": self.name,
            "filename": filename,
            "analysis": result["content"],
            "tokens_used": result["tokens_used"],
            "model": result["model"],
        }
