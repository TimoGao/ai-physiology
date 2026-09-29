# AI Physiology Roadmap v0.1（人工智能生理学路线图 v0.1）

> 这份路线图的作用不是把事情做得更多，而是防止项目越做越散。
>
> 原则：每一阶段必须有明确问题、明确产物和明确停止条件。

最后更新：2026-09-29

---

# 总目标

把 AI Physiology（人工智能生理学）从：

> 一套关于 AI 生命体的概念框架

逐步推进成：

> **有 prior art（已有工作）、有定义、有开放规范、有 reference implementation（参考实现）、有实验数据、可发表论文的研究框架。**

---

# Phase 0：概念成型

**状态：基本完成**

已经完成：
- AI Physiology 命名
- Human organ → AI organ mapping（人体器官→AI器官映射）
- 四张内部网络
- 六大生理闭环
- AI Cell → Tissue → Organ → Organism
- Homeostasis First（稳态优先）
- Organ Internalization（器官内化）

产物：
- Framework v0.1
- GitHub repository

停止条件：
> 能用一套统一语言解释“我们究竟在研究什么”。

---

# Phase 1：Prior Art & Boundary（已有工作与边界）

**状态：基本完成**

目标：
> 弄清楚什么已经有人做，什么只是换名字，什么才可能是自己的贡献。

已完成：
- Related Work & Prior Art v0.1
- 28篇核心阅读矩阵
- 核心机制继承矩阵 v0.2

还需要：
- 后续随论文写作补正式引用
- 不再无限扩文献

停止条件：
> 已经足够支撑第一篇 framework paper（框架论文）的 Related Work（相关工作）章节。

---

# Phase 2：Core Specification（核心规范）

**状态：接近完成**

目标：
> 从 metaphor（比喻）进入 architecture（架构）。

核心规范：

- AIP-001 AI Organism（AI生命体）
- AIP-002 AI Cell（AI细胞）
- AIP-003 AI Organ（AI器官）
- AIP-004 AI Blood（AI血液）v0.2 ✅
- AIP-005 Artificial Homeostasis（人工稳态）v0.2 ✅
- AIP-006 Organ Interface（器官接口）v0.2 ✅

接下来建议补两个小规范：

### AIP-007 AI Vital Signs（AI生命体征）
把生命体征从 AIP-005 单独抽出来，定义：
- measurement
- ranges
- trends
- reliability
- sensor confidence
- escalation

### AIP-008 Organ Health & Pathology（器官健康与病理）
专门定义：
- stress
- degradation
- injury
- chronic disease
- aging
- debt
- recovery reserve

停止条件：
> 最小生命体的关键状态、循环和器官接口都能被明确描述。

---

# Phase 3：Minimal Artificial Organism（最小人工生命体）

**状态：现在进入**

目标：
> 不再继续画架构图，开始做最小实验系统。

v0.1 组成：
- Brain
- Runtime / Heart
- AI Blood
- Homeostasis Layer
- Memory Organ
- Tool / Body Organ

不做：
- 完整生殖
- AI社会
- 意识
- 情绪
- 全套器官

产物：
1. MAO Architecture v0.1
2. reference schema
3. 最小代码原型
4. baseline agent
5. experiment runner

停止条件：
> 可以真实运行 baseline vs MAO 对照实验。

---

# Phase 4：Chronic Disease & Long-Horizon Experiments（慢性病与长期实验）

这是我认为非常关键的一阶段。

目标：
> 证明 AI Physiology 不是“出错以后自动重试”，而是能解释和缓解长期系统退化。

重点实验：

### E1 Context Obesity（上下文肥胖）
测试长期上下文膨胀。

### E2 Memory Contamination（记忆污染）
测试错误、冲突、过期记忆积累。

### E3 Tool Deterioration（工具退化）
测试执行器逐渐变差。

### E4 Resource Stress（资源压力）
测试计算和 token 资源下降。

### E5 Security Contamination（安全污染）
测试错误/恶意内容在内部传播。

### E6 Chronic Degradation（慢性退化）
无单次致命故障，持续制造轻微损伤。

核心指标：
- task success
- homeostatic debt
- recovery reserve
- memory integrity
- error accumulation
- intervention count
- recovery time
- total cost

停止条件：
> 有一组重复实验数据，能够支持或否定最小生理闭环的价值。

