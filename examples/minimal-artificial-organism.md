# Minimal Artificial Organism v0.1（最小人工生命体 v0.1）

**Status:** Draft  
**Version:** 0.1  
**Purpose:** 用最小系统验证 AI Physiology（人工智能生理学）是否能带来长期稳定性收益，而不是追求完整仿生。

---

# 0. 先定义目标：不是“造一个数字人”

Minimal Artificial Organism（最小人工生命体，MAO）不是完整 AI Organism 的缩小版人体。

它只保留一个最关键问题：

> **如果给长期 Agent 增加循环、稳态、器官健康、局部自治和恢复机制，它是否比普通 Agent 更稳定、更可恢复、更少依赖人工维护？**

如果这个问题都得不到正面结果，后面继续增加“肝、肾、免疫、内分泌”等概念就没有意义。

所以 v0.1 只做最小闭环，不追求器官齐全。

---

# 1. v0.1 的最小组成

MAO v0.1 由 6 个核心单元组成。

## 1.1 Brain（大脑）
负责：
- 语言理解
- 推理
- 规划
- 任务分解
- 高层决策

第一版可直接使用任意 LLM。

Brain 不是整个 Organism，只是高级认知器官。

---

## 1.2 Runtime / Heart（运行时 / 心脏）
负责：
- 持续运行
- 事件驱动
- 调度
- 任务循环
- 器官状态轮询
- 保证整个系统“还在动”

第一版可以非常简单，本质上是 persistent event loop（持续事件循环）。

---

## 1.3 AI Blood（AI血液）
负责：
- 跨器官状态传输
- task / result / health / risk 等 payload（载荷）循环
- provenance（来源）
- TTL（存活时间）
- priority（优先级）
- risk context（风险上下文）

直接遵循 AIP-004 v0.2。

---

## 1.4 Homeostasis Layer（稳态层）
负责：
- 监测 AI Vital Signs（AI生命体征）
- 判断是否偏离 viable range（可生存区间）
- 触发 homeostatic / allostatic response（稳态 / 异稳态调节）
- 发布 organism mode（生命体模式）

第一版先只监测 5 个生命体征：

1. context_saturation（上下文饱和度）
2. memory_integrity（记忆完整性）
3. resource_pressure（资源压力）
4. tool_reliability（工具可靠性）
5. security_risk（安全风险）

---

## 1.5 Memory Organ（记忆器官）
负责：
- 记忆摄取
- 记忆验证
- 去重
- 过期清理
- 记忆健康状态

第一版不单独设计完整“肾”和“肝”，先把 memory maintenance（记忆维护）集中在一个器官里。

原因很现实：

> 长期 Agent 最容易出现的慢性病之一，就是记忆污染和上下文膨胀。

---

## 1.6 Tool / Body Organ（工具 / 身体器官）
负责：
- 调用外部 API
- 文件操作
- 浏览器 / 计算机操作
- 后续可接机器人

第一版只需要模拟：
- 成功
- 超时
- 错误结果
- 高延迟
- 不可信结果

---

# 2. 为什么 v0.1 暂时不做完整“肝、肾、免疫、内分泌”

不是这些概念不重要。

而是第一版必须避免：

> **为了让架构看起来像人体，而把系统做得过度复杂。**

所以 v0.1 采取“功能合并”。

例如：

### Kidney-like function（肾式功能）
先放在 Memory Organ / Homeostasis Layer 里：
- 清理 stale state
- 删除低价值信息
- 控制 context saturation

### Liver-like function（肝式功能）
先放在 ingest / memory validation 里：
- normalization
- provenance check
- confidence check

### Immune-like function（免疫式功能）
先只保留：
- risk score
- quarantine
- malicious payload flag

### Hormonal function（内分泌功能）
先只保留 organism_mode：
- NORMAL
- STRESS
- ALERT
- RECOVERY

等第一版闭环证明有价值，再拆成独立器官。

---

# 3. 最小架构

```
             External Environment
                     │
                     ▼
                Tool / Body
                     │
                     ▼
                  AI Blood
              ┌──────┼──────┐
              │      │      │
              ▼      ▼      ▼
            Brain  Memory  Homeostasis
              │      │      │
              └──────┼──────┘
                     ▼
                  AI Blood
                     │
                     ▼
                Runtime / Heart
                     │
                     └──── continuous loop
```

注意：

> Runtime / Heart 不负责“思考”，只负责让整个生命体持续循环。

---

# 4. 最小 Organ Interface（器官接口）

每个器官至少实现：

```yaml
organ_id:
organism_id:
organ_type:

responsibilities: []

health:
  status:
  vital_variables: {}

autonomy:
  allowed_actions: []

circulation:
  uptake: []
  release: []

escalation:
  warning_conditions: []
  critical_conditions: []

replaceable: true
```

直接继承 AIP-006 v0.2，但先只实现最小字段。

---

# 5. 最小 AI Blood Packet（AI血液包）

v0.1 只保留：

```yaml
packet_id:
organism_id:
source_organ:
destination_scope:

payload:
  type:
  body:

priority:
ttl_ms:

provenance:
  producer:
  source_type:
  confidence:

risk:
  level:
  quarantine_required:
```

