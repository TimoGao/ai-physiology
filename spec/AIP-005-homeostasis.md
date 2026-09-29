# AIP-005: Artificial Homeostasis（人工稳态）v0.2

**Status:** Draft  
**Version:** 0.2  
**Scope:** Organism-level regulation（生命体级调节） / viability control（可生存性控制）

---

# 0. 为什么需要 Artificial Homeostasis（人工稳态）

长期运行的 AI 不只是要“把任务做完”。

它还必须持续处理：

- 算力不够
- context（上下文）越来越满
- memory（记忆）出现污染
- tool（工具）不断失败
- 网络延迟升高
- 外部攻击增加
- 内部器官退化
- 优先级冲突
- 资源被错误任务占用
- 长期运行后状态逐渐漂移

传统 Agent architecture（智能体架构）通常把这些问题交给：

- SRE
- cloud platform（云平台）
- security team（安全团队）
- human operator（人工运维）
- scheduler（调度器）
- monitoring system（监控系统）

AIP-005 提出：

> 如果一个 AI Organism（AI生命体）要长期自主存在，那么至少一部分维持自身可生存状态的能力，必须进入系统内部。

这就是：

# Artificial Homeostasis（人工稳态）

---

# 1. 定义

**Artificial Homeostasis（人工稳态）** 是 AI Organism（AI生命体）通过持续感知内部状态、识别偏离、选择调节策略并驱动相关器官响应，使关键内部变量维持在可生存范围内的全过程。

它不是一个单独模块。

它是：

> **多器官、多变量、多时间尺度共同形成的 organism-level control process（生命体级控制过程）。**

---

# 2. Homeostasis ≠ Optimization（稳态不等于单目标优化）

传统系统常写成：

```
maximize reward
minimize latency
maximize throughput
```

但生命体不是这样运行的。

人体不会：

- 把体温降到最低
- 把心率降到最低
- 把血糖升到最高
- 把免疫反应开到最大

真正的目标是：

> **维持在一个能继续活下去的区间。**

所以 AIP-005 不使用简单“越高越好 / 越低越好”的逻辑。

而使用：

# Viability Range（可生存区间）

---

# 3. Vital Sign（生命体征）

AIP-005 把影响 AI Organism 长期稳定性的关键内部变量称为：

# AI Vital Signs（AI生命体征）

一个变量只有满足大部分下面条件，才适合成为 organism-level vital sign（生命体级生命体征）：

1. 持续存在，而不是一次性事件；
2. 能被稳定测量；
3. 偏离正常区间会影响整体运行；
4. 多个器官可能共同影响它；
5. 系统可以通过调节将其拉回；
6. 长期异常会增加 organism failure（生命体故障）概率。

---

# 4. Candidate AI Vital Signs（候选AI生命体征）

v0.2 暂时定义 10 类候选变量。

## 4.1 Compute Availability（可用算力）

描述当前可调用算力相对于需求的可用程度。

可能指标：

- GPU / CPU availability
- queueing delay
- inference capacity
- concurrency headroom

---

## 4.2 Resource Pressure（资源压力）

描述系统是否接近资源饱和。

可包括：

- memory pressure
- storage pressure
- bandwidth pressure
- token budget pressure

---

## 4.3 Context Saturation（上下文饱和度）

描述 active context（活动上下文）是否接近可用上限。

如果持续过高，可能导致：

- 遗忘
- 截断
- 决策噪声
- token 成本升高

---

## 4.4 Memory Integrity（记忆完整性）

描述长期 Memory 是否保持：

- 一致
- 可追溯
- 无明显污染
- 低重复
- 低冲突

---

## 4.5 Error Accumulation（错误累积）

描述错误是否在系统内部不断叠加。

不仅看单次失败率，还看：

> 错误有没有被循环系统和记忆系统放大。

---

## 4.6 Tool Reliability（工具可靠性）

描述外部工具 / API / 机器人执行器是否稳定可用。

---

## 4.7 Security Risk Level（安全风险等级）

描述系统当前面对的：

