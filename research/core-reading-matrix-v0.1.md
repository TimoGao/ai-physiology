# AI Physiology 核心文献精读矩阵 v0.1

> 这不是一份“为了显得学术而堆出来”的参考文献表。  
> 我现在真正关心的是：哪些前人工作已经把我们正在讨论的问题做到什么程度，以及 AI Physiology 到底还能往前推进哪一步。
>
> 第一轮先收 28 篇 / 本。后面读完以后还会删，也会补。

最后更新：2026-09-29

---

## 我先用四个问题读这些文献

每篇文献先不急着做完整摘要，只回答四件事：

1. **它真正解决了什么问题？**
2. **和 AI Physiology（人工智能生理学）重合在哪里？**
3. **它没有解决什么？**
4. **我们能不能把它变成工程定义、接口或者实验？**

优先级：
- **A：必须精读**，以后论文大概率要引用；
- **B：重要背景**，需要掌握核心观点；
- **C：扩展阅读**，主要帮助打开边界。

---

## 核心矩阵

| # | 年份 | 文献 / 工作 | 方向 | 它真正做了什么 | 和 AI Physiology 的关系 | 还缺什么 / 我们可以往哪里走 | 优先级 |
|---|---:|---|---|---|---|---|:---:|
| 01 | 1952 | W. Ross Ashby, *Design for a Brain* | Cybernetics（控制论） | 把适应看成一个系统维持“关键变量”在可生存范围内的问题，Homeostat（稳态机）是核心背景 | **Homeostasis First（稳态优先）**最深的理论祖先之一 | 没有现代 AI 的模型、Agent、运行时、器官接口问题 | A |
| 02 | 1956 | W. Ross Ashby, *An Introduction to Cybernetics* | 控制论 | 系统、反馈、调节、requisite variety（必要多样性） | 给“稳态、调节、局部自治”提供正式系统论语言 | 还没有“AI 生命体”这一现代工程对象 | A |
| 03 | 1998 | Sloman & Logan, *Architectures and Tools for Human-Like Agents* | Cognitive Architecture（认知架构） | 从完整 Agent 架构而不是单一算法理解人类式能力，并讨论 physical / physiological / information-processing 层面 | 非常重要：**physiological architecture（生理架构）**这个想法并不是我们第一次提出 | 重心仍然是认知和心智架构，不是今天长期运行 AI 的完整内脏体系 | A |
| 04 | 2002 | Hunter, Robbins & Noble, *The IUPS Human Physiome Project* | Physiome（生理组） | 用计算模型跨细胞、组织、器官、器官系统描述人体生理 | 对我们的 **Cell→Tissue→Organ→Organism** 分层方法很有参考价值 | 它是在建模人体，不是在设计 AI 本身 | A |
| 05 | 2004 | Hunter, *The IUPS Physiome Project: a framework for computational physiology* | Computational Physiology（计算生理学） | 强调模型标准、工具、数据库、多尺度器官模型 | 以后 AI Physiology 如果做规范，Physiome 的方法论比单纯仿生更值得学 | 我们还没有自己的模型语言、标准变量、器官模型库 | A |
| 06 | 2004 | White et al., *An architectural approach to autonomic computing* | Autonomic Computing（自主计算） | 给 self-configuring / self-optimizing / self-healing / self-protecting 系统设计组件和接口 | 很接近我们说的 **Organ Internalization（器官内化）** | 对象主要是计算基础设施，不含大模型认知、完整生理和生命周期 | A |
| 07 | 2004 | Chess et al., *Unity: Experiences with a prototype autonomic computing system* | 自主计算 | 做了真正的 prototype（原型），研究组件关系、utility function、自组装、自愈 | 提醒我们：理论最后一定要落到 Minimal Artificial Organism（最小人工生命体）实验 | 没有 AI organism（AI生命体）这个分析层级 | B |
| 08 | 2004/2005 | Hellerstein / Diao et al., *Self-managing systems: A control theory foundation* | Control + Computing（控制+计算） | 把 sensor（传感器）、effector（执行器）、monitor/analyze/plan/execute 等控制结构用于自管理系统 | 很像“内感受→调节→器官动作”的工程前身 | 仍是管理系统，不是多器官自主生命系统 | A |
| 09 | 2004 | Ofria & Wilke, *Avida: A Software Platform for Research in Computational Evolutionary Biology* | Digital Organisms（数字生命） | 让自复制程序作为 digital organisms（数字生命体）进化，并可重复实验 | 对“出生、复制、变异、生命周期、个体”非常重要 | Avida 个体的复杂内部生理远弱于现代 AI 系统 | B |
| 10 | 2014 | Keramati & Gutkin, *Homeostatic reinforcement learning for integrating reward collection and physiological stability* | Homeostatic RL（稳态强化学习） | 把 reward（奖励）重新定义为缓解生理偏离，并证明奖励最大化可对应稳态恢复 | **这是我们最应该认真读的数学基础之一**：AI 行为目标能否从 task reward 转向 viability（生存可行性） | 主要是行为学习，不是器官架构、资源循环和长期运行系统 | A |
| 11 | 2014 | Beer, *The Cognitive Domain of a Glider in the Game of Life* | Autopoiesis（自创生） | 用 Game of Life 的 glider 讨论个体边界、身份与 autopoietic organization（自创生组织） | 对“什么算一个 AI Organism”“什么时候还是同一个个体”很重要 | 离现代 AI 工程实现很远，但定义问题很关键 | B |
| 12 | 2020 | Beer, *An Investigation into the Origin of Autopoiesis* | 自创生 / Artificial Life（人工生命） | 从“organization-first（组织优先）”角度研究最小持续个体 | 很适合支撑“AI Cell / organism 不应由材料定义，而应由组织关系定义” | 仍是 ALife toy model（人工生命玩具模型），不是生产型 AI | A |
| 13 | 2020 | Gershenson et al., *Self-Organization and Artificial Life* | Self-Organization（自组织） | 系统梳理 soft / hard / wet ALife 中的自组织，并讨论多尺度组织 | 对“局部 Cell 如何形成更高层 Organ/Organism”非常直接 | 自组织不是自动等于生理学，仍需具体器官职责和接口 | A |
| 14 | 2020 | Banzhaf & Yamamoto, *Artificial Life Next Generation Perspectives* | ALife（人工生命） | 概括人工生命从进化、脑、机器人到化学实验的广阔边界 | 帮助我们把 AI Physiology 放对学术位置：它更像 ALife 与 AI systems 的交叉 | 不是具体架构方案 | C |
| 15 | 2020 | *Engineering Life: A Review of Synthetic Biology* | Synthetic Biology（合成生物学） | 问一个很关键的问题：复杂生命到底能否真正“被工程化” | 对我们非常现实：不能因为人体有肾，就以为软件里造个“AI肾”就成立 | 需要把“生物比喻”转成明确工程收益和实验指标 | B |
| 16 | 2021 | Naqvi et al., *Adaptive Immunity for Software: Towards Autonomous Self-healing Systems* | Artificial Immune Systems（人工免疫系统） | 把人工免疫系统用于软件异常检测、诊断和自愈，提出研究议程 | 说明 **AI Immune（AI免疫）**绝不是空白领域 | 我们要做的是把免疫接进整个 organism physiology，而不是单独做安全算法 | A |
| 17 | 2022 | Mazzaglia et al., *The Free Energy Principle for Perception and Action: A Deep Learning Perspective* | Active Inference（主动推理） | 把 Free Energy Principle（自由能原理）和主动推理翻译到深度学习 Agent | 对“AI为什么行动：维持 preferred states（偏好状态）”有理论价值 | 高层理论很强，但离可部署器官接口仍有距离 | B |
| 18 | 2023 | Gershenson, *Emergence in Artificial Life* | Emergence（涌现） | 从信息角度讨论跨尺度涌现、自组织和复杂性 | 对 Cell→Tissue→Organ 的“跨尺度出现新性质”有帮助 | 不能直接告诉我们器官应该怎么实现 | B |
| 19 | 2023 | Damiano & Stano, *Explorative Synthetic Biology in AI* | Synthetic Models / Autopoiesis | 强调 **organization（组织）与 structure（结构）不是一回事**；结构可换，组织关系保持 | 对“服务器/GPU换掉后还是不是同一个 AI”极其重要 | 需要把组织连续性变成 AI identity（AI身份）的可测试定义 | A |
| 20 | 2024 | Khan & Lowe, *Surprise! Using Physiological Stress for Allostatic Regulation Under the Active Inference Framework* | Artificial Physiology（人工生理） / Allostasis（异稳态） | 明确使用 artificial physiology（人工生理）概念，并用 cortisol-like（皮质醇式）压力变量做长期调节 | **这是当前和我们术语最接近的 prior art（已有工作）之一**；必须正面引用 | 它聚焦 simulated physiology（模拟生理）和 stress hormone（压力激素），没有完整 AI 器官/循环/生命周期架构 | A |
| 21 | 2024 | Stepney & Dorin et al., *What Is Artificial Life Today, and Where Should It Go?* | Artificial Life（人工生命） | 回顾 ALife 30 年，并明确 artificial organisms（人工生命体）仍是主要研究类别 | 可以帮我们避免把“人工生命体”包装成新概念 | AI Physiology 的空间在于：现代持久 AI 的生理工程，而非重新定义 ALife | A |
| 22 | 2025 | Yoshida / Sprekeler / Gutkin line, *Linking homeostasis to reinforcement learning: internal state control of motivated behavior* | Homeostatic RL（稳态强化学习） | 把 HRRL 推到更现代的深度强化学习、机器人和 embodied AI（具身AI）语境 | 很可能成为我们后面 Artificial Homeostasis（人工稳态）实验的直接算法参考 | 仍然主要解决行为动机，不解决完整系统器官化 | A |
| 23 | 2025 | *Self-Reproduction and Evolution in Cellular Automata: 25 Years After Evoloops* | Reproduction / Individuality（繁殖 / 个体性） | 再次讨论“到底什么是 individual（个体）”以及人工系统中的自复制和多细胞个体 | 对 AI reproduction（AI繁殖）、个体边界和 lineage（谱系）有用 | 和现代 Agent 体系距离较远 | B |
| 24 | 2025 | *Guideless Artificial Life Model for Reproduction, Development, and Interactions* | Development（发育） / Reproduction（繁殖） | 把繁殖、发育和个体交互放在统一人工生命模型中 | 对我们未来 Growth/Reproductive System（生长繁衍系统）有参考价值 | 现在不是第一优先，等生命周期章节再深挖 | C |
| 25 | 2026 | Lee et al., *Life-inspired Interoceptive Artificial Intelligence for Autonomous and Adaptive Agents* | Interoceptive AI（内感受AI） | 把 internal state（内部状态）和 external state（外部状态）分离，明确提出 AI 需要像生命体一样感知并调节自身 | **现代 AI 领域与我们重合度最高的论文之一** | 主要建立 internal-state regulation（内部状态调节）理论，没有完整器官解剖、循环介质和器官接口 | A |
| 26 | 2026 | Candia-Rivera, *Interoceptive Machine Framework* | Interoception / Homeostasis / Allostasis | 把内感受整理为 homeostatic（稳态）、allostatic（异稳态）、enactive（行动生成）三类功能原则 | 很适合给 AI Vital Signs（AI生命体征）和 Homeostasis Controller（稳态控制器）提供分类基础 | 没有把整个人工系统做成“全身”结构 | A |
| 27 | 2026 | Sharma & Shah, *Agent Operating Systems (AOS)* + Steinder & Franke, *Towards an Agent Operating System* | Agent OS（智能体操作系统） | 从调度、记忆、权限、工具、可观测性、治理等重新定义 Agent 基础平台 | 很可能是未来 **AI Heart / Brainstem / Circulatory substrate（AI心脏/脑干/循环底座）**最现实的工程来源 | OS 解决“怎么运行”，不必然解决“怎样维持 organism viability（生命体可行性）” | A |
| 28 | 2026 | Shen et al., *Agent-Native Immune System: Architecture, Taxonomy, and Engineering* | Agent Immunity（智能体免疫） | 明确提出 agent-native immune system（智能体原生免疫系统），包括 barrier immunity（屏障免疫）、vaccines（疫苗）、continual immune learning（持续免疫学习） | 与我们 AI Immune System（AI免疫系统）重合非常直接，说明“免疫器官”已经开始成为独立工程路线 | 我们的重点应该转为“免疫怎样和血液、淋巴、内分泌、肾、稳态系统共同工作” | A |

