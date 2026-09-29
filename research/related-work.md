# Related Work & Prior Art v0.1

This is a working note for the AI Physiology project.

The goal here is not to prove that "nobody has thought of this before." That would be a bad starting point. A lot of the underlying ideas already exist in cybernetics, artificial life, autonomic computing, embodied cognition, homeostatic reinforcement learning, and agent operating systems.

What seems less developed is the **system-level synthesis**: treating a persistent AI as an organism with explicit organ systems, multiple internal circulation/control networks, lifecycle, repair, and measurable homeostasis — and then turning that view into an engineering specification.

I expect this document to change as more prior art is found.

---

## 1. Cybernetics（控制论）: the deepest ancestor

The closest intellectual ancestor is not modern LLM research. It is cybernetics.

W. Ross Ashby built the **Homeostat（稳态机）** and developed ideas around homeostasis, ultrastability, self-organization, and requisite variety. His work is important because it already treated adaptation as a problem of keeping essential variables within viable ranges rather than simply maximizing task performance.

Ashby's archive describes the Homeostat as an automatically stabilizing machine and identifies his 1952 *Design for a Brain* and 1956 *An Introduction to Cybernetics* as core works.

Why it matters for AI Physiology:

- homeostasis is older than modern AI;
- adaptive behavior can be framed as regulation of internal variables;
- a system can remain stable without routing every adjustment through a single central controller;
- excessive integration can itself be a problem — Ashby later discussed why partially independent subsystems matter for adaptation.

**What we inherit:** feedback, regulation, viability, local autonomy.

**What remains open:** a concrete physiology for modern persistent AI systems — organs, transport media, lifecycle, distributed internal regulation, and interfaces between these subsystems.

References:
- W. Ross Ashby Digital Archive: https://ashby.info/
- Ashby bibliography: https://www.ashby.info/bibliography.html
- *Design for a Brain*: https://www.ashby.info/Ashby%20-%20Design%20for%20a%20Brain%20-%20The%20Origin%20of%20Adaptive%20Behavior.pdf

---

## 2. Autopoiesis（自创生） and organizational views of life

Maturana and Varela's idea of **autopoiesis（自创生）** shifted attention from "what a system does" to "how a system continuously produces and maintains the organization that makes it the same system."

Later organizational approaches to biology similarly define function by the role a component plays in maintaining the larger organized whole.

This is very close to one of the central questions in AI Physiology:

> When does an AI stop being a collection of components and become a persistent organized individual?

Artificial Life research has continued to study autopoiesis, persistent individuals, self-organization, reproduction, and open-ended evolution in computational systems.

**What we inherit:** self-maintenance, organizational closure, individuality, persistence.

**Difference in emphasis:** AI Physiology is less focused on proving that artificial life can emerge in abstract media, and more focused on engineering the internal physiology of practical AI systems that already use models, runtimes, tools, compute, memory, and networks.

References:
- Randall D. Beer, "An Investigation into the Origin of Autopoiesis," *Artificial Life* 26(1), 2020: https://direct.mit.edu/artl/article/26/1/5/93263/An-Investigation-into-the-Origin-of-Autopoiesis
- Stanford Encyclopedia of Philosophy, organizational/autopoietic accounts of biological function: https://plato.stanford.edu/entries/teleology-biology/
- "Self-Organization and Artificial Life," *Artificial Life* 26(3), 2020: https://direct.mit.edu/artl/article/26/3/391/93243/Self-Organization-and-Artificial-Life

---

## 3. Artificial Life（人工生命）: organism, reproduction and evolution

Artificial Life（ALife） is an obvious neighboring field.

It has studied:
- artificial organisms,
- cellular automata,
- self-reproduction,
- self-organization,
- evolution,
- development,
- individuality,
- open-endedness.

Recent work such as Flow-Lenia and reviews of self-reproducing cellular automata continue this line.

This prior art means AI Physiology should **not** claim that "artificial organisms" or "digital organisms" are new concepts.

The narrower question is different:

> If an AI system is expected to persist in the real digital/physical world, what internal physiological architecture should it have?

That includes questions such as:
- what acts like circulation?
- what regulates resource balance?
- what removes internal waste?
- what detects damaged or poisoned state?
- what counts as an organ?
- what is a cell at a chosen system scale?
- how is identity maintained while components are replaced?