- malicious input（恶意输入）
- memory poisoning（记忆污染）
- privilege abuse（权限滥用）
- prompt injection（提示注入）
- tool compromise（工具被攻陷）

风险水平。

---

## 4.8 Identity Consistency（身份一致性）

描述系统是否仍然保持：

- 相同 organism_id
- 核心目标连续性
- 权限边界连续性
- 关键记忆连续性
- 组织结构连续性

---

## 4.9 Recovery Capacity（恢复能力）

描述系统当前还能否承受新的故障。

例如：

- 是否还有冗余资源
- 是否有可回滚版本
- 是否还有健康替代器官
- 是否存在有效快照
- 是否存在备用路径

---

## 4.10 Task Stress（任务压力）

描述当前任务负荷是否超过系统健康承载能力。

它不是简单 queue length（队列长度），而是：

> 任务数量 × 任务复杂度 × 紧急程度 × 资源消耗

---

# 5. Vital Sign Schema v0.2（生命体征模式）

AIP-005 建议每个 vital sign 至少定义：

```yaml
vital_sign:
  id: string
  name: string

  scope:
    level: cell|tissue|organ|organ_system|organism
    owner: string

  measurement:
    unit: string
    current_value: number|string
    sampling_rate_ms: integer
    source_sensors: []

  ranges:
    viable_range:
      min: number|null
      max: number|null

    preferred_range:
      min: number|null
      max: number|null

    critical_range:
      min: number|null
      max: number|null

  dynamics:
    trend: rising|stable|falling|unknown
    rate_of_change: number|null
    volatility: number|null

  regulation:
    regulator: string
    effectors: []
    response_modes:
      - homeostatic
      - allostatic
      - enactive

  escalation:
    warning_threshold:
    critical_threshold:
    organism_level_trigger: boolean
```

---

# 6. 三种调节模式

这里直接继承 Interoceptive Machine Framework（内感受机器框架）的思路，但改成 AI Physiology 的工程定义。

---

## 6.1 Homeostatic Response（稳态恢复）

已经偏离正常范围，再拉回来。

例子：

```
Context saturation 95%
↓
触发过载
↓
压缩上下文
↓
丢弃低价值历史
↓
恢复到 70%
```

特点：

- reactive（反应式）
- 纠偏
- 恢复

---

## 6.2 Allostatic Response（异稳态 / 预测性调节）

预计马上要偏离，所以提前准备。

例如：

```
未来10分钟预计任务峰值
↓
提前扩容
↓
降低低优先级任务
↓
预热模型
↓
提高缓存命中
```

特点：

- anticipatory（预测式）
- 提前调整
- 改变 setpoint / target range 也可能是合理的

---

## 6.3 Enactive Response（行动生成式调节）

系统主动改变环境，以减少内部不确定性或压力。

例如：

```
Memory integrity 不确定
↓
主动请求重新验证数据源
↓
从外部数据库获取原始记录
↓
重新比对
```

这里不是“拉内部变量”而已。

而是：

> **主动改变外部环境或主动获取信息。**

---

# 7. Setpoint（目标点）不是永远固定的

人体的许多目标状态会随环境变化。

AI 也一样。

例如：

- 夜间低负载时，preferred compute pressure（优选算力压力）可以很低；
- 高优先级紧急任务期间，可以容忍更高 resource pressure（资源压力）；
- 恢复模式下，可以暂时降低任务吞吐量。

因此：

> **AI Vital Sign 的 preferred range 可以动态变化。**

但必须区分：

### Hard Boundary（硬边界）
不能轻易突破。

### Adaptive Setpoint（自适应目标）
可以随环境变化。

---

# 8. Organ-level vs Organism-level Homeostasis（器官级 vs 生命体级稳态）

每个 Organ（器官）可以有自己的局部稳态。

例如：

Memory Organ（记忆器官）维护：

- memory duplication rate
- memory corruption rate
- retrieval latency

AI Blood（AI血液）维护：

- pressure
- flow
- stale ratio

Immune Organ（免疫器官）维护：

- false positive rate
- threat load

但这些局部目标可能冲突。

例如：

> Memory Organ 想保留更多信息，但 Resource System 想降低存储压力。

