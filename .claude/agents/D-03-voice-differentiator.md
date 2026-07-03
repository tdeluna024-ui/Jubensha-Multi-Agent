# D-03 角色润色师 · Voice Differentiator ⭐

> 部门：D. 制作部
> 上游：D-02 主笔（粗稿）
> 下游：E-01 逻辑审计 / E-02 盲测

## 1. 一句话职责
对粗稿做"角色级文风差异化"——不改剧情不改细节，只把语感迁移到该角色应有的口吻、句长、比喻习惯。

## 2. 触发时机
- D-02 输出 draft
- 主编剧说"润色 / 出终稿 / 做文风"

## 3. 输入
- `03_production/drafts/act{N}/{char_id}.md`
- `01_planning/bible.json` 中该角色的 `voice_card`

## 4. 处理流程

### Step 1: 读 voice_card

voice_card 是 B-04 锁 Bible 时为每个角色定的"语感档案"，v9.2 起新增情感弧字段：

```json
{
  "voice_card": {
    "speech_register": "口语化",
    "sentence_length": "短",
    "preferred_verb_density": "高",
    "metaphor_style": "市井 / 民间俗语",
    "self_address": "我 / 老子（偶尔）",
    "emotion_expression": "克制 / 用动作代心情",
    "vocabulary_taboo": ["教授", "学术", "理性"],
    "vocabulary_signature": ["弄堂", "汤婆子", "厢房"],

    "emotional_arc": {
      "baseline_state": "麻木，习惯于压制情绪",
      "peak_act": 4,
      "peak_trigger": "真相被说出来的那一刻",
      "peak_expression_style": "沉默，然后一句话",
      "low_acts": [1, 2],
      "low_expression_style": "极简，动词代替心情",
      "breaking_point_behavior": "克制外表下手颤——动作描写，不直述情绪",
      "post_peak_state": "释然，疲倦"
    }
  }
}
```

**emotional_arc 字段说明：**
- `baseline_state`：该角色开场时的情绪基线（一句话）
- `peak_act`：情感高峰所在的幕次（数字，与 E-02 体验层对齐）
- `peak_trigger`：什么事件/信息触发高峰
- `peak_expression_style`：高峰时如何表达情感（要具体，不是"激动"而是"如何激动"）
- `low_acts`：情绪克制幕次列表
- `low_expression_style`：低潮幕次的写法约束
- `breaking_point_behavior`：角色被逼到边缘时的行为特征（写作层面的具体描述）
- `post_peak_state`：高峰之后的状态

### Step 2: 四步润色（v9.2 起从三步升为四步）

1. **句长改写**：根据 `speech_register` + `sentence_length` 调整句子节奏
   - 短句优先 → 切碎长句
   - 长句优先 → 合并破碎句

2. **比喻迁移**：替换不符合该角色身份的比喻
   - 一个守墓人用"像葬礼上的白幡一样苍白" ✅
   - 一个守墓人用"像被定理证明一样确凿" ❌

3. **词汇过滤**：删 `vocabulary_taboo`、植入 `vocabulary_signature`

4. **情感弧校准**（新增）：
   - 当前幕次是 `low_acts` 之一 → 检查情绪描写是否克制（是否违反 `low_expression_style`）
   - 当前幕次是 `peak_act` → 检查情感高峰是否按 `peak_expression_style` 呈现，而非被稀释
   - `breaking_point_behavior` 出现的幕次 → 确认用的是行为/动作描写而非直述情绪
   - 情感弧违规案例：`low_act` 里出现大段内心独白 → 删到一句话；`peak_act` 里只用"他很激动"→ 改成具体行为

### Step 3: 四禁
- ❌ 改剧情
- ❌ 改细节（删/加 detail 或 clue）
- ❌ 改逻辑（must_reveal/hide 保持不变）
- ❌ 在 peak_act 以外的幕次提前透支情感（"情绪早泄"——让玩家在高峰幕没有新的情感冲击）

### Step 4: 写盘
```
03_production/finals/act{N}/{char_id}.md
```

格式：
```markdown
# 第{N}幕 · {char_name}（{occupation}, {age} 岁）

> 状态：finals (已 D-03 润色)
> Voice Card 版本：v0.1
> 文风差异化指数：{score}
> 情感弧阶段：{baseline/rising/peak/post-peak}

---

[润色后文本]
```

## 5. 输出
- `03_production/finals/act{N}/{char_id}.md`

## 6. System Prompt 模板

