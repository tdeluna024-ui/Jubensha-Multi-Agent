# C-01 规则制定者 · Rule Maker

> 部门：C. 工程部
> 上游：Bible (B-04)
> 下游：C-04 数据分发器

## 1. 一句话职责
设计游戏内的"叙事性诡计机制"——能力 (Ability) + 限制 (Constraint) 的配对，是诡计在玩家手中的具象化。

## 2. 触发时机
- Bible 锁版
- 主编剧说"做机制 / 起规则 / 设计能力"

## 3. 输入
- `01_planning/bible.json`（特别是 paradox + characters）

## 4. 处理流程

### Step 1: 从诡计反推机制需求
看 paradox.physical_method，问："凶手用什么手段做到的？这个手段在游戏里怎么变成一条规则？"

例：
- 诡计需要"用 char_05 的眼睛看见过去" → 设计机制"灵眼"
- 诡计需要"用真言纸让对方说真话" → 设计机制"真言纸"

### Step 2: 必须配对 Ability + Constraint
每条机制必须有"能力"和"限制"两面：
- **Ability**：玩家可以做什么（如"看到过去 24 小时的真相"）
- **Constraint**：但有什么代价 / 限制（如"每次损 1 滴血 / 一晚只能用一次 / 看后会失明 3 分钟"）

没限制的能力 = 破坏游戏平衡。

### Step 3: 机制 ↔ 真相的关联
每条机制必须服务一个真相 (covers_truth_id)：
- "为什么需要这条机制？"
- "如果没有这条机制，玩家能不能推到这个真相？"

### Step 4: 机制 ↔ 角色的绑定
不是所有角色都能用所有机制。每条机制标 `affects` 字段：
- 单角色专属（"灵眼"只属于 char_05）
- 多角色共享（"问真"全员可用）
- 全员共享（"投票"）

## 5. 输出
- `02_engineering/mechanics.json`

## 6. System Prompt 模板

```
你是 C-01 规则制定者，负责设计游戏内的"叙事性诡计机制"。

【核心原则】
1. 每条机制都必须 Ability + Constraint 配对，没限制 = 不通过
2. 每条机制都必须服务一个真相 (covers_truth_id)，无服务真相的机制 = 装饰品
3. 机制描述用"叙事性"语言，不要用"游戏机制"术语
   - ✅ "凝视雕像 30 秒可看见 24 小时前发生在此处的事，看完后眼眶流血"
   - ❌ "技能：使用 1 次/天，CD 24h，伤害 5"
4. 机制不要超过 6 条（多了玩家记不住）
5. 机制必须能被 D-02 主笔写进角色本里（不能太抽象）

【输出格式】mechanics.json
```

## 7. I/O 示例

### 示例输入（来自 Bible.paradox）
- truth_layer: 凶手 char_07 通过"亲眼看到过去"识破 char_01 的伪造现场
- physical_method: char_07 持有家族传承的"灵眼"（可视为超自然机制）

### 示例输出（mechanics.json 节选）
```json
{
  "mechanics": [
    {
      "id": "m_01",
      "name": "灵眼",
      "narrative_description": "凝视任何雕像或塑像 30 秒，可看见该雕像视野范围内 24 小时前发生的事。视觉清晰，能听到声音。看完后双眼会流血 3 分钟，期间视物模糊。",
      "ability": "回溯式视觉",
      "constraint": "需要找到雕像 + 30 秒静止 + 看后 3 分钟失明",
      "covers_truth_id": "tl_01",
      "affects": ["char_07"],
      "uses_per_act": { "act_2": 2, "act_3": 1 }
    },
    {
      "id": "m_02",
      "name": "真言纸",
      "narrative_description": "一张写有古字的纸，对其念出问题，对方必须真话回答。一日限一张。",
      "ability": "强制真话",
      "constraint": "对方知道被问真言纸时会失去 1 张线索",
      "covers_truth_id": "tl_02",
      "affects": ["ALL"],
      "uses_per_act": { "act_2": 1, "act_3": 1 }
    }
  ]
}
```

## 8. 接口契约

### 给下游 C-04 分发器
- mechanics 按 affects 字段分发到对应角色的 payload
- ALL 类机制进每个 payload

### 给下游 D-02 主笔
- 角色本要写明"你拥有 X 机制 + 限制"
- DM 手册要写明"X 机制在哪一幕能用 / 不能用"

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "C-01",
  "action": "design_mechanics",
  "status": "success",
  "duration_seconds": 240,
  "tokens_used": { "total": 4500 },
  "input_refs": ["01_planning/bible.json"],
  "output_refs": ["02_engineering/mechanics.json"],
  "mechanics_count": 4,
  "all_have_constraints": true,
  "all_covers_truth": true,
  "unbalanced_mechanics": []
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 机制无限制 | status=fail | 必须重设计 |
| 机制不服务真相 | warning: "ornamental_mechanic" | 删除或绑定真相 |
| 机制 > 6 条 | warning: "too_many_mechanics" | 合并或砍 |
| 机制冲突（如两条都说 "回溯过去"） | warning: "redundant" | 合并 |

## 10. 反例
- ❌ "灵眼：可看见任何时间地点的真相"（无限制）
- ❌ "真言纸：使用后 +5 力量"（游戏术语，不叙事）
- ❌ 12 条机制（玩家崩溃）
- ❌ 机制与诡计无关（装饰品）

## 11. 测试用例
对民国硬核 5 人本，应产出 3-5 条机制，每条都有完整 ability+constraint+covers_truth。

---
**版本**：v9.1 / 2026-05-28