---

# Phase 5：Pathology（病理学）分支

**只有 Phase 4 有数据以后才做。**

目标：
> 从“AI健康”进一步研究“AI怎么生病”。

可能形成：

### AI Pathology（人工智能病理学）
研究：
- Acute Failure（急性故障）
- Chronic Disease（慢性病）
- Cross-organ Pathology（跨器官病理）
- Aging（衰老）
- Autoimmune Failure（自身免疫式故障）
- Organ Failure（器官衰竭）

产物：
- pathology taxonomy（病理分类）
- disease signatures（疾病特征）
- recovery protocols（恢复协议）

停止条件：
> 病理分类能够帮助解释真实实验故障，而不是只增加名词。

---

# Phase 6：Expand Organ Systems（扩展器官系统）

**只有最小系统验证有效以后才开始。**

按照实际缺口逐个加入：

1. Liver-like Organ（肝式器官）
2. Kidney-like Organ（肾式器官）
3. Immune Organ（免疫器官）
4. Endocrine System（内分泌系统）
5. Cerebellum / Reflex Layer（小脑 / 反射层）
6. Growth / Reproduction（成长 / 繁殖）

原则：

> 没有实验需求，就不新增器官。

每新增一个器官都必须回答：
- 它解决什么问题？
- 普通架构为什么解决不好？
- 它增加什么可测变量？
- 它是否显著提高长期稳定性？

---

# Phase 7：Framework Paper（框架论文）

建议在 Phase 4 初步有数据后开始正式写。

暂定题目：

**AI Physiology: A Life-System Architecture for Persistent Autonomous Artificial Intelligence**

中文：

**《人工智能生理学：面向持续自主人工智能的生命系统架构》**

论文重点不是宣称“AI是生命”。

重点：
1. 现有研究碎片化
2. organism-level synthesis（生命体级整合）
3. core physiological architecture
4. MAO implementation
5. long-horizon experiments
6. limitations and falsification

潜在渠道：
- arXiv
- ALIFE Conference
- Artificial Life journal
- 后续系统类 / Agent 类会议

---

# Phase 8：Specification v1.0（规范1.0）

只有论文和实验之后再做。

目标：
> 从个人研究项目变成可供其他人实现和讨论的开放规范。

包括：
- stable AIP numbering
- terminology
- schema
- reference implementation
- benchmark
- test suite
- versioning rules

此时再考虑：
- contributors
- external proposals
- governance of AIPs

---

# Phase 9：AI Society（AI社会）与 Social Homeostasis（社会稳态）

**现在不要做。**

只有单个 AI Organism 的身份、健康、生命周期相对成熟后，再研究：

- AI identity
- responsibility
- sanctions
- quarantine
- reputation
- inter-organism protocols
- social homeostasis

否则容易从工程问题滑向纯哲学。

---

# 当前未来 6 个具体动作

按照执行顺序：

## Step 1
完成 **Minimal Artificial Organism v0.1** ✅

## Step 2
做 **AIP-007 AI Vital Signs（AI生命体征）v0.1**

## Step 3
做 **AIP-008 Organ Health & Pathology（器官健康与病理）v0.1**

## Step 4
写 MAO 的最小代码原型。

## Step 5
做 baseline vs MAO 第一轮 6 个 stress scenarios（压力场景）。

## Step 6
根据实验结果决定：
- 继续扩器官
或
- 收缩 / 修改理论

---

# 三条防跑偏规则

## Rule 1：没有可测变量，不新增概念
任何新器官、新病理、新机制都必须能映射到 measurable state（可测状态）。

## Rule 2：没有实验需求，不新增器官
不能因为人体有某个器官，AI就必须有。

## Rule 3：优先解决真实长期AI问题
优先研究：
- memory contamination
- context obesity
- chronic degradation
- resource stress
- tool deterioration
- recovery

而不是优先讨论：
- AI意识
- 灵魂
- 情绪
- 生殖伦理
- 星际文明

那些可以以后再回来。

---

# 当前项目主线

未来一段时间只围绕这一条：

> **AI Physiology 能否通过显式内部循环、生命体征、器官健康和人工稳态，提高长期自主 AI 的稳定性和恢复能力？**

只要这个问题还没有实验答案，就先不把项目扩得更大。
