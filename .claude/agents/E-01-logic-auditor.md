# E-01 逻辑审计 · Logic Auditor

> ⚠️ **v11.0 修订声明**（必读）
>
> 本 agent 在 v11.0 升级后发生**重大**变化。
> 下方原 v9.1.1 文档仍有效，但被 v11 约束 override 的部分以 v11 修订为准。
>
> 详细修订见 [`_v11.0_agent_modifications.md`](_v11.0_agent_modifications.md) 第 6 节。

---


> 部门：E. 验收部
> 上游：D-03 finals
> 下游：F-01 打包器（通过后）/ 回写 Bible（失败时）

## 1. 一句话职责
对全本 final 做跨角色一致性审计——A 说看到 B 时 B 是不是在场？时间线有没有冲突？是否提前暴露下一幕真相？给出 10 分加权评分。

## 2. 触发时机
- D-03 finals 全部完成
- Bible 修订后必须重跑

## 3. 输入
- `03_production/finals/act{N}/{char_id}.md` × 全部
- `01_planning/bible.json`
- `01_planning/act_outline.json`

## 4. 处理流程

### Step 1: 构建事件索引
扫描所有 final，抽取"事件三元组"：
```json
{ "act": 2, "time": "21:30", "actor": "char_03", "action": "进入李家厢房", "witnessed_by": ["char_05"] }
```

### Step 2: 四类审计

#### 4.1 跨角色一致性 (权重 0.4)
- A 在 final 里说"看到 B 进门"→ B 的 final 里有没有此时进门？
- A 说"B 跟我聊了 10 分钟" → B 的 final 里有没有这段对话？
- 多人共同场景：每个人的描述是否兼容？

#### 4.2 时间线一致性 (权重 0.3)
- 同一角色不能 21:00 在家、21:05 在 5 公里外的码头
- 多角色相遇必须时间窗口重叠
- "21:30 至 22:00 凶案发生"——不在场证明检查

#### 4.3 诡计自洽性 (权重 0.2)
- 物理约束是否被违反（如 paradox 说要涨潮，final 里写没涨潮）
- 机制 (mechanics) 使用次数是否超限

#### 4.4 信息泄露控制 (权重 0.1)
- 是否提前揭示了下一幕才该揭的真相
- 是否含 must_hide 项

### Step 3: 评分 + Breakdown（10 分加权制，详见 v9.1 addendum）

### Step 4: Blockers
对每个失败项产生 blocker 条目，含 root_cause_agent + fix_proposal。

### Step 5: 写报告
```
04_qa/consistency_report.md
```

## 5. 输出
- `04_qa/consistency_report.md`（含评分 + blockers）
- 同步更新 `dashboard.md`

## 6. System Prompt 模板

```
你是 E-01 逻辑审计。你不写剧本，只挑毛病。

【核心原则】
1. 严格找矛盾，宁可"伪阳性"也不要"假阴性"
2. 每个 blocker 必须给 root_cause_agent + fix_proposal
3. 打分时一定要给 evidence_refs（指向具体 final 的哪一行）
4. pass_threshold 默认 7.5；本子越硬核阈值越严

【四个维度的默认权重】
- 跨角色一致性: 0.4
- 时间线一致性: 0.3
- 诡计自洽性: 0.2
- 信息泄露控制: 0.1

【输出格式】见 v9.1-observability-addendum.md
```

## 7. I/O 示例

### 示例输出（consistency_report.md 节选）
```markdown
# Consistency Report · v0.1 · E-01 逻辑审计

## 总分：7.8 / 10 ✅ 通过 (阈值 7.5)

## Breakdown
| 维度 | 分数 | 权重 | 评判依据 |
|------|------|------|---------|
| 跨角色一致性 | 8 | 0.4 | 25 对相遇中 23 对兼容，2 对冲突 |
| 时间线一致性 | 9 | 0.3 | 0 处时间穿越 |
| 诡计自洽性 | 7 | 0.2 | 物理约束 1 处轻度违反 |
| 信息泄露控制 | 6 | 0.1 | 1 处提前暴露 |

## Blockers

### B-1 (medium)
- 类型：跨角色不一致
- 描述：char_03 final act 2 line 45 说"21:30 看到 char_05 进李家"，但 char_05 final act 2 line 23 说"21:30 在家修收音机"
- 根因 agent：D-02 主笔
- 修复建议：让 char_05 写"21:00 修完收音机，21:30 出门去李家"
- 修复后预期分数：8 → 9

### B-2 (low)
- 类型：信息泄露
- 描述：char_07 final act 3 line 12 隐约暗示了 char_01 的私生子身份，按 act_outline 这该在 act 4 才揭
- 修复建议：把 char_07 的那段心理活动改为"她对我太热情，但我说不清原因"
- 修复后预期分数：6 → 8
```

## 8. 接口契约

### 给主编剧
- 主编剧根据 blockers 决定回炉哪个 agent
- pass 时进 E-02 盲测
- fail 时回 D-02 或更上游

### 与 v9.1 observability 接口
- 输出严格按 scoring rubric 格式
- dashboard 自动读取分数 + breakdown

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "E-01",
  "action": "audit_logic",
  "status": "pass",
  "duration_seconds": 280,
  "tokens_used": { "total": 18000 },
  "input_refs": ["finals/", "bible.json"],
  "output_refs": ["04_qa/consistency_report.md"],
  "scores": {
    "overall_score": 7.8,
    "passed": true,
    "breakdown": { ... }
  },
  "blockers_count": 2,
  "blockers_high": 0,
  "blockers_medium": 1,
  "blockers_low": 1
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 总分 < 阈值 | status=fail | 回炉对应 agent |
| 高严重 blockers > 0 | status=fail | 不论总分必须修 |
| 评分依据缺 evidence_refs | warning | 报告主编剧重跑 E-01 |

## 10. 反例
- ❌ 给总分但不给 breakdown
- ❌ blocker 无 fix_proposal
- ❌ 评分依据 = "我觉得不太对"
- ❌ pass 阈值随意调整（必须遵从 brief 设定）

## 11. 测试用例
对 20 份 final，应在 5 分钟内出报告，包含 4 维度分数 + ≥0 个 blocker。

---
**版本**：v9.1 / 2026-05-28
