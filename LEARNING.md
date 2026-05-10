# LEARNING — api-lab-deepseek-minimal

> 这份文件回答：「我跑完这个仓库，应该真的学到什么？」

## 你跑完应该能回答的问题

1. 「低成本 OpenAI-compatible 模型」是怎么把价格压下来的？（参数量、推理基础设施、目标场景）
2. 哪些任务**适合**便宜模型？哪些任务**不要**省这点钱？
3. 同一份 prompt，便宜模型和昂贵模型的回答差距大吗？差距体现在哪？
4. 为什么我应该把 `DEEPSEEK_BASE_URL` 也作为变量从 `.env` 读取，而不是写死？

## 实操验证清单（务必动手）

### 阶段 A — 环境就绪
- [ ] `cp .env.example .env`
- [ ] `pip install -r requirements.txt`
- [ ] 在 DeepSeek 控制台拿 `sk-...` key（或换其它低成本兼容服务商）
- [ ] `.env` 三件套：`DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL`

### 阶段 B — 跑通最小调用
- [ ] `python3 main.py` → 看到中文回答
- [ ] `cat output/result.json`

### 阶段 C — 价值实验：同 prompt 跨模型横向对比
DeepSeek 仓库的精髓**不是"它能跑通"**，而是 **"和别人一比，差距/优势在哪"**。

- [ ] 用本仓库跑通后，把 `output/result.json` 重命名为 `output/run-deepseek.json`
- [ ] 把同一份 prompt（`请解释为什么低成本模型适合做批量初稿生成。`）拿到 `api-lab-openrouter-minimal` 也跑一次，模型选 `openai/gpt-4o`（更贵的）
- [ ] 重命名为 `output/run-gpt4o.json`
- [ ] 对比这两个 result.json 的 `content` 字段：
  - 长度差多少？
  - 论点结构差多少？
  - 有没有错别字、自相矛盾？
- [ ] 这种对比 **不需要**"基准跑分"——你的肉眼就是最重要的评估器

### 阶段 D — 价格直觉建立
- [ ] 去 DeepSeek 官网定价页看一眼输入/输出每 1M token 的价格
- [ ] 去 OpenAI 官网定价页看一眼 GPT-4o 的价格
- [ ] 算一下：你刚才那次调用，分别值多少钱？(`prompt_tokens × 输入价` + `completion_tokens × 输出价`)
- [ ] 把这个数字记在脑子里——以后你设计批量任务时会本能地避免烧钱

## 自检题

1. 如果某天 DeepSeek 把 `base_url` 改成 `https://api.deepseek.com/v2`（变了一下版本），本仓库的代码需要改吗？需要改几行？
2. 我能不能用本仓库的 `main.py` 去打**任意一家**便宜的 OpenAI-compatible 服务（比如智谱、月之暗面的兼容入口）？需要做什么准备？
3. "便宜模型适合批量初稿"——具体到你自己的任务，比如**给 1000 篇短文生成中文摘要**，你会全部用便宜模型，还是先用便宜模型过一遍、再用昂贵模型挑出有问题的复审？
4. 如果一个便宜模型在你的 prompt 上表现"突然变差"，可能的原因有哪些？（提示：模型版本悄悄换了、token 上限变了、限流降级了……）

## 与其它仓库的连接

| 关系 | 仓库 | 为什么去看 |
| --- | --- | --- |
| **同协议、不同价位** | `api-lab-openrouter-minimal` | 用 OpenRouter 找一个贵模型（如 GPT-4o）做"豪华对照" |
| **同协议、不同卖点** | `api-lab-groq-minimal` | DeepSeek 卖"便宜"，Groq 卖"快"——同样的协议，不同的优化方向 |
| **本地化思考** | `api-lab-ollama-local-minimal` | 本地小模型理论上"零边际成本"，但运维成本高——再多一个维度对比 |

## 你应该感受到的"啊哈"瞬间

- 当你**亲眼看到**便宜模型和昂贵模型在你这一个 prompt 上的差距，你会停止"无脑选最强"——你会基于场景选模型。
- 当你看着两个 result.json 想"咦这两段话好像差不多"——**这就是为什么大家敢把 80% 的工作扔给便宜模型**。
- 当你看着另一个 prompt 上"便宜模型胡说八道、昂贵模型也只是漂亮地胡说八道"——你会**反过来**怀疑"是不是 prompt 写得不够好"，而不是再去换更贵的模型。
