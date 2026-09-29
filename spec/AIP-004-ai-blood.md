# AIP-004: AI Blood（AI血液）v0.2

**Status:** Draft  
**Version:** 0.2  
**Scope:** Circulatory Plane（循环网） / cross-organ transport（跨器官传输）

---

# 0. 为什么需要 AI Blood（AI血液）

今天很多 AI 系统里已经有：

- message bus（消息总线）
- event stream（事件流）
- task queue（任务队列）
- context（上下文）
- memory（记忆）
- telemetry（遥测）
- security events（安全事件）
- resource scheduler（资源调度）

但这些东西通常彼此独立。

如果把一个长期运行的 AI 看作 AI Organism（AI生命体），问题就变成：

> 不同器官之间，是否需要一套统一的“内部循环介质”，持续运输状态、任务、资源、风险、身份和中间产物？

AIP-004 暂时把这类介质定义为：

# AI Blood（AI血液）

这里的“血液”不是为了做生物学拟人化，而是为了强调三件事：

1. **它是 transport medium（运输介质），不是某一种数据本身；**
2. **它需要持续循环，而不是一次性的函数调用；**
3. **它服务于 organism-level homeostasis（生命体级稳态），而不仅仅是业务通信。**

---

# 1. 定义

**AI Blood** 是 AI Organism（AI生命体）内部用于跨器官持续运输 physiological payloads（生理载荷）的标准化循环介质。

它至少承担：

- 状态运输
- 资源运输
- 任务运输
- 中间结果运输
- 风险信号运输
- 身份与来源信息运输
- 调节信号运输
- 器官健康信息运输

AI Blood 不是：

- 数据库
- 普通日志
- 单一消息队列
- 一个固定中间件
- 所有内部通信的统一替代品

它更接近：

> **一套跨器官的 circulation contract（循环契约）+ transport envelope（运输信封）+ pressure model（压力模型）+ exchange rules（交换规则）。**

---

# 2. AI Blood ≠ Data（AI血液不等于数据）

这是 AIP-004 最重要的一条。

在人类身体里：

- 血液不是氧气；
- 血液不是葡萄糖；
- 血液不是激素；
- 血液不是免疫细胞。

血液是承载这些东西的循环介质。

同样：

> **Data（数据）只是 AI Blood 中的一类 payload（载荷）。**

因此必须区分：

### Transport Medium（运输介质）
负责“怎么流”。

### Payload（载荷）
负责“流的是什么”。

### Organ Exchange（器官交换）
负责“器官如何摄取、加工、释放”。

---

# 3. 哪些东西应该进入 AI Blood

并不是所有内部状态都应该进入全身循环。

AIP-004 v0.2 把内部状态分成三层。

## 3.1 Local State（局部状态）

只在一个 Cell / Tissue / Organ 内部使用。

例如：

- 某个模型内部 KV cache
- 一个局部 tool retry counter（工具重试计数器）
- 某个视觉模型的中间 feature map（特征图）
- 一个局部控制器的瞬时 PID 状态

原则：

> **默认不进入 AI Blood。**

否则整个系统会被无意义状态淹没。

---

## 3.2 Circulating State（循环状态）

需要跨器官传输，但不必成为全身生命体征。

例如：

- 当前任务状态
- 工具结果
- 记忆候选项
- 风险标记
- 调度优先级
- 资源申请
- 器官健康摘要
- 数据来源与可信度
- 中间推理结果

这些是 AI Blood 的主要载荷。

---

## 3.3 Organism-wide State（全身状态）

需要进入 organism-level regulation（生命体级调节）的少量关键状态。

例如：

- compute stress（算力压力）
- memory integrity（记忆完整性）
- security alert level（安全警戒等级）
- recovery capacity（恢复能力）
- task overload（任务过载）
- energy/resource pressure（能源/资源压力）

这些状态会进一步进入 AIP-005 Artificial Homeostasis（人工稳态）。

原则：

> **不是所有 circulating state 都有资格成为 vital sign（生命体征）。**

---

# 4. 四类内部通信中，AI Blood 只负责其中一部分

