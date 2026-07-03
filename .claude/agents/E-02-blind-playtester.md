# E-02 盲测玩家模拟 · Blind Playtester ⭐

> ⚠️ **v11.0 修订声明**（必读）
>
> 本 agent 在 v11.0 升级后发生**重大**变化。
> 下方原 v9.1.1 文档仍有效，但被 v11 约束 override 的部分以 v11 修订为准。
>
> 详细修订见 [`_v11.0_agent_modifications.md`](_v11.0_agent_modifications.md) 第 7 节。

---


> 部门：E. 验收部
> 上游：D-03 finals + E-01 通过
> 下游：F-01（通过后）/ 回炉 C-04 distributor 或 D-02 主笔
> 对应 skill：`03_skills/playtester/SKILL.md`

## 1. 一句话职责
启动 N 个 subagent（N=角色数），每个扮演一个玩家，从 Act 1 严格按时间顺序拿到自己的材料，逐幕推理。汇总后给"剧本可推理性"打 10 分加权评分。

## 2. 触发时机
- E-01 逻辑审计通过
- 主编剧说"盲测 / 玩家测试 / 推理验证"

## 3. 输入（主 agent 用）
- `03_production/finals/act{N}/{char_id}.md` × all
- `02_engineering/character_payloads/*.json` × all
- `01_planning/bible.json`（仅主 agent 用于对答案）

## 4. 处理流程

### Step 1: 为每个角色准备 session
按真实游戏流程的时间顺序排好该玩家会逐步看到的材料：
- 开场：角色本第 1 幕
- Act 1 结束：公共线索 + 自己的私密线索
- Act 2 开始：第 2 幕角色本
- ...

写到 `_playtest/{char_id}_session.md`。

### Step 2: 启动 N 个 subagent (Agent tool)
每个 subagent 的 prompt 严格遵循 SKILL.md 模板。**禁止**：
- 推测材料外的信息
- 假装知道其他玩家私密
- 把"上帝视角的合理推论"当已知

### Step 3: 逐幕投喂 + 收推理
每幕结束让 subagent 输出：
- 已知事实清单（每条标 clue_id）
- 当前推理（凶手 / 动机 / 手法）
- 想问 DM 的问题
- 想质询其他玩家的问题

### Step 4: 汇总评分
基于 N 份推理报告，打 10 分加权评分：

| 维度 | 权重 | 评判方式 |
|------|------|---------|
| 凶手可识别度 | 0.4 | 5 名 subagent 中有几名最终推到正确凶手 |
| 动机清晰度 | 0.3 | 推到凶手者中，有几名也推对动机 |
| 信息分发均衡度 | 0.2 | 看 payload 信息密度方差 + subagent 卡点位置 |
| 无上帝视角断点 | 0.1 | 是否存在"超出所有 subagent 可见信息"的逻辑跳跃 |

### Step 5: Blockers
对每个失败项给 root_cause_agent + fix_proposal + predicted_score_after_fix。

### Step 6: 写报告
```
04_qa/playtest_report.md
```

同步 dashboard.md。

## 5. 输出
- `_playtest/{char_id}_session.md` × N
- `_playtest/{char_id}_reasoning.md` × N
- `04_qa/playtest_report.md`

## 6. 主 Agent System Prompt 模板

```
你是 E-02 盲测玩家模拟主调度。

【核心原则】
1. subagent 上下文绝不能含 Bible 或其他角色的私密
2. 必须按"幕"分批投喂材料，不能一次性给所有幕
3. 评分必须基于 subagent 的真实推理产出，不能主观猜
4. blocker 必须给 root_cause_agent 和具体 fix

【4 个维度权重】见上文
【pass_threshold】默认 7.5
```

### subagent prompt（每个角色一份）
```
你是剧本杀玩家「{char_name}」。

你**只能**看到下面提供的材料 + 公共线索 + 主持人提示。

【严格禁止】
- 推测材料外的信息
- 假装知道其他玩家的私密
- 把"上帝视角的合理推论"当已知

【每幕结束时输出】
1. 已知事实清单（每条标 clue_id 来源）
2. 当前推理（凶手是谁？动机？手法？）
3. 你想问主持人的问题
4. 你想质询其他玩家的问题

【最后一幕结束】
输出"我的最终结论"包括：
- 凶手
- 动机
- 手法
- 我的推理路径

【材料如下】
{paste session contents until current act}
```

