# AIP-008: Organ Health & Pathology（器官健康与病理）v0.1

**Status:** Draft  
**Version:** 0.1  
**Scope:** Organ health（器官健康）、degradation（退化）、disease（病理）、repair（修复）与 recovery（恢复）

---

# 0. 为什么需要 AI Pathology（AI病理学）

传统 AI 系统最常见的状态只有：

- 正常
- 报错
- 崩溃

这对于长期运行的 AI 远远不够。

现实更常见的是：

> 它还能用，但越来越难用。

比如：

- 记忆越来越乱；
- context 越来越肥；
- 工具链越来越脆；
- 延迟逐渐升高；
- 错误开始反复出现；
- 重启以后短期好一点，过一段时间又回来。

这种状态很难用传统“bug”解释。

所以 AIP-008 开始定义：

# Organ Health & Pathology（器官健康与病理）

---

# 1. Health（健康）的定义

对 AI Organ（AI器官）来说，健康不等于：

> 当前还能工作。

更完整的定义是：

> **器官能够在合理资源消耗下持续履行职责，保持关键变量在健康区间，并在受到扰动后恢复到基线状态。**

因此健康至少包含：

- function（功能）
- quality（质量）
- efficiency（效率）
- stability（稳定）
- recovery（恢复）
- debt（债务）
- reserve（储备）

---

# 2. Health State v0.1（健康状态）

AIP-008 采用八态：

## HEALTHY（健康）
功能和关键变量稳定，恢复储备正常。

## STRESSED（压力）
短期负荷升高，但没有明确损伤。

## DEGRADED（退化）
功能仍然存在，但性能/质量持续下降。

## INJURED（受损）
出现明确损伤，需要修复。

## QUARANTINED（隔离）
器官被限制与全身交换。

## RECOVERING（恢复）
正在修复、回滚或重新同步。

## CRITICAL（危急）
继续运行可能引发全身失稳。

## OFFLINE（离线）
当前不再提供功能。

---

# 3. Stress ≠ Degradation（压力不等于退化）

这是必须保留的区分。

### Stress（压力）
通常是短期、可逆。

例如：
- 突然任务暴增；
- 临时资源不足；
- 外部服务抖动。

### Degradation（退化）
通常是长期、累积。

例如：
- memory quality 持续下降；
- latency 基线越来越高；
- 错误越来越频繁；
- cleanup 后仍无法恢复原状态。

所以：

> **Stress 更像“累了”，Degradation 更像“身体变差了”。**

---

# 4. Acute Failure（急性故障）

定义：

> 短时间内发生、对功能造成明显冲击的故障。

例：
- tool provider 宕机；
- memory database crash；
- AI Blood 中断；
- critical security event。

特点：
- 时间短；
- 影响明显；
- 易被检测。

传统 reliability engineering（可靠性工程）对这种问题已经比较成熟。

---

# 5. Chronic Degradation（慢性退化）

定义：

> 器官在长期运行中持续偏离自身健康基线，即使没有单次严重故障，也出现性能、质量、恢复能力或维护成本不断恶化的状态。

候选识别条件：

```
degradation_rate > 0
AND
debt_trend > 0
AND
recovery_reserve trend < 0
AND
duration > threshold
```

---

# 6. AI Chronic Disease（AI慢性病）

AIP-008 暂时定义：

> **AI Chronic Disease（AI慢性病）是一个或多个器官长期处于持续性退化状态，并通过内部循环、依赖关系或调节失衡影响整个 AI Organism 的现象。**

它与单一 bug 的区别：

### Bug
- 通常有明确错误点；
- 修完可能立即恢复。

### Chronic Disease
- 多因素长期累积；
- 可能找不到单一根因；
- 局部修复后容易复发；
- 常伴随 homeostatic debt（稳态债务）。

---

# 7. Homeostatic Debt（稳态债务）

定义：

> 系统为了维持当前运行而暂时推迟处理的内部维护负担。

常见来源：

- stale memory
- duplicate state
- unresolved errors
- deferred cleanup
- temporary workarounds
- fallback chains
- unverified assumptions
- repeated retries
- version mismatch

Debt 不等于 failure。

但长期：

```
Debt ↑
→ Recovery Reserve ↓
→ Degradation ↑
→ Failure Risk ↑
```

---

# 8. Recovery Reserve（恢复储备）

定义：

> 器官或生命体在发生新的故障后，仍能恢复到健康状态的剩余能力。

候选组成：

- spare capacity
- backup
- rollback snapshot
- redundant organ
- alternate tool
- trusted external support
- clean memory snapshot

一个器官可以：