AI Physiology 目前定义四张全身网络：

1. Neural Plane（神经网）
2. Circulatory Plane（循环网）
3. Hormonal Plane（内分泌网）
4. Immune/Lymph Plane（免疫/淋巴网）

AI Blood 主要属于：

# Circulatory Plane（循环网）

因此不应该把所有通信都塞进 AI Blood。

---

## 4.1 Neural Plane（神经网）

特点：

- 快
- 定向
- 低延迟
- 命令性强

例如：

> “停止机械臂。”

这种消息应该走 Neural Plane，而不是等 AI Blood 慢慢循环。

---

## 4.2 Circulatory Plane（循环网）

特点：

- 持续
- 可观测
- 跨器官
- 承载多种 payload

例如：

- 当前任务上下文
- Memory candidate（记忆候选）
- Health summary（健康摘要）
- Resource allocation（资源分配）
- Provenance（来源）
- Intermediate result（中间结果）

这是 AI Blood 的核心范围。

---

## 4.3 Hormonal Plane（内分泌网）

特点：

- 慢
- 广播
- 持续
- 以模式和状态调节为主

例如：

```yaml
organism_mode: STRESS
level: 0.72
ttl: 600
```

它可以借用同一底层 transport（传输底座），但在逻辑上不等于 AI Blood 普通业务载荷。

---

## 4.4 Immune/Lymph Plane（免疫/淋巴网）

特点：

- 异常
- 风险
- 隔离
- 质量控制
- 修复

高风险对象不应该无限制回到普通 AI Blood。

它可能被转入：

> quarantine pool（隔离池） / lymph channel（淋巴通道）

等待进一步处理。

---

# 5. AI Blood Envelope v0.2（AI血液信封）

当前建议的最小结构：

```yaml
blood_packet:
  packet_id: string
  organism_id: string

  source:
    cell_id: string|null
    organ_id: string
    organ_type: string

  destination:
    scope: local|organ|multi_organ|organism
    organ_ids: []
    capability_tags: []

  payload:
    type: string
    schema_version: string
    body: any

  classification:
    state_scope: circulating|organism_wide
    physiological_class: nutrient|resource|task|result|health|risk|identity|regulatory|waste
    sensitivity: public|internal|restricted|critical

  circulation:
    priority: 0
    ttl_ms: 0
    max_hops: 0
    created_at: timestamp
    expires_at: timestamp|null

  provenance:
    producer: string
    source_type: user|sensor|model|tool|organ|system
    confidence: 0.0
    lineage: []
    signature: string|null

  health_context:
    source_health: healthy|degraded|stressed|injured|recovering|critical
    organism_mode: string|null

  risk_context:
    risk_level: 0.0
    quarantine_required: false
    immune_tags: []

  resource_context:
    compute_cost: number|null
    token_cost: number|null
    memory_cost: number|null
    bandwidth_cost: number|null
```

这不是最终协议，只是 v0.2 的 reference schema（参考模式）。

---

# 6. 为什么必须带 Provenance（来源）

长期运行的 AI 最大风险之一是：

> 系统内部后来已经不知道“这条信息到底从哪来的”。

因此进入 AI Blood 的 circulating payload（循环载荷）至少应该能回答：

- 谁生成的？
- 什么时候生成的？
- 是用户、模型、工具还是传感器产生的？
- 中间经过哪些器官？
- 是否被修改过？
- 当前可信度如何？

这就是：

# Provenance（来源链）

未来如果出现 memory poisoning（记忆污染）或错误传播，系统才有机会倒查。

---

# 7. AI Blood 的“寿命”

并不是所有信息都应该永远留在循环里。

因此每个 packet（包）至少应该有：

- created_at（创建时间）
- expires_at（过期时间）
- ttl（存活时间）
- max_hops（最大跳数）

可以把它理解成：

> **AI Blood 中的载荷也有半衰期。**

例如：

### 短寿命
实时控制状态、临时工具结果。

### 中寿命
任务上下文、阶段结果。

### 长寿命
身份信息、经过验证的知识、关键事件。