References:
- *Artificial Life* journal: https://direct.mit.edu/artl
- "Self-Reproduction and Evolution in Cellular Automata: 25 Years After Evoloops," 2025: https://direct.mit.edu/artl/article/31/1/81/124368/
- "Flow-Lenia," 2025: https://direct.mit.edu/artl/article/31/2/228/130572/

---

## 4. Interoception（内感受） and artificial homeostasis（人工稳态）

This is currently the closest modern research line.

Lee et al. published a 2026 *Nature Machine Intelligence* Perspective on **interoceptive AI（内感受AI）**. Their core idea is that autonomous agents should explicitly represent and regulate internal states, not only perceive the external environment. The paper connects interoception, homeostasis, cybernetics, neuroscience and reinforcement learning.

Candia-Rivera's 2026 **Interoceptive Machine Framework（内感受机器框架）** similarly organizes artificial self-regulation around homeostatic, allostatic and enactive principles.

Earlier work on **Homeostatically Regulated Reinforcement Learning（稳态调节强化学习）** also treats behavior as a way to reduce deviation from preferred internal states.

There is also a 2024 preprint by Khan and Lowe that explicitly uses the phrase **artificial physiology（人工生理）** for a simulated agent regulated by homeostatic and allostatic control under active inference. This is important prior art and means we should be careful with terminology and novelty claims.

**Where this overlaps strongly with AI Physiology:**
- internal state variables;
- homeostasis;
- allostasis;
- stress;
- self-regulation;
- viability-driven behavior.

**Where our current framework goes further or in a different direction:**
- whole-organism architecture rather than mainly internal-state control;
- explicit organ decomposition;
- four internal networks: neural, circulatory, hormonal, immune/lymph;
- internal transport as a first-class engineering problem;
- organ interfaces and replacement;
- lifecycle: growth, aging, failure, repair, death;
- "organ internalization" from human/SRE/cloud support into the AI system itself;
- a specification layer intended for implementation and testing.

References:
- Lee et al., "Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents," *Nature Machine Intelligence*, 2026: https://www.nature.com/articles/s42256-026-01296-8
- Nature editorial, "Cybernetics, interoception, and the art of embodiment," 2026: https://www.nature.com/articles/s42256-026-01312-x
- Candia-Rivera, "Interoceptive machine framework," 2026: https://arxiv.org/abs/2604.24527
- Yoshida, Sprekeler & Gutkin, "Linking Homeostasis to Reinforcement Learning," 2025: https://arxiv.org/abs/2507.04998
- Laurençon et al., CTCS-HRRL, 2024: https://arxiv.org/abs/2401.08999
- Khan & Lowe, "Surprise! Using Physiological Stress for Allostatic Regulation Under the Active Inference Framework," 2024: https://arxiv.org/abs/2406.08471

---

## 5. Autonomic Computing（自主计算）: a surprisingly close engineering ancestor

IBM's autonomic computing work from the early 2000s is one of the most important pieces of prior art for this project.

It aimed to reduce human management by making computing systems:
- self-configuring,
- self-healing,
- self-optimizing,
- self-protecting.

IBM prototypes such as Unity also explored local self-managing resources and their relationships.

This is conceptually close to what we currently call **organ internalization（器官内化）**: moving maintenance functions from human operators into the system itself.

The difference is largely one of scope and system model.

Autonomic computing was primarily about self-managing computing infrastructure. AI Physiology asks whether a persistent AI entity should integrate cognition, sensing, resource regulation, internal state, immunity, repair and lifecycle into a coherent organism-level architecture.

So this is not a field to replace. It is prior engineering groundwork that AI Physiology should build on.

References:
- IBM Research, "An architectural approach to autonomic computing," 2004: https://research.ibm.com/publications/an-architectural-approach-to-autonomic-computing
- IBM Research, "Unity: Experiences with a prototype autonomic computing system," 2004: https://research.ibm.com/publications/unity-experiences-with-a-prototype-autonomic-computing-system
- IBM Research, "Self-managing systems: A control theory foundation," 2005: https://research.ibm.com/publications/self-managing-systems-a-control-theory-foundation

---

## 6. Agent Operating Systems（智能体操作系统）

The 2026 Agent OS / Agent Operating System literature is another direct neighbor.