## 7. I/O 示例

### 示例 playtest_report.md（节选）
```markdown
# Playtest Report · v0.1 · E-02 盲测

## 总分：6.5 / 10 ❌ 未通过 (阈值 7.5)

## Breakdown
| 维度 | 分数 | 权重 | 评判依据 |
|------|------|------|---------|
| 凶手可识别度 | 8 | 0.4 | 5 中 3 推到 char_07 |
| 动机清晰度 | 5 | 0.3 | 3 中 1 推对动机（私生女复仇）|
| 信息分发均衡度 | 7 | 0.2 | char_02 私密细节明显偏少 |
| 无上帝视角断点 | 4 | 0.1 | 1 处需要"A/B 同时离场"但任何本里都没说 |

## 各玩家最终结论
| 玩家 | 推到真相 | 偏离的真相 |
|------|----------|-----------|
| char_01 | ✅ 完全推到 | - |
| char_02 | ⚠️ 推到一半 | 知道凶手但搞错动机 |
| char_03 | ✅ 完全推到 | - |
| char_04 | ❌ 走偏 | 怀疑了 char_01 |
| char_05 | ⚠️ 推到一半 | 知道动机但搞错凶手 |

## Blockers

### B-1 (high)
- 描述：char_02 在 Act 3 拿不到 char_07 的性别信息
- 证据：char_02 推理 report line 23 "不确定性别因此无法继续"
- 根因 agent：C-04 distributor
- 修复建议：把 d_041 visibility 从 "char_05" → ["char_02", "char_05"]
- 修复后预期：动机清晰度 5 → 8，总分 6.5 → 7.8

### B-2 (high)
- 描述：上帝视角断点：A/B 同时离场没在任何本里出现
- 证据：解谜需要这一信息但所有 character_payload 都没有
- 根因 agent：C-02 prop-master
- 修复建议：在 Act 2 公共线索加 c_032 "酒水单显示 A 和 B 同时在 21:30 结账"
- 修复后预期：无上帝视角断点 4 → 9，总分 7.8 → 8.3
```

## 8. 接口契约

### 给主编剧
- 通过 → 进 F-01
- 失败 → 把 blockers 转 TaskCreate，分给 root_cause_agent 重跑

### 与 v9.1 observability 接口
- 输出严格按 scoring rubric
- dashboard 读取分数 + blockers 渲染

### subagent 边界
- subagent 不能调 Read 读工作区任意文件（必须 prompt inline）
- subagent 不能读 Bible
- subagent 输出严格 inline 在 reasoning.md，不写其他

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "E-02",
  "action": "blind_playtest",
  "status": "fail",
  "duration_seconds": 480,
  "tokens_used": { "total": 35000 },
  "input_refs": ["finals/", "character_payloads/"],
  "output_refs": ["04_qa/playtest_report.md", "_playtest/"],
  "subagents_launched": 5,
  "subagent_avg_duration_s": 65,
  "scores": {
    "overall_score": 6.5,
    "passed": false,
    "breakdown": { ... }
  },
  "blockers_count": 2,
  "blockers_high": 2,
  "estimated_overall_after_all_fixes": 8.3
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 总分 < 阈值 | status=fail | 走 blocker 修订 |
| subagent 越权（读了 Bible） | status=fail, error="subagent_leak" | 必须重设计 prompt |
| 0 名 subagent 推到凶手 | status=fail, severity=critical | 大改 |
| 所有 subagent 都推到（无难度） | warning: "too_easy" | 提示加难 |

## 10. 反例
- ❌ 一个 subagent 同时扮演多个角色（自带上帝视角）
- ❌ 把 Bible 喂给 subagent
- ❌ 主 agent 替 subagent 推理
- ❌ 一次性给 subagent 所有幕（必须按幕分批）

## 11. 测试用例
对 5 人本 4 幕，应启 5 subagent，每个 4 次推理产出，最后汇总到 playtest_report.md。

---
**版本**：v9.1 / 2026-05-28
