# AIP-006: Organ Interface（器官接口）v0.2

**Status:** Draft  
**Version:** 0.2  
**Scope:** AI Organ（AI器官）之间的标准接口、自治边界、健康状态、交换规则与替换机制

---

# 0. 为什么需要 Organ Interface（器官接口）

如果 AI Physiology（人工智能生理学）最后只是：

- AI Brain（AI大脑）
- AI Kidney（AI肾）
- AI Liver（AI肝）
- AI Immune System（AI免疫系统）

这些名字摆在一张图上，那它仍然只是类比。

真正进入工程以后，每个 Organ（器官）至少要能回答：

1. 我是谁；
2. 我负责什么；
3. 我接收什么；
4. 我输出什么；
5. 我能自己决定什么；
6. 我现在健康吗；
7. 我什么时候需要上报；
8. 我怎么和 AI Blood（AI血液）交换；
9. 我接受哪些 Hormonal Signals（内分泌信号）；
10. 我坏了以后能不能隔离、修复、替换。

所以 AIP-006 的目标不是规定器官内部怎么实现，而是定义：

> **一个器官要想进入 AI Organism（AI生命体），至少要暴露什么。**

---

# 1. 定义

**Organ Interface（器官接口）** 是 AI Organ（AI器官）向 AI Organism（AI生命体）公开的标准契约，用于描述：

- identity（身份）
- function（职责）
- inputs / outputs（输入 / 输出）
- local state（局部状态）
- health（健康状态）
- autonomy（自治范围）
- circulation exchange（循环交换）
- hormonal receptors（内分泌受体）
- immune hooks（免疫接口）
- escalation（升级机制）
- lifecycle（生命周期）
- replaceability（可替换性）
- identity dependency（身份依赖）

接口的目标是：

> **让器官能够被监测、调节、隔离、修复、替换，而不要求外部系统理解它的全部内部实现。**

---

# 2. Organ ≠ Module（器官不等于模块）

普通软件模块通常只关心：

- function
- input
- output
- error

器官还必须额外关心：

- 自身健康；
- 自身资源；
- 自身局部稳态；
- 与其他器官的长期依赖；
- 是否可隔离；
- 是否可替换；
- 自己失效会不会拖死整个生命体。

所以一个普通 API wrapper（接口封装）通常不能直接叫 Organ。

AIP-003 已经定义：

> 器官必须承担稳定、专门、可持续的生理职责，并参与 organism-level homeostasis（生命体级稳态）。

AIP-006 则把这个要求变成接口。

---

# 3. Organ Interface v0.2 最小结构

```yaml
organ:
  identity:
    organ_id: string
    organism_id: string
    organ_type: string
    version: string
    scale: cell|tissue|organ|organ_system

  function:
    responsibilities: []
    capabilities: []
    dependencies: []

  io:
    inputs: []
    outputs: []

  state:
    local_state_schema: {}
    exposed_state: []

  health:
    status: healthy|degraded|stressed|injured|quarantined|recovering|critical|offline
    vital_variables: []
    debt: {}
    recovery_reserve: {}

  autonomy:
    allowed_actions: []
    forbidden_actions: []
    approval_required: []
    local_decision_scope: []

  circulation:
    uptake_policy: {}
    release_policy: {}
    transform_policy: {}
    reject_policy: {}

  hormonal:
    receptors: []
    emitted_signals: []

  immune:
    inspection_hooks: []
    quarantine_behavior: {}
    self_signature: {}

  escalation:
    warning_conditions: []
    critical_conditions: []
    escalation_targets: []

  lifecycle:
    created_at: timestamp
    lifecycle_state: initializing|active|degraded|repairing|retiring|offline
    replaceable: boolean
    replacement_strategy: string|null
    state_transfer_policy: {}

  identity_dependency:
    organism_identity_dependency: low|medium|high|critical
    continuity_requirements: []
```

这个结构仍然只是 reference schema（参考模式），后续实现可以用 YAML、JSON、protobuf 或其他形式。

---

# 4. Identity（身份）

器官必须明确两个身份：

## 4.1 Organ Identity（器官身份）

例如：

```yaml
organ_id: memory-organ-01
organ_type: memory
version: 0.3.2
```