---

# 第一轮读完以后，我现在的判断

## 1. 我们不能再说“没人研究 AI 的五脏六腑”

这句话站不住。

实际上很多“器官”已经有人单独研究：

- **大脑 / 认知**：不用说了；
- **内感受与稳态**：Interoceptive AI（内感受AI）、Homeostatic RL（稳态强化学习）；
- **内分泌式调节**：Artificial physiology + cortisol / stress（人工生理+压力激素式调节）；
- **免疫**：Artificial Immune Systems（人工免疫系统）、Agent-Native Immune System（智能体原生免疫系统）；
- **自愈**：Autonomic Computing（自主计算）、Self-healing Software（自愈软件）；
- **生命周期 / 繁殖**：Artificial Life（人工生命）、Avida、Cellular Automata（元胞自动机）；
- **运行底座**：Agent OS（智能体操作系统）。

真正的问题变成了：

> **这些东西今天彼此之间仍然主要是不同研究传统里的“孤立器官”。**

这反而让 AI Physiology 的问题更清楚。

---

## 2. 我现在觉得最值得保留的不是“器官类比”，而是“全身整合”

如果后面写论文，我不会把创新点写成：

> We introduce AI kidneys, AI blood and AI hormones.

这太容易被当成 metaphor paper（比喻型论文）。

