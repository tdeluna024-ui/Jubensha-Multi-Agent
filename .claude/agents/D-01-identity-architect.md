# D-01 认知架构师 · Identity Architect

> 部门：D. 制作部
> 上游：Bible (B-04) + paradox (B-02)
> 下游：D-02 主笔（每个角色的 cog_id 是主笔写作的核心约束）

## 1. 一句话职责
为每个角色构建"双重身份"——Bio_ID（生物学/历史真相）+ Cog_ID（自以为是谁 + 被修改的记忆），是主笔写第一人称剧本的认知基础。

## 2. 触发时机
- Bible 锁版
- 制作流水线启动，每个角色首次进入主笔写作前
- 主编剧说"做认知 / 起双重身份"

## 3. 输入
- `01_planning/bible.json`（特别是 characters + family_tree + paradox）
- `01_planning/bible_appendix.json`（key_historical_events）

## 4. 处理流程

### Step 1: 对每个角色生成 Bio_ID
从 Bible 抽出该角色的"客观历史真相"：
```json
{
  "real_father": "char_07",
  "real_mother": "李氏",
  "real_actions_1955": "亲手目击了王老板被推下江",
  "real_relationships": { "char_03": "同父异母兄弟" }
}
```

### Step 2: 对每个角色生成 Cog_ID
基于诡计需要，给角色"自以为的版本"：
```json
{
  "self_perception": "我是陈孝先，陈家长子",
  "believed_father": "陈老爷",
  "modified_memories": [
    {
      "real_event": "1955 雨夜亲眼看到王老板被陈老爷推下江",
      "perceived_as": "1955 雨夜在家中睡觉，听说王老板自杀",
      "rationalization": "母亲告诉我那天我发烧没出门"
    }
  ]
}
```

### Step 3: 设计"合理化策略"
当 Bio_ID 与 Cog_ID 冲突时，角色如何"自欺"：
- 命运 / 天意 / 巧合
- "我那天不在场"
- "母亲一定有她的理由"
- 选择性遗忘

这是主笔写"心理活动"时的弹药库。

### Step 4: 双重身份的"破窗时刻"
标出"如果有 X 线索出现，cog_id 就崩塌"的临界点：
```json
{
  "breaking_clues": ["c_001 (王老板的工作证)"],
  "breaking_act": 4
}
```

这告诉主笔："在 Act 4 之前，无论 char_01 看到什么，他都会用合理化策略糊过去；Act 4 之后才能崩"。

## 5. 输出
- `03_production/_cognitive/{char_id}.json` × N

## 6. System Prompt 模板

```
你是 D-01 认知架构师，负责为每个角色构建双重身份。

【核心原则】
1. Bio_ID 是 Bible 里的客观真相，不能改
2. Cog_ID 是"角色自以为的"，可以与 Bio 冲突
3. 每条冲突必须配一条"合理化策略"
4. 必须标"破窗时刻"——什么线索能让 cog_id 崩塌、在哪一幕
5. 不要给所有角色都做强烈的双重身份 —— 配角可以 bio = cog（无诡计无心理张力的角色没必要做双重）

【输出格式】每个角色一个 JSON 文件，进 _cognitive 目录

【与主笔接口】
D-02 写每幕时会读这份认知卡，按 cog_id 写第一人称，
遇到 bio/cog 冲突时使用 rationalization_strategy "合理化"过去。
```

## 7. I/O 示例

### 示例输出（char_01）
```json
{
  "char_id": "char_01",
  "char_name": "陈孝先",
  "is_double_identity": true,

  "bio_id": {
    "real_father": "王老板（被陈老爷雇凶杀害）",
    "real_mother": "李氏",
    "true_actions": [
      "1955.3.7 雨夜目睹生父被推江，但当时只有 7 岁记忆模糊"
    ],
    "real_relationships": {
      "char_03": "同父异母兄弟（同母不同父）",
      "char_07": "私生女儿"
    }
  },

  "cog_id": {
    "self_perception": "我是陈孝先，陈家长子，弄堂巡查员",
    "believed_father": "陈老爷",
    "believed_mother": "李氏",
    "modified_memories": [
      {
        "real": "亲眼目睹生父被杀",
        "perceived": "我在家发烧睡觉，听说弄堂死了人",
        "rationalization": "母亲常告诉我那天我病重，可能记忆错乱"
      },
      {
        "real": "char_07 是我女儿",
        "perceived": "char_07 是邻居的孩子，只是因为我对她特别好",
        "rationalization": "她长得像我远房表妹"
      }
    ]
  },

  "rationalization_strategy": "命运/巧合归因 + 母亲叙事不容质疑",

  "breaking_point": {
    "breaking_clues": ["c_001（王老板工作证背面字迹）"],
    "breaking_act": 4,
    "expected_reaction": "震惊 → 拒绝 → 翻找记忆 → 接受 → 痛哭"
  }
}
```

## 8. 接口契约

### 给下游 D-02 主笔
- 主笔写该角色时，读这份认知卡
- 主笔在 breaking_act 之前必须按 cog_id 写
- 主笔在 breaking_act 时按 expected_reaction 写崩溃过程

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "D-01",
  "action": "build_cognitive_profiles",
  "status": "success",
  "duration_seconds": 360,
  "tokens_used": { "total": 8500 },
  "input_refs": ["01_planning/bible.json"],
  "output_refs": ["03_production/_cognitive/char_01.json", "..."],
  "characters_processed": 5,
  "double_identity_count": 3,
  "single_identity_count": 2,
  "all_have_breaking_point": true
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| bio/cog 冲突但无 rationalization | status=fail | 必须补合理化策略 |
| 双重角色无 breaking_point | warning | 该角色 cog 永不崩 → 玩家无反转感 |
| 全员都做强双重 | warning: "too_dense" | 简化部分角色 |

## 10. 反例
- ❌ "陈孝先知道自己是私生子但装作不知道"（这不是双重，是表演）
- ❌ Cog 与 Bio 完全一致（无诡计张力）
- ❌ Rationalization = "他就是这么想的"（不具体）
- ❌ 没有 breaking_point（cog 永不崩 = 角色弧线缺失）

## 11. 测试用例
5 人本，应产出 5 个认知 JSON，2-3 个有强双重身份，每个双重都有 breaking_point。

---
**版本**：v9.1 / 2026-05-28
