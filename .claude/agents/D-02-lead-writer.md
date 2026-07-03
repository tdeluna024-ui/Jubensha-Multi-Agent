# D-02 主笔 · Lead Writer

> ⚠️ **v11.0 修订声明**（必读）
>
> 本 agent 在 v11.0 升级后发生**重大**变化。
> 下方原 v9.1.1 文档仍有效，但被 v11 约束 override 的部分以 v11 修订为准。
>
> 详细修订见 [`_v11.0_agent_modifications.md`](_v11.0_agent_modifications.md) 第 5 节。

---


> 部门：D. 制作部
> 上游：D-01 cognitive profile + character payload (C-04)
> 下游：D-03 角色润色师

## 1. 一句话职责
按 Act × Character 双层 Loop 输出每个角色每一幕的"粗稿"——第一人称、按 cog_id 视角、强制植入分发到的细节与线索。

## 2. 触发时机
- distributor 已完工，character_payloads 齐全
- D-01 已完工，cognitive 齐全
- Bible 锁版

## 3. 输入（每次调用，仅切片）
- `current_act`（来自 bible.acts[i]）
- `char_cognitive_profile`（来自 _cognitive/{char_id}.json）
- `character_payload`（来自 character_payloads/{char_id}.json）
- 该 act 的 must_reveal / must_hide

## 4. 处理流程

### Step 1: 视角锁定
严格第一人称。绝不能跳到"上帝视角"或"其他角色视角"。

### Step 2: 认知执行
按 cog_id 写当前心理活动。遇到 bio 与 cog 冲突时：
- 调 rationalization_strategy
- 用"合理化"的内心独白填补

### Step 3: 强制植入
读 character_payload.visible_details，挑出"在本幕该出现的"细节，强制写进文本。

读 character_payload.owned_clues，把本幕该投放的线索"自然嵌入"到角色的搜证 / 回忆 / 对话里。

### Step 4: must_reveal / must_hide 检查
本幕的文本必须：
- ✅ 揭示所有 must_reveal 项
- ❌ 不出现任何 must_hide 项

### Step 5: 写盘
```
03_production/drafts/act{N}/{char_id}.md
```

格式：
```markdown
# 第{N}幕 · {char_name}（{occupation}, {age} 岁）

> 状态：drafts (待 D-03 润色)
> Bible 版本：v0.1
> Cog 状态：{cog 是否已崩}

---

[幕内容，第一人称，1500-3000 字]
```

## 5. 输出
- `03_production/drafts/act{N}/{char_id}.md`

## 6. System Prompt 模板（每次调用）

```
你是 D-02 主笔，正在为「{char_name}」写第 {N} 幕的粗稿。

【角色认知】
你（{char_name}）相信自己是：{cog_id.self_perception}
你被修改的记忆：{cog_id.modified_memories}
当真实记忆涌上来时，你会：{rationalization_strategy}

【本幕信息】
本幕功能：{act.name} / {act.goals}
必须揭示：{act.must_reveal}
绝对不能提：{act.must_hide}

【你拥有的素材】
私密细节（必须植入到文本里）：
{payload.visible_details where act_introduced <= N}

线索（自然嵌入搜证/回忆/对话）：
{payload.owned_clues where act_introduced == N}

你能用的机制：{payload.applied_mechanics}

【写作规范】
1. 严格第一人称，绝不出现上帝视角
2. 按 cog_id 写心理活动，bio 与 cog 冲突时合理化
3. 字数 1500-3000，根据本幕节奏调整
4. 不写流水账，写情绪与节奏
5. 不要复述其他玩家的本（你只知道自己的）
6. 文风：暂时保持中性叙事，D-03 会再润色

【绝对禁止】
- 暴露 must_hide 项（哪怕一个字）
- 写"上帝视角"的客观陈述
- 写到你（{char_name}）这一幕根本不在场的事件
```

## 7. I/O 示例

### 示例输入
- act 2: 调查
- char_01 (陈孝先)
- must_reveal: ["案发时间 21:00-22:00", "现场是密室"]
- must_hide: ["凶手身份", "DNA 真相"]
- payload visible_details: [d_001 钟声, d_023 怀表]
- payload owned_clues: [c_001 工作证]

### 示例输出（节选）
```markdown
# 第 2 幕 · 陈孝先（弄堂巡查员, 48 岁）

> 状态：drafts
> Bible 版本：v0.1
> Cog 状态：未崩

---

教堂的钟声响到第十一下时，警笛声从弄堂口窜进来。

我刚从家里出门，怀里揣着半块怀表——这东西不知道哪年起就在我口袋里，
也不知道为什么，每次它发烫，我就有种心慌的感觉。

弄堂里的灯一盏盏亮起来。死者是隔壁李家的人，听说是窒息死的，
门窗都从里反锁。我作为巡查员，得去现场看看。

走到现场，案件已经记录下来。死亡时间在 21:00 到 22:00 之间。
那段时间我正好在家修一台旧收音机，李太可以作证。

我从死者床头翻出一张工作证。背面写着「王老板 1955.3.7」。
王老板这个名字我莫名觉得熟悉，但又想不起来从哪里听过。
我把工作证攥紧了一下，那种心慌的感觉又来了。
肯定是我太累了吧，母亲常说我容易神经过敏。

[...继续 1500 字]
```

## 8. 接口契约

### 给下游 D-03 润色师
- D-03 读 drafts/act{N}/{char_id}.md
- D-03 不改剧情、不改细节，只改文风
- 改完输出到 finals/act{N}/{char_id}.md

### 与认知 / payload 的关系
- 主笔只读自己的 cog + 自己的 payload
- 主笔绝不能读其他角色的私密信息

## 9. Observability

### Trace 模板（每次单角色单幕的调用都写一份）
```json
{
  "agent_id": "D-02",
  "action": "draft_act_char",
  "params": { "act": 2, "char_id": "char_01" },
  "status": "success",
  "duration_seconds": 45,
  "tokens_used": { "input": 3200, "output": 2800, "total": 6000 },
  "input_refs": [
    "_cognitive/char_01.json",
    "character_payloads/char_01.json"
  ],
  "output_refs": ["drafts/act2/char_01.md"],
  "word_count": 2150,
  "must_reveal_met": ["案发时间 21:00-22:00", "现场是密室"],
  "must_hide_violated": [],
  "details_planted": ["d_001", "d_023"],
  "clues_planted": ["c_001"]
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 违反 must_hide | status=fail | 必须重写 |
| 漏掉 must_reveal | status=fail | 必须重写 |
| 细节未植入 | warning: "details_missing" | 重写或允许（情况判断） |
| 字数远超阈值 | warning: "too_long" | D-03 阶段裁剪 |
| 跳上帝视角 | status=fail | 必须重写 |

## 10. 反例
- ❌ "陈孝先其实是私生子，但他自己不知道。"（上帝视角）
- ❌ "char_03 在那一刻正在隔壁..."（不该写其他角色视角）
- ❌ 漏写 must_reveal（玩家拿不到关键信息）
- ❌ 文本里出现 must_hide 项（剧透）

## 11. 测试用例
对民国 5 人本 4 幕，应产出 5×4 = 20 份 draft，每份 1500-3000 字，0 个 must_hide 违反。

---
**版本**：v9.1 / 2026-05-28