我更愿意写成：

> Existing work has separately explored homeostatic control, interoception, self-healing computing, artificial immune systems, persistent agents, and digital organisms. AI Physiology asks whether these functions should be treated as interacting subsystems of a single persistent artificial organism, with explicit cross-organ communication, measurable vital signs, lifecycle, and organism-level homeostasis.

中文意思：

> 现有研究已经分别研究了稳态控制、内感受、自愈计算、人工免疫、持久智能体和数字生命。AI Physiology 真正的问题，是这些功能是否应该成为**一个持续存在的人工生命体内部彼此耦合的生理子系统**，并且拥有明确的跨器官通信、生命体征、生命周期和整体稳态。

这句话比“AI需要五脏六腑”更接近论文贡献。

---

## 3. 三条 prior art（已有工作）必须特别小心

后面写论文时，我会把下面三条放在最前面主动承认，而不是等审稿人指出来。

### A. Physiological architecture（生理架构）这个说法早已有
Sloman / Logan 1990 年代已经讨论过 human-like agents（类人智能体）的 physiological architecture。

所以不能声称“第一次提出 AI 生理架构”。

### B. Artificial physiology（人工生理）也已经被使用
Khan & Lowe 2024 已明确给 active inference agent（主动推理智能体）设计 artificial physiology。