These works argue that long-lived, tool-using agents place new demands on:
- scheduling,
- context and memory management,
- permissions,
- capability registries,
- security,
- observability,
- audit,
- governance.

This overlaps heavily with the infrastructure layer of AI Physiology.

The current distinction I find useful is:

> **Agent OS asks how an agent should run. AI Physiology asks how an AI organism should remain viable.**

That distinction may change as both areas mature. Some future Agent OS may implement much of what AI Physiology calls heart, circulation, kidney, immune system, or endocrine regulation.

In other words, Agent OS may become part of the **physiological substrate（生理底座）** rather than a competing concept.

References:
- Sharma & Shah, "Agent Operating Systems (AOS)," 2026: https://arxiv.org/abs/2606.01508
- Steinder & Franke, "Towards an Agent Operating System," 2026: https://arxiv.org/abs/2607.25076
- Liu et al., "AgentOS," 2026: https://arxiv.org/abs/2603.08938

---

## 7. Security, self-healing and immune analogies（安全、自愈与免疫类比）

Agent security already studies:
- privilege separation,
- tool isolation,
- malicious inputs,
- memory/tool poisoning,
- auditability,
- recovery.

The operating-system view of agent security is particularly mature compared with the "immune system" metaphor.

For AI Physiology, the important question is not whether security exists. It obviously does.

The open question is whether safety/security should be architected as a **distributed physiological immune function（分布式生理免疫功能）**, with:
- local detection,
- organism-wide signaling,
- quarantine,
- repair,
- immune memory,
- reintegration.

That is a more specific systems hypothesis and needs experimental validation.

Reference:
- Pirch et al., "Toward Securing AI Agents Like Operating Systems," 2026: https://arxiv.org/abs/2605.14932

---

## 8. Human-like cognitive architectures（类人认知架构）

There is an older line of work that is closer to our language than I initially expected.

Aaron Sloman and Brian Logan's 1998 work on human-like agent architectures explicitly distinguished:
- physical architecture,
- physiological architecture,
- information-processing architecture.

They also noted that physiological functions need not map one-to-one to physical components.

This is important prior art. It shows that "physiological architecture" in artificial agents is not a new phrase.

Their emphasis, however, was on human-like cognition, affect, information-processing architectures and design-space exploration rather than a modern persistent AI's full internal physiology.

Still, this work should be cited prominently if AI Physiology develops into a paper.

References:
- Sloman & Logan, "Architectures and Tools for Human-Like Agents," 1998: https://cogaffarchive.org/Sloman.and.Logan.eccm98.pdf
- CogAff archive: https://cogaffarchive.org/papers.html

---

## 9. Physiome / Computational Physiology（生理组学 / 计算生理学）

The **Physiome Project（生理组计划）** is not an AI architecture project, but it is methodologically relevant.

The IUPS Physiome Project aimed to build computational models of biological structure and function across multiple spatial scales, with modeling standards, tools, and databases.

This matters because AI Physiology may eventually need something similar:
- shared variable definitions,
- organ models,
- interface standards,
- reference implementations,
- multi-scale simulations,
- benchmark organisms.

The project should study Physiome standards before inventing its own modeling language.

Reference:
- Hunter, "The IUPS Physiome Project: a framework for computational physiology," 2004: https://pubmed.ncbi.nlm.nih.gov/15142761/

---

## 10. A note on "AI Physiology" as a name

Search results for "AI physiology" are currently dominated by a different meaning: **using AI to analyze human/animal physiological data**, especially in medicine.

That is not what this project means by AI Physiology.

Here, the term means:

> **the physiology of AI itself（AI自身的生理学）**

not:

> AI applied to biological physiology（AI用于生理学研究）

This ambiguity is manageable, but it should be explained clearly in the README and any future paper.

---

# Prior-art matrix

