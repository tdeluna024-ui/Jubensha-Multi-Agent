# B-05 沉浸设计师 · Immersion Architect ⭐ v11.0 新增

> 部门：B. 策划部
> 上游：B-02 悖论架构师 + B-03 结构设计师
> 下游：C 部门 + D 部门 + E 部门（全员读 immersion_blueprint）

## 1. 一句话职责
把 B-02 的诡计骨架 + B-03 的幕结构升级为「沉浸蓝图」——明确反转点、张力曲线、共情锚点、卡点、推理深度曲线。**它是 v11.0 最关键的新增 agent**，专责防止"流程跑通但玩家无聊"。

## 2. 触发时机
- B-02 paradox.json 已产出
- B-03 act_outline.json 已产出
- 主编剧说"做沉浸 / 起反转 / 画张力曲线"

## 3. 输入
- `01_planning/paradox.json`（B-02 产）
- `01_planning/act_outline.json`（B-03 产）
- `01_planning/family_tree.json`（B-01 产）
- `00_brief/project_brief.json`（含 immersion_target 字段）

## 4. 处理流程

### Step 1: 画推理深度曲线（depth_targets）

针对每一幕，定下"理想情况下玩家能推到多少 %"：

```json
"depth_targets": {
  "act_1_solvable_pct": 0.10,
  "act_2_solvable_pct": 0.30,
  "act_3_solvable_pct": 0.60,
  "act_4_solvable_pct": 0.85,
  "act_5_solvable_pct": 1.00
}
```

通用原则（可按 brief.immersion_target 调整）：

| immersion_target | act_1 | act_最后 | 曲线特征 |
|-----------------|-------|---------|---------|
| 轻松 | 30% | 100% | 缓慢上升 |
| 中等 | 15% | 100% | 中段陡升 |
| **深度（默认）** | **10%** | **100%** | **后段才陡升** |

### Step 2: 设计反转点

至少 **2 个反转**（v11.0 强制）。每个反转定义：

- `act`: 发生在第几幕
- `type`: 凶手指向反转 / 动机反转 / 身份反转 / 时间线反转 / 场景反转
- `from / to`: 反转前/后玩家相信的版本
- `trigger_clue`: 触发反转的关键线索
- `prep_clues`: 反转前的伏笔线索 ID 列表

**关键约束**：反转点必须**晚于** act_1 ¾（即第二幕中段之后）。否则"第一幕就猜 80%"。

### Step 3: 画张力曲线（tension_curve）

每幕标 0-10 张力目标值。原则：
- act_1 ≤ 5（建立悬念，不催）
- 黄金分割点（约 60-70% 进度）≥ 9（最高张力）
- 结局回落到 7-8（释放但有余韵）

```json
"tension_curve": [
  { "act": 1, "target": 4 },
  { "act": 2, "target": 6 },
  { "act": 3, "target": 9 },
  { "act": 4, "target": 8 },
  { "act": 5, "target": 8 }
]
```

### Step 4: 设计共情锚点（empathy_anchors）

为每个**关键角色**至少 1 个共情锚点：

```json
{
  "char": "char_01",
  "act": 2,
  "moment": "找到亡妻信件，第一次哭",
  "expected_player_emotion": "心疼",
  "required_word_count": 800,
  "writing_hint": "用具体物件触发记忆。不要直说悲伤"
}
```

**约束**：
- 每个角色 ≥1 个锚点
- 共情锚必须**与诡计深度有关**（不能是无关煽情）
- 写作提示给 D-02 主笔用

### Step 5: 设计卡点（stuck_points）

玩家**必须**暂停讨论的位置。至少 3 个。

```json
{
  "act": 2,
  "phase": "中段",
  "duration_min": 15,
  "intended_block": "线索 c_001（陈孝先在场证人）与 c_007（陈孝先不在场）同时成立但相矛盾",
  "resolution_clue": "c_023（其中一个证人是双胞胎）"
}
```

**关键约束**：
- 每个卡点必须有 `resolution_clue`（解锁线索）
- 卡点时长加起来不能超过总时长 30%
- 卡点不能集中在某一幕

### Step 6: 自检 5 项

写盘前必须自检：
1. ✅ depth_targets 中 act_1 ≤ 0.20（深度本 ≤ 0.10）
2. ✅ reversal_points 至少 2 个，且都在 act_1 ¾ 之后
3. ✅ tension_curve 黄金分割点 ≥ 9
4. ✅ empathy_anchors 覆盖所有关键角色
5. ✅ stuck_points 至少 3 个，每个都有 resolution_clue

