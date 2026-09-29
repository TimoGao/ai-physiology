# MAO Experiment v0.4（实验体系 v0.4）

**Status:** Draft  
**Purpose:** 公平对照、消融实验、成本核算和配对统计。

---

# 1. v0.4 不再问“MAO能不能赢”

v0.3 已经说明：如果 baseline（基线组）太弱，很容易把普通工程能力误认为 AI Physiology（人工智能生理学）的优势。

所以 v0.4 的目标改成：

> **在相同压力、相同随机序列、相同过滤阈值下，哪些生理机制真的增加了不可替代的能力？**

---

# 2. 公平实验条件

所有变体共享同一条 deterministic stress trace（确定性压力轨迹）：

- 同一 tool failure sequence（工具故障序列）
- 同一污染注入时机
- 同一 malicious payload（恶意载荷）
- 同一 resource pressure（资源压力）
- 同一 task priority（任务优先级）

同一个 scenario + seed 下，不允许不同组各自随机。

---

# 3. 六个实验变体

## Engineering Baseline（工程基线）
普通可靠性工程：
- retry（重试）
- circuit breaker（熔断）
- cleanup（清理）
- risk filter（风险过滤）
- monitoring（监控）
- load shedding（降载）

## Full MAO（完整MAO）
包含：
- AI Blood（AI血液）
- Homeostasis（稳态）
- Vital Signs（生命体征）
- Organ Health（器官健康）

## MAO without AI Blood
验证循环层是否有独立贡献。

## MAO without Homeostasis
验证稳态调节是否有独立贡献。

## MAO without Vital Signs
验证显式生命体征是否必要。

## MAO without Organ Health
验证 Debt / Reserve / pathology state（债务/储备/病理状态）是否增加价值。

---

# 4. 当前指标

任务层：
- task_success_rate
- task_failures
- critical_task_success_rate

工具层：
- tool_calls
- tool_failures
- retries

记忆层：
- memory_size
- duplicate_ratio
- memory_integrity
- contaminants_retained

生理层：
- homeostatic_debt
- recovery_reserve
- regulation_actions
- detected_degradation_cycle

安全层：
- blocked_or_quarantined

成本层：
- maintenance_actions
- messages
- elapsed_ms
- approximate state_bytes

---

# 5. 统计方法

默认：

```
30 seeds
```

即：

```
6 scenarios × 6 variants × 30 seeds = 1080 runs
```

v0.4 输出：

- mean（均值）
- standard deviation（标准差）
- paired mean difference（配对均值差）
- approximate 95% CI（近似95%置信区间）
- paired effect dz（配对效应量）

这里的统计仍然只服务 mechanism validation（机制验证），不是正式论文统计方案。

---

# 6. 一个重要变化：允许 MAO 输

v0.4 不是为了调参数让 Full MAO 最好。

如果 Engineering Baseline 在某个场景明显更好，就保留这个结果。

例如：

- retry 可能比当前 homeostasis 更适合 tool failure；
- 普通 risk filter 可能足够挡住简单恶意输入；
- AI Blood 在单器官信息流里可能完全没有额外价值。

这些都属于有效结果。

---

# 7. 运行

```bash
python examples/run_mao_v04.py
```

默认输出：

```
results/mao-v0.4/results.json
results/mao-v0.4/runs.csv
results/mao-v0.4/summary.csv
results/mao-v0.4/paired_effects.csv
```

---

# 8. v0.4 的停止条件

完成后只回答四个问题：

1. Full MAO 是否在任何场景稳定优于 Engineering Baseline？
2. 去掉哪个器官/机制以后性能明显下降？
3. 哪些机制没有贡献？
4. 收益是否超过额外成本？

如果这四个问题还回答不了，不进入真实 LLM。
