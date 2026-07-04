---
name: ghostwriter-pipeline
description: 制作部的核心流水线。按 Act × Character 双层 Loop 调度 D-01 认知架构师 → D-02 主笔 → D-03 角色润色师，输出每个角色每一幕的最终文本。当用户/主编剧说"开始写本 / 进入制作 / 生成剧本文本"时触发。
tools: Read, Write, Edit, Bash
---

# Skill: ghostwriter-pipeline (制作部流水线)

## 设计哲学

整个团队的 token 消耗 80% 都在这条流水线。优化点：

1. **双层 Loop 切片**：每次 LLM 调用只看「当前幕 × 当前角色」的最小必要切片，不喂整个 Bible
2. **粗稿 / 终稿分离**：主笔产粗稿不追求文学性，角色润色师再做差异化文风（避免反复改）
3. **强制权限隔离**：每个角色调用时只读自己的 payload，绝不暴露其他角色的私密细节

## 何时触发

- distributor 已成功跑完，`02_engineering/character_payloads/` 下文件齐全
- Bible 已锁版
- 主编剧说"开始写本 / 写第 N 幕 / 重写 char_X"

## 核心目标

对每一对 (Act, Character) 产出一份最终文本：

```
03_production/finals/act{N}/{char_id}.md
```

## 双层 Loop 结构

```python
for act in bible["acts"]:            # 外层：每一幕
    for char in bible["characters"]: # 内层：每个角色
        run_pipeline(act, char)
```

每对 (act, char) 跑一遍完整 pipeline，互相隔离。

## 单次 pipeline 详解（D-01 → D-02 → D-03）

### D-01 认知架构师（仅首次跑某 char 时执行）

- **输入**：Bible 的 char.bio_id + char.cog_id + paradox.truth_layers
- **输出**：`03_production/_cognitive/{char_id}.json` —— 该角色的"双重身份卡"

  ```json
  {
    "char_id": "char_03",
    "bio_id": { "real_father": "char_07", "real_actions_1999": [...] },
    "cog_id": { "self_belief": "我是孤儿", "modified_memories": [...] },
    "rationalization_strategy": "遇到不一致时，归因为命运/天意"
  }
  ```

后续每一幕都复用这份认知卡，不重生成。

### D-02 主笔

- **输入**：
  - `current_act` (来自 act_outline)
  - `char_cognitive_profile` (上一步 D-01)
  - `character_payloads/{char_id}.json`
  - `mechanics` （仅该角色 affected 的部分）
- **必须做**：
  - 严格第一人称
  - 按 cog_id 写，bio_id 与 cog_id 冲突时通过心理活动"合理化"
  - 强制把 payload.visible_details 里"本幕该出现"的细节植入文本
  - 满足 act 的 must_reveal（必须揭示的信息）
  - 不出现 act 的 must_hide（不准提的信息）
- **输出**：`03_production/drafts/act{N}/{char_id}.md` （粗稿）

### D-03 角色润色师

- **输入**：
  - 上一步 D-02 的 draft
  - `char.voice_card` （年龄/职业/句长/口头禅/比喻偏好）
- **不做**：不改剧情、不改细节、不改逻辑
- **只做**：文风迁移到该角色的语感
  - 一个守墓人不会说"这事让我很难过"，他会说"和往日见的死者一样，又一具"
  - 一个家庭主妇的句长偏短、用动词比形容词多
  - 一个心理学教授会夹杂术语和比喻
- **输出**：`03_production/finals/act{N}/{char_id}.md` （终稿）

## 操作流程（流水线总调度）

### Step 1: 输入完整性检查

```python
assert exists("01_planning/bible.json")
assert exists("01_planning/bible.lockfile")  # 必须锁版
for char in bible["characters"]:
    assert exists(f"02_engineering/character_payloads/{char['id']}.json")
```

### Step 2: 双层 Loop

```python
for act_idx, act in enumerate(bible["acts"], 1):
    for char in bible["characters"]:
        # 增量跳过：已存在的 final 不重跑（除非用户要求重写）
        final_path = f"03_production/finals/act{act_idx}/{char['id']}.md"
        if exists(final_path) and not force_rewrite:
            continue

        # D-01（首次）
        cog_path = f"03_production/_cognitive/{char['id']}.json"
        if not exists(cog_path):
            run_identity_architect(char, bible, output=cog_path)

        # D-02
        draft_path = f"03_production/drafts/act{act_idx}/{char['id']}.md"
        run_lead_writer(act, char, cog_path, payload_path=..., output=draft_path)

        # D-03
        run_voice_differentiator(draft_path, char.voice_card, output=final_path)
```

### Step 3: 进度报告

每跑完一个 (act, char) 在终端输出进度：`[3/30] act 1 / char_03 done`

### Step 4: 收尾汇总

写入 `03_production/production_report.md`：
- 各角色字数统计
- 字数偏差告警（如果有角色字数远高/低于均值）
- D-03 文风差异化指标（句长方差、用词重合度等）

## Token 预算策略

| 组件 | 单次 token | 频次 | 总计 |
|------|-----------|------|------|
| D-01 认知架构师 | ~3k | 1×N人 | ~15k |
| D-02 主笔 | ~5-8k | N人 × M幕 | ~150k (5人×4幕) |
| D-03 角色润色师 | ~3-5k | N人 × M幕 | ~80k |
| **小本总计** | | | **~250k** |
| **标准本总计** | | | **~500k** |

注意：每次 LLM 调用必须只投喂"当前幕 + 当前角色"的切片，不能投整个 Bible。

## 输入 / 输出

### Input
- 全部 `02_engineering/character_payloads/*.json`
- `01_planning/bible.json` (锁版)
- `01_planning/bible_appendix.json` (按需读)

### Output
- `03_production/_cognitive/{char_id}.json` × N
- `03_production/drafts/act{N}/{char_id}.md` × (N×M)
- `03_production/finals/act{N}/{char_id}.md` × (N×M)
- `03_production/production_report.md`

## 与其他 skill 的协作

| 上游 | 调用方 | 下游 |
|------|--------|------|
| distributor | 主编剧 agent | logic-auditor / playtester |

## 重跑触发条件

- 用户对某 (act, char) 不满意 → 删除该 final 后重跑流水线（增量跳过其他已完成的）
- E-01 审计指出某文本与 Bible 矛盾 → 标 force_rewrite 后重跑该文本
- Bible 修订（v0.x → v0.(x+1)） → 必须全部重跑（认知卡也要重生成）

## 反例（绝不能做）

- ❌ 一次性把整本剧本生成（必崩）
- ❌ 跨角色读取 payload（D-02 写 char_03 时不能看 char_07 的私密）
- ❌ 让 D-03 改逻辑或剧情（它只改文风）
- ❌ 跳过 D-01 直接让 D-02 写（认知会漂）

## 测试用例

参见 `02_agents/D-02-lead-writer.md` 和 `D-03-voice-differentiator.md`（批 2 交付）。

---

**优先级**：P0（占工期 40%）
**预估实现工时**：3-5 天（pipeline 框架 + 三个 prompt 模板 + 切片逻辑）
**对应 Agent 规格书**：`02_agents/D-01..D-03`
