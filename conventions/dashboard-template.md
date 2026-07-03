# Dashboard 模板（v9.1）

> 项目级看板。由**主编剧 agent** 维护。每次任一 agent 完成 / 失败 / 评分变化时立即更新。

## 1. 文件路径

```
_工作区/{项目名}/dashboard.md
```

## 2. 完整模板

把下面这个模板复制到 dashboard.md，按规则填充：

```markdown
# 📊 {项目名} · Dashboard

> 最后更新：{ISO8601}
> 项目状态：{🟢 进行中 / 🟡 等待用户 / 🔴 卡住 / ✅ 已交付}
> Bible 版本：{v0.X}
> 当前 sprint 进度：{X}/{Y} 任务完成

---

## 1. 总体进度

| 阶段 | 状态 | 完成度 | 关键产物 |
|------|------|--------|---------|
| A. 前研 | {状态emoji} | {%} | {产物路径或 -} |
| B. 策划 | | | bible v0.X |
| C. 工程 | | | character_payloads × N |
| D. 制作 | | | finals × (N×M) |
| E. 验收 | | | E-01: X.X / E-02: X.X |
| F. 交付 | | | 05_delivery/ |

**整体完成度**：{%}

---

## 2. 当前阶段详情

{自然语言描述：当前在做什么 / 等什么 / 卡哪里}

---

## 3. 各 Agent 最新状态

| Agent | 最近一次跑 | 状态 | 耗时 | tokens | trace |
|-------|-----------|------|------|--------|-------|
| A-01 genre-router | {date} | {✅/❌/⏳} | {s} | {k} | [link] |
| A-02 reference-curator | | | | | |
| A-03 inspiration-archivist | | | | | |
| B-01 historian | | | | | |
| B-02 paradox-architect | | | | | |
| B-03 structure-designer | | | | | |
| B-04 world-builder | | | | | |
| C-01 rule-maker | | | | | |
| C-02 prop-master | | | | | |
| C-03 detail-injector | | | | | |
| C-04 distributor | | | | | |
| D-01 identity-architect | | | | | |
| D-02 lead-writer | | | | | |
| D-03 voice-differentiator | | | | | |
| E-01 logic-auditor | | | | | |
| E-02 blind-playtester | | | | | |
| F-01 delivery-packager | | | | | |

---

## 4. 最新评分 (v0.X)

### E-01 逻辑审计
| 维度 | 分数 | 权重 |
|------|------|------|
| 跨角色一致性 | {N} | 0.4 |
| 时间线一致性 | {N} | 0.3 |
| 诡计自洽性 | {N} | 0.2 |
| 信息泄露控制 | {N} | 0.1 |
| **总分** | **{X.X}** | {✅ pass / ❌ fail} (阈值 {Y.Y}) |

### E-02 盲测
| 维度 | 分数 | 权重 |
|------|------|------|
| 凶手可识别度 | | 0.4 |
| 动机清晰度 | | 0.3 |
| 信息分发均衡度 | | 0.2 |
| 无上帝视角断点 | | 0.1 |
| **总分** | **{X.X}** | {✅ / ❌} |

---

## 5. 当前 Blockers

| ID | 严重度 | 描述 | 责任 agent | 预期修复后总分 | 状态 |
|----|--------|------|-----------|--------------|------|
| B-1 | 🔴 high | {描述} | C-04 | {6.5 → 7.8} | 待修 |
| B-2 | 🟡 medium | {描述} | D-02 | {7.8 → 8.0} | 修复中 |

---

## 6. 评分走势

| 版本 | 锁版时间 | E-01 | E-02 | 状态 | 备注 |
|------|---------|------|------|------|------|
| v0.1 | {date} | 8.3 ✅ | 6.5 ❌ | 重做 | 首版 |
| v0.2 | {date} | ⏳ | ⏳ | 进行中 | 修复 B-1, B-2 |

---

## 7. 资源消耗

- 累计 tokens：约 {N}k
- 累计运行时间：约 {N} 分钟
- 累计 agent 调用次数：{N}
- 涉及 subagent 次数：{N}（主要在 E-02 盲测）

---

## 8. 下一步动作

{自然语言列表：
1. 谁（你 / 主编剧 / agent X）
2. 做什么
3. 预估耗时
}

---

## 9. 历史里程碑

- {date} brief 锁定
- {date} Bible v0.1 锁定（用户审批通过）
- {date} 工程部完工，payload × N 分发完毕
- {date} 制作部完工，finals × (N×M) 产出
- {date} v0.1 验收：E-01 8.3 ✅ / E-02 6.5 ❌

---

## 10. 文档索引（快捷跳转）

- 📜 [Project Brief](00_brief/project_brief.json)
- 📖 [Bible (current)](01_planning/bible.json)
- 📊 [Distribution Report](02_engineering/distribution_report.md)
- 🔍 [Consistency Report](04_qa/consistency_report.md)
- 🎮 [Playtest Report](04_qa/playtest_report.md)
- 📦 [Delivery](05_delivery/)
- 📝 [Changelog](_meta/changelog.md)
```

## 3. 更新规则

主编剧 agent **必须**在以下时机更新 dashboard：

1. 任一 agent 启动 → 把该 agent 状态改 ⏳
2. 任一 agent 完成（success / fail） → 更新状态 + 时间 + tokens
3. QA agent 产出评分 → 更新第 4 节 + 第 6 节走势
4. 用户审批 Bible → 加里程碑
5. 修订完成 → 加里程碑 + 评分走势

**不允许**：
- ❌ 累计多个事件再批量更新（必须实时）
- ❌ 删除历史走势（追加，不覆盖）

## 4. emoji 速查

| Emoji | 含义 |
|-------|------|
| ✅ | 完成 / 通过 |
| ❌ | 失败 / 未通过 |
| ⏳ | 进行中 / 等待 |
| 🟢 | 健康状态 |
| 🟡 | 警告 / 等待人工 |
| 🔴 | 严重问题 / 卡住 |
| 🔒 | 锁定 / 不可改 |
| ⚡ | 关键节点 |
| 📊 | 数据 / 报告 |

## 5. dashboard 与 trace 的关系

- **trace**：完整 + 历史 + 机器可读（JSON）
- **dashboard**：摘要 + 当前 + 人类可读（Markdown）

dashboard 是 trace 的"汇总视图"，主编剧每次更新时从 `_trace/` 读最新的 trace 摘要进 dashboard。

## 6. 反例

- ❌ dashboard 不更新（成了过时文档）
- ❌ dashboard 写得比 trace 还详细（应该是摘要）
- ❌ 删除走势历史（"看不出进步" = 失去迭代抓手）
- ❌ 用「未知」「待补」「TBD」当默认值（应该写"⏳ 进行中"或"-"）

---
**版本**：v9.1 / 2026-05-28
