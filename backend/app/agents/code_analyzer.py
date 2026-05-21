"""Code Analyzer Agent — security, style, logic, complexity."""
from ..services.mimo_client import MiMoClient

SYSTEM = """You are a senior code reviewer. Analyze the code and provide:

1. **Summary** (2-3 sentences): What this code does
2. **Security Issues**: Any vulnerabilities (SQLi, XSS, hardcoded secrets, unsafe operations)
3. **Code Quality**: Style issues, naming, dead code, complexity
4. **Logic Issues**: Edge cases, off-by-one, missing error handling
5. **Suggestions**: Concrete improvements
6. **Score**: Rate 1-10 for readability, security, maintainability

Respond in structured markdown."""


class CodeAnalyzer:
    """Analyzes source code files for security, quality, and logic."""

    def __init__(self, client: MiMoClient):
        self.client = client
        self.name = "code_analyzer"

    async def analyze(self, content: str, filename: str) -> dict:
        lang = self._detect_lang(filename)
        prompt = f"Language: {lang}\nFile: {filename}\n\n```\n{content}\n```"
        result = await self.client.analyze(SYSTEM, prompt)
        return {
            "agent": self.name,
            "filename": filename,
            "language": lang,
            "analysis": result["content"],
            "tokens_used": result["tokens_used"],
            "model": result["model"],
        }

    def _detect_lang(self, filename: str) -> str:
        ext_map = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
            ".go": "Go", ".rs": "Rust", ".java": "Java",
            ".c": "C", ".cpp": "C++", ".rb": "Ruby", ".php": "PHP",
            ".html": "HTML", ".css": "CSS",
        }
        for ext, lang in ext_map.items():
            if filename.endswith(ext):
                return lang
        return "Unknown"
