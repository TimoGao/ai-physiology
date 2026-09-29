# MAO Experiment v0.3 — First 10-Seed Results（第一轮10随机种子结果）

**Date:** 2026-09-29  
**Runs:** 6 scenarios × 2 baselines × 10 seeds = **120 runs**  
**Status:** Engineering validation only（仅工程验证，不能作为理论成立证据）

---

# 1. 先说结论

第一轮结果没有支持“MAO 已经证明优于普通 Agent”这种说法。

更有价值的结论是：

> **当 Strong Baseline（更强工程基线）加入 retry（重试）、memory cleanup（记忆清理）、risk filter（风险过滤）之后，MAO 在一些场景中的优势明显缩小。**

这说明我们必须继续区分：

- 哪些收益来自普通工程实践；
- 哪些收益才真正来自 AI Blood（AI血液）、Vital Signs（生命体征）、Homeostasis（稳态）、Organ Health（器官健康）。

目前数据主要证明：

> **实验框架已经开始具备“反驳我们自己”的能力。**

这比得到一个漂亮的正结果更重要。

---

# 2. Strong Baseline vs MAO — 第一轮主要结果

| 场景 | Strong Baseline | MAO | 当前能得出的判断 |
|---|---|---|---|
| Context Obesity（上下文肥胖） | duplicate ratio 10.64%；memory size 188 | duplicate ratio 0%；memory size 156.8 | MAO 清理更彻底，但平均触发约90次调节，成本还没算，不能直接说更优 |
| Memory Contamination（记忆污染） | duplicate ratio 1.23%；memory size 163 | duplicate ratio 0%；memory integrity 0.98 | 差异已经很小；而且两边过滤阈值并不完全等价，需要重做公平实验 |
| Tool Deterioration（工具退化） | 最终失败均值2.4次；平均重试37次 | tool reliability约0.741；约57次调节 | 当前缺少MAO的可比失败数，暂时不能判断谁更好 |
| Resource Pressure（资源压力） | 普通基线没有真正受到资源限制 | MAO进入STRESS并降载约27.7轮 | 当前只能证明“规则会触发”，不能证明MAO更有用 |
| Malicious Payload（恶意载荷） | 20/20恶意输入被普通risk filter拒绝 | 20/20被AI Blood隔离 | 两边都解决了问题，目前没有显示生理架构额外优势 |
| Chronic Degradation（慢性退化） | duplicate ratio约1.56%；失败2.9次；大量retry | duplicate 0；debt约0.072；reserve约0.84 | MAO状态更可观测，但10/10都没有触发当前“慢性退化”判定，说明定义/实验需要重审 |

---

# 3. 一个很重要的发现：Strong Baseline 很能打

之前 Naive Baseline（朴素基线）很弱。

例如 Context Obesity：

- Naive Baseline duplicate ratio：约 **65.7%**
- Strong Baseline：约 **10.6%**
- MAO：**0%**

如果只拿 Naive Baseline 比，我们很容易得到：

> “MAO 大幅解决上下文肥胖。”

但加入普通周期清理以后，差距从 65.7% vs 0% 缩成了 10.6% vs 0%。

这告诉我们：

> **很多所谓“生理机制优势”，首先必须和成熟的软件工程方法比较，而不是和一个什么都不做的 Agent 比。**

这会成为后续实验的基本原则。

---

# 4. 六个场景逐项判断

## E1 Context Obesity（上下文肥胖）

目前最明显的正向信号之一。

MAO：
- duplicate ratio = 0
- memory size 平均约 156.8

Strong Baseline：
- duplicate ratio = 10.64%
- memory size = 188
- 已经主动清理约292条重复内容

但 MAO 平均出现约 **90.2 次 regulation events（调节事件）**。

问题变成：

> 为了减少约10%的重复，90次调节到底值不值？

v0.4 必须加入：
- compute overhead
- maintenance operations
- latency cost

否则不能判断。

---

## E2 Memory Contamination（记忆污染）

当前实验不够公平。

MAO Memory Organ 直接拒绝：

```
confidence < 0.5
```

Strong Baseline 只有：

```
confidence < 0.3
```

也就是说 MAO 天生使用了更严格的过滤规则。

所以这一轮不能用于证明“器官机制优于普通filter”。

v0.4 必须统一阈值。

---

## E3 Tool Deterioration（工具退化）

Strong Baseline：
- failures 平均 2.4
- retries 平均 37

MAO：
- 最终 tool reliability 平均约 0.741
- regulation events 平均约 57.2