一条信息是否进入长期 Memory（记忆），应该是另外一个过程。

---

# 8. Organ Exchange（器官交换）

器官与 AI Blood 的关系，不应只有：

> send / receive（发送 / 接收）

更适合使用四个词：

## 8.1 Uptake（摄取）

器官从 AI Blood 中主动获取它需要的 payload。

例如：

Memory Organ（记忆器官）摄取高价值事件。

---

## 8.2 Transform（加工）

器官对摄入内容进行处理。

例如：

Liver-like Organ（肝式器官）：

- 清洗
- 规范化
- 去毒
- 归一化
- 标注 provenance
- 降噪

---

## 8.3 Release（释放）

器官把新的状态或处理结果重新释放进循环。

---

## 8.4 Reject（拒绝）

器官发现不符合要求的载荷时：

- 拒绝摄取
- 降低可信度
- 转入 quarantine（隔离）
- 通知 immune system（免疫系统）

---

# 9. Exchange Policy（交换策略）

每个 AI Organ（AI器官）应该声明自己的交换策略。

示例：

```yaml
exchange_policy:
  accepts:
    - payload.type: task_result
    - payload.type: memory_candidate

  rejects:
    - sensitivity: critical

  uptake_conditions:
    min_confidence: 0.75
    max_risk_level: 0.30

  transforms:
    - normalize
    - validate
    - deduplicate

  releases:
    - validated_memory
    - health_summary
```

这部分后面会进入 AIP-006 Organ Interface（器官接口）。

---

# 10. AI Blood Pressure（AI血压）

如果使用“血液”这个概念，就必须定义什么叫 pressure（压力），否则只是比喻。

AIP-004 v0.2 暂时把 AI Blood Pressure 定义为：

> **单位时间内内部循环需求相对于当前循环处理能力的压力状态。**

它不是一个单一指标，至少可以由以下变量组成：

```
queue_depth
message_rate
average_latency
p95_latency
dropped_packets
retry_rate
bandwidth_utilization
processing_backlog
priority_inversion
```

可以先形成一个 composite pressure（综合压力）：

```
BloodPressure =
f(queue_depth,
  latency,
  bandwidth_utilization,
  retry_rate,
  backlog)
```

这里先不急着规定最终数学公式。

---

# 11. Blood Pressure 状态

v0.2 暂时定义四档：

### NORMAL（正常）
循环容量充足。

### ELEVATED（升高）
出现持续排队和延迟。

### HIGH（高压）
关键器官开始受到影响。

### CRITICAL（危急）
需要 organism-level response（生命体级响应）。

例如 CRITICAL 时可能触发：

- 停止低优先级任务；
- 降低非关键 context 流量；
- 延迟 Memory consolidation（记忆固化）；
- 限制新 Agent spawn（新智能体生成）；
- 切换到 STRESS hormone mode（压力激素模式）；
- 扩容 transport/runtime。

这就开始和 AIP-005 Artificial Homeostasis（人工稳态）连起来。

---

# 12. AI Blood Flow（AI血流）

除了压力，还需要 flow（流量）。

候选生命参数包括：

- packets/sec
- bytes/sec
- useful_payload_ratio
- stale_payload_ratio
- rejected_payload_ratio
- quarantined_payload_ratio
- organ-to-organ latency
- circulation completion time

这里面有一个我认为比较重要的指标：

# Useful Circulation Ratio（有效循环比）

```
有效循环载荷
----------------
总循环载荷
```

如果系统每天 90% 都是在搬运无效 context、重复日志和过期状态，那么即使吞吐量很高，也不是健康循环。

---

# 13. AI Blood Oxygenation（AI血液“含氧量”）暂不定义

人体血氧很重要，但在 AI 系统里目前没有足够清楚的一一对应。

可能候选：

- 可用算力
- 可用能源
- 可用 token budget
- 低延迟计算容量

但现在直接叫 “AI oxygen（AI氧气）” 会过度类比。

所以 v0.2 暂不定义。

原则：

> **没有明确工程收益的生物映射，不进入规范。**