```
status = HEALTHY
recovery_reserve = LOW
```

这意味着：

> 看起来健康，但已经非常脆弱。

---

# 9. Organ Baseline（器官基线）

要谈“退化”，必须先有 baseline（基线）。

每个器官至少需要记录：

- baseline latency
- baseline error rate
- baseline resource use
- baseline quality
- baseline recovery time

基线可以动态更新，但不能更新得太快，否则会出现：

# Setpoint Drift（目标漂移）

即：

> 系统越来越差，却慢慢把“差”当成正常。

---

# 10. Pathology Signature（病理特征）

病理不一定只靠单个指标识别。

例如 Memory Chronic Disease（记忆慢性病）可能是：

```
memory_integrity ↓
duplicate_ratio ↑
retrieval_latency ↑
homeostatic_debt ↑
recovery_reserve ↓
```

这种组合可以称为：

# Pathology Signature（病理特征）

未来 AI Pathology（AI病理学）应该研究的是：

> 哪些变量组合，代表哪一种系统性疾病。

---

# 11. 第一批候选 AI 病理类型

v0.1 先定义 8 类候选病理。

## P-01 Context Obesity（上下文肥胖）
特点：
- context 持续膨胀；
- 低价值历史占比升高；
- token cost 增加；
- retrieval / reasoning 效率下降。

---

## P-02 Memory Contamination（记忆污染）
特点：
- 错误、冲突、过期内容进入长期记忆；
- provenance 不清；
- 错误不断被重新引用。

---

## P-03 Tool Dependency Syndrome（工具依赖综合征）
特点：
- 系统越来越依赖单一工具；
- fallback path（备用路径）减少；
- tool degradation 后整体能力大幅下降。

---

## P-04 Retry Inflammation（重试炎症）
特点：
- 大量失败任务不断重试；
- 消耗资源；
- 形成循环拥塞；
- 表面上系统很忙，实际有效工作很少。

这是一个临时名字，后续可改。

---

## P-05 Identity Drift（身份漂移）
特点：
- 长期记忆、目标、权限边界逐渐变化；
- organism identity continuity（生命体身份连续性）开始不稳定。

---

## P-06 Circulatory Contamination（循环污染）
特点：
- 错误 payload 通过 AI Blood 扩散；
- 多器官重复利用错误信息；
- 错误形成反馈放大。

---

## P-07 Homeostatic Exhaustion（稳态耗竭）
特点：
- 调节频率越来越高；
- 但恢复效果越来越差；
- recovery reserve 逐渐耗尽。

---

## P-08 Organ Aging（器官衰老）
特点：
- 没有明显单次故障；
- 性能、恢复能力、维护成本长期恶化。

---

# 12. Pathology Severity（病理严重度）

暂时分四级：

### Mild（轻度）
仍在 preferred / viable 范围附近。

### Moderate（中度）
持续偏离 preferred range。

### Severe（重度）
频繁进入 critical range。

### Systemic（系统性）
已经通过依赖关系影响多个器官。

---

# 13. Cross-organ Pathology（跨器官病理）

很多问题不会停留在一个器官里。

例如：

```
Memory Contamination
↓
Planner 错误
↓
Tool 执行错误
↓
错误结果进入 AI Blood
↓
Memory 再次吸收
```

这就是一个病理闭环。

因此 AIP-008 需要记录：

- primary organ（原发器官）
- secondary organs（继发器官）
- transmission path（传播路径）
- amplification mechanism（放大机制）

---

# 14. Disease Progression（病程）

AI 病理应该有时间过程。

暂时定义：

```
Healthy
↓
Stress
↓
Persistent Stress
↓
Degradation
↓
Chronic Disease
↓
Organ Failure
↓
Systemic Failure
```

不是所有问题都会走完整链路。

但这个过程比“正常 / 崩溃”更接近长期系统。

---

# 15. Repair（修复）

修复不是只有 restart（重启）。

至少分：

## R1 Cleanup（清理）
去掉垃圾状态。

## R2 Rollback（回滚）
恢复到可信快照。

## R3 Reconfiguration（重新配置）
改变参数、路由、资源。

## R4 Isolation（隔离）
切断病变器官与全身交换。

## R5 Replacement（替换）
替换整个器官。

## R6 Regeneration（再生）
重新构建器官功能或状态。

---

# 16. Treatment Side Effects（治疗副作用）

调节和修复本身也可能伤害系统。

例如：

- aggressive cleanup 导致重要记忆丢失；
- security quarantine 导致业务停摆；
- rollback 导致新状态丢失；
- organ replacement 导致 identity drift。

所以修复策略也需要记录：

