# MAO v0.5.1 — Longitudinal Health Benchmark（纵向健康基准）

**Status:** Draft  
**Purpose:** 检验 Homeostatic Debt（稳态债务）与 Recovery Reserve（恢复储备）是否具备超出普通趋势监控的长期预测价值。

---

# 1. 为什么做 v0.5.1

v0.5 的结果是一个明确的负结果：

> 在明显故障、明显污染、明显资源压力等场景里，成熟 Reliability Engineering（可靠性工程）已经能处理大部分问题，Physiology Layer（生理层）没有表现出稳定增量价值。

所以 v0.5.1 不再测试“已经越线”的问题，而专门测试：

> **Low-and-Slow Degradation（低强度长期退化）**

特点：
- 单个指标大部分时间都没有明显越界；
- 每次变化都很小；
- 系统短期仍然可用；
- 多个变量长期共同漂移；
- 最后在新的扰动下可能出现系统性失败。

---

# 2. 比较对象

## Adaptive Monitoring Baseline（自适应监控基线）

使用普通工程可观测方法：
- moving average（移动平均）
- trend / slope（趋势 / 斜率）
- rolling error（滚动错误）
- level + trend composite score（水平+趋势复合分）

## Physiology Monitor（生理监测器）

使用：
- Homeostatic Debt（稳态债务）
- Recovery Reserve（恢复储备）
- debt trend（债务趋势）
- reserve decline（储备下降）

这保证了生理层不能仅仅因为“会看趋势”而获胜。

---

# 3. 首轮规模

- 200 seeds
- 每个 seed：
  - 1 条 degraded trajectory（缓慢退化轨迹）
  - 1 条 healthy trajectory（健康对照轨迹）
- 400 条轨迹
- 2 类监测器分别评估
- 共 800 次评估
- 每条轨迹 240 个时间步

---

# 4. 首轮结果

| 指标 | Adaptive Monitoring | Physiology Monitor |
|---|---:|---:|
| Future-failure AUC（未来故障预测AUC） | 0.765 | 0.781 |
| Early-warning recall（提前预警召回率） | 100.0% | 92.5% |
| False early-warning rate（假提前预警率） | 95.8% | 37.1% |
| Mean lead time（真阳性平均提前量） | 162.8 | 103.5 |

当前最值得注意的不是 AUC 提高了 0.016，而是：

> Physiology Monitor 显著减少了“到处报警”的情况。

但它的代价也很明确：
- 漏掉了一部分未来故障；
- 报警时间更晚。

因此它不是全面胜出，而是表现出不同的 precision / recall trade-off（精确率/召回率权衡）。

---

# 5. 当前能说什么

可以说：

> 在当前合成纵向基准中，Debt / Reserve 型监测开始表现出与普通趋势监控不同的预测行为，尤其是假预警明显更少，同时故障排序能力略有提高。

不能说：
- Debt 已被证明有效；
- Reserve 已被证明能预测真实 AI 故障；
- AI Chronic Disease（AI慢性病）已被证明存在。

原因：
> future-failure label（未来故障标签）仍然来自我们自己设计的 synthetic generator（合成生成器）。

---

# 6. 下一步

进入：

# MAO v0.5.2 — Predictive Validity & Calibration（预测有效性与校准）

只做：
1. ROC / Precision-Recall 曲线
2. threshold calibration（阈值校准）
3. 相同 false-positive budget（误报预算）下比较
4. 多种非线性、阶段性、恢复后复发的退化轨迹
5. Debt-only / Reserve-only / Debt+Reserve 消融

只有 v0.5.2 仍保留增量信号，再进入真实 LLM。