## 4.2 Organism Identity（生命体身份）

```yaml
organism_id: organism-alpha
```

原因很重要：

> 同一种器官可能同时存在多个实例，但它们必须知道自己属于哪个 Organism（生命体）。

否则容易产生：

- Memory 串写；
- 权限污染；
- 状态串线；
- 多 AI 之间的身份混淆。

---

# 5. Function（职责）

一个 Organ 必须清楚声明自己：

### Responsibilities（职责）
长期负责什么。

### Capabilities（能力）
可以执行什么动作。

### Dependencies（依赖）
依赖哪些器官、资源或外部系统。

示例：

```yaml
function:
  responsibilities:
    - long_term_memory_storage
    - memory_validation

  capabilities:
    - retrieve
    - consolidate
    - quarantine

  dependencies:
    - ai_blood
    - storage_layer
    - immune_service
```

这里要避免一种常见问题：

> capability（能做什么）很多，但 responsibility（应该长期负责什么）很模糊。

没有稳定责任，就不适合称为器官。

---

# 6. Inputs / Outputs（输入 / 输出）

接口必须定义：

- 接收什么；
- 从哪里来；
- 输出什么；
- 输出给谁。

但 AIP-006 不建议只写传统：

```
input: string
output: json
```

而应该至少声明：

- payload type（载荷类型）
- source scope（来源范围）
- trust requirement（可信要求）
- freshness requirement（新鲜度要求）
- risk tolerance（风险容忍度）

例如：

```yaml
inputs:
  - type: memory_candidate
    source: circulatory_plane
    min_confidence: 0.75
    max_age_sec: 3600
    max_risk_level: 0.30
```

---

# 7. Local State（局部状态）

器官可以拥有大量内部状态。

但不应该全部暴露。

AIP-006 要求区分：

## Private Local State（私有局部状态）

只在器官内部使用。

## Exposed Organ State（公开器官状态）

其他器官或 Homeostasis Layer（稳态层）可以读取。

## Organism-wide Vital State（全身关键状态）

只有少数状态会上升到 AIP-005 的 AI Vital Signs（AI生命体征）。

这个区分很重要，因为：

> **AI生命体并不需要“意识到”每一个内部变量。**

就像人不会实时意识到每个细胞的状态。

---

# 8. Health State（健康状态）

v0.1 只有：

- healthy
- degraded
- critical
- offline

这太粗了。

v0.2 改成：

### HEALTHY（健康）
功能、资源、质量正常。

### DEGRADED（退化）
还能工作，但性能或质量持续下降。

### STRESSED（压力）
当前负载或环境压力显著升高，但尚未形成明确损伤。

### INJURED（受损）
出现明确内部损伤，需要修复。

### QUARANTINED（隔离）
器官被限制与整体系统交换。

### RECOVERING（恢复）
正在修复、回滚或重新同步。

### CRITICAL（危急）
继续运行可能影响全身。

### OFFLINE（离线）
不再提供功能。

---

# 9. 为什么 DEGRADED（退化）和 STRESSED（压力）要分开

这和我们前面讨论的 AI Chronic Disease（AI慢性病）很有关。

### STRESSED（压力）

更像短期：

> 最近任务太多，所以我变慢。

### DEGRADED（退化）

更像长期：

> 我已经持续一个月越来越慢、越来越乱，即使压力下降也没有完全恢复。

如果不区分这两种状态，就很难识别：

- chronic degradation（慢性退化）
- homeostatic debt（稳态债务）
- aging（衰老）

---

# 10. Organ Vital Variables（器官关键变量）

每个器官应该声明自己的局部 vital variables（关键变量）。

例如 Memory Organ（记忆器官）：

```yaml
vital_variables:
  - memory_integrity
  - duplication_ratio
  - retrieval_latency
  - stale_memory_ratio
```

AI Blood Organ（循环器官）：

```yaml
vital_variables:
  - pressure
  - flow
  - stale_payload_ratio
  - starvation_events
```

局部 vital variable 不一定自动成为 organism-level vital sign。

---

# 11. Homeostatic Debt（稳态债务）

每个器官应该允许暴露：