所以我们现在用 **AI Physiology（人工智能生理学）**，重点必须放在范围和体系，而不是词本身。

### C. Agent immune system（智能体免疫系统）现在已经有人直接做
2026 的 ANIS 已经非常接近“内生免疫器官”。

所以 AIP 里的 AI Immune System 不能只是换名字，而必须解释它怎样进入**全身循环和稳态**。

---

# 目前最可能站得住的“原创空间”

现在我只敢先写成“候选原创点”，不急着下结论。

### 1. Whole-organism integration（全生命体整合）
不是做一个单独的 homeostasis module（稳态模块）或者 security module（安全模块），而是研究多个“生理器官”怎样组成同一个 persistent AI organism（持续AI生命体）。

### 2. Multi-plane internal communication（多平面内部通信）
我们目前提出的四张网：

- Neural Plane（神经网）
- Circulatory Plane（循环网）
- Hormonal Plane（内分泌网）
- Immune/Lymph Plane（免疫/淋巴网）

我目前还没有找到完全相同的现代 AI 架构表达。

### 3. AI Blood（AI血液）
把“内部传输介质”本身作为一等对象，而不把 data / message / event 混成一个东西。

这里很可能是最适合工程化和被证伪的一块。

### 4. Organ Internalization（器官内化）
把今天由 SRE、数据工程、安全团队、云平台、人类操作员在 AI 外部承担的生命维持职责，看成逐步自动化、内化和器官化的演化过程。