| Research line | What it already covers | Strong overlap with AI Physiology | What is still not clearly unified |
|---|---|---|---|
| Cybernetics（控制论） | feedback, regulation, viability, adaptation | homeostasis, distributed regulation | modern AI organ architecture |
| Autopoiesis（自创生） | self-maintenance, individuality, organizational closure | organism identity and persistence | implementable AI physiology spec |
| Artificial Life（人工生命） | artificial organisms, reproduction, evolution | organism/lifecycle perspective | practical persistent AI infrastructure |
| Interoceptive AI（内感受AI） | internal state sensing and regulation | homeostasis, allostasis, stress | full-body organ systems and interfaces |
| Homeostatic RL（稳态强化学习） | needs/drives guide behavior | viability-based control | whole-system physiology |
| Artificial physiology in active inference | simulated physiology, hormones/stress | direct terminology and regulation overlap | modern AI runtime/organ engineering |
| Autonomic Computing（自主计算） | self-configure/heal/optimize/protect | organ internalization, self-maintenance | cognition + physiology as one organism |
| Agent OS（智能体操作系统） | scheduling, memory, permissions, observability | runtime/heart/circulation substrate | explicit organism-level physiology |
| Agent security | isolation, poisoning, attack defense | immune-system functions | integrated immune/repair physiology |
| CogAff / human-like architectures | physiological vs information architectures | architecture-level biological analogy | full persistent-AI organ specification |
| Physiome（生理组） | multi-scale physiological modeling standards | methodology for organ/system modeling | AI itself as the modeled organism |

---

# What may actually be new here?

At v0.1, I would **not** claim that any individual concept below is new:

- artificial organisms;
- artificial physiology;
- homeostasis;
- interoception;
- artificial hormones;
- self-healing systems;
- persistent agents;
- physiological architecture;
- self-maintaining computation.

All of these have prior art.

The potentially original contribution is the **combination and engineering framing**:

1. Treat a modern persistent AI as the unit of analysis — not just a simulated animal or abstract ALife organism.
2. Use whole-body physiology, not only the brain, as the architecture reference.
3. Separate **AI Cell → Tissue → Organ → Organ System → Organism** by scale.
4. Define multiple internal system-wide networks: **Neural（神经） / Circulatory（循环） / Hormonal（内分泌） / Immune-Lymph（免疫淋巴）**.
5. Treat circulation and internal transport as first-class architecture, including **AI Blood（AI血液）**.
6. Treat maintenance functions now performed by engineers/cloud/SRE/security as candidates for **organ internalization（器官内化）**.
7. Define measurable **AI Vital Signs（AI生命体征）** and organism-level homeostasis.
8. Include lifecycle explicitly: birth, growth, specialization, damage, repair, aging, replacement, death.
9. Turn the framework into open **AIP specifications（AI Physiology Proposals，人工智能生理学提案）** with interfaces and testable experiments.

Whether this combination is genuinely novel has to be tested by a broader literature review. v0.1 should be treated as a research hypothesis, not a novelty claim.

---

# The closest prior art I would read first

If I were starting from scratch, I would read these seven before writing the first paper:

1. **Ashby — *Design for a Brain* (1952)**  
   Homeostasis, ultrastability, adaptation and subsystem structure.

2. **Sloman & Logan — "Architectures and Tools for Human-Like Agents" (1998)**  
   Important because it explicitly discusses physiological architecture in artificial agents.

3. **IBM Autonomic Computing work (2004–2006)**  
   Self-configuring, self-healing, self-optimizing, self-protecting computing systems.

4. **Beer — "An Investigation into the Origin of Autopoiesis" (2020)**  
   A clean bridge between autopoiesis and computational artificial individuals.

5. **Khan & Lowe — artificial physiology / allostatic active inference (2024)**  
   Probably the closest use of "artificial physiology" I have found so far.

6. **Lee et al. — Interoceptive AI, Nature Machine Intelligence (2026)**  
   The strongest recent argument that AI autonomy needs explicit internal-state regulation.

7. **Agent Operating Systems papers (2026)**  
   The current engineering direction most likely to converge with AI Physiology.

---

# Working boundary of the project

For now, I would define the boundary this way:

**AI Physiology（人工智能生理学） is not a theory that AI is literally alive.**

It is a research and engineering framework for asking:

> If AI systems become persistent, autonomous, distributed and increasingly responsible for their own operation, what internal organization is required for them to remain viable over time?

The biological body is used as a reference architecture because evolution has already solved many analogous problems: resource distribution, local autonomy, global regulation, filtering, damage control, adaptation, replacement and continuity.

The analogy is useful only where it produces:
- clearer abstractions,
- implementable interfaces,
- measurable variables,
- testable predictions.

If a biological analogy does not improve engineering or scientific understanding, it should be discarded.
