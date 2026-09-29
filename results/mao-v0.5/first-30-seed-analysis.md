# MAO v0.5 — First 30-Seed Analysis（第一轮30随机种子分析）

**Date:** 2026-09-29  
**Runs:** 6 scenarios × 2 variants × 30 seeds = **360 runs**  
**Comparison:** Reliability Engineering（可靠性工程） vs Reliability Engineering + AI Physiology（可靠性工程 + 人工智能生理层）

---

# 1. 结论先说

这一轮是目前最重要的一次负结果。

在当前 synthetic benchmark（合成基准）里：

> **加入 Physiology Layer（生理层）没有带来可测的任务成功率、记忆完整性、污染控制或维护效果提升。**

六个场景里，两组的：
- task success
- memory integrity
- duplicate ratio
- contaminants retained
- maintenance actions
- retry / fallback behavior

几乎完全一致。

Physiology 组额外增加了：
- Vital Sign measurement（生命体征测量）
- Homeostasis evaluation（稳态判断）
- Homeostatic Debt（稳态债务）
- Recovery Reserve（恢复储备）
- regulation actions（调节动作）

但在当前实验里，这些新增状态**没有转化成额外的实际效果**。

---

# 2. 为什么会这样

原因不是简单的“AI Physiology错了”。

而是 v0.5 暴露出：

> **当前 Physiology Layer 做的动作，和 Reliability Only 组已有的工程维护动作高度重叠。**

例如两组都会：

- context saturation 高时 cleanup；
- memory integrity 低时 cleanup；
- 高 resource pressure 时 load shedding；
- 高 risk payload 时过滤；
- tool failure 时由同一 Reliability Substrate 负责 retry / fallback / circuit breaker。

因此 Physiology Layer 当前更多是在：

> “重新测量和重新描述同一件事”，

而没有产生真正新的控制能力。

---

# 3. 关键结果

## Context Obesity（上下文肥胖）

两组完全一致：

- task success = **1.000**
- memory integrity ≈ **0.9636**
- duplicate ratio = **0**
- maintenance actions = **101**

Physiology 组额外平均执行：
- regulation actions ≈ **103.3**

但没有换来额外健康收益。

运行时间在当前 Python 合成实现中约增加 **39.7%**。

---

## Memory Contamination（记忆污染）

两组同样：

- task success = **1.000**
- memory integrity ≈ **0.9748**
- contaminants retained = **1**
- maintenance actions = **23**

Physiology 组额外：
- regulation actions ≈ **81.1**

但结果没有改善。

---

## Tool Deterioration（工具退化）

因为双方已经共享：

- retry
- timeout
- fallback
- circuit breaker

所以结果完全一致：

- task success = **1.000**
- memory integrity = **0.98**
- retries ≈ **108.9**
- fallback calls ≈ **17.6**

Physiology 层没有增加任务可靠性。

这支持 v0.4 的修正：

> **AI Physiology不应该负责替代短期可靠性机制。**

---

## Resource Pressure（资源压力）

两组：

- task success = **1.000**
- critical task success = **1.000**
- memory integrity = **0.98**

Physiology 组有额外 mode / regulation，但并没有改善结果。

说明当前的 Vital Signs 只是把普通资源监控换成了“生理语言”。

---

## Malicious Payload（恶意载荷）

两边都通过同样的 risk filter 阻断攻击。

结果：
- contaminants retained = **0**
- memory integrity = **0.98**
- task success = **1.000**

当前场景仍无法证明“生理层”在安全方面有增量价值。

---

## Chronic Degradation（慢性退化）

这是最关键的一项，但结果仍然相同：

两组：
- task success = **1.000**
- memory integrity ≈ **0.9676**
- duplicate ratio = **0**
- contaminants retained = **2**
- maintenance actions = **57**

Physiology 组虽然计算出了 Debt / Reserve，并平均产生约 **171.3 次 regulation actions**，但：
- 没有更早识别出退化；
- 没有减少污染；
- 没有提高任务表现；
- 没有减少维护动作。

因此当前版本的 Homeostatic Debt / Recovery Reserve 仍然是**描述性指标**，还没有证明是有用的预测变量。

---

# 4. 一个非常关键的研究判断

v0.5 后，不能再用下面这种逻辑：

> “系统有Vital Signs，所以比普通系统高级。”

因为普通 observability（可观测性）也能测很多状态。

真正需要证明的是：

> **Vital Signs / Debt / Reserve 能否发现普通监控发现不了的长期失稳，或者能否比静态阈值更早预测未来故障。**

否则这些只是：
- metrics aggregation（指标聚合）
- observability naming（可观测性重新命名）

而不是新的生理机制。

---

# 5. 这一轮其实帮我们找到真正该测的东西

当前六个场景大量属于：

> “已经超过阈值的问题”。

普通 reliability / monitoring 已经能处理。

真正的 AI Physiology 假设应该放到：

# Low-and-Slow Degradation（低强度长期退化）

特点：

- 单个指标都没有越过报警阈值；
- 每次问题都很小；
- 系统短期任务成功率仍然很高；
- 但多个变量长期共同漂移；
- Recovery Reserve 缓慢下降；
- Homeostatic Debt 持续累积；
- 最终在未来某个时刻出现系统性失稳。

这才真正对应我们最开始讨论的：

> **AI慢性病。**

---

# 6. 下一步不建议直接上真实LLM

按 Roadmap 原来的停止条件：

> v0.5 如果没有稳定增量价值，就不进入真实LLM。

这一轮没有通过这个门槛。

所以现在应该做一个小版本：

# MAO v0.5.1 — Longitudinal Health Benchmark（纵向健康基准）

只测试三件东西：

1. **Trend Detection（趋势检测）**  
   在单项指标都没越阈值时，能否识别持续恶化趋势。

2. **Debt Prediction（债务预测）**  
   Homeostatic Debt 是否能预测未来 failure，而不是只描述当前状态。

3. **Recovery Reserve Prediction（恢复储备预测）**  
   Recovery Reserve 下降是否能提前预测“下一次小故障将无法自行恢复”。

同时必须加入一个更强的对照：

> **Adaptive Monitoring Baseline（自适应监控基线）**

它也可以看：
- moving average（移动平均）
- trend（趋势）
- rolling error rate（滚动错误率）

这样才能验证 Debt / Reserve 到底是不是有独立价值。

---

# 7. 当前理论状态

经过 v0.3 → v0.4 → v0.5，框架已经明显收窄：

最初：
> AI需要一套完整“人工生理系统”。

现在更谨慎的研究问题是：

> **长期AI是否存在一类传统短期可靠性工程难以处理的慢性退化问题；如果存在，显式长期健康状态（Vital Signs、Debt、Reserve）是否能更早预测和调节这种退化？**

这个问题更小，但也更可研究。

---

# 8. 当前结论

**v0.5 没有通过“进入真实LLM”的门槛。**

这不是失败。

它说明当前的生理层还没有证明自己比成熟工程监控多做了什么。

下一步应该继续证伪：

> **如果连低强度长期退化、趋势预测和恢复储备预测都无法体现增量价值，那么 AI Physiology 的工程部分应该进一步收缩。**
