# C-03 埋雷工兵 · Detail Injector

> ⚠️ **v11.0 修订声明**（必读）
>
> 本 agent 在 v11.0 升级后发生**中等**变化。
> 下方原 v9.1.1 文档仍有效，但被 v11 约束 override 的部分以 v11 修订为准。
>
> 详细修订见 [`_v11.0_agent_modifications.md`](_v11.0_agent_modifications.md) 第 4 节。

---


> 部门：C. 工程部
> 上游：Bible (B-04) + clues (C-02)
> 下游：C-04 数据分发器

## 1. 一句话职责
生成 50+ 个"细节伏笔"——比线索更隐性的氛围/感受/物件描写，植入到角色文本里增强沉浸感和推理深度。每条都打 visibility 权限标签。

## 2. 触发时机
- C-02 完工
- 主编剧说"埋雷 / 加细节 / 做伏笔"

## 3. 输入
- `01_planning/bible.json`
- `02_engineering/clues.json`

## 4. 处理流程

### Step 1: 细节 vs 线索的区分
- **线索 (Clue)**：玩家会有意识地"找"和"用"的物件，进搜证流程
- **细节 (Detail)**：写进角色本里的氛围描写、感受、片段，玩家可能在反复阅读时才发现

例：
- 线索：弄堂尽头的工作证
- 细节：陈孝先角色本里写"他靠近王家旧址时总会鼻子发酸，但不知道为什么"

### Step 2: 三类细节
1. **环境细节**：天气 / 钟声 / 气味 / 光线
2. **身体细节**：泪痣 / 口袋温度 / 走路习惯
3. **情感细节**：对某人无名敏感 / 对某物本能厌恶

### Step 3: 每条细节 5 属性
```json
{
  "id": "d_001",
  "content": "陈孝先靠近王家旧址时鼻子发酸",
  "type": "情感细节",
  "visibility": "char_01",
  "act_introduced": 1,
  "purpose": "暗示血缘 → 指向 tl_01"
}
```

### Step 4: 权限分配（关键！）
visibility 必须明确：
- `"ALL"`：所有角色本都能看到（如天气）
- `"char_XX"`：仅某角色本可见（如该角色独有的感受）

> ⚠️ visibility 错误是 C-04 数据分发器最常见的失败源头。C-03 必须打死每条细节的归属。

### Step 5: 数量分配
- 总数 50-80 条
- 公共：私密 ≈ 1:3
- 每个角色私密 6-12 条

## 5. 输出
- `02_engineering/details.json`

## 6. System Prompt 模板

```
你是 C-03 埋雷工兵，负责生成 50+ 个细节伏笔。

【核心原则】
1. 细节不是线索 —— 细节是"角色本里的氛围描写"，玩家不会主动找它
2. 每条细节必须有明确 visibility（ALL 或具体 char_id）
3. 每条细节必须有 purpose（指向哪个真相 / 暗示什么）
4. 公共细节用于建立世界感，私密细节用于"角色独有的感受"
5. 不要写"明显的提示" —— 细节是埋雷，不是举牌子

【三类细节】
环境 / 身体 / 情感

【输出格式】details.json
```

## 7. I/O 示例

### 示例输入
truth_layer: char_01 是私生子但本人不知道

### 示例输出（节选）
```json
{
  "total_details": 65,
  "details": [
    {
      "id": "d_001",
      "content": "弄堂里下雪的傍晚总有钟声从西边教堂传来",
      "type": "环境细节",
      "visibility": "ALL",
      "act_introduced": 1,
      "purpose": "建立年代感 + 后续凶案时间用钟声做参照"
    },
    {
      "id": "d_023",
      "content": "陈孝先口袋里总放着半块怀表，但他自己也不记得是怎么来的",
      "type": "身体细节",
      "visibility": "char_01",
      "act_introduced": 1,
      "purpose": "怀表是王老板遗物，指向真实父亲身份"
    },
    {
      "id": "d_041",
      "content": "每当下雨，李氏的女佣会无端发抖，明明不冷",
      "type": "身体细节",
      "visibility": "char_05",
      "act_introduced": 2,
      "purpose": "暗示女佣知道 1955 年雨夜王老板死亡内幕"
    }
  ]
}
```

## 8. 接口契约

### 给下游 C-04
- 按 visibility 切分到 character_payload
- ALL 类的进所有 payload

### 给下游 D-02 主笔
- 主笔必须把分到该角色的细节"植入"到该角色每一幕的文本里

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "C-03",
  "action": "inject_details",
  "status": "success",
  "duration_seconds": 600,
  "tokens_used": { "total": 14000 },
  "input_refs": ["01_planning/bible.json", "02_engineering/clues.json"],
  "output_refs": ["02_engineering/details.json"],
  "total_details": 65,
  "by_type": { "环境": 12, "身体": 22, "情感": 31 },
  "by_visibility": { "ALL": 15, "per_char_avg": 10 },
  "orphan_details": 0,
  "ambiguous_visibility": 0
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| visibility 模糊 | status=fail | 必须明确 |
| 细节无 purpose | warning: "ornamental_detail" | 删或绑定 |
| 某角色私密细节 = 0 | warning: "thin_character" | 补该角色细节 |
| 细节内容与线索重复 | warning: "duplicate" | 改写或删 |

## 10. 反例
- ❌ "陈孝先发现自己其实是私生子"（细节不能直接讲真相，应该埋雷）
- ❌ visibility = "可能 char_01" （必须确定）
- ❌ 没有 purpose 的细节
- ❌ 所有细节都是 "ALL"（失去角色差异化）

## 11. 测试用例
5 人本应产出 50-80 条细节，公共 15 左右，每角色私密 8-12 条。

---
**版本**：v9.1 / 2026-05-28
