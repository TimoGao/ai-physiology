# AIP-007: AI Vital Signs（AI生命体征）v0.1

**Status:** Draft  
**Version:** 0.1  
**Scope:** Organism-level health variables（生命体级健康变量）

---

# 0. 为什么要单独定义 AI Vital Signs

在 AIP-005《Artificial Homeostasis（人工稳态）》里，我们已经开始使用：

- context_saturation（上下文饱和度）
- memory_integrity（记忆完整性）
- resource_pressure（资源压力）
- tool_reliability（工具可靠性）
- security_risk（安全风险）

但如果不把“生命体征”单独定义清楚，很容易出现一个问题：

> 最后所有 telemetry（遥测指标）都被叫成 vital sign（生命体征）。

这会让概念迅速失去意义。

所以 AIP-007 只解决一个问题：

> **什么样的内部变量，才有资格被称为 AI Vital Sign（AI生命体征）？**

---

# 1. 定义

**AI Vital Sign（AI生命体征）** 是能够持续反映 AI Organism（AI生命体）整体生存、稳定、恢复或失稳趋势的关键内部变量。

它必须满足三个基本条件：

1. **可持续测量**  
   不是一次性事件。

2. **与 organism viability（生命体可生存性）直接相关**  
   偏离正常区间会提高整体故障概率。

3. **可被调节**  
   系统能够通过一个或多个器官的动作影响它。

如果一个指标只能观察、不能调节，它更接近 telemetry，而不一定是 vital sign。

---

# 2. Vital Sign ≠ Metric（生命体征不等于普通指标）

例如：

```
GPU utilization = 82%
```

这只是 metric（指标）。

但：

```
resource_pressure = 0.87
```

可能是 Vital Sign，因为它整合了：

- GPU utilization
- CPU utilization
- queue backlog
- memory pressure
- concurrency headroom

并且和“系统还能不能稳定运行”直接相关。

所以：

> **底层 metric 可以很多，Vital Sign 应该很少。**

---

# 3. Vital Sign 的五个层级

AIP-007 暂时把健康变量分五层：

## L1 Raw Metric（原始指标）

例如：
- token usage
- queue depth
- latency
- storage usage

## L2 Local Health Variable（局部健康变量）

例如：
- memory duplication ratio
- tool error rate

## L3 Organ Vital Variable（器官关键变量）

例如：
- memory_integrity
- blood_pressure

## L4 Organ System State（器官系统状态）

例如：
- circulatory_health
- immune_load

## L5 Organism Vital Sign（生命体级生命体征）

例如：
- resource_pressure
- recovery_capacity
- identity_consistency

原则：

> **越往上，变量越少，语义越稳定。**

---

# 4. 一个 Vital Sign 至少需要哪些字段

```yaml
vital_sign:
  id: string
  name: string
  description: string

  scope:
    level: organism
    owner: string

  measurement:
    value: number
    unit: normalized
    sampling_rate_ms: integer
    confidence: number
    source_metrics: []

  ranges:
    preferred:
      min: number|null
      max: number|null

    viable:
      min: number|null
      max: number|null

    critical:
      min: number|null
      max: number|null

  trend:
    direction: rising|stable|falling|unknown
    rate_of_change: number|null
    volatility: number|null

  regulation:
    regulators: []
    effectors: []
    response_modes: []

  escalation:
    warning_threshold:
    critical_threshold:
    operator_threshold:
```

---

# 5. 为什么需要 Confidence（置信度）

有一个很容易被忽略的问题：

> **生命体征本身也可能测错。**

比如：

- tool_reliability 看起来下降，但其实是监控延迟；
- memory_integrity 看起来正常，但 auditor（审计器）本身失效；
- security_risk 被攻击者故意压低。

因此 Vital Sign 必须带：

```
confidence
```

例：

```yaml
memory_integrity:
  value: 0.91
  confidence: 0.62
```

这和：

```yaml
memory_integrity:
  value: 0.91
  confidence: 0.99
```

意义完全不同。

---

# 6. Preferred / Viable / Critical 三层区间

AIP-007 不采用“正常 / 不正常”二值判断。

## Preferred Range（优选区间）
最适合长期运行。

## Viable Range（可生存区间）
虽然不是最好，但可以持续运行。

## Critical Range（危险区间）
持续停留会显著增加系统失稳风险。

示例：