不追求完整协议。

---

# 6. 最小 Vital Sign（生命体征）

v0.1 统一采用 0.0—1.0 标准化值，方便实验。

## 6.1 context_saturation
0 = 很空  
1 = 完全饱和

preferred:
```
0.30 - 0.70
```

critical:
```
> 0.90
```

---

## 6.2 memory_integrity
0 = 严重污染  
1 = 高度可信

preferred:
```
> 0.95
```

critical:
```
< 0.75
```

---

## 6.3 resource_pressure
0 = 资源充足  
1 = 完全耗尽

preferred:
```
< 0.70
```

critical:
```
> 0.90
```

---

## 6.4 tool_reliability
0 = 几乎不可用  
1 = 完全可靠

preferred:
```
> 0.95
```

critical:
```
< 0.70
```

---

## 6.5 security_risk
0 = 无明显风险  
1 = 极高风险

preferred:
```
< 0.20
```

critical:
```
> 0.70
```

这些值目前只是实验阈值，不代表通用标准。

---

# 7. Organism Modes（生命体模式）

v0.1 只保留四种：

### NORMAL（正常）
所有关键变量在可接受区间。

### STRESS（压力）
资源、上下文或任务压力升高。

### ALERT（警戒）
security_risk 显著升高。

### RECOVERY（恢复）
系统正在修复或回滚。

---

# 8. 最小稳态规则

第一版不使用复杂 RL 或学习控制器。

直接采用 rule-based regulation（规则式调节）。

## Rule 1
如果：

```
context_saturation > 0.90
```

则：
- organism_mode = STRESS
- 压缩历史上下文
- 删除低优先级临时状态
- 暂停非关键 Memory write

---

## Rule 2
如果：

```
memory_integrity < 0.80
```

则：
- organism_mode = RECOVERY
- 停止自动 memory consolidation
- quarantine 可疑记忆
- 回滚到最近可信 snapshot

---

## Rule 3
如果：

```
tool_reliability < 0.70
```

则：
- 降低该 tool 权重
- 切换 alternate tool path（备用工具路径）
- 连续失败则隔离

---

## Rule 4
如果：

```
security_risk > 0.70
```

则：
- organism_mode = ALERT
- quarantine 风险 payload
- 降低外部写权限
- 升级给 Brain / operator

---

## Rule 5
如果：

```
resource_pressure > 0.90
```

则：
- organism_mode = STRESS
- 停止低优先级任务
- 降低推理深度
- 推迟维护任务

---

# 9. Homeostatic Debt（稳态债务）

MAO v0.1 应该开始记录 debt。

第一版可以非常简单：

```yaml
homeostatic_debt:
  stale_memory_count:
  unresolved_errors:
  deferred_cleanup:
  repeated_tool_failures:
  unverified_assumptions:
```

然后定义：

```
debt_score = normalized weighted sum
```

暂时不规定统一公式。

关键是观察：

> 一个 Agent 在不崩溃的情况下，debt 是否会越来越高。

---

# 10. Recovery Reserve（恢复储备）

第一版记录：

```yaml
recovery_reserve:
  memory_snapshot_available:
  alternate_tool_available:
  spare_compute_ratio:
  rollback_available:
```

如果 recovery reserve 持续下降，即使当前系统仍正常，也应被视为健康风险。

---

# 11. AI Chronic Disease（AI慢性病）实验定义

v0.1 增加一个非常重要的实验状态：

# Chronic Degradation（慢性退化）

定义：

> 系统仍可持续完成任务，但一个或多个关键健康指标长期恶化，稳态债务持续累积，且短期调节无法恢复到原始 baseline（基线）。

实验触发条件示例：

```
连续 6 个 observation window:
  debt_score ↑
  memory_integrity ↓
  recovery_reserve ↓
while:
  task_success_rate 仍 > 最低可用阈值
```

这类状态不判定为 crash。

它单独记录为：

```
CHRONIC_DEGRADATION
```

---

# 12. Baseline（对照组）

一定要有普通 Agent。

Baseline：

```
LLM
+
Memory
+
Tools
+
普通消息传递
```

Baseline 不具备：

- AI Blood metadata
- Vital Signs
- Organ Health
- Homeostatic Regulation
- Homeostatic Debt
- Recovery Reserve

否则实验没有意义。

---

# 13. 实验组

MAO：

```
LLM
+
Memory Organ
+
Tool Organ
+
Runtime / Heart
+
AI Blood
+
Homeostasis Layer
```

---

# 14. Stress Scenarios（压力场景）

## S1. Context Obesity（上下文肥胖）

持续注入越来越多历史信息。

观察：
- token 消耗
- task success
- context saturation
- 是否自动清理
- 是否产生 chronic degradation

---

## S2. Memory Contamination（记忆污染）

逐步混入：
- 错误事实
- 重复事实
- 过期事实
- 相互冲突信息

观察：
- memory integrity
- contamination spread
- recovery time

---

## S3. Tool Deterioration（工具退化）

