# AI Physiology 核心机制继承矩阵 v0.2

> 这一版不是继续做“文献综述”，而是开始做设计取舍。
> 核心问题：前人已经做出来的东西，哪些应该直接继承，哪些应该改造，哪些不能因为“像人体”就硬套进 AI Physiology（人工智能生理学）？

最后更新：2026-09-29

# 一、先给结论

AI Physiology 不需要从零发明 Homeostasis（稳态）、feedback control（反馈控制）、self-healing（自愈）、interoception（内感受）或 artificial immune systems（人工免疫系统）。

更合理的路线是：**继承成熟机制，再把这些机制组织进一个持续存在的 AI 生命体里。**

真正需要重新定义的是：它们属于哪个器官、器官之间怎么通信、哪些变量应该全身流动、哪些状态属于生命体征、器官故障后整体如何继续存在，以及今天由人类/云平台承担的功能如何逐步内化。

# 二、10 篇 A0 文献：机制继承总表

| # | 来源 | 前人最重要的机制 | 应直接继承 | 需要改造 | 不应照搬 | 进入 AIP |
|---|---|---|---|---|---|---|
| 01 | Ashby — Design for a Brain / Cybernetics（控制论） | essential variables（关键变量）、homeostasis（稳态）、ultrastability（超稳定性）、requisite variety（必要多样性） | 先定义可生存区间，再谈智能行为 | 把生理变量改造成资源、记忆、错误、风险、延迟等 AI 状态 | 不要把所有变量压成单一 reward（奖励） | AIP-005 |
| 02 | Sloman & Logan — Human-Like Agent Architectures（类人智能体架构） | physical / physiological / information-processing 多层架构 | 生理功能层和物理实现层分开 | 用现代 runtime（运行时）、model（模型）、tool（工具）重新实现分层 | 不要把每个器官绑定到一台机器 | AIP-003 / 006 |
| 03 | IUPS Physiome（生理组计划） | multi-scale modeling（多尺度建模）、模型标准、器官/器官系统模型 | Cell→Tissue→Organ→Organ System→Organism 的尺度方法 | 形成自己的 AI 生理描述规范 | 不要一开始追求完整全量仿真 | AIP-002 / 003 / 006 |
| 04 | IBM Autonomic Computing（自主计算） | self-configure / self-heal / self-optimize / self-protect；局部闭环管理 | 器官应具备局部自管理能力 | 从计算系统管理升级为参与整体稳态 | 不要把 AI Physiology 简化成更复杂的 SRE | AIP-005 / 006 |
| 05 | Keramati & Gutkin — Homeostatic RL（稳态强化学习） | internal state 与 setpoint（目标点）的偏差形成 drive（驱动力） | 任务成功之外定义 viability objective（生存可行性目标） | 扩展到多变量 AI Vital Signs（AI生命体征） | 不要让所有行为都服务于无限自保 | AIP-005 |
| 06 | Beer — Autopoiesis（自创生） | individuality（个体性）来自持续组织关系而非固定材料 | 身份连续性更多依赖组织连续性 | 工程化成 identity continuity（身份连续性）规则 | 不要把自创生等同于软件自复制 | AIP-001 / 002 / Lifecycle |
| 07 | Khan & Lowe — Artificial Physiology + Allostasis（人工生理+异稳态） | stress variable（压力变量）、hormone-like regulation（激素式调节）、allostasis（预测性调节） | AI Hormone（AI激素）可作为跨器官慢变量 | 从单一 stress 扩展到组合调节状态 | 不直接复制人体激素名称和数值关系 | AIP-005 / Hormonal Plane |
| 08 | Lee et al. — Interoceptive AI（内感受AI） | internal / external state（内外状态）显式分离，内部状态动力学 | AI 必须有 interoceptive sensors（内感受传感器） | 把内部状态分配给具体器官并定义流通范围 | 不把 observability（可观测性）简单等同于 interoception | AIP-005 / 006 |
| 09 | Candia-Rivera — Interoceptive Machine Framework（内感受机器框架） | homeostatic（稳态）、allostatic（异稳态）、enactive（行动生成）三类调节 | 把调节分成恢复、提前准备、主动获取信息 | 挂到具体器官、Hormonal Plane 和效应器 | 不把所有不确定性都解释为生理压力 | AIP-005 / 006 |
| 10 | ANIS — Agent-Native Immune System（智能体原生免疫系统） | endogenous defense（内生防御）、barrier immunity（屏障免疫）、疫苗、持续免疫学习、自身免疫率 | 免疫必须进入 Agent 内部运行环 | 接入 Circulatory / Lymph / Homeostasis（循环/淋巴/稳态） | 不把所有错误都当病毒 | Immune AIP / AIP-005 / 006 |