---

# 14. Waste（废物）也可以进入 AI Blood

人体代谢废物会进入血液，再送到肾、肝、肺等器官处理。

AI 里也可能有类似东西：

- stale context（过期上下文）
- duplicate memory（重复记忆）
- failed task artifacts（失败任务产物）
- invalid intermediate result（无效中间结果）
- corrupted state（损坏状态）
- low-confidence residue（低置信残留）
- obsolete plan（过期计划）

这些可以被标记：

```yaml
physiological_class: waste
```

然后由 Kidney / Liver / Immune-like organs（肾/肝/免疫式器官）处理。

---

# 15. Circulatory Contamination（循环污染）

如果错误内容进入循环并被多个器官不断复用，会出现：

# Circulatory Contamination（循环污染）

例如：

```
错误工具输出
↓
进入 AI Blood
↓
Memory 摄取
↓
Planner 使用
↓
生成新错误
↓
再次进入循环
```

最终错误可能不断自我放大。

因此必须有：

- provenance
- confidence
- expiry
- validation
- quarantine
- lineage tracing

这也是为什么 AI Blood 不能只是消息队列。

---

# 16. Circulatory Identity（循环身份）

所有 packet 都必须明确属于哪个 organism：

```yaml
organism_id: string
```

原因很简单：

未来一个 infrastructure（基础设施）上可能同时运行多个 AI Organism。

如果没有清晰 organism boundary（生命体边界），就会出现：

- 跨生命体 Memory 污染；
- 身份混淆；
- 权限串联；
- 状态泄漏。

因此：

> **AI Blood 必须有 organism-level namespace（生命体级命名空间）。**

---

# 17. Organism Boundary（生命体边界）

AI Blood 能否跨出 organism boundary？

默认：

# NO

跨生命体通信应该先经过：

- external interface（外部接口）
- identity verification（身份验证）
- policy check（规则检查）
- data transformation（数据转换）

然后作为新的 external input（外部输入）进入另一生命体。

否则两个 AI Organism 的循环系统实际上就混成一个了。

---

# 18. Failure Modes（失败模式）

AIP-004 当前定义至少八类故障：

## F1. Congestion（拥塞）
循环需求超过处理能力。

## F2. Contamination（污染）
错误、恶意或损坏 payload 扩散。

## F3. Staleness（陈旧）
大量过期状态仍然继续循环。

## F4. Starvation（饥饿）
某些关键器官长期得不到资源或状态。

## F5. Flooding（洪泛）
某个器官持续产生过多 payload。

## F6. Circulation Break（循环中断）
器官之间无法完成必要交换。

## F7. Identity Leakage（身份泄漏）
跨 organism 的 payload 被错误混入。

## F8. Priority Inversion（优先级倒置）
低价值载荷长期占据循环资源，影响关键任务。

---

# 19. Minimum Health Metrics（最小健康指标）

任何 AI Blood 实现至少 SHOULD 暴露：

```yaml
blood_health:
  pressure_state:
  message_rate:
  queue_depth:
  p50_latency:
  p95_latency:
  drop_rate:
  retry_rate:
  stale_ratio:
  contamination_events:
  quarantine_rate:
  useful_circulation_ratio:
  critical_organ_starvation:
```

这些指标后续可以部分提升成 AI Vital Signs（AI生命体征）。

---

# 20. Reference Implementation（参考实现）暂不绑定技术栈

AIP-004 不规定一定使用：

- Kafka
- NATS
- Redis Streams
- RabbitMQ
- gRPC
- HTTP
- MCP
- custom event bus（自定义事件总线）

这些只是 implementation choices（实现选择）。

一个实现可以：

- Neural Plane 用 gRPC；
- Circulatory Plane 用 NATS / Kafka；
- Hormonal Plane 用 broadcast topic（广播主题）；
- Immune/Lymph Plane 用独立 risk channel（风险通道）。

AIP 定义的是：

> **physiological contract（生理契约）**

而不是某个具体中间件。

---

# 21. Minimal AI Blood v0.2（最小AI血液）

