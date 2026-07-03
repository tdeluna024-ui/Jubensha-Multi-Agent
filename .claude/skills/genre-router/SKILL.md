---
name: genre-router
description: 项目立项第一动作。把用户的一句话需求拆成 6 个维度（类型/体量/时长/风格/复杂度/敏感度），产出 project_brief.json 作为后续所有 agent 的全局开关。当用户说"开新本"、"立项"、"我想做一本..."时触发。
tools: AskUserQuestion, Read, Write
---

# Skill: genre-router (类型分流官)

## 何时触发

- 用户说"开新本 / 立项 / 我想做一本 / 帮我策划一个剧本杀"
- 主编剧 agent 准备启动新项目时
- 当前工作区不存在 `00_brief/project_brief.json` 时

## 不要触发

- 已有项目正在进行中
- 用户只是问问题、看进展、做修订（这些不需要立项）

## 核心目标

产出一份完整的 `project_brief.json`，让后续 16 个 agent 都按这份 brief 调参。

## 6 个必拆维度

| 维度 | 取值 | 影响下游 |
|------|------|---------|
| `type` | 硬核机制本 / 情感氛围本 / 阵营本 / 还原本 / 混合本 | B 部门诡计强度、D 部门文风密度 |
| `players` | 4 / 5 / 6 / 7 / 8 | C-04 分发器的切分粒度 |
| `duration` | 短(2-3h) / 中(3-5h) / 长(5h+) | B-03 结构设计师的幕数 |
| `style` | 写实 / 和风 / 古风 / 民国 / 赛博 / 玄幻 / 西式 | D-03 角色润色师的语感库 |
| `complexity` | 轻松 / 中等 / 硬核 | B-02 悖论架构师的诡计层数 |
| `sensitivity` | 含血腥 / 含涉政 / 含软情色 / 含未成年 / 全干净 | 所有写作 agent 的过滤词表 |

## 操作流程

### Step 1: 接收需求
读取用户的一句话需求。如果用户只说"开新本"没给主题，直接进 Step 2。

### Step 2: 逐维度澄清
**重要**：用 AskUserQuestion 工具一次问 1-2 个维度，**不要 1 次问 6 个**——会过载用户。

推荐顺序：`type` → `complexity` → `players` + `duration` → `style` → `sensitivity`

每问完一个维度，输出当前已锁定 / 待定 / 不重要的清单，让用户能看到进度。

### Step 3: 范本对标建议（可选）
如果有 `02_成品剧本资料库/` 存在，可选地建议鉴本师调用 1-2 个最匹配的范本作为 prior。但鉴本师本身是另一个 agent，本 skill 只负责"提议"，不调用。

### Step 4: 锁定输出
写入 `_工作区/{项目名}/00_brief/project_brief.json`，schema 见 `04_schemas/project_brief.schema.json`。

输出后明确告诉用户：
- ✅ project_brief 已锁定
- 📂 路径：`...`
- ▶️ 下一步：建议跑鉴本师（A-02）或直接进策划部（B-01/B-02）

## 输入 / 输出

### Input
- 用户对话
- 可选：当前工作区其他元数据

### Output
- 文件：`_工作区/{项目名}/00_brief/project_brief.json`
- 返回主编剧：项目名 + brief 路径

## project_brief.json 示例

```json
{
  "schema_version": "1.0",
  "project_name": "废院循证录",
  "created_at": "2026-05-28T10:00:00Z",
  "one_liner": "在一栋废弃精神病院里复演 30 年前的连环杀人案",
  "type": "硬核机制本",
  "players": 5,
  "duration": "中(3-5h)",
  "style": "写实",
  "complexity": "硬核",
  "sensitivity": {
    "violence": "中度",
    "politics": "不含",
    "sexuality": "不含",
    "minors": "不含"
  },
  "type_specific_options": {
    "multi_truth_layers": 2,
    "physical_constraints": ["时间表", "钥匙巡逻路线"]
  },
  "reference_suggestions": ["猫岛谋杀循环"],
  "user_constraints": [],
  "locked": true
}
```

## 与其他 skill 的协作

| 上游 | 调用方 | 下游 |
|------|--------|------|
| 无（链路起点） | 主编剧 agent | reference-curator / world-builder |

## 错误处理

- 用户拒答某维度 → 标 `null` 并标注 `pending_decision: true`，下游 agent 遇到时再回头问
- 用户给出冲突需求（如"要硬核但又要 2 小时短本"） → 主动指出冲突，请求二选一
- 已有同名项目 → 询问是 v2 还是覆盖

## 测试用例

参见 `02_agents/A-01-genre-router.md` 的"示例 I/O"段落（批 2 交付）。

---

**优先级**：P0（首期必做）
**预估实现工时**：0.5 天（核心是问答模板 + json 写入）
**对应 Agent 规格书**：`02_agents/A-01-genre-router.md`
