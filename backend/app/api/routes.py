"""API routes for OmniAnalyser."""
import os
from fastapi import APIRouter, UploadFile, File, Request, HTTPException

router = APIRouter()


@router.post("/analyze")
async def analyze_file(file: UploadFile = File(...), request: Request = None):
    """Analyze a single uploaded file."""
    content = await file.read()
    text = content.decode("utf-8", errors="replace")
    tracker = request.app.state.token_tracker
    client = request.app.state.mimo_client

    ext = os.path.splitext(file.filename or "")[1].lower()
    image_exts = {".png", ".jpg", ".jpeg", ".webp"}

    if ext in image_exts:
        from app.agents.image_analyzer import ImageAnalyzer
        agent = ImageAnalyzer(client)
        import base64
        b64 = base64.b64encode(content).decode()
        data_url = f"data:image/{ext[1:]};base64,{b64}"
        result = await agent.analyze(data_url, file.filename)
    elif ext in {".csv", ".json"}:
        from app.agents.data_analyzer import DataAnalyzer
        result = await DataAnalyzer(client).analyze(text, file.filename)
    elif ext in {".py", ".js", ".ts", ".go", ".rs", ".java", ".c", ".cpp", ".rb", ".php", ".html", ".css"}:
        from app.agents.code_analyzer import CodeAnalyzer
        result = await CodeAnalyzer(client).analyze(text, file.filename)
    else:
        from app.agents.doc_analyzer import DocAnalyzer
        result = await DocAnalyzer(client).analyze(text, file.filename)

    tracker.log(result["agent"], result["tokens_used"], file.filename, result.get("model", ""))
    return {"status": "success", "result": result}


@router.post("/batch")
async def batch_analyze(files: list[UploadFile] = File(...), request: Request = None):
    """Analyze multiple files in parallel."""
    import asyncio
    client = request.app.state.mimo_client
    tracker = request.app.state.token_tracker

    async def process_one(file: UploadFile):
        content = await file.read()
        text = content.decode("utf-8", errors="replace")
        ext = os.path.splitext(file.filename or "")[1].lower()

        if ext in {".py", ".js", ".ts", ".go", ".rs", ".java"}:
            from app.agents.code_analyzer import CodeAnalyzer
            result = await CodeAnalyzer(client).analyze(text, file.filename)
        elif ext in {".csv", ".json"}:
            from app.agents.data_analyzer import DataAnalyzer
            result = await DataAnalyzer(client).analyze(text, file.filename)
        else:
            from app.agents.doc_analyzer import DocAnalyzer
            result = await DocAnalyzer(client).analyze(text, file.filename)

        tracker.log(result["agent"], result["tokens_used"], file.filename, result.get("model", ""))
        return result

    results = await asyncio.gather(*[process_one(f) for f in files])
    total_tokens = sum(r["tokens_used"] for r in results)
    return {"status": "success", "count": len(results), "total_tokens": total_tokens, "results": results}


@router.post("/chat")
async def chat_about_file(request: Request):
    """Ask questions about a previously analyzed file."""
    body = await request.json()
    question = body.get("question", "")
    context = body.get("context", "")
    client = request.app.state.mimo_client
    tracker = request.app.state.token_tracker

    system = "You are a helpful AI assistant. Answer questions about the given code/document/data."
    prompt = f"Context:\n{context[:6000]}\n\nQuestion: {question}"
    result = await client.analyze(system, prompt)
    tracker.log("chat", result["tokens_used"], model=result["model"])
    return {"status": "success", "answer": result["content"], "tokens_used": result["tokens_used"]}


@router.get("/stats")
async def get_stats(request: Request):
    """Get current token usage statistics."""
    return request.app.state.token_tracker.get_stats()


@router.get("/stats/history")
async def get_stats_history(request: Request):
    """Get 7-day usage history."""
    return {"history": request.app.state.token_tracker.get_history(7)}


@router.get("/stats/agents")
async def get_agent_stats(request: Request):
    """Get per-agent token breakdown."""
    return {"agents": request.app.state.token_tracker.get_agent_breakdown()}


@router.get("/health")
async def health():
    return {"status": "ok"}
