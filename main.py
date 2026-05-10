"""api-lab-deepseek-minimal

最小化体验一次 DeepSeek（或同类低成本 OpenAI-compatible）API 调用。
重点：
- 服务地址不写死，从 .env 读 DEEPSEEK_BASE_URL
- 模型名不写死，从 .env 读 DEEPSEEK_MODEL
- 这样换成其它低成本兼容服务商时，只改 .env 即可
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

PROMPT = "请解释为什么低成本模型适合做批量初稿生成。"
TIMEOUT_SECONDS = 30
MAX_TOKENS = 100


def main() -> int:
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    base_url = os.getenv("DEEPSEEK_BASE_URL", "").strip().rstrip("/")
    model = os.getenv("DEEPSEEK_MODEL", "").strip()

    missing = [k for k, v in {
        "DEEPSEEK_API_KEY": api_key,
        "DEEPSEEK_BASE_URL": base_url,
        "DEEPSEEK_MODEL": model,
    }.items() if not v]
    if missing:
        print(f"[错误] .env 缺少以下变量: {', '.join(missing)}")
        print("       请运行: cp .env.example .env，然后填好后再运行。")
        return 2

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": MAX_TOKENS,
    }

    print(f"[信息] endpoint = {url}")
    print(f"[信息] model    = {model}")
    print(f"[信息] prompt   = {PROMPT}")

    started = time.time()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        print(f"[失败] 请求超时（{TIMEOUT_SECONDS}s）。")
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"[失败] 网络请求异常: {exc}")
        return 1
    elapsed = time.time() - started

    if resp.status_code != 200:
        print(f"[失败] HTTP {resp.status_code}")
        print(f"        响应片段: {resp.text[:300]}")
        print("        常见原因: API Key 无效 / base_url 错 / 模型名错 / 余额不足。")
        return 1

    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        print("[失败] 响应结构不符合 OpenAI-compatible /chat/completions 预期。")
        print(f"        原始响应片段: {resp.text[:300]}")
        return 1

    print()
    print("[成功] 模型返回内容：")
    print(content)
    print()
    print(f"[信息] 耗时 {elapsed:.2f}s")

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    result = {
        "provider": "deepseek-or-compatible",
        "base_url": base_url,
        "model": model,
        "prompt": PROMPT,
        "elapsed_seconds": round(elapsed, 3),
        "content": content,
    }
    out_file = out_dir / "result.json"
    out_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[信息] 已写入 {out_file}（不会被 git 提交）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
