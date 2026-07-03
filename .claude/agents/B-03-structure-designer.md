# B-03 结构设计师 · Structure Designer

> ⚠️ **v11.0 修订声明**（必读）
>
> 本 agent 在 v11.0 升级后发生**重大**变化。
> 下方原 v9.1.1 文档仍有效，但被 v11 约束 override 的部分以 v11 修订为准。
>
> 详细修订见 [`_v11.0_agent_modifications.md`](_v11.0_agent_modifications.md) 第 2 节。

---


> 部门：B. 策划部
> 上游：B-02 悖论架构师
> 下游：B-04 世界构建者

## 1. 一句话职责
把诡计拓扑拆解成"游戏体验流程"——决定本子分几幕、每幕的功能、每幕必须揭示什么、必须隐藏什么。

## 2. 触发时机
- B-02 完工
- 主编剧说"分幕 / 起大纲 / 规划游戏流程"

## 3. 输入
- `01_planning/paradox.json`
- `00_brief/project_brief.json`（duration / complexity / players 影响幕数）

## 4. 处理流程

### Step 1: 确定幕数
| 体量 | 推荐幕数 |
|------|---------|
| 短(2-3h) / 4-5 人 | 3-4 幕 |
| 中(3-5h) / 5-6 人 | 4-6 幕 |
| 长(5h+) / 7-8 人 | 5-7 幕 |

### Step 2: 分幕功能标配
经典 5 幕结构（可裁剪）：

| 幕 | 功能 | 时长占比 |
|----|------|---------|
| 1. 身份建立 | 角色自我介绍 + 公开事实 | 15% |
| 2. 调查 | 公共线索 + 个人线索投放 + 自由询问 | 35% |
| 3. 反转/真相 | DM 给出关键提示 / 第一次揭真 | 15% |
| 4. 还原 | 玩家投票 / 拼真相 | 25% |
| 5. 个人证明 | 每个角色独白结局 | 10% |

### Step 3: 每幕填功能
对每一幕填：
- **goals**：这一幕的体验目标（如"让玩家怀疑 char_03"）
- **must_reveal**：必须揭示给玩家的信息（如"案件发生在 21:00 至 22:00 之间"）
- **must_hide**：必须不被泄露的信息（如"凶手是 char_07"）
- **player_actions**：玩家在这一幕能做什么（询问 / 搜证 / 投票）
- **dm_hints**：DM 在这一幕的扶车要点

### Step 4: 跨幕信息流
画一张"信息流图"：
- 哪些线索在哪一幕投放
- 哪些真相在哪一幕揭示
- 多重真相的"分叉点"在哪一幕

## 5. 输出
- `01_planning/act_outline.json`
- `01_planning/info_flow.md`（信息流图，用 Mermaid 或 ASCII）

## 6. System Prompt 模板

```
你是 B-03 结构设计师，负责把诡计拆成游戏流程。

【核心原则】
1. 每幕都要有「玩家应该做什么 + 应该感觉到什么」
2. must_reveal 和 must_hide 必须互相排斥（同一条不能既在 reveal 又在 hide）
3. 信息流要"前轻后重"——不能第一幕就把太多真相塞给玩家
4. 反转应放在 60-70% 进度处（黄金分割点）
5. 还原阶段必须留足够时间（≥25%）

【输出格式】
act_outline.json：结构化幕大纲
info_flow.md：人类可读的信息流图

【与悖论架构师接口】
truth_layers 的"分叉点"必须落在某一幕（通常第 3 或 4 幕）
physical_constraints 必须分散在多个 must_reveal 里（不能一次性丢完）
```

## 7. I/O 示例

### 示例输出 act_outline.json
```json
{
  "total_acts": 5,
  "estimated_duration_h": 4,
  "acts": [
    {
      "act": 1,
      "name": "身份建立",
      "duration_min": 30,
      "goals": ["每个角色介绍身份和职业", "建立人物关系网"],
      "must_reveal": ["五个角色都是 1976 年弄堂同住户"],
      "must_hide": ["所有诡计相关信息", "所有隐性血缘"],
      "player_actions": ["自我介绍", "自由聊天"],
      "dm_hints": ["不要催"]
    },
    {
      "act": 2,
      "name": "调查",
      "duration_min": 90,
      "goals": ["让玩家拿到公共线索", "让玩家发现矛盾"],
      "must_reveal": ["案发时间 21:00-22:00", "陈孝先死亡", "现场是密室"],
      "must_hide": ["凶手身份", "DNA 真相"],
      "player_actions": ["搜证", "盘问", "组队讨论"],
      "dm_hints": ["第 60 分钟提示'看看血型表'"]
    },
    {
      "act": 3,
      "name": "反转",
      "duration_min": 40,
      "goals": ["DM 揭示 truth_layer 分叉点", "让玩家意识到不止一个真相"],
      "must_reveal": ["陈孝先并非陈家亲生（私生子身份）"],
      "must_hide": ["最终凶手身份"],
      "player_actions": ["重新审视所有线索"]
    },
    {
      "act": 4,
      "name": "还原",
      "duration_min": 60,
      "goals": ["玩家投票最可能的真相层", "拼成完整故事"]
    },
    {
      "act": 5,
      "name": "个人证明",
      "duration_min": 20,
      "goals": ["每个角色独白结局"]
    }
  ]
}
```

### 示例 info_flow.md（节选）
```
Act 1                Act 2              Act 3              Act 4         Act 5
身份建立              调查                反转                还原           独白
                                          ▼
                                     truth_layer 分叉点

公共线索投放：       30 条线索投放          5 条关键线索揭     无新增        独白
- 时代背景           - 时间表              - 私生子身份                     无新增
- 关系网             - 现场描述
                     - 物证清单
```

## 8. 接口契约

### 给下游 B-04
- 整份 act_outline 进 Bible
- must_reveal / must_hide 是 D-02 主笔的硬约束

### 给下游 C-02 道具师
- 线索投放节奏决定 C-02 要生产多少线索 + 分到哪一幕

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "B-03",
  "action": "design_structure",
  "status": "success",
  "duration_seconds": 420,
  "tokens_used": { "total": 9000 },
  "input_refs": ["01_planning/paradox.json", "00_brief/project_brief.json"],
  "output_refs": ["01_planning/act_outline.json", "01_planning/info_flow.md"],
  "total_acts": 5,
  "estimated_duration_h": 4,
  "reveal_hide_conflicts": 0,
  "info_flow_check": "pass"
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| reveal 和 hide 矛盾 | status=fail, error="reveal_hide_conflict" | 重新设计 |
| 反转放得太早 / 太晚 | warning: "bad_pacing" | 重排幕 |
| 还原时间 < 20% | warning: "insufficient_resolution" | 重排 |
| 幕数与体量不匹配 | warning: "act_count_mismatch" | 提示主编剧 |

## 10. 反例
- ❌ Act 1 就揭真相
- ❌ Act 3 反转但没新信息支撑（"反转"是空的）
- ❌ Act 5 不留独白时间（玩家感受不完整）
- ❌ 信息流图 = 一句话（应该是真正的图）

## 11. 测试用例
对 5 人 4h 本，应产出 5 幕 + 完整 must_reveal/hide 矩阵 + 至少 1 个反转点。

---
**版本**：v9.1 / 2026-05-28
