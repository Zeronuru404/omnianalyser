"""Image Analyzer Agent — describe, OCR, detect objects."""
from ..services.mimo_client import MiMoClient

SYSTEM = """You are an image analysis expert. Analyze the image and provide:

1. **Description**: Detailed description of what's in the image
2. **Text Detection**: Any text visible in the image (OCR)
3. **Objects**: List of objects/people/scenes detected
4. **Context**: What this image might be about (business, technical, personal)
5. **Suggestions**: How this image could be used or improved

Respond in structured markdown."""


class ImageAnalyzer:
    """Analyzes images — describe, OCR, object detection."""

    def __init__(self, client: MiMoClient):
        self.client = client
        self.name = "image_analyzer"

    async def analyze(self, image_url: str, filename: str) -> dict:
        prompt = f"Analyze this image: {filename}"
        result = await self.client.analyze_vision(SYSTEM, prompt, image_url)
        return {
            "agent": self.name,
            "filename": filename,
            "analysis": result["content"],
            "tokens_used": result["tokens_used"],
            "model": result["model"],
        }