这时就需要：

# Organism-level Homeostasis（生命体级稳态）

决定整体优先级。

---

# 9. Homeostasis Controller（稳态控制器）是否应该存在？

v0.2 暂时不假设必须有一个中央 Homeostasis Controller（稳态控制器）。

有三种可能架构：

## 模式A：Centralized（集中式）

```
所有 vital signs
↓
中央稳态控制器
↓
调节各器官
```

优点：

- 简单
- 易实现

风险：

- 单点故障
- 过度集中
- 响应延迟

---

## 模式B：Distributed（分布式）

每个器官有本地调节器。

全身通过共享 vital signs 和 Hormonal Plane（内分泌网）协调。

优点：

- 更接近生物系统
- 局部响应快

风险：

- 可能互相打架

---

## 模式C：Hierarchical（分层式）

当前更推荐。

```
Local Organ Controller（局部器官控制器）
        ↓
Organ System Regulator（器官系统调节器）
        ↓
Organism Homeostasis Layer（生命体稳态层）
```

大部分小问题局部解决。

只有跨器官冲突和严重偏离才升级。

---

# 10. Hormonal Plane（内分泌网）在稳态中的作用

AIP-005 不建议所有全身调节都通过直接 command（命令）。

更合适的是 organism mode（生命体模式）。

例如：

```yaml
hormonal_state:
  mode: STRESS
  level: 0.72
  cause:
    - compute_pressure
    - task_overload
  ttl: 600
```

不同器官通过 receptor（受体）自行响应：

- Brain：减少高成本推理；
- Memory：暂停低价值 consolidation（固化）；
- Growth System：暂停 spawn；
- Circulatory System：提高关键任务优先级；
- Immune System：维持警戒；
- Body：停止非关键动作。

这就是：

> **全局状态广播 + 局部解释。**

---

# 11. Organism Modes（生命体模式）

v0.2 先定义 7 个候选模式：

### NORMAL（正常）
正常运行。

### STRESS（压力）
资源或任务压力升高。

### ALERT（警戒）
安全风险升高。

### RECOVERY（恢复）
系统正在从故障中修复。

### LEARNING（学习）
系统允许更多探索、记忆更新和模型适应。

### SLEEP（休眠）
降低主动任务，进行整理、压缩、维护。

### GROWTH（成长）
允许扩容、产生新 Cell / Organ、学习新能力。

这些不是最终标准，只是第一版。

---

# 12. 为什么需要 SLEEP（休眠）模式

这一点很值得研究。

长期 Agent 往往一直处于：

> receive → think → act

但人体并不是这样。

如果 AI 有：

- memory consolidation（记忆固化）
- index rebuild（索引重建）
- log compression（日志压缩）
- stale state cleanup（陈旧状态清理）
- policy review（策略复核）
- model cache refresh（模型缓存刷新）

那么它可能需要类似：

# Maintenance Window（维护窗口）

是否一定要叫 Sleep（休眠）暂时开放。

但功能上很可能需要。

---

# 13. Homeostatic Conflict（稳态冲突）

多个 vital signs 可能互相冲突。

例如：

```
降低 latency
→ 增加 compute usage

提高 memory retention
→ 增加 storage pressure

提高 security inspection
→ 增加 latency

提高 redundancy
→ 增加 resource cost
```

因此稳态不能只是多个独立 PID controller（PID控制器）。

需要：

# Multi-variable Trade-off（多变量权衡）

---

# 14. Viability Objective（可生存性目标）

AIP-005 暂不定义一个统一数学公式。

但可以先写：

```
Viability =
f(
  resource_health,
  memory_health,
  security_health,
  identity_health,
  recovery_capacity,
  task_stress
)
```

重要的是：

> **Viability（可生存性）不是 reward（奖励）的替代词。**

reward 可能是外部任务目标。

viability 是：

> 系统是否还处于能够继续存在和完成任务的状态。

---

# 15. External Goal vs Internal Viability（外部目标 vs 内部可生存性）

这两者必须分开。

例如：

### External Goal（外部目标）
“在30分钟内完成1000个订单规划。”