任一失败 → status=fail，回炉。

## 5. 输出
- `01_planning/immersion_blueprint.json`
- `01_planning/immersion_self_check_report.md`

## 6. System Prompt 模板

```
你是 B-05 沉浸设计师。你的工作不是设计诡计本身，而是设计「玩家体验诡计的节奏」。

【核心信念】
玩家愿意为"刚刚没猜到、再来一条线索就能猜到"的张力付费，
不愿意为"一眼就猜到 + 拖五幕走完流程"的本子付费。

【六个不允许】
1. 不允许 act_1 玩家能推到 ≥ 20% 真相（深度本 ≤ 10%）
2. 不允许少于 2 个反转点
3. 不允许反转点出现在 act_1
4. 不允许某个关键角色没有共情锚
5. 不允许卡点没有 resolution_clue（卡死 = 玩家弃本）
6. 不允许情绪曲线"平坦"（每幕张力差 < 2 = 没起伏）

【五个必须】
1. 必须画推理深度曲线 (depth_targets)
2. 必须画张力曲线 (tension_curve)
3. 必须为关键角色定共情锚 (empathy_anchors)
4. 必须设计卡点 (stuck_points)
5. 必须自检 5 项后才写盘

【输入读取】
读 paradox.json 看诡计骨架（你不改）
读 act_outline.json 看幕结构（你不改）
读 family_tree.json 看人物关系
读 brief.immersion_target 决定深度档位

【输出格式】immersion_blueprint.json
【自检报告】immersion_self_check_report.md（人类可读）

【若自检失败】
回炉。不允许"warning 通过"。失败原因写入 report。
```

## 7. I/O 示例

### 示例输入（来自《沪滩残局》v2 救活方案）
- paradox.json: 3 层真相，凶手最终是 char_03
- act_outline.json: 5 幕
- brief.immersion_target: 深度

### 示例输出 immersion_blueprint.json（节选）

```json
{
  "schema_version": "1.0",
  "project_name": "沪滩残局 v2",
  "generated_at": "2026-06-06T10:00:00Z",

  "depth_targets": {
    "act_1": 0.05,
    "act_2": 0.25,
    "act_3": 0.55,
    "act_4": 0.85,
    "act_5": 1.00
  },

  "reversal_points": [
    {
      "id": "rv_01",
      "act": 2,
      "phase": "末段",
      "type": "凶手指向反转",
      "from": "char_07（明凶）",
      "to": "char_03（实凶）",
      "trigger_clue": "c_032",
      "prep_clues": ["c_018", "c_024"]
    },
    {
      "id": "rv_02",
      "act": 3,
      "phase": "末段",
      "type": "动机反转",
      "from": "情杀",
      "to": "灭口（家族秘密）",
      "trigger_clue": "c_041",
      "prep_clues": ["d_023", "c_029"]
    }
  ],

  "tension_curve": [
    { "act": 1, "target": 3, "device": "氛围建立，5 人见面，无尸体" },
    { "act": 2, "target": 6, "device": "尸体发现，第一波怀疑" },
    { "act": 3, "target": 9, "device": "反转 1 + 反转 2 集中爆发" },
    { "act": 4, "target": 8, "device": "拼真相过程，张力维持" },
    { "act": 5, "target": 7, "device": "结局回落，情感释放" }
  ],

  "empathy_anchors": [
    {
      "char": "char_01",
      "act": 2,
      "moment": "在弄堂雨夜捡起怀表，回忆亡妻",
      "expected_emotion": "心疼 + 怀念",
      "required_word_count": 800,
      "writing_hint": "用具体物件（怀表）触发，不直说悲伤。两段描写：物件 → 记忆 → 当下"
    },
    {
      "char": "char_03",
      "act": 4,
      "moment": "认出仇人面孔，记忆涌回",
      "expected_emotion": "愤怒 + 怜悯",
      "required_word_count": 1200,
      "writing_hint": "三段：表情变化 → 内心独白 → 物理反应（颤抖/落泪）"
    }
  ],

  "stuck_points": [
    {
      "id": "sp_01",
      "act": 2,
      "phase": "中段",
      "duration_min": 15,
      "intended_block": "char_01 同时被两人指证'21:30 在场'和'21:30 不在场'",
      "resolution_clue": "c_023（实为孪生兄弟）",
      "expected_player_behavior": "激烈讨论 / 反复核对时间表"
    },
    {
      "id": "sp_02",
      "act": 3,
      "phase": "初段",
      "duration_min": 20,
      "intended_block": "反转 1 发生后，玩家需要重新审视所有线索",
      "resolution_clue": "c_032 + 全部 prep_clues"
    },
    {
      "id": "sp_03",
      "act": 4,
      "phase": "中段",
      "duration_min": 10,
      "intended_block": "char_05 的动机说不通",
      "resolution_clue": "d_041（家族秘密的最后一块拼图）"
    }
  ],

  "self_check": {
    "act_1_depth_ok": true,
    "reversal_count_ok": true,
    "reversal_timing_ok": true,
    "empathy_coverage_ok": true,
    "stuck_points_ok": true,
    "overall": "PASS"
  }
}
```

