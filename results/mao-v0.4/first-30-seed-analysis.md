# MAO Experiment v0.4 — First 30-Seed Analysis（第一轮30随机种子分析）

**Date:** 2026-09-29  
**Runs:** 6 scenarios × 6 variants × 30 seeds = **1080 runs**  
**Interpretation:** synthetic mechanism validation（合成机制验证）

---

# 1. 结论先放前面

这一轮结果比 v0.3 更“难看”，但研究价值更高。

> **当前 Full MAO 并没有整体优于 Engineering Baseline（工程基线）。**

尤其在 Tool Deterioration（工具退化）和 Chronic Degradation（慢性退化）场景里，普通 retry（重试）+ circuit breaker（熔断）明显比当前 MAO 的单次执行 + 稳态调节更有效。

这意味着一个重要修正：

> **AI Physiology 不应该替代可靠性工程。它更可能是建立在可靠性工程之上的“长期健康管理层”。**

---

# 2. 当前最重要的五个发现

## 发现1：Homeostasis（稳态）和 Vital Signs（生命体征）在记忆问题上有明显作用

Context Obesity（上下文肥胖）：

- Full MAO：duplicate ratio ≈ **0**
- No Homeostasis：duplicate ratio ≈ **0.65**
- No Vital Signs：duplicate ratio ≈ **0.65**

Memory Contamination（记忆污染）：

- Full MAO：memory integrity ≈ **0.967**
- No Homeostasis / No Vital Signs：≈ **0.720**

Chronic Degradation（慢性退化）：

- Full MAO：memory integrity ≈ **0.899**
- No Homeostasis / No Vital Signs：≈ **0.699**

这说明当前原型里：

> **显式状态感知 + 调节闭环，确实是维持记忆健康的核心机制。**

但这仍可能只是“更聪明的cleanup policy（清理策略）”，后续还需要和更成熟的 adaptive maintenance（自适应维护）基线比较。

---

## 发现2：AI Blood（AI血液）当前几乎没有独立贡献

Full MAO 和 No Blood 在六个场景中的主要结果几乎一致。

这并不意外。

当前 MAO 只有非常少的“器官”，信息流也很简单。

因此：

> **在没有真正多器官路由、来源追踪、TTL、跨器官污染传播的实验里，AI Blood 目前只是额外传输层。**

所以不能因为概念漂亮就保留。

下一阶段如果要继续验证 AI Blood，必须专门做：
- multi-organ routing（多器官路由）
- provenance tracing（来源追踪）
- stale payload（过期载荷）
- cross-organ contamination（跨器官污染）
- congestion（拥塞）

否则 AIP-004 应该降级成普通 transport metadata layer（传输元数据层）。

---

## 发现3：普通可靠性工程在工具退化上明显胜过当前 MAO

Tool Deterioration：

- Engineering Baseline task success ≈ **0.996**
- Full MAO ≈ **0.885**

原因非常明确：

Engineering Baseline 有 retry（重试），MAO 当前没有。

这不是 MAO 理论“失败”，而是说明我们之前比较的层级不对。

> **Homeostasis 不能拿来代替 retry、熔断、超时、fallback。**

因此后面的 MAO 应该是：

```
Reliability Engineering
+
Physiology Layer
```

而不是：

```
Reliability Engineering
vs
Physiology Layer
```

---

## 发现4：简单 Malicious Payload（恶意载荷）不需要“免疫系统”

两边都能拦住高风险攻击：

- Engineering Baseline：普通 risk filter
- MAO：AI Blood quarantine / organ rejection

当前没有额外优势。

所以后续如果研究 AI Immune System（AI免疫系统），不能再用“risk=0.95的明显攻击”测试。

真正值得测的是：

- low-and-slow poisoning（低强度长期投毒）
- 多阶段污染
- 内部可信源被污染
- 一个器官污染另一个器官
- 已经进入 memory 后的持续扩散

---

## 发现5：Organ Health（器官健康）目前更像“诊断层”，还不是“性能层”

去掉 Organ Health：

- task success 基本不变
- memory integrity 基本不变
- cleanup 也基本不变

变化主要是：

- 无法计算 debt（稳态债务）
- 无法计算 reserve（恢复储备）
- 无法做 pathology-style detection（病理式识别）

所以当前最合理的定位是：

> **Organ Health 不是直接提高任务性能，而是提供长期诊断和预测能力。**

这要到真实 24h / 72h 长期实验里才可能体现价值。

---

# 3. Full MAO vs Engineering Baseline：当前代价

当前 synthetic benchmark（合成基准）里 Full MAO 通常：

- 执行时间更高；
- 调节动作更多；
- 多出内部消息；
- 某些场景 task success 更低。

例如 Chronic Degradation：

- Engineering Baseline success ≈ **0.992**
- Full MAO ≈ **0.833**

这个差距主要来自 baseline 的 retry 机制。

所以现在绝对不能说：

> “MAO 更稳定。”

准确说法应该是：

> **当前 MAO 在记忆健康维护方面展现出机制价值，但整体任务可靠性还不如带常规可靠性工程的基线。**

---

# 4. 这一轮对理论框架的真正修正

原来的隐含想法有一点像：

> 生理架构可能是一种新的 Agent runtime（智能体运行时）。

v0.4 之后，我认为应该修正成：

> **AI Physiology 更可能是一层长期健康管理架构，运行在成熟的 reliability substrate（可靠性底座）之上。**

也就是：

```
LLM / Agent
↓
Reliability Engineering
  retry / timeout / fallback / circuit breaker
↓
AI Physiology
  vital signs / homeostasis / debt / reserve / pathology
↓
Infrastructure
```

这个定位比“重新发明Agent操作系统”更清楚。

---

# 5. 消融实验目前支持什么

当前证据强弱：

### Homeostasis（稳态）
**有正向信号。**
主要体现在 context / memory maintenance。

### Vital Signs（生命体征）
**有正向信号。**
没有显式测量，homeostasis 无法工作。

### Organ Health（器官健康）
**暂未证明性能收益。**
当前价值主要是诊断。

### AI Blood（AI血液）
**当前没有证明独立收益。**
需要专门的多器官实验。

---

# 6. 现在不应该马上接真实 LLM

虽然路线图原来是 v0.4 后接真实模型，但这一轮暴露出一个更基础的问题：

> MAO 还缺普通 reliability substrate（可靠性底座）。

如果直接接 LLM，结果会被 retry / timeout / fallback 的缺失污染。

因此下一步建议先做一个很小的：

# MAO v0.5 — Reliability Substrate Integration（可靠性底座整合）

只加入：
- retry
- timeout
- fallback
- circuit breaker

然后再重复 v0.4。

目标是：

> **比较“成熟工程基线”与“成熟工程基线 + 生理层”。**

这样才公平。

---

# 7. 当前理论没有被证明，但已经被明显收窄

这是好事。

现在我们更清楚：

AI Physiology 可能真正研究的不是：

> AI怎样完成一次任务。

而是：

> **一个已经具备基本工程可靠性的长期AI，怎样感知自己的慢性状态、维持长期健康、发现系统性退化并恢复。**

如果后面这个价值也验证不出来，那理论就应该继续收缩。