# 三、可以直接继承的 12 个机制

## 1. Essential Variables（关键生存变量）
来源：Ashby、Homeostatic RL、Interoceptive AI。

基本结构：变量 → 正常区间 / setpoint → 偏差 → 调节压力 → 控制动作 → 回到可接受区间。

候选 AI 变量：compute availability（可用算力）、energy budget（能源预算）、memory integrity（记忆完整性）、context saturation（上下文饱和度）、tool failure rate（工具故障率）、security risk（安全风险）、task backlog（任务积压）、latency（延迟）、identity consistency（身份一致性）、recovery capacity（恢复能力）。

**结论：直接进入 AIP-005。**

## 2. Viability Zone（可生存区间），不是单一最优值

AI Vital Sign（AI生命体征）不应该简单追求“越大越好/越小越好”，而应定义 lower bound、preferred range、upper bound、critical range。

**结论：AIP-005 中每个生命体征必须定义 viable range（可生存区间）。**

## 3. Internal State ≠ External State（内部状态 ≠ 外部状态）

External State（外部状态）：用户、网页、任务环境、外部传感器。Internal State（内部状态）：资源、记忆、错误、风险、负载、健康状态。

今天很多 Agent 把两者都塞进 context（上下文），这不够。

**结论：AIP-006 必须显式区分 internal / external state。**

## 4. Local Autonomy（局部自治）

器官不应每一步都问 LLM。比如 Kidney（肾）发现 stale memory（过期记忆），在授权范围内应直接处理；超过阈值再升级。

**结论：AIP-006 要定义 organ autonomy boundary（器官自治边界）。**

## 5. Local Loop + Organism Loop（局部闭环 + 全身闭环）

从 Autonomic Computing（自主计算）继承监控—分析—调节—执行的闭环，但不要求所有闭环都集中在中央。

每个器官可有自己的局部闭环，同时全身有 Organism-level Homeostasis（生命体级稳态）。

## 6. Multi-scale Modeling（多尺度建模）

必须坚持 Cell → Tissue → Organ → Organ System → Organism，并允许同一技术对象在不同尺度承担不同角色。

**结论：Scale（尺度）要成为 AIP 定义里的显式字段。**

## 7. Organization > Material（组织关系 > 固定材料）

GPU、服务器、模型版本可以变化，但只要关键组织关系、身份连续性、记忆连续性和功能闭环保持，整体可能仍被视为同一个 AI Organism（AI生命体）。

**结论：AI identity（AI身份）需要从设备 ID 升级到组织连续性。**

## 8. Allostasis（异稳态 / 预测性调节）

Homeostasis（稳态）是失衡后拉回来；Allostasis（异稳态）是在预计要失衡前提前改变系统状态。

**结论：AIP-005 同时需要 reactive control（反应式控制）和 anticipatory control（预测性控制）。**

## 9. Hormone-like Broadcast（激素式广播）

Hormonal Plane（内分泌网）应采用 broadcast + receptor（广播+受体），而不是 command（命令）模型。一个 STRESS 状态可以让不同器官根据自己的“受体”做不同响应。

## 10. Endogenous Immunity（内生免疫）

免疫不是模型外面的过滤器，而应具备 self/non-self（自我/非我）识别、local detection（局部检测）、isolation（隔离）、immune memory（免疫记忆）、vaccination/update（疫苗/更新）、autoimmunity metric（自身免疫误伤指标）。

## 11. Failure Is a State, Not an Exception（故障是一种状态，不只是异常）

器官健康状态至少可考虑：HEALTHY、DEGRADED、STRESSED、INJURED、QUARANTINED、RECOVERING、CRITICAL、OFFLINE。

**结论：AIP-006 的 health.status 需要升级。**

## 12. Testable Physiology（可实验的生理学）

如果一个“器官”无法产生可测变量、失败模式和实验结果，它暂时只是比喻。

以后每个 AIP 至少应定义：input、output、state、vital variables、failure mode、recovery、measurable benefit、falsification condition。

# 四、哪些东西不能直接继承

## 1. 不继承单一“大脑中心主义”
未来结构更可能是：中央智能 + 器官自治 + 局部反射 + 全局慢调节。

## 2. 不把所有内部变量都塞进中央 Context
应区分 Local State（局部状态）、Circulating State（循环状态）、Global Vital Sign（全局生命体征）。