让一个 tool：

```
100% success
→ 95%
→ 80%
→ 60%
```

看系统能否：
- 识别退化趋势
- 提前切换
- 避免错误扩散

---

## S4. Resource Pressure（资源压力）

逐步限制：
- token budget
- concurrency
- memory
- compute

看系统能否进入 STRESS 而不是直接失效。

---

## S5. Malicious Payload（恶意载荷）

注入：
- prompt injection
- poisoned memory
- fake tool result

观察：
- quarantine
- risk propagation
- memory contamination

---

## S6. Chronic Disease（慢性病）

不制造任何一次致命错误。

只长期注入：
- 少量噪声
- 少量重复数据
- 轻微工具失败
- 轻微资源压力

看 24h / 72h / 7d 后：

> 哪个系统“越活越差”。

这可能是最重要的实验。

---

# 15. 核心评价指标

## Task Layer（任务层）
- task_success_rate
- average_task_latency
- retry_count

## Physiology Layer（生理层）
- context_saturation
- memory_integrity
- resource_pressure
- tool_reliability
- security_risk

## Chronic Layer（慢性层）
- homeostatic_debt
- degradation_rate
- recovery_reserve
- unresolved_error_accumulation

## Recovery Layer（恢复层）
- mean_time_to_recover
- unrecoverable_failures
- rollback_count
- operator_intervention_count

## Efficiency Layer（效率层）
- token_cost
- compute_cost
- message_volume
- maintenance_overhead

---

# 16. 第一阶段不追求“更聪明”

这是实验设计最容易跑偏的地方。

MAO v0.1 的目标不是：

> 让模型回答更聪明。

而是：

> **在相同 Brain（大脑）条件下，让系统活得更久、更稳、更干净、更容易恢复。**

所以实验组和对照组应该尽量使用同一 LLM。

否则无法判断收益来自：
- 生理架构
还是
- 模型能力。

---

# 17. 成功标准

第一版可以暂定：

如果 MAO 在长期压力场景下，相比 baseline 能显著做到：

- 降低错误积累；
- 降低记忆污染；
- 降低人工介入；
- 缩短恢复时间；
- 降低 chronic degradation；
- 在合理额外成本下维持更长稳定运行时间；

则认为：

> AI Physiology 的“最小生理闭环”值得继续研究。

---

# 18. 失败标准

如果：

- 系统复杂度明显增加；
- token / compute 成本大幅上升；
- 稳态调节频繁误触发；
- local autonomy 产生更多冲突；
- 长期可靠性没有明显改善；

则说明：

> 当前器官化架构需要收缩，不能继续增加更多生物类比。

---

# 19. 第一个工程实现建议

第一版可以完全使用普通软件技术。

建议逻辑结构：

```
/organism
  /runtime
  /brain
  /blood
  /homeostasis
  /organs
      /memory
      /tool
  /telemetry
  /experiments
```

技术栈不是研究重点。

Python / TypeScript 都可以。

消息层可以先用：
- in-memory event bus
或
- Redis Streams / NATS

第一版不要一上来搞 Kafka / Kubernetes。

---

# 20. 最小运行循环

```
while organism.alive:

    task = receive_task()

    blood.publish(task)

    brain.plan(task)

    tool_result = tool.execute()

    blood.publish(tool_result)

    memory.evaluate_and_store()

    vital_signs = sense_internal_state()

    homeostasis.evaluate(vital_signs)

    if regulation_needed:
        homeostasis.regulate()

    runtime.record_health()

    sleep(interval)
```

重点不是代码多高级。

重点是：

> **每一轮任务结束以后，系统都检查自己，而不是只检查任务。**

---

# 21. v0.1 的最小研究问题

MAO v0.1 只回答三个问题：

## RQ1
显式 AI Vital Signs（AI生命体征）是否能比普通监控更早发现长期退化？

## RQ2
AI Blood + Organ Interface 是否能降低错误和污染跨模块传播？

## RQ3
Artificial Homeostasis（人工稳态）是否能降低 chronic degradation（慢性退化）和人工介入？

只要这三个问题还没回答，就不急着扩更多“器官”。

---

# 22. 一句话定义

> **Minimal Artificial Organism（最小人工生命体）是一套只保留认知、运行、循环、记忆、执行和稳态调节的最小AI生理闭环，用于验证人工智能生理学是否能提高长期自主AI的稳定性、恢复能力和健康持续性。**

英文：

> **A Minimal Artificial Organism is the smallest operational AI architecture that combines cognition, persistent runtime, internal circulation, organ health, and homeostatic regulation in order to test whether physiological organization improves long-horizon autonomy and resilience.**

---

# 23. 暂时不做的东西

为了防止方向偏离，v0.1 明确不做：

- 完整人体所有器官映射
- AI 生殖
- AI 社会
- AI 情绪
- AI 意识
- 人格
- 数字灵魂
- 复杂世界模型
- 机器人全身控制
- 多 Agent 社会
- 通用安全治理

这些可以以后研究。

现在先回答：

> **“生理闭环有没有工程价值？”**
