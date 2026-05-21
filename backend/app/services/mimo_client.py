"""MiMo API client for multi-model inference."""
import httpx


class MiMoClient:
    """Unified client for MiMo V2.5 series models."""

    def __init__(self, api_key: str, base_url: str, model: str, vl_model: str = "mimo-v2.5-vl"):
        self.model = model
        self.vl_model = vl_model
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=120.0,
        )

    async def analyze(self, system: str, prompt: str) -> dict:
        """Send analysis prompt to MiMo V2.5-Pro."""
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
        resp = await self._client.post("/chat/completions", json={
            "model": self.model, "messages": messages
        })
        resp.raise_for_status()
        data = resp.json()
        usage = data.get("usage", {})
        return {
            "content": data["choices"][0]["message"]["content"],
            "tokens_used": usage.get("total_tokens", 0),
            "model": self.model,
        }

    async def analyze_vision(self, system: str, prompt: str, image_url: str) -> dict:
        """Send image analysis to MiMo V2.5-VL."""
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]},
        ]
        resp = await self._client.post("/chat/completions", json={
            "model": self.vl_model, "messages": messages
        })
        resp.raise_for_status()
        data = resp.json()
        usage = data.get("usage", {})
        return {
            "content": data["choices"][0]["message"]["content"],
            "tokens_used": usage.get("total_tokens", 0),
            "model": self.vl_model,
        }

    async def close(self):
        await self._client.aclose()