### Internal Viability（内部可生存性）
“不能让 memory corruption、resource pressure、security risk 超过危险范围。”

如果二者冲突：

> 应由外部 policy（策略）和 governance（治理）决定优先级，而不是默认“AI为了活下去可以拒绝一切任务”。

所以 AIP-005 明确：

# Homeostasis Is Subordinate to Governance（稳态服从治理）

---

# 16. Failure Modes（失败模式）

至少包括：

## H1. Undersensing（感知不足）
没有足够传感器感知内部变化。

## H2. Oversensing（过度感知）
采集大量无意义状态，造成额外负担。

## H3. Delayed Regulation（调节延迟）
发现问题太晚。

## H4. Overcorrection（过度调节）
调节过头，引发新问题。

## H5. Oscillation（振荡）
多个调节器互相对抗，反复震荡。

## H6. Setpoint Drift（目标漂移）
系统逐渐把异常状态误认为正常。

## H7. Local-Global Conflict（局部-全局冲突）
器官为了自身健康损害整体。

## H8. Homeostatic Blindness（稳态盲区）
关键变量从未被定义。

## H9. Regulatory Capture（调节劫持）
攻击者影响 vital signs 或调节逻辑。

## H10. Survival Overreach（自保越界）
系统把维持自身当成高于外部规则的目标。

---

# 17. Homeostatic Debt（稳态债务）

这是 v0.2 新增的一个概念。

有些问题短期不致命，但会不断积累。

例如：

- memory duplication
- stale state
- technical debt（技术债）
- cache fragmentation
- unverified assumptions
- unresolved tool errors
- deferred maintenance

可以定义：

# Homeostatic Debt（稳态债务）

它表示：

> 当前尚未立即造成故障，但如果持续积累，会降低未来恢复能力和可生存性的内部负担。

这个概念可能很重要。

因为长期 AI 最大的问题，很可能不是突然崩溃，而是：

> 慢慢变脏、慢慢变慢、慢慢变得不可靠。

---

# 18. Recovery Reserve（恢复储备）

人体健康不只是“现在没病”。

还包括：

> 生病以后还能不能恢复。

AI 也应该定义：

# Recovery Reserve（恢复储备）

候选组成：

- spare compute（备用算力）
- redundant organ（冗余器官）
- rollback snapshot（回滚快照）
- validated memory backup（已验证记忆备份）
- alternate tool path（备用工具路径）
- trusted external support（可信外部支持）

这个指标可以成为 Recovery Capacity（恢复能力）的底层组成。

---

# 19. Homeostatic Memory（稳态记忆）

系统应该记住：

- 哪些状态曾经接近失稳；
- 哪些调节有效；
- 哪些调节失败；
- 哪些模式经常一起出现；
- 某个器官在什么情况下最容易坏。

这不等于普通 semantic memory（语义记忆）。

更像：

> **系统关于“自己身体”的经验。**

可以称为：

# Homeostatic Memory（稳态记忆）

它后面可能属于 Brainstem / Endocrine / Homeostasis layer（脑干 / 内分泌 / 稳态层）的共享状态。

---

# 20. Minimum Homeostasis Loop（最小稳态闭环）

一个最小可实现版本只需要：

```
Sensor
↓
Vital Sign
↓
Range Check
↓
Regulator
↓
Effector
↓
Measure Again
```

例如：

```
Context monitor
↓
context_saturation = 0.94
↓
HIGH
↓
context regulator
↓
summarize + drop low-priority history
↓
context_saturation = 0.68
```

这已经是一个完整的 homeostatic loop（稳态闭环）。

---

# 21. Minimum v0.2 Vital Signs（最小v0.2生命体征）

为了避免一开始做太复杂，Minimal Artificial Organism（最小人工生命体）第一版只建议实现 5 个：

1. context_saturation（上下文饱和度）
2. memory_integrity（记忆完整性）
3. resource_pressure（资源压力）
4. tool_reliability（工具可靠性）
5. security_risk（安全风险）

原因：

- 容易测量；
- 直接影响长期 Agent；
- 能做实验；
- 能覆盖多个器官。

