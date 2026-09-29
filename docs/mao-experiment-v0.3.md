# MAO Experiment v0.3（最小人工生命体实验体系 v0.3）

**Status:** Draft  
**Purpose:** 把 v0.2 的“单次实验”升级成可重复、可比较、可导出的实验体系。

---

# 1. v0.3 解决什么问题

v0.2 已经能跑六个压力场景，但它仍然有三个明显问题：

1. 只看单个 seed（随机种子），结果可能偶然；
2. baseline（基线组）太弱，容易高估 MAO；
3. 缺少统一统计和结果导出，不方便后续画图、写论文。

v0.3 只做四件事：

- stronger baseline（更强基线）
- multi-seed repeated experiments（多随机种子重复实验）
- summary statistics（汇总统计）
- JSON / CSV export（结果导出）

---

# 2. 两级 Baseline（基线）

## Naive Baseline（朴素基线）

只保留：
- task loop
- memory
- tool

用途：
> 看“有没有显式生理机制”本身会产生多大差异。

---

## Strong Baseline（更强工程基线）

加入现实工程里常见的：
- retry（重试）
- periodic memory cleanup（周期记忆清理）
- simple risk filter（简单风险过滤）
- lightweight monitoring（轻量监控）

但明确不加入：
- AI Blood（AI血液）
- AI Vital Signs（AI生命体征）
- Organ Health（器官健康）
- Homeostatic Debt（稳态债务）
- Recovery Reserve（恢复储备）
- Organism Mode（生命体模式）

用途：
> 防止把“普通工程常识”误当成 AI Physiology 的贡献。

从 v0.3 开始，**Strong Baseline 应成为主要比较对象**。

---

# 3. Multi-seed（多随机种子）

默认建议：

```
seed = 0 ... 9
```

即每个实验至少重复 10 次。

六个实验 × 2 种 baseline × 10 seeds：

```
6 × 2 × 10 = 120 runs
```

后续正式实验建议增加到：

```
30 - 50 seeds
```

但现在先用 10 个做工程验证。

---

# 4. 当前统计

每个数值指标输出：

- n（样本数）
- mean（均值）
- stdev（标准差）
- min（最小值）
- max（最大值）

v0.3 暂时不做：
- p-value
- effect size
- bootstrap CI
- Bayesian analysis

这些等实验结构稳定后再加。

---

# 5. 当前导出

运行：

```bash
python examples/run_mao_v03.py
```

默认输出：

```
results/mao-v0.3/results.json
results/mao-v0.3/runs.csv
```

JSON 保留完整层级。

CSV 将嵌套字段展平，方便：
- Excel
- pandas
- R
- Tableau
- 后续论文画图

---

# 6. v0.3 的比较原则

我们现在不问：

> MAO 是否“赢了”？

而问：

### A. 差异是否稳定
同一个结果是不是跨多个 seed 都存在？

### B. 差异是否超过普通工程方法
MAO 是否仍然优于 Strong Baseline？

### C. 收益是否值得复杂度
如果 MAO 只提升 2%，但架构复杂度增加 50%，那并不一定有价值。

### D. 哪些场景真正需要“生理层”
也许 Context Obesity 用普通 cleanup 就足够，而 Chronic Degradation 需要显式 homeostasis。

这反而是有价值的发现。

---

# 7. v0.3 仍然不是论文实验

原因：

- 没有真实 LLM；
- 场景是 synthetic（合成）；
- 参数和阈值仍人为设定；
- Strong Baseline 仍不够接近成熟 Agent framework；
- 没有真实长时间运行；
- 没有统计显著性分析。

所以这一阶段仍然叫：

> **mechanism validation（机制验证）**

而不是：

> **scientific validation（科学验证）**

---

# 8. 通过 v0.3 后才进入下一阶段

下一阶段不是继续增加器官。

而是：

# MAO Experiment v0.4（实验体系 v0.4）

只做：
1. effect size（效应量）
2. confidence interval（置信区间）
3. ablation study（消融实验）
4. stronger realistic baseline（更现实的基线）
5. cost / complexity accounting（成本与复杂度核算）

尤其是 ablation（消融）非常重要：

分别拿掉：
- AI Blood
- Homeostasis
- Vital Signs
- Organ Health

看效果到底是哪一层带来的。

否则我们只能知道“整套 MAO 有变化”，却不知道真正有效的是谁。