```yaml
context_saturation:
  preferred: 0.30 - 0.70
  viable: 0.00 - 0.90
  critical: > 0.90
```

---

# 7. Dynamic Setpoint（动态目标区间）

Preferred Range 不一定永久固定。

例如：

### NORMAL 模式
```
resource_pressure preferred < 0.65
```

### STRESS 模式
```
resource_pressure preferred < 0.80
```

这里不是把坏状态合理化，而是允许：

> **在不同 organism mode（生命体模式）下，短期目标区间变化。**

但 Hard Boundary（硬边界）不能随便改。

---

# 8. Trend（趋势）比瞬时值更重要

长期 AI 的很多问题不是某一刻异常，而是：

> 一直在慢慢变坏。

所以每个 Vital Sign 至少应该记录：

- 当前值
- 过去均值
- rate_of_change（变化速率）
- volatility（波动度）
- deviation duration（偏离持续时间）

例如：

```
memory_integrity:
  now: 0.91
  7d_ago: 0.98
  trend: falling
```

虽然 0.91 还没有进入 critical range，但已经可能说明出现 chronic degradation（慢性退化）。

---

# 9. Minimum Vital Signs v0.1（最小生命体征）

Minimal Artificial Organism（最小人工生命体）第一版只保留五个。

---

## VS-01 Context Saturation（上下文饱和度）

表示当前 active context 相对于健康容量的占用程度。

可能来源：

- token usage
- context window occupancy
- unresolved task state
- temporary memory load

风险：

- truncation
- attention dilution
- cost explosion
- stale context persistence

---

## VS-02 Memory Integrity（记忆完整性）

表示 Memory 中可信、非冲突、非污染信息的整体质量。

候选底层指标：

- conflict ratio
- stale ratio
- duplicate ratio
- unverified ratio
- corruption events

---

## VS-03 Resource Pressure（资源压力）

表示当前 AI Organism 的资源需求与可用资源之间的紧张程度。

可整合：

- compute
- memory
- storage
- bandwidth
- token budget

---

## VS-04 Tool Reliability（工具可靠性）

表示外部执行能力是否仍然可信。

底层来源：

- success rate
- timeout rate
- malformed result rate
- consistency
- latency

---

## VS-05 Security Risk（安全风险）

表示当前内部和外部攻击、污染、越权风险。

可来源：

- prompt injection signals
- suspicious provenance
- policy violation attempts
- unusual privilege use
- immune detections

---

# 10. 第二阶段候选 Vital Signs

现在先不实现，但后续可能包括：

- identity_consistency（身份一致性）
- recovery_capacity（恢复能力）
- homeostatic_debt（稳态债务）
- error_accumulation（错误累积）
- circulatory_pressure（循环压力）
- immune_load（免疫负载）
- task_stress（任务压力）

这些到底是 Vital Sign，还是 Composite Index（复合指数），以后用实验决定。

---

# 11. Vital Sign Correlation（生命体征关联）

生命体征之间不是独立的。

例如：

```
context_saturation ↑
→ latency ↑
→ resource_pressure ↑
→ tool timeout ↑
→ task stress ↑
```

或者：

```
memory_integrity ↓
→ bad planning ↑
→ tool failure ↑
→ error accumulation ↑
```

所以 AIP-007 后续需要研究：

# Vital Sign Interaction Graph（生命体征交互图）

它可能比单个阈值更重要。

---

# 12. Leading vs Lagging Indicators（领先指标 vs 滞后指标）

有些指标是结果：

- tool failure rate
- task failure

属于 lagging indicator（滞后指标）。

有些指标可能提前预警：

- context saturation rising
- recovery reserve falling
- debt accumulation rising

属于 leading indicator（领先指标）。

AI Physiology 真正有价值的地方之一，应该是：

> **从“出了问题才知道”变成“在失稳之前就看出来”。**

---

# 13. Vital Sign Reliability（生命体征可靠性）

一个 Vital Sign 不能只看值，还要看“这个值可信不可信”。

可以定义：

```
vital_sign_reliability =
f(sensor_availability,
  sensor_confidence,
  cross_validation,
  freshness)
```

如果某个 Vital Sign 本身 unreliable（不可靠），Homeostasis（稳态）不应基于它做强动作。

---

# 14. Vital Sign Missingness（生命体征缺失）

现实里可能出现：