但当前 MAO summary 没有导出：
- tool calls
- actual failures
- recovery attempts

所以暂时无法做 apples-to-apples comparison（同口径比较）。

这是 v0.4 必须补的数据。

---

## E4 Resource Pressure（资源压力）

现在这个实验只证明：

> 当 resource_pressure > 0.9 时，Homeostasis 会进入 STRESS 并暂停低优先级工作。

但 Strong Baseline 实际上没有受到同等的：
- CPU限制
- token限制
- queue限制
- latency惩罚

所以它不是严格的 A/B test。

下一版必须让两边面对**同一个资源预算**，然后比较：
- 成功任务数
- critical task completion
- latency
- failure rate
- total resource cost

---

## E5 Malicious Payload（恶意载荷）

这是最值得冷静的一项。

Strong Baseline：
- 20个攻击
- 20个全部被普通 risk filter 拒绝

MAO：
- 20个攻击
- 20个全部被 AI Blood quarantine（隔离）

也就是说：

> **当前实验完全没有证明“AI免疫/AI血液”比普通安全过滤更好。**

这不意味着 AI Blood 没用。

只意味着现在攻击场景太简单。

后续应该测试：
- 多阶段攻击
- 低风险长期污染
- 跨器官传播
- 已经进入内部循环后的污染

否则普通 filter 足够。

---

## E6 Chronic Degradation（慢性退化）

这是目前最有意思，但也最需要修改的一项。

MAO 最终：
- Homeostatic Debt（稳态债务）约 0.072
- Recovery Reserve（恢复储备）约 0.84
- duplicate ratio = 0

但：

> 10个seed中，当前 chronic-degradation detector（慢性退化检测器）一次都没有触发。

有两种可能：

### 解释A
MAO 的调节确实把慢性退化压住了。

### 解释B
我们定义的慢性病阈值太粗，根本检测不出来。

当前数据无法区分。

所以 v0.4 要把 chronic disease（慢性病）从“一个最终布尔值”升级成：
- slope（趋势斜率）
- area under deviation（偏离面积）
- recovery failure
- baseline drift

---

# 5. 当前不能说什么

第一轮结果出来以后，下面这些话都不能说：

- “AI Physiology 已经被证明有效。”
- “MAO 比传统 Agent 更稳定。”
- “AI Blood 比 message bus 更先进。”
- “AI慢性病已经被实验证明存在。”

这些都还没有足够证据。

---

# 6. 当前可以说什么

目前可以比较稳妥地说：

1. AI Physiology 的核心概念可以被转化为可运行代码；
2. Vital Signs、Debt、Reserve、Organ Health 可以被持续观测；
3. MAO 与普通工程基线之间可以建立可重复对照实验；
4. Strong Baseline 显著缩小了很多差异；
5. 当前实验已经暴露出多项需要改进的公平性和指标问题；
6. 因此下一步应该做更严格的 ablation（消融）和成本核算，而不是继续扩理论。

---

# 7. v0.4 必须修改的实验设计

## 1. 公平阈值
MAO 与 baseline 的 risk / confidence / cleanup 规则必须尽量一致。

## 2. 相同外部压力
两组必须受到同样的：
- resource budget
- failure pattern
- malicious payload
- task sequence

## 3. 增加 MAO 可比指标
必须新增：
- tool failures
- tool calls
- successful tasks
- retries / recovery actions
- regulation cost

## 4. Ablation Study（消融实验）
至少比较：

- Full MAO
- MAO without AI Blood
- MAO without Homeostasis
- MAO without Organ Health
- Strong Baseline

## 5. Overhead（额外开销）
必须记录：
- extra messages
- extra state
- regulation count
- CPU time
- memory use

否则“更健康”可能只是靠大量维护换来的。

---

# 8. 第一轮真正带来的研究进展

这次最重要的进展不是某个数字。

而是研究问题已经从：

> “这个理论听起来对不对？”

变成了：

> **“在相同资源、相同压力和相同工程能力下，显式生理架构到底增加了什么不可替代的能力？”**

如果最终答案是：

> 普通 retry + cleanup + filter 已经足够。

那么 AI Physiology 就必须收缩。

如果某些长期问题只有显式 Vital Signs、Homeostatic Debt、Recovery Reserve、跨器官调节才能稳定处理，那么这才是框架真正站得住的地方。

---

# 9. 下一步

进入 **MAO Experiment v0.4**。

目标不是“让MAO赢”。

目标是：

> **把实验做得足够公平，让MAO有机会输。**

只有这样，后面的结果才值得相信。