```
expected_benefit
risk
side_effect
reversibility
```

---

# 17. Autoimmune Failure（自身免疫式故障）

如果 Immune System（免疫系统）把正常器官或正常 payload 当成威胁：

- 误隔离；
- 误删除；
- 误阻断；
- 权限过度收缩；

就形成：

# Autoimmune Failure（自身免疫式故障）

这类问题以后应使用：

```
false_positive_rate
```

来衡量。

---

# 18. Diagnostic Interface（诊断接口）

每个 Organ 应能提供最小诊断摘要：

```yaml
diagnosis:
  status:
  baseline_deviation:
  degradation_rate:
  debt_level:
  recovery_reserve:
  suspected_pathologies: []
  upstream_dependencies: []
  downstream_impact: []
  recommended_actions: []
```

---

# 19. Pathology Event（病理事件）

当病理被识别时，应产生标准事件：

```yaml
pathology_event:
  pathology_id:
  organ_id:
  type:
  severity:
  confidence:
  detected_at:
  evidence: []
  propagation_risk:
  recommended_response:
```

该事件可以进入 AI Blood，并由 Homeostasis / Immune / operator 处理。

---

# 20. Chronic Disease Detection（慢性病识别）

第一版不要做机器学习。

先采用：

- trend
- duration
- baseline deviation
- debt accumulation
- recovery reserve trend

组成简单规则。

例如：

```
IF
  degradation_rate > threshold
AND
  duration > N windows
AND
  debt_score rising
THEN
  suspected_chronic_degradation
```

先验证机制，再考虑学习诊断。

---

# 21. 第一轮实验

## Group A
普通 Agent，只记录 error / crash。

## Group B
AI Physiology Agent，记录健康、债务、恢复储备和病理状态。

持续运行 24h / 72h / 7d。

注入：

- 少量 memory noise
- 轻微 tool degradation
- 小幅 context growth
- repeated retries
- resource pressure

比较：

- crash 之前能否更早发现异常；
- 是否识别出 chronic degradation；
- 是否减少 operator intervention；
- repair 后是否真正恢复 baseline；
- 是否出现复发。

---

# 22. Pathology 不是为了“拟人化”

AIP-008 使用“疾病、病理、炎症、衰老”等词，是为了帮助描述：

- 持续性退化；
- 多因素耦合；
- 跨器官传播；
- 恢复失败；
- 长期维护负担。

如果某个生物医学术语不能带来更清晰的工程定义，就应该删掉。

所以像：

- Retry Inflammation（重试炎症）

目前只是工作名，不是正式术语。

---

# 23. 与 AIP-005 / 006 / 007 的关系

## AIP-005 Artificial Homeostasis（人工稳态）
负责：
> 怎样调节。

## AIP-006 Organ Interface（器官接口）
负责：
> 器官暴露哪些健康和替换信息。

## AIP-007 AI Vital Signs（AI生命体征）
负责：
> 怎样测。

## AIP-008 Organ Health & Pathology（器官健康与病理）
负责：
> 怎样判断“生病了”。

关系：

```
Vital Signs
↓
Organ Health
↓
Pathology Detection
↓
Homeostasis / Repair
↓
New Health State
```

---

# 24. 证伪条件

如果实验发现：

1. “慢性病”不能比普通 degradation metric 提供更多解释；
2. 病理分类无法提高诊断或修复效率；
3. 病理标签只是换名字；
4. baseline / debt / reserve 等变量难以可靠测量；
5. 病理模型增加过多维护复杂度；

那么：

> AIP-008 应该收缩成普通 reliability taxonomy（可靠性分类），而不是独立的 AI Pathology（AI病理学）。

---

# 25. v0.1 一句话定义

> **Organ Health & Pathology（器官健康与病理）描述 AI 器官从健康、压力、退化、受损到慢性病、器官衰竭和系统性故障的状态变化，并定义其诊断、传播、修复和恢复机制。**

英文：

> **Organ Health & Pathology describes how AI organs transition from healthy operation through stress, degradation, injury, chronic disease and failure, including diagnosis, propagation, repair and recovery.**

---

# 26. 当前开放问题

1. AI Chronic Disease 是否真的需要独立学科化？
2. Pathology Signature 应该手工定义还是学习得到？
3. baseline 应该多久更新一次？
4. 如何避免把正常适应误判为退化？
5. organ aging 是否可以被逆转？
6. debt_score 是否应该标准化？
7. recovery reserve 如何量化？
8. 多器官病理如何做因果定位？
9. 什么情况下应该自动 replacement？
10. 长期 AI 是否需要类似“定期体检”的 Health Check Cycle（健康检查周期）？