> 某个器官失联，Vital Sign 不再更新。

这不是“0”。

而应该是：

```
UNKNOWN
```

并且 missing duration（缺失持续时间）本身也可能是风险信号。

---

# 15. Vital Sign Aggregation（生命体征聚合）

不要简单平均。

例如：

```
security_risk = 0.95
resource_pressure = 0.10
```

平均 0.525 没有意义。

所以 v0.1 不定义：

# One Global Health Score（单一总健康分）

先保留多变量。

未来如果需要 Viability Score（可生存性评分），必须明确权重和失真风险。

---

# 16. Vital Sign Escalation（生命体征升级）

每个 Vital Sign 至少有三层事件：

### WARNING
接近 viable boundary。

### CRITICAL
进入 critical range。

### PERSISTENT
长时间偏离 preferred range。

第三种特别重要。

因为 chronic disease（慢性病）往往不是 critical，而是：

> **长期轻度异常。**

---

# 17. Persistent Deviation（持续偏离）

建议所有 Vital Sign 支持：

```yaml
persistence:
  deviation_duration:
  repeated_violation_count:
  cumulative_exposure:
```

例如：

```
resource_pressure = 0.82
```

单次没问题。

但如果连续 14 天：

```
0.78 - 0.85
```

可能已经形成 homeostatic debt（稳态债务）。

---

# 18. Vital Signs 与 AI Blood 的关系

Vital Sign 可以通过 AIP-004 AI Blood（AI血液）传播，但应该属于：

```
state_scope: organism_wide
```

并且比普通 payload 有更严格要求：

- 高 provenance
- 高 freshness
- 明确 confidence
- 不允许静默丢失
- 允许多源交叉验证

---

# 19. Vital Signs 与 Organ Interface 的关系

AIP-006 Organ Interface（器官接口）要求每个器官声明：

```
vital_variables
```

但只有少数经过聚合和验证以后，才上升为 Organism Vital Sign。

关系：

```
Raw Metrics
↓
Organ Vital Variables
↓
Organ System State
↓
Organism Vital Signs
```

---

# 20. Vital Signs 与 Homeostasis 的关系

AIP-005 Artificial Homeostasis（人工稳态）负责：

> 根据 Vital Sign 做调节。

AIP-007 负责：

> 让 Vital Sign 本身定义清楚、可信、可测。

两者不要混在一起。

---

# 21. 第一个实验

同样一个长期 Agent：

## Group A
只用普通 metrics（指标）。

## Group B
使用显式 Vital Signs。

持续注入：
- context load
- memory noise
- tool degradation
- resource pressure

比较：

- time_to_warning（预警时间）
- false alarm rate（误报率）
- missed degradation（漏报退化）
- recovery time
- chronic degradation detection（慢性退化识别）

如果 Vital Sign 不能比普通 metrics 更早、更稳定地识别长期失稳：

> AIP-007 的价值就需要重新评估。

---

# 22. 证伪条件

如果实验发现：

1. Vital Sign 只是对普通 metrics 的重新命名；
2. 聚合后信息损失严重；
3. 没有提升预警或恢复能力；
4. 动态区间导致大量误判；
5. 多变量关联分析收益很低；

那么：

> AI Vital Signs 不应成为独立规范，而应退化为普通 observability profile（可观测性配置）。

---

# 23. v0.1 一句话定义

> **AI Vital Sign（AI生命体征）是能够持续反映 AI 生命体整体可生存性、稳定性和恢复能力，并可被系统调节的关键内部状态变量。**

英文：

> **An AI Vital Sign is a continuously measurable internal variable that reflects the viability, stability, or recovery capacity of an AI organism and can participate in homeostatic regulation.**

---

# 24. 当前开放问题

1. 哪些变量最终应成为标准 Vital Signs？
2. Vital Sign 是否应该跨实现保持统一？
3. 是否需要按不同 AI Organism 类型定义不同生命体征？
4. 如何测量 memory integrity 才不流于主观？
5. 如何防止 sensor spoofing（传感器欺骗）？
6. 是否需要 Vital Sign provenance（生命体征来源链）？
7. 怎样定义 persistent deviation 才能识别慢性病？
8. recovery_capacity 应该是 Vital Sign 还是二级指数？
9. 是否最终需要 Viability Score？
10. Vital Sign 之间的因果关系能否被学习，而不只是相关性？