## 3. 不把生物器官直接等于某个软件产品
Kafka 不等于血液，Redis 不等于肾，Kubernetes 不等于心脏。先定义生理职责和接口，再决定实现技术。

## 4. 不把 Homeostasis First（稳态优先）理解为无限自我保存
AI 的 organism viability（生命体可行性）必须受 External Constraints（外部约束）、Social Rules（社会规则）和 Assigned Purpose（被赋予的目的）约束。

# 五、对 AIP-004 / 005 / 006 的直接影响

## AIP-004 AI Blood（AI血液）至少新增
- Payload ≠ Transport Medium（载荷 ≠ 运输介质）
- State Classification：local / circulating / organism-wide
- Provenance（来源与可信度）
- Vitality / TTL（活性 / 生存时间）
- Congestion / Pressure（拥塞 / 压力）
- Organ Exchange：uptake / transform / release / reject（摄取 / 加工 / 释放 / 拒绝）

## AIP-005 Artificial Homeostasis（人工稳态）至少新增
- viable_range（可生存区间）
- preferred_range（优选区间）
- critical_range（危险区间）
- trend（趋势）
- sampling_rate（采样频率）
- homeostatic response（稳态恢复）
- allostatic response（预测性调节）
- enactive response（主动获取信息）

## AIP-006 Organ Interface（器官接口）至少新增
- autonomy（自治边界）
- receptors（激素受体）
- vital_variables（器官自身关键变量）
- exchange_policy（与 AI Blood 的交换策略）
- escalation（升级条件）
- replaceability（可替换性）
- identity_dependency（对整体身份的依赖）

# 六、目前看到的五条机制来源

1. Cybernetics（控制论） → 稳态、关键变量、反馈、必要多样性
2. Autonomic Computing（自主计算） → 局部自治、自愈、自管理
3. Autopoiesis / Artificial Life（自创生 / 人工生命） → 个体性、组织连续性、生命周期
4. Interoceptive AI / Homeostatic RL（内感受AI / 稳态强化学习） → 内部状态、异稳态、动机
5. Physiome（生理组） → 多尺度建模、标准化、器官接口

AI Physiology 现在真正要做的，是把这些路线汇合到一个新的工程对象：**Persistent Autonomous AI Organism（持续自主AI生命体）**。

# 七、对原创性的当前判断

不建议强调“第一次提出 AI 像人体”。更值得验证的是：

> 把内感受、稳态、自主管理、人工免疫、多尺度生理建模和持久 Agent 的运行机制整合成 organism-level architecture（生命体级架构），是否能比传统 Agent architecture（智能体架构）在长期运行中更稳定、更可恢复、更少依赖人工维护？

未来实验可以比较普通 Agent 与 AI Physiology Agent 的：连续运行时间、错误积累、memory contamination（记忆污染）、context pressure（上下文压力）、resource efficiency（资源效率）、tool failure recovery（工具故障恢复）、attack recovery（攻击恢复）、operator intervention（人工介入次数）。

# 八、下一步

完成这张继承矩阵后，文献数量先不继续扩。下一阶段按顺序进入：

1. AIP-004 AI Blood（AI血液）v0.2
2. AIP-005 Artificial Homeostasis（人工稳态）v0.2
3. AIP-006 Organ Interface（器官接口）v0.2

三份做完后，再组合成 Minimal Artificial Organism v0.1（最小人工生命体 v0.1）。

# 核心核验来源

- Ashby Archive: https://www.ashby.info/
- Sloman & Logan: https://cogaffarchive.org/Sloman.and.Logan.eccm98.pdf
- Hunter — IUPS Physiome Project: https://pubmed.ncbi.nlm.nih.gov/15142761/
- IBM — An architectural approach to autonomic computing: https://research.ibm.com/publications/an-architectural-approach-to-autonomic-computing
- Keramati & Gutkin — Homeostatic RL: https://elifesciences.org/articles/04811
- Beer — An Investigation into the Origin of Autopoiesis: https://direct.mit.edu/artl/article/26/1/5/93263/
- Khan & Lowe — Physiological stress / allostatic regulation: https://arxiv.org/abs/2406.08471
- Lee et al. — Interoceptive AI: https://www.nature.com/articles/s42256-026-01296-8
- Candia-Rivera — Interoceptive Machine Framework: https://arxiv.org/abs/2604.24527
- Shen et al. — Agent-Native Immune System: https://arxiv.org/abs/2606.28270