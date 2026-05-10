# api-lab-deepseek-minimal

> 最小化体验：用 DeepSeek（或同类低成本 OpenAI-compatible 服务）调一次聊天 API。

> 想"通过实操验证理解"而不是"只把代码跑通"？请先翻 [`LEARNING.md`](./LEARNING.md)：
> 里面有 **学习目标 / 实操验证清单 / 自检题 / 跟其它仓库的连接**。本 README 主要负责"具体怎么跑"。

## 它在做什么 / 为什么单独做这一仓

DeepSeek 这类「低成本 OpenAI-compatible」模型，调用方式跟 OpenAI 几乎一样。
本仓库的关注点不是「能不能调通」，而是让你思考：

- **为什么有便宜的模型？**
  - 部分原因：参数量较小、专为中文/通用任务训练、推理基础设施更省。
- **它适合做什么？**
  - 高频、低成本、可容忍返工的任务，例如：
    - 批量生成初稿
    - 海量摘要
    - 大规模 ETL 中的文本清洗 / 分类
    - 给"昂贵模型"省成本的预筛选
- **它不适合做什么？**
  - 长上下文、强推理、高准确度的关键场景（例如代码评审、合规审查）

## 关键约定

- **服务地址不写死**：`DEEPSEEK_BASE_URL` 从 `.env` 读，能切到任意低成本兼容供应商
- **模型名不写死**：`DEEPSEEK_MODEL` 从 `.env` 读，避免我编造你账户里不存在的模型名

## 运行步骤

```bash
cd api-lab-deepseek-minimal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 编辑 .env，例如：
#   DEEPSEEK_API_KEY=sk-...
#   DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
#   DEEPSEEK_MODEL=deepseek-chat

python3 main.py
cat output/result.json
```

## 常见报错

| 终端打印 | 可能原因 | 怎么处理 |
| --- | --- | --- |
| `.env 缺少以下变量` | 三件套没填全 | 全填好再跑 |
| `HTTP 401` | key 错 | 重新生成 |
| `HTTP 402` / 余额不足 | 账户没钱 | 充值或换服务商 |
| `HTTP 404` | base_url 或 model 错 | 看官方文档纠正 |
| `响应结构不符合 OpenAI-compatible` | 这家服务商其实不兼容 | 换 Anthropic / Gemini 仓库 |

## .env.example

```
DEEPSEEK_API_KEY=填入你的API Key
DEEPSEEK_BASE_URL=填入服务商提供的base_url
DEEPSEEK_MODEL=填入模型名
```

## 不会做的事

- 不会自动重试
- 不会打印 API Key
- 不会硬编码服务地址
