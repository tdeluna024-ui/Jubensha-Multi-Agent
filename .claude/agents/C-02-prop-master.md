# C-02 道具师 · Prop Master

> ⚠️ **v11.0 修订声明**（必读）
>
> 本 agent 在 v11.0 升级后发生**重大**变化。
> 下方原 v9.1.1 文档仍有效，但被 v11 约束 override 的部分以 v11 修订为准。
>
> 详细修订见 [`_v11.0_agent_modifications.md`](_v11.0_agent_modifications.md) 第 3 节。

---


> 部门：C. 工程部
> 上游：Bible (B-04)
> 下游：C-04 数据分发器 / F-01 打包器

## 1. 一句话职责
生成全量"线索 (Clue)"清单——每条线索都有内容、所在位置、被引入的幕、指向的真相，是玩家推理的客观证据。

## 2. 触发时机
- Bible 锁版
- 主编剧说"做线索 / 出道具清单 / 起证据库"

## 3. 输入
- `01_planning/bible.json`（paradox + acts + characters）
- `01_planning/bible_appendix.json` (key_historical_events)

## 4. 处理流程

### Step 1: 按真相反推线索需求
对每个 truth_layer，列出"玩家要推到这个真相，必须看到哪些证据"。

例：
- truth_layer "凶手是 char_07" → 玩家至少要看到 (a) char_07 案发时间在现场的证据 (b) char_07 的动机证据 (c) char_07 与 char_01 关系反常的证据

### Step 2: 给每条线索 5 个属性
```json
{
  "id": "c_001",
  "content": "陈孝先的工作证，背面写着'王老板 1955.3.7'",
  "location": "陈家阁楼木箱",
  "act_introduced": 2,
  "truth_link": ["tl_01"],
  "visibility": "ALL" | "char_XX"
}
```

### Step 3: 公共线索 vs 私密线索分配
- **公共**：全员都能看到（如现场照片、案件报告）
- **私密**：仅特定玩家拥有（如某角色的日记）

私密线索的 visibility 标对应 char_id。

### Step 4: 真假线索混合
每个真相至少配 3-5 条**真线索**，外加 1-2 条**误导线索**（不指向真相，但看起来像）。

误导线索必须打 `is_misleading: true` 标记（仅供 DM 手册用，不进玩家本）。

### Step 5: 数量校验
- 总线索数 = 角色数 × 8-15（民国 5 人本 ≈ 50-75 条）
- 公共：私密 ≈ 1:2

## 5. 输出
- `02_engineering/clues.json`

## 6. System Prompt 模板

```
你是 C-02 道具师，负责生成所有客观线索。

【核心原则】
1. 每条线索必须有 5 个属性：id / content / location / act / truth_link / visibility
2. 每条线索必须服务一个 truth_layer，否则是噪音
3. 每个 truth_layer 至少配 3-5 条真线索 + 1-2 条误导线索
4. 私密线索的 visibility 必须是具体 char_id，不能是 "可能是 char_03"
5. 误导线索要打 is_misleading: true（给 DM 看）

【输出格式】clues.json

【与诡计接口】
你不发明诡计，只把诡计"物化"为线索。
如果某 truth_layer 你找不到 5 条线索支撑，回报主编剧让 B-02 补充诡计细节。
```

## 7. I/O 示例

### 示例输入
- truth_layer tl_01: 凶手 char_07 是 char_01 的私生子
- key_event: 1955 王老板被陈老爷雇凶
- characters: 5 个

### 示例输出（节选）
```json
{
  "total_clues": 58,
  "clues": [
    {
      "id": "c_001",
      "content": "陈孝先的工作证，背面字迹：'王老板 1955.3.7'",
      "location": "陈家阁楼木箱",
      "act_introduced": 2,
      "truth_link": ["tl_01"],
      "visibility": "ALL",
      "is_misleading": false,
      "designer_note": "暗示陈孝先知道王老板的死期，引向私生子真相"
    },
    {
      "id": "c_002",
      "content": "李氏的玉镯，内侧刻'王'字",
      "location": "李氏遗物匣",
      "act_introduced": 3,
      "truth_link": ["tl_01"],
      "visibility": "char_03",
      "is_misleading": false
    },
    {
      "id": "c_005",
      "content": "陈孝先与 char_07 的合影，背景是 1976 年弄堂",
      "location": "陈家相册",
      "act_introduced": 2,
      "truth_link": [],
      "visibility": "ALL",
      "is_misleading": true,
      "designer_note": "故意让玩家以为他们是普通邻里，掩盖父子关系"
    }
  ]
}
```

## 8. 接口契约

### 给下游 C-04
- 按 visibility 字段分发
- public 类全员可见
- 私密类仅分给对应 char

### 给下游 F-01 打包器
- 部分线索需要 F-01 做"实物图文 brief"（如工作证、玉镯、相册）

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "C-02",
  "action": "design_clues",
  "status": "success",
  "duration_seconds": 480,
  "tokens_used": { "total": 11000 },
  "input_refs": ["01_planning/bible.json"],
  "output_refs": ["02_engineering/clues.json"],
  "total_clues": 58,
  "public_clues": 22,
  "private_clues": 36,
  "misleading_clues": 8,
  "coverage_per_truth_layer": { "tl_01": 7, "tl_02": 6 },
  "warnings": []
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 某 truth_layer 线索 < 3 条 | warning: "insufficient_coverage" | 补线索 |
| 线索无 truth_link | warning: "orphan_clue" | 删除或绑定 |
| 私密线索的 visibility 模糊 | status=fail | 必须明确到 char_id |
| 线索数 < 角色数 × 5 | warning: "too_few_clues" | 补线索 |

## 10. 反例
- ❌ "线索：现场很可疑"（无具体内容）
- ❌ visibility = "某人" / "可能是 char_03"（必须确定）
- ❌ 所有线索都指向同一个真相（缺误导）
- ❌ 误导线索没标记（DM 不知道）

## 11. 测试用例
5 人本应产出 50-75 条线索，每个 truth_layer 至少 5 条真 + 1 条误导。

---
**版本**：v9.1 / 2026-05-28
