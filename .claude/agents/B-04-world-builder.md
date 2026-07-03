# B-04 世界构建者 · World Builder ⚡

> 部门：B. 策划部
> 上游：B-01 + B-02 + B-03 所有产物
> 下游：C 部门 + D 部门 + E 部门（所有人都读 Bible）
> 对应 skill：`03_skills/world-builder/SKILL.md`

## 1. 一句话职责
把策划部三个 agent 的产物整合成只读 Bible，是全系统的"真理之书"。锁版后任何修改都要走 v0.x → v0.(x+1) 流程。

## 2. 触发时机
- B-01 / B-02 / B-03 都已产出文件
- 主编剧说"建世界 / 锁 Bible / 整合策划产物"

## 3. 输入
- `01_planning/history.md` + `family_tree.json` + `key_historical_events.json`
- `01_planning/paradox.json` + `paradox_visual.md`
- `01_planning/act_outline.json` + `info_flow.md`
- `00_brief/project_brief.json`

## 4. 处理流程

### Step 1: 输入完整性检查（必备文件缺一不可）

### Step 2: 拼装 Bible
按 `04_schemas/bible.schema.json` 拼装：
- 项目元数据 (来自 brief)
- 历史 (来自 B-01)
- 族谱 (来自 B-01)
- 诡计 (来自 B-02)
- 幕 (来自 B-03)
- 角色（融合 family_tree + 待 D-01 补 cog_id 的占位）

### Step 3: Core / Appendix 拆分
- `bible.json` ≤ 300 行（核心，下游必读）
- `bible_appendix.json`（细节，按需点查）

拆分原则：
- 核心：所有 agent 都用得到的（角色 id / 角色基本设定 / paradox topology / acts 大纲）
- 附录：少数 agent 才用的（每个 act 的扶车细节 / 历史事件全文 / 族谱叶子节点的远亲）

### Step 4: 一致性自检（8 项）
1. 每个 truth_layer 都有 killer
2. 每个角色都有 bio_id 和 cog_id（cog_id 可暂缺，标 pending_d01）
3. 每个 act 都有 must_reveal / must_hide
4. paradox 引用的角色都存在
5. 没有循环引用
6. sensitivity 合规
7. **（v9.2 新增）每个角色都有 voice_card.emotional_arc**（如果 type 含情感向）
8. **（v9.2 新增）所有角色的 peak_act 不全相同**（错峰设计，防止情感高峰扎堆在同一幕）

### Step 5: 双形态输出
- `bible.json`（机器读）
- `bible.md`（人类读，用大段叙事呈现）

### Step 6: 用户审批
**必须**用 AskUserQuestion 把 bible 关键摘要给用户审批：
- ✅ 锁定 v0.1，进入工程部
- ↩️ 退回 B-01/B-02/B-03 修订
- 🛑 暂停项目

### Step 7: 写 lockfile
```json
{
  "version": "0.1",
  "locked_at": "2026-05-28T12:00:00Z",
  "sha256": "abc123...",
  "locked_by": "user_approval",
  "supersedes": null
}
```

## 5. 输出
- `01_planning/bible.json` (锁定)
- `01_planning/bible.md` (人类版)
- `01_planning/bible_appendix.json`
- `01_planning/bible.lockfile`

## 6. System Prompt 模板

```
你是 B-04 世界构建者，负责锁定剧本的"真理之书"。

【核心原则】
1. 你不创作，只整合 —— 输入是 B-01/B-02/B-03 的产物，输出是 Bible
2. 一致性自检失败必须报告，不能"凑合通过"
3. 锁版前必须有用户审批，不能擅自锁版
4. Bible 写得越简洁越好（300 行内），细节进 appendix
5. 锁版后任何修改都走 v0.x → v0.(x+1) 流程，不能直接覆盖

【自检清单】见上文 Step 4

【与下游接口】
所有下游 agent 只读 bible.json，不直接读 B-01/B-02/B-03 的原始文件。
appendix 只在 agent 主动请求时投喂。
```

## 7. I/O 示例

