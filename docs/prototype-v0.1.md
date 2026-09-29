# MAO Prototype v0.1（最小人工生命体代码原型）

这不是生产系统，也不是完整 AI Agent 平台。

它的作用只有一个：

> 把 AIP-004 / 005 / 006 / 007 / 008 最小化以后真正跑起来，验证“生理闭环”是否有可测价值。

## 当前实现

- `AIBlood`：带 organism_id、TTL、risk、quarantine、pressure 的内存循环层
- `MemoryOrgan`：记录 memory integrity、duplicate ratio、homeostatic debt、recovery reserve
- `ToolOrgan`：模拟执行器可靠性退化
- `HomeostasisLayer`：监测 5 个 Vital Signs 并执行规则式调节
- `MinimalArtificialOrganism`：把器官、循环和稳态拼成持续运行闭环
- `BaselineAgent`：不带生理机制的对照组
- `run_chronic_degradation_experiment`：第一轮慢性退化对照实验

## 为什么先不用真实 LLM

v0.1 故意不依赖 OpenAI、Anthropic 或本地大模型。

第一轮先验证系统机制本身：
- 循环
- 健康状态
- 稳态
- 维护
- 退化
- 恢复

等这些机制稳定后，再接真实 LLM。

否则实验结果很容易被模型本身的随机性掩盖。

## 本地运行

```bash
python -m pip install -e .
python examples/run_mao.py
```

测试：

```bash
python -m pip install pytest
pytest
```

## 当前不是“智能生命”

这个 prototype 不声称：
- 有意识
- 有人格
- 有自我
- 是真正生命

它只是一个可运行的系统架构实验。
