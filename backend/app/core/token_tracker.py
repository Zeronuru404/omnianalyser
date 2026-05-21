"""Real-time token usage tracking."""
import time
from collections import defaultdict
from datetime import datetime, timedelta


class TokenTracker:
    """Tracks token consumption per agent, per file, per day."""

    def __init__(self):
        self._daily_usage: dict[str, int] = defaultdict(int)
        self._agent_usage: dict[str, int] = defaultdict(int)
        self._file_usage: list[dict] = []
        self._call_count: int = 0
        self._start_time: float = time.time()

    def log(self, agent: str, tokens: int, filename: str = "", model: str = ""):
        """Log a token usage event."""
        today = datetime.now().strftime("%Y-%m-%d")
        self._daily_usage[today] += tokens
        self._agent_usage[agent] += tokens
        self._call_count += 1
        self._file_usage.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "tokens": tokens,
            "filename": filename,
            "model": model,
        })

    def get_today(self) -> int:
        today = datetime.now().strftime("%Y-%m-%d")
        return self._daily_usage.get(today, 0)

    def get_stats(self) -> dict:
        uptime_min = int((time.time() - self._start_time) / 60)
        return {
            "tokens_today": self.get_today(),
            "total_calls": self._call_count,
            "uptime_minutes": uptime_min,
            "per_agent": dict(self._agent_usage),
            "recent_files": self._file_usage[-10:],
        }

    def get_history(self, days: int = 7) -> list[dict]:
        """Get daily usage for the last N days."""
        history = []
        for i in range(days):
            day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            history.append({"date": day, "tokens": self._daily_usage.get(day, 0)})
        return list(reversed(history))

    def get_agent_breakdown(self) -> dict:
        return dict(self._agent_usage)