如果现在做第一个 prototype（原型），我建议不要把所有东西都做进去。

最小版本只需要：

### 必须有
1. organism_id
2. source organ
3. destination scope
4. payload type
5. provenance
6. confidence
7. risk level
8. TTL
9. priority
10. health metrics

### 先不做
- 完整加密体系
- 全部四张网
- 复杂数学血压模型
- 全生命周期 lineage
- 跨 organism circulation

先验证一个问题：

> **相比普通 message bus（消息总线），带有生理分类、来源、风险、寿命和压力调节的循环层，是否能让长期 Agent 系统更稳定？**

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
+
Message Bus
```

## AI Blood Agent

```
LLM
+
Memory
+
Tools
+
AI Blood Layer
```

给两个系统连续运行长期任务。

持续加入：

- noisy data（噪声数据）
- stale data（过期数据）
- conflicting task（冲突任务）
- bad tool result（错误工具结果）
- high load（高负载）
- malicious payload（恶意载荷）

比较：

- error propagation（错误传播）
- stale state accumulation（陈旧状态积累）
- memory contamination（记忆污染）
- recovery time（恢复时间）
- dropped critical task（关键任务丢失）
- operator intervention（人工介入）
- compute / token cost（算力 / token 成本）

如果 AI Blood Layer 没有带来长期稳定性收益：

> **AIP-004 的设计就需要被修改。**

---

# 23. 与 AIP-005 / AIP-006 的边界

## AIP-004 负责
**怎么流。**

## AIP-005 Artificial Homeostasis（人工稳态）负责
**什么时候需要调节，以及调节到什么范围。**

## AIP-006 Organ Interface（器官接口）负责
**每个器官如何接入循环、暴露状态、接受调节。**

三者关系：

```
AIP-006 Organ
      │
      │ uptake / release
      ▼
AIP-004 AI Blood
      │
      │ vital state
      ▼
AIP-005 Homeostasis
      │
      │ regulatory action
      ▼
AIP-006 Organ
```

形成第一个真正的生理闭环。

---

# 24. 当前仍未解决的问题

v0.2 暂时保留这些开放问题：

1. 一个 transport schema 是否足够支撑所有器官？
2. Circulatory Plane 和 Hormonal Plane 是否应该物理隔离？
3. AI Blood Pressure 最合理的数学定义是什么？
4. 什么 payload 有资格成为 organism-wide state？
5. Memory 应该直接摄取 AI Blood，还是必须先经过 Liver-like validation（肝式验证）？
6. 如何定义“循环速度过快”而不仅是“过慢”？
7. AI Blood 是否需要类似 blood type（血型）的兼容性机制？
8. 多个 AI Organism 合并时，内部循环如何融合？
9. 一个 AI Organism 分裂时，AI Blood lineage（循环谱系）如何继承？
10. 在物理机器人中，数字循环与电力/热管理是否应该看成两套不同 circulatory systems（循环系统）？

---

# 25. v0.2 的一句话定义

> **AI Blood（AI血液）不是“数据”的拟人化称呼，而是 AI 生命体内部用于跨器官持续运输状态、资源、任务、风险和中间产物，并携带来源、寿命、优先级和健康信息的标准化循环介质。**

英文：

> **AI Blood is a standardized internal circulation medium for transporting physiological payloads among organs of an AI organism, with explicit provenance, lifetime, priority, risk, identity, and health context.**

---

# 26. 证伪条件

AIP-004 不应成为一个无法被反驳的概念。

如果未来实验发现：

1. 普通事件总线已经足以实现长期稳定 AI；
2. provenance / TTL / physiological classification 等机制没有显著收益；
3. 独立循环层反而显著增加复杂度与故障率；
4. 器官之间并不需要持续共享状态；
5. organism-level homeostasis 不依赖循环层；

那么：

> **AI Blood 作为独立架构层就不成立，应该退化成普通 messaging / state infrastructure（消息/状态基础设施）。**

这条保留。

因为只有存在明确的失败条件，AIP-004 才是工程假设，而不是一个漂亮比喻。