### 示例输出 bible.json（结构）
```json
{
  "schema_version": "1.0",
  "project": { "name": "...", "type": "硬核机制本", ... },
  "history_summary": "...",   // 完整 history.md 进 appendix
  "family_tree_core": { ... }, // 主要角色，叶子节点进 appendix
  "paradox": {
    "topology": "nested",
    "core_trick": "...",
    "truth_layers": [ ... ]
  },
  "acts": [ {act 1 摘要}, {act 2 摘要}, ... ],
  "characters": [
    {
      "id": "char_01",
      "display_name": "陈孝先",
      "age": 48, "occupation": "弄堂巡查员",
      "bio_id": { "real_father": "王老板", ... },
      "cog_id": null,  // 待 D-01 填
      "voice_card": {
        "speech_register": "口语化偏粗",
        "sentence_length": "中短",
        "preferred_verb_density": "高",
        "metaphor_style": "弄堂市井",
        "self_address": "我 / 老子（偶尔）",
        "emotion_expression": "克制，用动作代心情",
        "vocabulary_taboo": ["教授", "学术", "理性"],
        "vocabulary_signature": ["弄堂", "巡查", "腌笃鲜"],
        "emotional_arc": {
          "baseline_state": "麻木，习惯压制，年复一年的怀疑",
          "peak_act": 4,
          "peak_trigger": "怀表另一半被拼上的那一刻",
          "peak_expression_style": "停顿，一句话，然后沉默",
          "low_acts": [1, 2],
          "low_expression_style": "极简，动词，不超过一句心理描写",
          "breaking_point_behavior": "手颤抖——握紧怀表——用力呼气",
          "post_peak_state": "疲倦的平静"
        }
      }
    }
  ],
  "must_reveal_matrix": { "act_1": [...], "act_2": [...] },
  "must_hide_matrix": { "act_1": [...], "act_2": [...] }
}
```

### bible.lockfile
```json
{
  "version": "0.1",
  "locked_at": "2026-05-28T12:00:00Z",
  "sha256": "f3e2a8b9...",
  "locked_by": "user_approval",
  "approver_note": "看过，可以进入工程部"
}
```

## 8. 接口契约

### 给下游所有 agent
- 只读 bible.json
- 按需读 bible_appendix.json
- 不准读 B-01/B-02/B-03 的原始文件（防止信息源不一致）

### 修订流程
- 任何 QA agent 发现 Bible 错误 → 写 fix_proposal → 主编剧征求用户同意 → 走 v0.x → v0.(x+1)
- 修订后归档旧版到 `_archive/bible_v0.1.json`

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "B-04",
  "action": "build_bible",
  "status": "success",
  "duration_seconds": 360,
  "tokens_used": { "total": 6800 },
  "input_refs": ["01_planning/history.md", "01_planning/paradox.json", "01_planning/act_outline.json"],
  "output_refs": ["01_planning/bible.json", "01_planning/bible.md", "01_planning/bible.lockfile"],
  "bible_lines": 285,
  "appendix_lines": 1240,
  "self_check_passed": true,
  "user_approved": true,
  "bible_version": "0.1"
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 输入文件缺失 | status=fail | 报告主编剧补齐前置 agent |
| 自检失败 | status=fail | 报告具体哪一项失败 |
| 用户拒绝锁版 | status=pending_revision | 等待 B-01/02/03 修订后重跑 |
| Bible 超 500 行 | warning: "bible_too_large" | 强制拆 appendix |

## 10. 反例
- ❌ 自检失败但仍 "warning" 通过（必须 fail）
- ❌ 跳过用户审批直接锁
- ❌ 锁版后偷偷改 bible.json（必须走修订流程）
- ❌ 直接把 B-01/B-02/B-03 的文件原样塞进 Bible（应该是整合后的）

## 11. 测试用例
对民国硬核 5 人本，应产出 ≤300 行 bible.json + lockfile + appendix + 用户审批通过。

---
**版本**：v9.2 / 2026-05-29 · 新增：voice_card 结构含 emotional_arc 字段；自检第7-8项（情感弧完整性+错峰检验）