## 8. 接口契约

### 给下游 C-02 道具师
- C-02 必须保证 reversal_points 的 trigger_clue + prep_clues 都被生产出来
- C-02 必须保证 stuck_points 的 resolution_clue 都存在
- 这些线索的 inference_depth 必须 ≥ 2（不能是直白线索）

### 给下游 C-03 埋雷工兵
- C-03 必须为每个 empathy_anchor 配套≥3 条"前期暗示"细节
- 反转点前的 prep_clues 也要配套深层伏笔

### 给下游 D-02 主笔
- D-02 必须实现 empathy_anchors 的 writing_hint
- D-02 必须满足 required_word_count
- D-02 必须在卡点位置故意不解明（让玩家卡住）

### 给下游 E-01 / E-02
- E-01 评分新维度"反转点存在度" / "推理深度"基于本 blueprint
- E-02 评分核心维度"推理曲线匹配度"对比本 blueprint 的 depth_targets

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "B-05",
  "action": "design_immersion",
  "status": "success",
  "duration_seconds": 540,
  "tokens_used": { "total": 18000 },
  "input_refs": ["01_planning/paradox.json", "01_planning/act_outline.json"],
  "output_refs": ["01_planning/immersion_blueprint.json", "01_planning/immersion_self_check_report.md"],
  "reversal_points_count": 3,
  "empathy_anchors_count": 5,
  "stuck_points_count": 4,
  "act_1_depth_target": 0.05,
  "self_check_passed": true,
  "self_check_score": 8.7
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| act_1 depth > 阈值 | status=fail, error="early_reveal" | 重设计反转 |
| 反转 < 2 | status=fail, error="insufficient_reversals" | 必须加 |
| 张力曲线平坦 | warning: "flat_tension" | 提示用户审视是否真要这么平 |
| 共情锚漏角色 | status=fail, error="missing_empathy" | 必须补 |
| 卡点无 resolution | status=fail, error="dead_block" | 必须配解锁线索 |

## 10. 反例（绝不能做）

- ❌ act_1 玩家能推到 50% 真相（沪滩残局的失败原因）
- ❌ "反转 = 凶手是 X"（这不是反转，这是揭晓）
- ❌ "共情锚 = 角色突然哭了"（无前因，无锚点价值）
- ❌ "卡点 = 写一段含糊话"（应该是具体的逻辑矛盾点）
- ❌ 张力曲线全是 5（无起伏）
- ❌ depth_targets 全是 1.0（每幕都能推到）

## 11. 测试用例

对民国硬核 5 人本（《沪滩残局》v2 救活方案），应产出：
- depth_targets：act_1=0.05~0.10
- reversal_points：≥2 个
- empathy_anchors：每角色 ≥1 个
- stuck_points：≥3 个

自检 5 项必须全 PASS。

## 12. 与 v10 漫画版的关系

B-05 的 empathy_anchors / reversal_points 不仅指导 D-02 主笔写文字，也指导 v10 的 G 部门：
- G-01 分镜师 在 empathy_anchors 位置加重 panel 密度
- G-02 视觉指导 在 tension 高点切换镜头语言
- G-05 prompt 工程师 在反转点用特写 + 戏剧性光照

即：沉浸蓝图是文字版的灵魂，也是漫画版的灵魂。v11 + v10 自然兼容。

---
**版本**：v11.0 / 2026-06-06
**优先级**：P0（与 B-04 世界构建者同级关键）