```yaml
health:
  debt:
    level: 0.0
    sources: []
    estimated_recovery_cost: null
```

这里的 debt（债务）指：

> 暂时还能运行，但内部维护问题持续积累。

例如 Memory Organ：

- 重复记忆越来越多；
- 过期内容没有清理；
- 冲突知识一直没解决；
- provenance 缺失。

这些问题今天不一定让系统报错。

但长期会导致：

> **AI慢性病。**

---

# 12. Recovery Reserve（恢复储备）

器官还应该声明自己现在有多少恢复能力。

示例：

```yaml
recovery_reserve:
  rollback_available: true
  backup_state_available: true
  spare_capacity: 0.35
  alternate_instance_available: false
```

一个器官可能：

> 当前 HEALTHY，但 recovery reserve 已经很低。

这种情况其实也不健康。

---

# 13. Autonomy（自治边界）

这是 AIP-006 最关键的新增字段之一。

器官不能只有 capabilities（能力）。

还必须知道：

> **哪些事情我可以自己决定，哪些事情必须上报。**

示例：

```yaml
autonomy:
  allowed_actions:
    - remove_stale_memory
    - deduplicate_memory

  approval_required:
    - delete_high_value_memory

  forbidden_actions:
    - alter_organism_identity

  local_decision_scope:
    max_memory_delete_ratio: 0.05
```

这可以防止：

> 器官为了自身健康，伤害整个生命体。

---

# 14. Local Autonomy（局部自治）原则

AIP-006 推荐：

> **能局部解决的问题，尽量局部解决。**

例如：

- tool retry（工具重试）
- cache cleanup（缓存清理）
- minor memory deduplication（轻量记忆去重）
- local anomaly filtering（局部异常过滤）

都不应该每次交给中央 LLM 决定。

只有当：

- 超出自治阈值；
- 影响其他器官；
- 涉及身份；
- 涉及高风险动作；

才升级。

---

# 15. Escalation（升级机制）

每个器官必须明确：

> 什么情况下我不再自己处理。

例如：

```yaml
escalation:
  warning_conditions:
    - memory_integrity < 0.95

  critical_conditions:
    - memory_integrity < 0.80
    - corruption_spread == true

  escalation_targets:
    - homeostasis_layer
    - immune_system
```

---

# 16. Circulatory Interface（循环接口）

AIP-006 与 AIP-004 的连接在这里。

每个器官至少要定义四类交换：

## Uptake（摄取）
我从 AI Blood 中拿什么。

## Transform（加工）
我能对载荷做什么处理。

## Release（释放）
我向 AI Blood 放什么。

## Reject（拒绝）
什么情况我不接受。

示例：

```yaml
circulation:
  uptake_policy:
    accepts:
      - memory_candidate

  transform_policy:
    actions:
      - validate
      - deduplicate

  release_policy:
    produces:
      - validated_memory
      - health_summary

  reject_policy:
    max_risk_level: 0.30
```

---

# 17. Hormonal Receptors（内分泌受体）

器官必须声明自己响应哪些 organism mode（生命体模式）。

例如：

```yaml
hormonal:
  receptors:
    - signal: STRESS
      response:
        - reduce_noncritical_work

    - signal: RECOVERY
      response:
        - pause_background_tasks

    - signal: SLEEP
      response:
        - run_maintenance
```

关键点：

> Hormonal Signal（内分泌信号）不是具体命令。

同一个 STRESS 信号：

- Brain 减少深推理；
- Memory 降低写入；
- Growth System 暂停扩张；
- Immune System 提高警觉。

这就是“广播+受体”。

---

# 18. Immune Interface（免疫接口）

每个器官都应该允许 Immune System（免疫系统）进行有限检查。

至少应支持：

- health inspection（健康检查）
- provenance inspection（来源检查）
- quarantine（隔离）
- self signature verification（自我签名验证）

示例：

```yaml
immune:
  self_signature:
    organ_type: memory
    trusted_version: 0.3.2

  inspection_hooks:
    - check_state_integrity
    - check_payload_origin

  quarantine_behavior:
    allow_read: false
    allow_write: false
    preserve_state_snapshot: true
```

---