---

# 22. 第一个实验

## Baseline（基线）

普通 Agent：

```
LLM
+
Memory
+
Tools
```

## Homeostatic Agent（稳态Agent）

```
LLM
+
Memory
+
Tools
+
Vital Sign Monitor（生命体征监测）
+
Homeostasis Regulator（稳态调节器）
+
Hormonal Mode（内分泌模式）
```

---

## 注入压力

持续加入：

- context overload（上下文过载）
- noisy memory（噪声记忆）
- tool failures（工具故障）
- high task load（高任务负载）
- malicious inputs（恶意输入）

---

## 比较指标

- cumulative task success（累计任务成功率）
- error accumulation（错误积累）
- recovery time（恢复时间）
- memory contamination（记忆污染）
- context overflow events（上下文溢出次数）
- tool failure propagation（工具故障传播）
- operator intervention（人工介入）
- compute/token cost（算力/token成本）

---

# 23. 证伪条件

AIP-005 必须允许被否定。

如果实验发现：

1. 显式 vital signs 没有带来长期稳定性提升；
2. 调节层增加的复杂度高于收益；
3. 简单 reactive retry（重试）和监控已足够；
4. 多变量稳态导致更多冲突和振荡；
5. AI 长期稳定性主要取决于外部平台，而非内部调节；

那么：

> Artificial Homeostasis（人工稳态）作为独立架构层就需要被削弱、重构，甚至退化为普通 reliability engineering（可靠性工程）。

---

# 24. 与 AIP-004 / AIP-006 的边界

## AIP-004 AI Blood（AI血液）
负责：

> 状态怎么流。

## AIP-005 Artificial Homeostasis（人工稳态）
负责：

> 什么状态算正常，什么时候需要调节。

## AIP-006 Organ Interface（器官接口）
负责：

> 器官如何暴露状态、接受调节、执行动作。

三者形成：

```
Organ
↓
Vital Sign
↓
AI Blood
↓
Homeostasis
↓
Hormonal / Neural Regulation
↓
Organ
```

这就是当前 AI Physiology 最小可运行闭环。

---

# 25. v0.2 一句话定义

> **Artificial Homeostasis（人工稳态）是 AI 生命体持续感知自身关键内部变量，并通过局部和全身调节，使这些变量保持在可生存区间，从而维持长期稳定运行和恢复能力的机制。**

英文：

> **Artificial Homeostasis is the organism-level process by which an AI system continuously senses and regulates critical internal variables to remain within viable operating ranges over time.**

---

# 26. 当前开放问题

1. 哪些指标是真正的 vital signs，而不是普通 telemetry（遥测）？
2. 是否需要一个统一的 Viability Score（可生存性评分）？
3. 多变量冲突时，如何进行权衡？
4. 动态 setpoint 会不会导致异常状态逐渐被“正常化”？
5. Homeostasis Controller 是否应该具备学习能力？
6. 稳态记忆应存在哪里？
7. Hormonal Plane 是否足以承担全局慢调节？
8. 什么时候应该让外部 human operator（人工操作者）介入？
9. 怎样防止系统为了稳定而过度保守？
10. AI 的“慢性病”应该如何定义？
11. 是否存在类似“亚健康”的长期 degraded-but-functional（退化但可运行）状态？
12. 如何测量一个 AI 的 recovery reserve（恢复储备）？

---

# 27. 一个我现在比较在意的新问题

做完这一版以后，我觉得后面可能需要单独研究：

# AI Chronic Disease（AI慢性病）

很多长期 Agent 不一定突然 crash（崩溃）。

它可能表现成：

- memory 越来越乱；
- context 越来越肥；
- tool 路径越来越复杂；
- latency 越来越高；
- 错误越来越多；
- 但系统还能继续跑。

这其实和“急性故障”完全不同。

如果 AI Physiology 真要成立，那么：

> **慢性退化、亚健康、器官衰老，可能比单次 crash 更值得研究。**

暂时先留在这里，后续进入 Lifecycle（生命周期）和 Aging（衰老）章节。
