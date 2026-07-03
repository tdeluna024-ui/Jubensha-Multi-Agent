---
name: playtester
description: 盲测玩家模拟。启动 N 个 subagent（每个扮演一个角色），从 Act 1 开始严格只读自己的材料 + 公共线索，逐幕写出推理，验收剧本的"可推理性"。当用户/主编剧说"盲测 / 玩家测试 / 推理验证"时触发。
tools: Read, Write, Agent
---

# Skill: playtester (盲测玩家模拟) ⭐ v9.0 核心新增

## 设计哲学

逻辑审计（E-01）查的是"剧本本身有没有矛盾"。盲测查的是"玩家拿着剧本能不能玩出来"。

这是两个完全独立的质量维度：

| 维度 | 检查什么 | 失败示例 |
|------|---------|---------|
| 逻辑审计 | 跨角色一致性 | "A 说看到 B，但 B 不在场" |
| 盲测 | 玩家视角可达性 | "结论需要 char_03 知道家族秘密，但 char_03 的本里没线索" |

只有逻辑审计通过、盲测也通过的本，才是真的能玩的本。

## 何时触发

- 制作流水线 ghostwriter-pipeline 已跑完所有 final
- 逻辑审计 E-01 已通过（不通过先回去修）
- 主编剧说"盲测 / 跑玩家测试 / 验证可推理性"

## 核心目标

启动 N 个 subagent（N = 角色数），每个 subagent 扮演一个玩家，严格按"逐幕拿到材料"的方式从头玩到尾，最后输出推理。

汇总成 `playtest_report.md`，回答：
1. 玩家能不能推到核心真相？
2. 推不到的话，断点在哪一幕、缺哪条线索？
3. 哪些信息分发不均（某玩家信息密度过高/过低）？
4. 有没有"上帝视角才能解的逻辑断点"？

## 操作流程

### Step 1: 准备每个玩家的"剧情包"

对每个角色生成一个 `_playtest/{char_id}_session.md`，按时间顺序排好该玩家会逐步看到的所有材料：

```markdown
# Playtest Session: char_03

## 收到的角色本（开场）
[内容]

## Act 1: 公共线索
[内容]

## Act 1: 个人线索
[内容]

## Act 2: 调查阶段公共信息
[内容]

## Act 2: 个人新增线索
[内容]

...
```

注意：**必须按真实游戏流程的时间顺序展示**，不能让 subagent 一次看完所有内容。

### Step 2: 启动 N 个 subagent

用 Agent 工具启动 N 个并行 subagent，每个的 prompt 大致是：

```
你是剧本杀玩家"{char_name}"。

你**只能**看到下面提供的材料 + 公共线索 + 主持人提示。
**禁止**：
- 推测材料外的信息
- 假装知道其他玩家的私密内容
- 把"上帝视角"的合理推论当成已知

每读完一幕，输出该幕结束时你的：
1. 已知事实清单（每条标 clue_id 来源）
2. 当前推理（凶手是谁？动机？手法？）
3. 你想问主持人的问题
4. 你想质询其他玩家的问题

最后一幕结束后输出"我的最终结论"。

材料如下：
{paste session contents}
```

### Step 3: 汇总 N 份推理报告

每个 subagent 返回它的逐幕推理 + 最终结论。

把 N 份合并成 `04_qa/playtest_report.md`：

```markdown
# Playtest Report

## 1. 各玩家最终结论
| 玩家 | 推到真相? | 偏离的真相 |
|------|----------|-----------|
| char_01 | ✅ 完全推到 | - |
| char_02 | ⚠️ 推到一半 | 知道凶手但搞错动机 |
| char_03 | ❌ 走偏 | 怀疑了无辜角色 |
...

## 2. 关键断点分析
- **Act 3 断点**：char_02 / char_03 都卡在"无法确定 char_07 的真实性别"
  - 缺失线索：char_07 的医疗档案应该至少分给 char_02
  - 建议：把 detail_id=d_041 的 visibility 从 "char_05" 改为 ["char_02", "char_05"]

## 3. 信息密度分析
| 玩家 | 私密细节数 | 线索数 | 偏差 |
|------|----------|--------|------|
| char_01 | 12 | 8 | 中等 |
| char_02 | 4 | 3 | ⚠️ 过低 |

## 4. 上帝视角断点
- "A 与 B 同时离场"——所有玩家本里都没说，但解谜需要这个信息

## 5. 建议修订动作
- [ ] 调整 d_041 的 visibility
- [ ] 给 char_02 补 2 条私密细节
- [ ] 在 Act 2 公共线索里加"A 与 B 同时离场"
```

### Step 4: 把修订建议回写到任务清单

`playtest_report.md` 的「建议修订动作」部分要自动转成 TaskCreate 任务，交给主编剧分配给相应 agent 重跑。

## 输入 / 输出

### Input
- `03_production/finals/act{N}/{char_id}.md` × all
- `02_engineering/character_payloads/{char_id}.json` × all
- `01_planning/bible.json` (仅 main agent 用于核对真相，不发给 subagent)

### Output
- `_playtest/{char_id}_session.md` × N （subagent 输入）
- `_playtest/{char_id}_reasoning.md` × N （subagent 输出）
- `04_qa/playtest_report.md` （汇总）

## 与其他 skill 的协作

| 上游 | 调用方 | 下游 |
|------|--------|------|
| ghostwriter-pipeline + logic-auditor | 主编剧 agent | distributor (回炉) / ghostwriter-pipeline (重写) |

## 关键安全约束

- ⚠️ subagent 的上下文里**绝不能**出现 Bible 全文
- ⚠️ subagent 的上下文里**绝不能**出现其他角色的私密细节
- ⚠️ 主 agent 才能看 Bible 用于"对答案"，subagent 只能"猜"
- ⚠️ subagent 不能调用 Read 工具读工作区任意文件（必须 prompt 里 inline 提供材料）

## 反例（绝不能做）

- ❌ 让一个 subagent 同时扮演多个角色（会自带上帝视角）
- ❌ 把 Bible 喂给 subagent（盲测就不盲了）
- ❌ 主 agent 替 subagent 推理（必须由 subagent 自己产出）
- ❌ 一次性给 subagent 所有幕的材料（必须按幕分批投喂）

## 重跑触发条件

每次修订（不论是 visibility 调整、文本重写、还是 Bible 改版）后都需要重跑盲测。建议：

- 小修订 → 只重跑受影响的 subagent
- 大修订（Bible 改版）→ 全量重跑

## 测试用例

参见 `02_agents/E-02-blind-playtester.md`（批 2 交付）。

---

**优先级**：P0（质量保证核心）
**预估实现工时**：2-3 天（subagent 编排 + session 切分 + 汇总分析）
**对应 Agent 规格书**：`02_agents/E-02-blind-playtester.md`
