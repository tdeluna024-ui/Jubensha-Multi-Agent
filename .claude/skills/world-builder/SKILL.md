---
name: world-builder
description: 把策划部 B-01..B-03 的产物（历史 / 诡计拓扑 / 幕大纲）整合成一份只读的 Global World Bible。这是全流程的"真理之书"，锁版后所有下游 agent 必须以它为准。当用户/主编剧说"建世界 / 锁 Bible / 整合策划产物"时触发。
tools: Read, Write, Edit
---

# Skill: world-builder (世界构建者)

## 何时触发

- B-01 史官 / B-02 悖论架构师 / B-03 结构设计师 都已经产出各自文件
- 主编剧准备进入工程部（C 部门）前必须先跑这个
- 用户说"建世界 / 锁 Bible / 整合 / 出真理之书"

## 这是整个系统最关键的 skill 之一

Bible 锁版前 = 一切都可以改
Bible 锁版后 = 一切都不准擅自改（要改必须走 Bible v0.x → v0.(x+1) 的流程）

## 核心目标

把分散在 `01_planning/` 下的几个独立文件整合成一份 `bible.json` + `bible.md`，并执行一致性自检。

## 操作流程

### Step 1: 输入清单检查

必备文件（缺一不可，缺则报错并提示主编剧补全）：
- `01_planning/history.md` （史官产出）
- `01_planning/paradox.json` （悖论架构师产出）
- `01_planning/act_outline.json` （结构设计师产出）

可选文件：
- `01_planning/family_tree.json`
- `01_planning/genre_specific_*.json`

### Step 2: 整合

按 `04_schemas/bible.schema.json` 的结构拼装。关键拼装动作：

1. **核心 vs 附录拆分**：把 Bible 拆成两份
   - `bible.json` （核心，<= 300 行，所有下游 agent 都会读）
   - `bible_appendix.json` （细节，可按需点查，不进默认上下文）

2. **truth_layers 编号化**：把悖论架构师的 truth_layers 数组打 ID（`tl_01`, `tl_02`...）

3. **角色 ID 标准化**：所有角色统一用 `char_XX` 编号，原始姓名进 `display_name` 字段

4. **must_reveal / must_hide 矩阵**：每一幕生成"必须揭示"和"必须隐藏"的清单，是 D-02 主笔的硬约束

### Step 3: 自检（必跑）

执行以下检查，任一失败必须报告：

| 检查项 | 失败示例 |
|--------|---------|
| 每个 truth_layer 都有 killer | "第二轮还原没指定凶手" |
| 每个角色都有 bio_id 和 cog_id | "char_03 缺 cog_id" |
| 每个 act 都有 must_reveal / must_hide | "act 3 没说必须隐藏什么" |
| paradox 引用的角色都存在 | "诡计提到 char_07 但只有 5 个角色" |
| 没有循环引用 | "char_01.cog_parent_ids → char_03 → char_01" |
| sensitivity 范围合规 | "history.md 含未成年涉性内容但 brief 标了'不含未成年'" |

### Step 4: 写盘

```
01_planning/
├── bible.json              ← 核心，只读
├── bible.md                ← 人类可读版
├── bible_appendix.json     ← 细节
└── bible.lockfile          ← 包含 sha256 + 锁版时间戳
```

锁版后立即生成 `bible.lockfile`：
```
{
  "version": "0.1",
  "locked_at": "2026-05-28T12:00:00Z",
  "sha256": "abc123...",
  "locked_by": "user_approval",
  "supersedes": null
}
```

### Step 5: 必须经过用户审批

写盘完成后，**不要直接进下一阶段**。必须用 AskUserQuestion 把 bible 的关键摘要展示给用户，让用户选：
- ✅ 锁定 v0.1，进入工程部
- ↩️ 退回修订（指出哪里要改，回到 B-01/B-02/B-03）
- 🛑 暂停项目

## Bible 修订流程（锁版后）

锁版后任何修改都不能直接覆盖 `bible.json`：

1. 创建 `bible_v0.2_proposal.json` （diff 形式）
2. 标注修订原因（来自哪个 QA report / 用户要求）
3. 用 AskUserQuestion 让用户审批
4. 审批通过后，归档 `bible_v0.1.json` 到 `_archive/`，新版生效

详见 `05_conventions/data-contracts.md`。

## 输入 / 输出

### Input
- `01_planning/history.md`
- `01_planning/paradox.json`
- `01_planning/act_outline.json`
- 可选附加文件

### Output
- `01_planning/bible.json` (核心)
- `01_planning/bible.md` (人类版)
- `01_planning/bible_appendix.json`
- `01_planning/bible.lockfile`

## 与其他 skill 的协作

| 上游 | 调用方 | 下游 |
|------|--------|------|
| B-01/B-02/B-03 产物 | 主编剧 agent | distributor / 整个 D 部门 |

## 反例（绝不能做）

- ❌ 把 `bible.json` 写得超过 500 行（应该走 appendix）
- ❌ 跳过用户审批直接锁版
- ❌ 锁版后偷偷改 `bible.json` 而不走修订流程
- ❌ 自检失败但只 warning 不 block

## 测试用例

参见 `02_agents/B-04-world-builder.md` 的"示例 I/O"段落（批 2 交付）。

---

**优先级**：P0
**预估实现工时**：1-2 天（schema 校验 + 整合 + 审批流程）
**对应 Agent 规格书**：`02_agents/B-04-world-builder.md`
