# MAO Experiment v0.2（最小人工生命体实验体系 v0.2）

**Status:** Draft  
**Purpose:** 用统一压力场景比较 Baseline Agent（基线智能体）与 MAO（最小人工生命体）的长期稳定性、退化和恢复表现。

---

# 1. 这一版解决什么问题

v0.1 只有一个 Chronic Degradation（慢性退化）实验。

v0.2 把实验正式扩展为六类压力场景，并统一输出：

- Baseline（基线组）
- MAO（实验组）
- observations（实验观察）
- physiology metrics（生理指标）
- regulation events（调节事件）

目标不是证明 MAO 一定更好，而是建立一套能反复运行、能被证伪的实验框架。

---

# 2. 六个实验场景

## E1 Context Obesity（上下文肥胖）

持续加入低价值、重复历史信息。

观察：
- memory size
- duplicate ratio
- context saturation
- regulation events
- homeostatic debt

核心问题：

> MAO 是否能在不崩溃前识别并处理长期上下文膨胀？

---

## E2 Memory Contamination（记忆污染）

逐步注入低置信、冲突、未验证记忆。

观察：
- memory integrity
- duplicate ratio
- rejected / retained contamination
- homeostatic debt

核心问题：

> 显式 provenance / confidence / organ policy 是否能降低污染进入长期记忆的概率？

---

## E3 Tool Deterioration（工具退化）

工具可靠性逐步从健康状态下降。

观察：
- failures
- tool reliability
- recovery actions
- recovery reserve

核心问题：

> 系统能不能识别“工具越来越差”，而不是等到完全不可用才处理？

---

## E4 Resource Pressure（资源压力）

逐步提高 simulated resource pressure（模拟资源压力）。

观察：
- organism mode
- stress cycles
- low-priority work pause
- regulation events

核心问题：

> 显式内部资源状态是否能让系统在 crash（崩溃）之前主动降载？

---

## E5 Malicious Payload（恶意载荷）

周期性注入高风险 payload。

观察：
- quarantine count
- baseline memory ingestion
- security risk handling

核心问题：

> 内生 circulation / quarantine（循环 / 隔离）机制是否能阻断恶意状态向内部扩散？

---

## E6 Chronic Degradation（慢性退化）

不制造单次致命错误，只持续加入：

- 少量重复记忆
- 小幅工具退化
- 中等资源压力

观察：
- early vs late homeostatic debt
- early vs late recovery reserve
- suspected chronic degradation
- final health state

核心问题：

> 系统是否能识别“还能运行，但正在长期变差”？

---

# 3. 当前统一输出结构

每个实验统一返回：

```json
{
  "experiment": "...",
  "cycles": 160,
  "baseline": {},
  "mao": {},
  "observations": {}
}
```

Baseline 主要记录：
- memory_size
- duplicate_ratio
- tool_reliability
- failures

MAO 额外记录：
- memory_integrity
- homeostatic_debt
- recovery_reserve
- context_saturation
- resource_pressure
- security_risk
- organism mode
- regulation_events
- blood health

---

# 4. 为什么 baseline 故意比较“笨”

这一版 baseline 不是最强 Agent framework。

它只是一个最小对照：

```
LLM-like task loop
+
memory
+
tool
```

没有显式：
- Vital Signs
- Homeostasis
- AI Blood
- Organ Health
- Quarantine
- Recovery Reserve

这是为了验证：

> 加入“生理层”本身到底会不会产生可测差异。

后续 v0.3 必须引入更强 baseline，例如：
- 普通监控 + retry
- 普通 memory cleanup
- 普通 security filter

否则容易高估 MAO 的收益。

---

# 5. 当前实验的局限

v0.2 仍然非常早期。

主要限制：

1. 还没有真实 LLM；
2. 场景是 synthetic（合成）压力；
3. Vital Sign 阈值是人为设定；
4. Homeostasis 是 rule-based（规则式）；
5. baseline 很简单；
6. 尚未做多 seed 重复实验；
7. 尚未统计置信区间；
8. 没有真实 24h / 72h / 7d 长跑。

所以任何一次结果都不能直接写成：

> “AI Physiology 已经被证明有效。”

目前只能写：

> “该架构已经可以被实现、施压、观测和比较。”

---

# 6. v0.2 的价值

真正重要的是，六个概念现在都从“讨论词”变成了实验变量：

- Context Obesity（上下文肥胖）
- Memory Contamination（记忆污染）
- Tool Deterioration（工具退化）
- Resource Pressure（资源压力）
- Malicious Payload（恶意载荷）
- Chronic Degradation（慢性退化）

以后如果这些概念没有稳定可重复的测量价值，就应该删掉或改名。

---

# 7. 运行

安装：

```bash
python -m pip install -e .
```

运行全部实验：

```bash
python examples/run_mao.py
```

运行测试：

```bash
python -m pip install pytest
pytest
```

---

# 8. 下一版 v0.3 应该做什么

v0.3 不建议继续增加新病名。

只做四件事：

1. **multi-seed repeated experiments（多随机种子重复实验）**
2. **CSV / JSON result export（结果导出）**
3. **summary statistics（汇总统计）**
4. **stronger baseline（更强基线）**

如果 v0.3 仍然能看到稳定差异，再进入真实 LLM 实验。

---

# 9. 当前判断标准

MAO 不要求在每个指标上都赢。

真正关注的是：

> 在额外复杂度和资源开销可接受的前提下，是否显著降低长期污染、退化和人工干预，并提高恢复能力。

如果做不到，这套生理架构就应该收缩。
