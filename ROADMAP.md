# AI Physiology Roadmap v0.3（人工智能生理学路线图）

> 这份是执行路线，不是愿景清单。
>
> 当前主问题已经收窄为：
>
> **长期 AI 是否存在传统短期可靠性工程难以处理的慢性退化；如果存在，Vital Signs（生命体征）、Homeostatic Debt（稳态债务）和 Recovery Reserve（恢复储备）能否更早、更稳地识别和调节这种退化？**

最后更新：2026-09-29

---

# 当前状态

## 01 理论框架
**状态：第一轮完成，暂停扩张**

已有：
- AI Physiology（人工智能生理学）定义
- Cell → Tissue → Organ → Organism
- 四张内部通信网络
- 六类生理闭环
- Organ Internalization（器官内化）
- Homeostasis First（稳态优先）

原则：
> 除非实验逼着我们改，否则不继续扩“大理论”。

---

## 02 Prior Art（已有工作）
**状态：够用，暂停扩张**

已有：
- Related Work & Prior Art v0.1
- 28篇核心文献矩阵
- 核心机制继承矩阵 v0.2

原则：
> 等正式写论文时再补文献，不继续无边界扩展。

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

原则：
> 暂停新增 AIP，先验证已有机制。

---

# 实验路线已经走过什么

## MAO v0.3
完成重复实验、Strong Baseline（更强基线）、JSON/CSV、统计汇总。

## MAO v0.4
完成公平压力轨迹、消融实验、成本核算。

关键修正：
> AI Physiology 不应该替代 Reliability Engineering（可靠性工程）。

## MAO v0.5
把 retry / timeout / fallback / circuit breaker 正式放到底层。

关键结果：
> 在明显故障场景中，“可靠性工程 + 生理层”没有比单纯可靠性工程表现出稳定增量收益。

因此没有直接进入真实 LLM。

---

# 当前阶段：MAO v0.5.1 — Longitudinal Health Benchmark

目标：
> 不测已经越线的问题，而测 Low-and-Slow Degradation（低强度长期退化）。

比较：
- Adaptive Monitoring Baseline（自适应监控基线）
- Physiology Monitor（生理监测器：Debt + Reserve）

首轮规模：
- 200 seeds
- 400 longitudinal trajectories（纵向轨迹）
- 800 monitor evaluations（监测评估）
- 每条240个时间步

首轮信号：
- AUC：0.765 → 0.781
- 假提前预警率：95.8% → 37.1%
- 召回率：100.0% → 92.5%
- 平均提前量：162.8 → 103.5

当前解释：
> 生理监测器表现得更“克制”：假警报明显更少，但漏报更多、报警更晚。

这只是 synthetic signal（合成信号），不是理论验证。

---

# 下一关：MAO v0.5.2 — Predictive Validity & Calibration

这是进入真实LLM之前最后一个合成验证关卡。

只做五件事：

## 1. Threshold Calibration（阈值校准）
不能用固定手工阈值直接比较。

## 2. ROC / Precision-Recall
比较完整曲线，而不是单个阈值点。

## 3. Same False-Positive Budget（相同误报预算）
例如都限制在：
- 5%
- 10%
- 20%

看谁的 recall（召回率）和 lead time（提前量）更好。

## 4. Multiple Degradation Shapes（多种退化形态）
至少增加：
- 线性慢漂移
- 阶段性恶化
- 暂时恢复后复发
- 单器官慢退化
- 多变量交叉退化

## 5. Debt / Reserve Ablation（债务/储备消融）
比较：
- Debt only
- Reserve only
- Debt + Reserve
- 普通 adaptive monitoring

停止条件：
> 如果 v0.5.2 的增量信号消失，不进入真实LLM，继续收缩理论。

如果信号仍然存在：
> 才进入 Real LLM v0.6。

---

# Real LLM v0.6（真实大模型实验）

第一版只接一个模型。

保持一致：
- model
- prompt
- tools
- task set
- reliability substrate

只改变：
- Reliable Agent
vs
- Reliable Agent + AI Physiology

测试：
- persistent memory（持续记忆）
- long context（长上下文）
- repeated tool failure（重复工具失败）
- low-and-slow memory pollution（低强度长期记忆污染）
- persistent workspace（持续工作区）

完成标准：
> 在真实Agent里仍出现与合成纵向基准相同方向的长期健康预测差异。

---

# Long-Horizon Run（长期运行）

如果真实LLM小实验通过，再做：

### 24h
验证工程稳定性。

### 72h
观察 debt / reserve 是否开始分化。

### 7d
观察 chronic degradation（慢性退化）是否真正出现。

### 30d
资源允许后再考虑。

主要观察：
- Homeostatic Debt
- Recovery Reserve
- Memory Integrity
- Error Accumulation
- Human Intervention
- Cost Drift
- Performance Drift

---

# 后续才做的事情

## AI Pathology（AI病理学）
只有真实长期实验反复出现稳定病理模式后再定义疾病。

原则：
> 先观察疾病，再命名疾病。

## 扩展器官
只有实验缺口需要时才加入：
- Liver-like Organ（肝式器官）
- Kidney-like Organ（肾式器官）
- Immune Organ（免疫器官）
- Endocrine System（内分泌系统）

原则：
> 不是因为人体有，所以AI有；而是因为实验缺，所以才长出来。

## 第一篇论文
至少等到：
> Real LLM + 72h / 7d long-run 之后。

---

# 当前五个关卡

1. 能不能说清楚？—— 已通过  
2. 能不能写成规范？—— 已通过第一轮  
3. 能不能写成程序？—— 已通过第一轮  
4. 有没有稳定实验增量收益？—— **正在验证，v0.5.1首次出现弱正信号**  
5. 真实AI里还成立吗？—— 尚未进入

---

# 当前固定执行顺序

1. MAO v0.5.1 ✅
2. MAO v0.5.2 Predictive Validity & Calibration
3. 如果通过 → Real LLM v0.6
4. 24h → 72h → 7d 长跑
5. 根据真实结果回修 AIP-004~008
6. 再决定是否发展 AI Pathology 和扩展器官
7. Framework Paper（框架论文）

在真实长跑前：
> **不扩AI社会、不扩生殖、不扩意识、不扩全套器官。**