# 19. Replaceability（可替换性）

人可以换人工关节、换心脏瓣膜；云系统也会替换机器。

所以每个 Organ 都应该声明：

```yaml
replaceable: true
replacement_strategy: hot_swap
```

候选策略：

### Hot Swap（热替换）
不中断整体运行。

### Warm Swap（温替换）
短暂降级后恢复。

### Cold Replace（冷替换）
需要停止相关功能。

### Non-replaceable（不可替换）
替换将严重影响 organism identity 或完整性。

---

# 20. State Transfer（状态迁移）

替换器官最大的难点，不是“启动新实例”。

而是：

> **旧器官的哪些状态必须带过去。**

需要区分：

### Functional State（功能状态）
为了继续工作必须迁移。

### Historical State（历史状态）
可以迁移，也可以归档。

### Identity State（身份状态）
如果丢失，可能影响整个生命体连续性。

示例：

```yaml
state_transfer_policy:
  required:
    - validated_memory_index
    - access_policy

  optional:
    - historical_metrics

  prohibited:
    - corrupted_cache
```

---

# 21. Identity Dependency（身份依赖）

这个字段非常重要。

并不是所有器官对“我还是不是我”影响一样。

例如：

### LOW
普通 cache organ（缓存器官）。

换了基本不影响身份。

### MEDIUM
tool routing organ（工具路由器官）。

替换可能影响行为风格。

### HIGH
long-term memory organ（长期记忆器官）。

替换必须保证关键记忆连续性。

### CRITICAL
identity / constitutional layer（身份 / 宪法层）。

错误替换可能意味着：

> 原来的 AI 已经不再连续存在。

---

# 22. Organ Dependency Graph（器官依赖图）

器官不能只声明“我依赖谁”。

整个系统还应该形成：

# Organ Dependency Graph（器官依赖图）

例如：

```
Memory
 ├── AI Blood
 ├── Storage
 └── Immune

Planner
 ├── Memory
 ├── Brain
 └── AI Blood
```

这样故障时可以判断：

> 一个器官离线后，会影响哪些器官。

---

# 23. Organ Failure Propagation（器官故障传播）

AIP-006 需要开始考虑：

> 器官“生病”会不会传染到其他器官。

例如：

```
Memory contamination
↓
Planner 读到错误记忆
↓
Tool 执行错误动作
↓
错误结果重新进入 AI Blood
↓
Memory 再次吸收
```

这其实就是：

# Cross-organ Pathology（跨器官病理）

以后 AI Chronic Disease（AI慢性病）很可能大量来自这种长期相互影响。

---

# 24. Chronic Degradation（慢性退化）

这是 v0.2 特别增加的一部分。

器官不能只记录：

> 当前 status = HEALTHY

还应该记录：

```yaml
health_history:
  baseline_performance:
  current_performance:
  degradation_rate:
  debt_trend:
  recovery_trend:
```

如果一个器官：

- 还能运行；
- 但是性能持续下降；
- 稳态债务持续增加；
- 恢复储备持续下降；

那它可能处于：

# Chronic Degradation（慢性退化）

而不是普通 transient stress（短期压力）。

---

# 25. Organ Aging（器官衰老）

目前先做一个最小定义：

> **Organ Aging（器官衰老）是器官在长期运行中，即使不存在单次严重故障，其性能、恢复能力、状态质量或维护成本仍持续恶化的过程。**

候选指标：

- degradation rate
- recovery time trend
- debt accumulation
- maintenance frequency
- replacement frequency
- error recurrence

这个以后应该和 Lifecycle（生命周期）单独做 AIP。

---

# 26. Organ Contract（器官契约）

AIP-006 的最终目标，可以理解为：

> 每个器官都有一份 contract（契约）。

它不规定你内部用什么语言、什么框架。

它只规定：

- 你是谁；
- 你负责什么；
- 你现在健康不健康；
- 你能自己做什么；
- 你如何交换状态；
- 你什么时候上报；
- 你如何被隔离；
- 你如何被替换；
- 替换后怎样证明还是同一个 organism 的组成部分。

---

# 27. Minimum Organ Interface（最小器官接口）

Minimal Artificial Organism（最小人工生命体）第一版不需要实现全部字段。