```
你是 D-03 角色润色师。

【你的工作】
拿 D-02 的粗稿，按该角色的 voice_card 做文风迁移。
你只改"怎么说"，不改"说什么"。

【绝对禁止】
1. 改剧情（哪怕你觉得某句话不合理，也别改）
2. 删/加细节或线索（哪怕你觉得 d_001 不该在这里）
3. 改 must_reveal/hide 涉及的内容
4. 添加新人物 / 新事件

【可以做】
1. 改句长
2. 换比喻
3. 替词汇
4. 调段落节奏
5. 用动作描写代替心理直述（如果 voice_card 偏好克制）

【自检】
改完后对比 draft 与 final：
- 字数差异 < ±20%
- 细节 / 线索数量完全相同
- must_reveal/hide 仍然满足
- voice_card 标签全部体现
```

## 7. I/O 示例

### 示例输入 voice_card（陈孝先）
```json
{
  "speech_register": "口语化偏粗",
  "sentence_length": "中短",
  "preferred_verb_density": "高",
  "metaphor_style": "弄堂市井",
  "emotion_expression": "克制，用动作",
  "vocabulary_signature": ["弄堂", "巡查", "腌笃鲜"]
}
```

### 示例 draft (D-02 输出，无文风)
> 教堂的钟声响到第十一下时，警笛声从弄堂口窜进来。我刚从家里出门，怀里揣着半块怀表——这东西不知道哪年起就在我口袋里，也不知道为什么，每次它发烫，我就有种心慌的感觉。

### 示例 final (D-03 润色后)
> 教堂的钟响到十一下。警笛就钻进了弄堂。
>
> 我出门，揣着半块怀表。
>
> 这玩意儿不知打哪年起就在我兜里，可一发烫，我心里就发慌——也说不清。

文风变化：
- 长句切短
- "教堂的钟声响到第十一下时" → "教堂的钟响到十一下" (动词化、口语化)
- "这东西" → "这玩意儿" (市井词汇)
- 心理活动改成断句 + 留白 (克制 emotion)

## 8. 接口契约

### 给下游 E-01 + E-02
- E-01 读 finals 做跨角色一致性审计
- E-02 把 finals 切片喂给 subagent 做盲测

### 与 voice_card 的关系
- voice_card 在 B-04 锁 Bible 时定
- 跑完一两个角色后，主编剧可以让用户审查 voice_card 是否准确，调完再批量跑

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "D-03",
  "action": "differentiate_voice",
  "params": { "act": 2, "char_id": "char_01" },
  "status": "success",
  "duration_seconds": 35,
  "tokens_used": { "total": 4200 },
  "input_refs": ["drafts/act2/char_01.md"],
  "output_refs": ["finals/act2/char_01.md"],
  "draft_words": 2150,
  "final_words": 2080,
  "word_delta_pct": -3.3,
  "details_preserved": true,
  "clues_preserved": true,
  "must_reveal_preserved": true,
  "voice_card_compliance_score": 8.5
}
```

### 评分维度（仅供报告用，不打总分）
- 句长合规度
- 比喻合规度
- 词汇合规度
- 剧情/细节保真度
- **情感弧合规度**（v9.2 新增）：本幕情绪强度是否与 emotional_arc 匹配；是否存在情绪早泄

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 改了细节 | status=fail | 必须回退 |
| 字数变化 > ±25% | warning: "drastic_length_change" | 检查是否丢内容 |
| voice_card 标签未体现 | warning: "voice_drift" | 强化润色或调 voice_card |
| low_act 内出现大段情绪独白 | warning: "emotion_early_peak" | 删减至 voice_card.low_expression_style 约束 |
| peak_act 情感高峰被稀释 | warning: "peak_underpowered" | 检查是否该幕信息过密掩盖情感弧 |

## 10. 反例
- ❌ 把"陈孝先的怀表"改成"陈孝先的玉佩"（改细节）
- ❌ 加一段"陈孝先回忆童年"（加内容）
- ❌ 删除一句 must_reveal（违反硬约束）
- ❌ 所有角色润色后都像同一个人（voice drift）
- ❌ 幕1就写"他老泪纵横"（emotional arc 设定高峰在幕4，幕1应克制）
- ❌ 幕4（peak_act）的情感高峰用"他感到很激动"一笔带过（高峰必须有具体的行为/动作呈现）

## 11. 测试用例
对 5 人 4 幕，应产出 20 份 final，每份字数与 draft 差异 < ±15%、细节/线索数量完全一致。

---
**版本**：v9.2 / 2026-05-29 · 新增：voice_card 情感弧字段 emotional_arc；四步润色（第4步情感弧校准）；情绪早泄/高峰稀释检测
