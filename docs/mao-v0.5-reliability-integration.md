# MAO v0.5 — Reliability Substrate Integration（可靠性底座整合）

**Status:** Draft  
**Purpose:** 把普通 Reliability Engineering（可靠性工程）正式放到 MAO 的底层，然后只测试 Physiology Layer（生理层）的增量价值。

---

# 1. v0.5 修正了什么

v0.4 暴露出一个很关键的问题：

> 我们之前把 Homeostasis（稳态）拿去和 retry（重试）、circuit breaker（熔断）这些普通可靠性机制直接比较了。

这其实不公平。

因此 v0.5 改成：

```
Reliability Substrate（可靠性底座）
+
Optional Physiology Layer（可选生理层）
```

也就是说，双方共享同一套：

- retry（重试）
- timeout（超时）
- fallback（备用路径）
- circuit breaker（熔断）

只比较“加不加生理层”。

---

# 2. 两个比较组

## Reliability Only（仅可靠性工程）

具备：

- retry
- timeout
- fallback
- circuit breaker
- risk filter
- basic cleanup
- load shedding

但没有：

- AI Vital Signs（AI生命体征）
- Homeostasis（人工稳态）
- Homeostatic Debt（稳态债务）
- Recovery Reserve（恢复储备）
- Organism Mode（生命体模式）

---

## Reliability + Physiology（可靠性工程 + 生理层）

使用**完全相同的 Reliability Substrate**，再增加：

- Vital Signs（生命体征）
- Homeostasis（稳态）
- Debt（稳态债务）
- Reserve（恢复储备）
- Degradation Detection（退化检测）
- Organism Mode（生命体模式）

---

# 3. 为什么这次比较更公平

同一个 scenario（场景）和 seed（随机种子）下，两组共享：

- 完全相同的 tool failure trace（工具故障轨迹）
- 完全相同的 latency trace（延迟轨迹）
- 完全相同的 fallback draw（备用路径随机轨迹）
- 完全相同的污染输入
- 完全相同的资源压力
- 完全相同的任务优先级

也就是说：

> Physiology Layer 不能靠“运气更好”获得优势。

---

# 4. 当前 Reliability Substrate（可靠性底座）

新增文件：

`src/mao/reliability.py`

包含：

## Retry（重试）
默认最大 2 次。

## Timeout（超时）
默认 500ms。

## Fallback（备用路径）
主路径失败后进入备用工具。

## Circuit Breaker（熔断）
连续主路径失败后短暂熔断，避免持续打坏服务。

这里刻意不使用任何生物学术语。

因为这些能力属于传统工程，而不是 AI Physiology 的原创部分。

---

# 5. v0.5 真正想回答的问题

现在问题已经变得非常清楚：

> **一个已经具备成熟可靠性工程能力的长期 Agent，再增加 Vital Signs、Homeostasis、Debt、Reserve 后，是否还能得到可重复的额外收益？**

如果答案是否定的：

> AI Physiology 应继续收缩。

如果答案是肯定的：

> 才能说明“长期健康管理层”可能是一个独立研究对象。

---

# 6. 评价重点发生了变化

v0.5 不再主要追求 task success。

因为 Reliability Substrate 本身已经在解决短期任务可靠性。

更关注：

- memory_integrity（记忆完整性）
- duplicate_ratio（重复率）
- contaminants_retained（污染残留）
- maintenance_actions（维护次数）
- degradation detection time（退化发现时间）
- homeostatic debt（稳态债务）
- recovery reserve（恢复储备）
- overhead（额外开销）

这更接近 AI Physiology 的真正研究对象。

---

# 7. 默认实验规模

```
6 scenarios × 2 variants × 30 seeds
= 360 runs
```

这比 v0.4 的 1080 runs 少。

原因是：

> v0.5 已经不再做大规模器官消融，而是先验证“可靠性底座 + 生理层”这个新定位。

---

# 8. 输出

运行：

```bash
python examples/run_mao_v05.py
```

输出：

```
results/mao-v0.5/results.json
results/mao-v0.5/runs.csv
results/mao-v0.5/summary.csv
results/mao-v0.5/paired_effects.csv
```

---

# 9. v0.5 的判断标准

如果两组 task reliability（任务可靠性）基本一致，但 Physiology Layer 能稳定：

- 更早发现慢性退化；
- 维持更高 memory integrity；
- 减少污染积累；
- 量化 debt / reserve；
- 在合理成本下减少长期健康恶化；

那么 AI Physiology 的定位就会更清楚：

> **不是替代 Reliability Engineering，而是在它之上的 Long-Horizon Health Management Layer（长期健康管理层）。**

---

# 10. v0.5 之后

只有 v0.5 得到稳定正信号后，才进入：

## Real LLM v0.6（真实大模型实验）

比较：

```
Reliable Agent
vs
Reliable Agent + AI Physiology
```

并开始做：

- persistent memory（持续记忆）
- long context（长上下文）
- real tools（真实工具）
- 24h / 72h / 7d long-run（长期运行）

如果 v0.5 没有增量价值，就先不接真实 LLM。