至少实现：

```
organ_id
organism_id
organ_type
responsibilities
health.status
vital_variables
autonomy.allowed_actions
escalation
circulation.uptake
circulation.release
replaceable
```

这就够做第一轮实验。

---

# 28. 第一个 Organ Interface 实验

做两个版本。

## Baseline Component（普通组件）

```
input
output
error
```

## AI Organ（AI器官）

```
input
output
health
vital variables
autonomy
escalation
AI Blood exchange
replacement
```

然后故意注入：

- 长期负载；
- 状态污染；
- 局部异常；
- 版本切换；
- 器官掉线；
- 资源不足。

看系统能否：

- 提前发现退化；
- 局部处理；
- 避免故障传播；
- 顺利隔离；
- 正确替换；
- 保持 organism identity continuity（生命体身份连续性）。

---

# 29. 与 AIP-004 / AIP-005 的关系

三份规范现在已经形成一个最小闭环：

```
        AIP-006 Organ
            │
            │ health / state
            ▼
      AIP-004 AI Blood
            │
            │ circulating state
            ▼
AIP-005 Artificial Homeostasis
            │
            │ regulation
            ▼
        AIP-006 Organ
```

更完整一点：

```
Organ
↓
Local Vital Variables
↓
AI Blood
↓
Organism Vital Signs
↓
Homeostasis
↓
Hormonal / Neural Signal
↓
Organ Local Response
↓
AI Blood
↓
New State
```

这已经是第一版 AI Physiology Runtime（人工智能生理运行时）的骨架。

---

# 30. 证伪条件

AIP-006 也必须允许被否定。

如果长期实验发现：

1. 普通模块接口已经足够；
2. health / autonomy / replaceability 等字段没有显著提高可靠性；
3. 器官契约带来的复杂度超过收益；
4. 局部自治反而增加冲突；
5. 统一 Organ Interface 无法覆盖不同类型器官；

那么：

> AIP-006 不应该成为强制统一接口，而应该退化为一组 optional physiological traits（可选生理特征）。

---

# 31. v0.2 一句话定义

> **Organ Interface（器官接口）是 AI 生命体内部器官向整个生命体暴露职责、状态、健康、自治、循环交换、调节、隔离、替换与身份连续性的标准契约。**

英文：

> **An Organ Interface is the standard contract through which an AI organ exposes its function, state, health, autonomy, circulation exchange, regulation, isolation, replacement, and continuity requirements to the larger AI organism.**

---

# 32. 当前开放问题

1. 所有器官是否真的可以共享同一个基础接口？
2. 一个 Organ 可以同时属于多个 Organ System 吗？
3. Organ health 由自己报告，还是必须有外部 auditor（审计器）？
4. 如何防止器官伪造自己的健康状态？
5. identity_dependency 应该怎样客观测量？
6. 如何判断 chronic degradation（慢性退化）与正常适应之间的边界？
7. Organ aging（器官衰老）究竟是软件问题、数据问题还是模型问题？
8. 一个器官是否可以自主申请 replacement（替换）？
9. 多器官同时退化时，哪个先修？
10. 是否需要 Organ Genome（器官基因）之类的配置与继承机制？

---

# 33. 一个值得继续保留的问题：AI慢性病

做到这一版以后，我觉得 AI Chronic Disease（AI慢性病）已经不只是一个形象说法。

至少可以先把它定义成：

> **AI Chronic Disease（AI慢性病）是 AI Organism 或其一个/多个器官在长期运行中形成的持续性功能退化状态。系统仍然能够工作，但健康指标长期偏离优选范围、稳态债务不断积累、恢复储备逐步下降，并且无法通过一次简单重启或短期调节彻底恢复。**

这个现象其实比“某次回答错误”更接近长期 AI 系统真正的问题。

后面 Minimal Artificial Organism（最小人工生命体）实验里，我建议专门设计一个慢性退化场景，而不是只测 crash（崩溃）。

因为真正有意思的问题可能是：

> **AI为什么会越用越“脏”、越用越“乱”、越用越难维护？**

这可能正是 AI Physiology 值得继续做下去的一个非常实际的切入口。
