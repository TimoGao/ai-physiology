# AI Physiology Roadmap v0.2（人工智能生理学路线图）

> 这份是执行路线，不是愿景清单。
>
> 主线只有一个：
>
> **AI Physiology 能否通过显式内部循环、生命体征、器官健康和人工稳态，提高长期自主 AI 的稳定性、恢复能力，并降低慢性退化？**

最后更新：2026-09-29

---

# 现在做到哪里了

## 01 理论框架
**状态：完成第一轮**

已经有：
- AI Physiology（人工智能生理学）定义
- Cell → Tissue → Organ → Organism
- 四张内部通信网络
- 六类生理闭环
- Organ Internalization（器官内化）
- Homeostasis First（稳态优先）

当前原则：
> 不再继续扩“大理论”，除非实验逼着我们改。

---

## 02 Prior Art（已有工作）
**状态：够用，暂停扩张**

已经完成：
- Related Work & Prior Art v0.1
- 28篇核心文献矩阵
- 核心机制继承矩阵 v0.2

下一次再扩文献：
> 等正式写论文时再补。

---

## 03 AIP Core Specification（核心规范）
**状态：第一轮完成**

已有：
- AIP-001 AI Organism（AI生命体）
- AIP-002 AI Cell（AI细胞）
- AIP-003 AI Organ（AI器官）
- AIP-004 AI Blood（AI血液）v0.2
- AIP-005 Artificial Homeostasis（人工稳态）v0.2
- AIP-006 Organ Interface（器官接口）v0.2
- AIP-007 AI Vital Signs（AI生命体征）v0.1
- AIP-008 Organ Health & Pathology（器官健康与病理）v0.1

当前原则：
> 暂停新增 AIP，先用实验检验已有规范。

---

# 接下来的正式执行顺序

## Phase A：MAO Experiment v0.3
**当前阶段：正在完成**

目标：
> 把“单次演示”升级成重复实验。

内容：
- Strong Baseline（更强基线）
- 10 seeds 重复
- mean / stdev / min / max
- JSON / CSV export
- 六类 stress scenarios

完成标准：
> 六类实验都可以批量重复、统一输出、稳定复现。

---

## Phase B：MAO Experiment v0.4
**下一步**

目标：
> 判断“差异是不是真的存在，以及到底是谁带来的”。

要做：

### 1. Statistical robustness（统计稳健性）
- 30-50 seeds
- confidence interval（置信区间）
- effect size（效应量）

### 2. Ablation Study（消融实验）
分别去掉：
- AI Blood
- Homeostasis
- Vital Signs
- Organ Health

验证：
> 哪一层真正有用？

### 3. Cost Accounting（成本核算）
比较：
- extra messages
- compute overhead
- memory overhead
- latency overhead
- maintenance complexity

### 4. Stronger Baseline 2.0
加入更成熟的：
- retry policy
- cleanup policy
- circuit breaker
- health check
- security filter

完成标准：
> MAO 的收益仍然能够超过“普通工程优化”。

---

## Phase C：真实 LLM 实验
**v0.4 之后再做**

目标：
> 把 synthetic agent（合成智能体）换成真实 LLM Agent。

第一版只接一个模型。

保持相同：
- model
- prompt
- tools
- task set

只改变：
- 普通 Agent
vs
- MAO Agent

测试：
- long context
- memory pollution
- repeated tool failure
- multi-step task
- persistent workspace

完成标准：
> 在真实 Agent 里仍然能观察到同样的慢性退化和恢复差异。

---

## Phase D：Long-Horizon Run（长期运行）

这是后面真正关键的一步。

建议三个时间尺度：

### 24h
先发现明显 bug 和循环问题。

### 72h
看 debt（债务）是否开始积累。

### 7d
看 chronic degradation（慢性退化）是否出现。

后面如果资源允许：

### 30d
才真正接近“长期 AI 系统”研究。

主要观察：
- Homeostatic Debt
- Recovery Reserve
- Memory Integrity
- Error Accumulation
- Human Intervention
- Cost Drift
- Performance Drift

---

## Phase E：AI Pathology（AI病理学）
**只有长期实验出现真实病理模式后才推进**

现在我们已经提出：
- Context Obesity
- Memory Contamination
- Chronic Degradation
- Homeostatic Exhaustion
等。

但下一步不是继续发明病名。

只有当长期实验真的反复出现某种模式，才：
- 定义 pathology signature（病理特征）
- 命名
- 分级
- 研究传播路径
- 研究治疗方案

原则：
> 先观察疾病，再命名疾病。

---

## Phase F：扩展器官
**至少在真实LLM实验之后**

是否加入：
- Liver-like Organ（肝式器官）
- Kidney-like Organ（肾式器官）
- Immune Organ（免疫器官）
- Endocrine System（内分泌系统）

全部由实验决定。

例如：
如果 Memory Contamination 始终是核心问题，
才正式拆出：
- Liver-like validation
- Kidney-like cleanup

如果安全污染是核心问题，
才独立 Immune Organ。

原则：
> 不是因为人体有，所以 AI 有；而是因为实验缺，所以才长出来。

---

## Phase G：第一篇论文

我建议不是现在就写。

比较合适的时间点：

> **真实LLM实验 + 至少一轮 72h / 7d 长跑之后。**

第一篇论文结构大致：

1. Problem：长期AI为什么会慢性退化
2. Related Work
3. AI Physiology Framework
4. MAO Architecture
5. Vital Signs / Debt / Recovery Reserve
6. Experiment Design
7. Baseline vs MAO
8. Ablation
9. Long-Horizon Results
10. Limitations / Falsification

题目暂定：

**AI Physiology: A Life-System Architecture for Persistent Autonomous AI**

中文：
**《人工智能生理学：面向持续自主AI的生命系统架构》**

---

# 你现在可以把整个项目理解成五个关卡

## 关卡1：能不能说清楚？
已经通过。

## 关卡2：能不能写成规范？
已经通过第一轮。

## 关卡3：能不能写成程序？
已经通过第一轮。

## 关卡4：有没有稳定实验收益？
**现在正在验证。**

## 关卡5：真实AI里还成立吗？
下一阶段。

只有关卡4和5通过，这个方向才真正站得住。

---

# 我建议未来 8 个动作不要变

1. 完成 MAO Experiment v0.3
2. 跑第一轮 10-seed 数据
3. 做 v0.4 消融 + 统计
4. 选一个真实 LLM 接入
5. 做真实 Agent 六场景实验
6. 做 24h → 72h → 7d 长跑
7. 根据真实病理回修 AIP-004~008
8. 开始 Framework Paper（框架论文）

在第 6 步之前：
> **不扩 AI 社会、不扩生殖、不扩意识、不扩全套器官。**

这样方向基本不会偏。
