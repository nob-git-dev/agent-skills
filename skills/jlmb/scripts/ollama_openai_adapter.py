#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["fastapi", "uvicorn", "httpx"]
# ///
"""
Ollama API -> OpenAI Chat Completions adapter.

shi3z/japanese-llm-benchmark は Ollama の /api/generate を直叩きするため、
vLLM / llama.cpp / その他の OpenAI 互換サーバーを使いたい場合に
このプロキシを経由させる。

起動例:
    uv run scripts/ollama_openai_adapter.py \\
        --upstream http://127.0.0.1:8000/v1 \\
        --model example-model \\
        --port 11500

ベンチマーク側:
    python benchmark.py --host localhost:11500 --models example-model
"""
import argparse
import json
import os
import time

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse  # noqa: F401
import uvicorn


def make_app(
    upstream: str,
    default_model: str,
    api_key: str | None,
    disable_thinking: bool,
    extra_chat_template_kwargs: dict | None,
) -> FastAPI:
    app = FastAPI()
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    def _build_oai_body(model: str, messages: list, opts: dict) -> dict:
        body = {
            "model": model,
            "messages": messages,
            "stream": False,
            "temperature": opts.get("temperature", 0.3),
            "max_tokens": opts.get("num_predict", 2048),
        }
        ctk = dict(extra_chat_template_kwargs or {})
        if disable_thinking:
            ctk["enable_thinking"] = False
        if ctk:
            body["chat_template_kwargs"] = ctk
        return body

    def _extract_content_and_reasoning(msg: dict) -> tuple[str, str]:
        content = msg.get("content") or ""
        # vLLM puts thinking in `reasoning`; some servers use `reasoning_content`
        reasoning = msg.get("reasoning") or msg.get("reasoning_content") or ""
        # llama.cpp / DeepSeek often inline <think>...</think> inside content
        if "<think>" in content and "</think>" in content:
            import re as _re
            think_blocks = _re.findall(r"<think>(.*?)</think>", content, _re.DOTALL)
            if think_blocks and not reasoning:
                reasoning = "\n".join(think_blocks)
            content = _re.sub(r"<think>.*?</think>", "", content, flags=_re.DOTALL).strip()
        return content, reasoning

    @app.get("/api/tags")
    async def tags():
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{upstream}/models", headers=headers)
            r.raise_for_status()
            data = r.json()
        models = [{"name": m["id"], "model": m["id"]} for m in data.get("data", [])]
        return {"models": models}

    @app.post("/api/generate")
    async def generate(req: Request):
        body = await req.json()
        model = body.get("model") or default_model
        prompt = body.get("prompt", "")
        opts = body.get("options", {}) or {}

        oai_body = _build_oai_body(model, [{"role": "user", "content": prompt}], opts)

        start = time.time()
        async with httpx.AsyncClient(timeout=3600) as c:
            r = await c.post(f"{upstream}/chat/completions", headers=headers, json=oai_body)
            r.raise_for_status()
            data = r.json()
        elapsed = time.time() - start

        msg = (data.get("choices") or [{}])[0].get("message", {}) or {}
        content, reasoning = _extract_content_and_reasoning(msg)
        usage = data.get("usage", {}) or {}
        completion_tokens = usage.get("completion_tokens", len(content))

        return JSONResponse({
            "model": model,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "response": content,
            "thinking": reasoning,
            "done": True,
            "eval_count": completion_tokens,
            "eval_duration": int(elapsed * 1e9),
        })

    @app.post("/api/chat")
    async def chat(req: Request):
        body = await req.json()
        model = body.get("model") or default_model
        messages = body.get("messages", [])
        opts = body.get("options", {}) or {}

        oai_body = _build_oai_body(model, messages, opts)

        start = time.time()
        async with httpx.AsyncClient(timeout=3600) as c:
            r = await c.post(f"{upstream}/chat/completions", headers=headers, json=oai_body)
            r.raise_for_status()
            data = r.json()
        elapsed = time.time() - start

        msg = (data.get("choices") or [{}])[0].get("message", {}) or {}
        content, _ = _extract_content_and_reasoning(msg)
        usage = data.get("usage", {}) or {}
        completion_tokens = usage.get("completion_tokens", len(content))

        return JSONResponse({
            "model": model,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "message": {"role": "assistant", "content": content},
            "done": True,
            "eval_count": completion_tokens,
            "eval_duration": int(elapsed * 1e9),
        })

    @app.post("/completion")
    async def llamacpp_completion(req: Request):
        """llama.cpp 互換の /completion エンドポイント。

        shi3z/benchmark.py は :11434 以外のポートを llama.cpp と判定して
        この形式を叩いてくる。プロンプトは DeepSeek-V4 のチャットトークンで
        ラップされているので、それを剥がしてから OpenAI chat completions に
        変換して上流に投げる。
        """
        import re as _re
        body = await req.json()
        raw_prompt = body.get("prompt", "")
        n_predict = body.get("n_predict", 2048)
        temperature = body.get("temperature", 0.3)
        stream = body.get("stream", False)

        # DeepSeek-V4 ラッパーを剥がす: <｜begin▁of▁sentence｜><｜User｜>...<｜Assistant｜></think>
        user_text = raw_prompt
        m = _re.search(r"<｜User｜>(.*?)<｜Assistant｜>", raw_prompt, _re.DOTALL)
        if m:
            user_text = m.group(1).strip()
        else:
            # 他のラッパー（例: <|im_start|>user ... <|im_end|>）にもざっくり対応
            m2 = _re.search(r"<\|im_start\|>user\s*(.*?)<\|im_end\|>", raw_prompt, _re.DOTALL)
            if m2:
                user_text = m2.group(1).strip()

        oai_body = _build_oai_body(
            default_model,
            [{"role": "user", "content": user_text}],
            {"num_predict": n_predict, "temperature": temperature},
        )
        # stream は今のところ非対応。stream=True で来ても非ストリームで返す。
        oai_body["stream"] = False

        start = time.time()
        async with httpx.AsyncClient(timeout=3600) as c:
            r = await c.post(f"{upstream}/chat/completions", headers=headers, json=oai_body)
            r.raise_for_status()
            data = r.json()
        elapsed = time.time() - start

        msg = (data.get("choices") or [{}])[0].get("message", {}) or {}
        content, _ = _extract_content_and_reasoning(msg)
        usage = data.get("usage", {}) or {}
        completion_tokens = usage.get("completion_tokens", len(content))

        if stream:
            # 簡易ストリーム: 1チャンクで全文を返す（benchmark.py は非ストリーム想定だが、
            # coding_benchmark.py がストリーミング消費するため SSE 形式で1回だけ吐く）
            async def gen():
                payload = json.dumps({
                    "content": content,
                    "tokens_predicted": completion_tokens,
                    "stop": True,
                })
                yield f"data: {payload}\n\n"
            return StreamingResponse(gen(), media_type="text/event-stream")

        return JSONResponse({
            "content": content,
            "tokens_predicted": completion_tokens,
            "stop": True,
            "generation_settings": {"n_predict": n_predict, "temperature": temperature},
            "timings": {"predicted_ms": int(elapsed * 1000)},
        })

    @app.get("/api/ps")
    async def ps():
        return {"models": [{"name": default_model, "model": default_model}]}

    @app.get("/health")
    async def health():
        return {"status": "ok", "upstream": upstream, "default_model": default_model}

    return app


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", required=True,
                    help="OpenAI 互換エンドポイントの /v1 まで (例: http://127.0.0.1:8000/v1)")
    ap.add_argument("--model", required=True, help="デフォルトで使うモデル名 (served-model-name)")
    ap.add_argument(
        "--bind",
        default="127.0.0.1",
        help="Listen address; keep loopback unless remote access is explicitly secured",
    )
    ap.add_argument("--port", type=int, default=11500)
    ap.add_argument(
        "--api-key-env",
        default="OPENAI_API_KEY",
        help="上流APIキーを読む環境変数名。不要なら空文字を指定する",
    )
    ap.add_argument("--disable-thinking", action="store_true",
                    help="chat_template_kwargs={enable_thinking:false} を常に渡す (Qwen3系の thinking 抑止)")
    ap.add_argument("--chat-template-kwargs", default=None,
                    help='JSON 文字列で chat_template_kwargs を上書き (例: \'{"enable_thinking":false}\')')
    args = ap.parse_args()

    extra_ctk = json.loads(args.chat_template_kwargs) if args.chat_template_kwargs else None
    api_key = os.environ.get(args.api_key_env) if args.api_key_env else None

    app = make_app(
        args.upstream.rstrip("/"),
        args.model,
        api_key,
        args.disable_thinking,
        extra_ctk,
    )
    uvicorn.run(app, host=args.bind, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