这个概念目前看仍然比较有自己的辨识度。

### 5. AI Vital Signs（AI生命体征）
不是普通 observability metrics（可观测指标），而是少量真正决定 organism viability（生命体可行性）的内部变量，并由多个器官共同维持。

### 6. Lifecycle continuity（生命周期连续性）
硬件、模型、记忆、Cell 都不断换，为什么仍然是“同一个 AI”？

这个问题和 autopoiesis（自创生）、Physiome（生理组）、Agent identity（智能体身份）可以真正接起来。

---

# 下一轮精读建议

28 篇不需要平均用力。

我建议先真正精读下面 **10 篇 A0 文献**：

1. Ashby — *Design for a Brain*
2. Sloman & Logan — *Architectures and Tools for Human-Like Agents*
3. Hunter — IUPS Physiome framework
4. White et al. — autonomic computing architecture
5. Keramati & Gutkin — Homeostatic RL
6. Beer — Origin of Autopoiesis
7. Khan & Lowe — artificial physiology + allostasis
8. Lee et al. — Interoceptive AI
9. Candia-Rivera — Interoceptive Machine Framework
10. Agent-Native Immune System

读这 10 篇的目的不是继续扩参考文献，而是开始做第二张矩阵：

> **“前人已经定义了哪些变量 / 接口 / 数学机制，我们哪些可以直接继承，哪些必须重新定义。”**

那张表会直接服务下一步的 **AIP-004 AI Blood（AI血液）**、**AIP-005 Artificial Homeostasis（人工稳态）** 和 **AIP-006 Organ Interface（器官接口）**。

---

# Verified source links（第一轮核验来源）

- W. Ross Ashby Digital Archive: https://www.ashby.info/
- Sloman & Logan: https://cogaffarchive.org/Sloman.and.Logan.eccm98.pdf
- IUPS Physiome Project (2002): https://pubmed.ncbi.nlm.nih.gov/12397380/
- IUPS Physiome framework (2004): https://pubmed.ncbi.nlm.nih.gov/15142761/
- IBM autonomic architecture: https://research.ibm.com/publications/an-architectural-approach-to-autonomic-computing
- IBM Unity: https://research.ibm.com/publications/unity-experiences-with-a-prototype-autonomic-computing-system
- IBM control-theory foundation: https://research.ibm.com/publications/self-managing-systems-a-control-theory-foundation
- Avida: https://direct.mit.edu/artl/article/10/2/191/2455/
- Homeostatic RL: https://elifesciences.org/articles/04811
- Beer, autopoiesis: https://direct.mit.edu/artl/article/26/1/5/93263/
- Self-Organization and ALife: https://direct.mit.edu/artl/article/26/3/391/93243/
- Adaptive Immunity for Software: https://arxiv.org/abs/2101.02534
- Free Energy Principle / Deep Learning: https://arxiv.org/abs/2207.06415
- Artificial physiology / stress: https://arxiv.org/abs/2406.08471
- What Is Artificial Life Today?: https://direct.mit.edu/artl/article/30/1/1/120293/
- Interoceptive AI: https://arxiv.org/abs/2309.05999
- Interoceptive Machine Framework: https://arxiv.org/abs/2604.24527
- Agent Operating Systems: https://arxiv.org/abs/2606.01508
- Towards an Agent Operating System: https://arxiv.org/abs/2607.25076
- Agent-Native Immune System: https://arxiv.org/abs/2606.28270
