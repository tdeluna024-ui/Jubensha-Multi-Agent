# 数据契约（Data Contracts）

> 每个 stage 的"入口必备文件 → 出口产物"约定。主编剧调度时按这份约定判断"能不能进入下一阶段"。

## 0. 黄金法则

**文件系统是唯一真相。**

agent 之间禁止靠"内存传参"、禁止把数据塞进上下文里"提交"给下一个 agent。
所有交付物必须落盘 → 下一个 agent Read 文件 → 处理 → 落盘。

## 1. 总流水线 v10.0

```
Stage 0:    用户对话
            ↓
Stage A:    前研部 (genre-router → reference-curator → inspiration-archivist)
            ↓ project_brief.json + reference_cards/
Stage B:    策划部 (historian + paradox-architect → structure-designer → world-builder)
            ↓ 结构设计完成（B-03 output）
Stage B.5:  ★ 体验架构 (M-01 experience-director) [Bible 锁版前]
            ↓ experience_blueprint.json (用户审批)
Stage B-🔒: Bible 锁版 (B-04 + 用户审批)
            ↓ bible.json + bible.lockfile (🔒 关键里程碑)
Stage C:    工程部 (rule-maker + prop-master + detail-injector → distributor)
            ↓ clues.json + character_payloads/
Stage C.5:  ★ canonical 编译 (C-05 canonical-state-compiler)
            ↓ canonical_story_state.json + .sha256 (🔒 事实锚点)
Stage D+M:  并行生产
            D: 制作部 (identity-architect → lead-writer × N × M → voice-differentiator × N × M)
            M: 多模态部 (M-02 视觉 + M-03 音视频 + M-04 控场台) [均读 canonical]
            ↓ finals/ + 06_multimodal/ + 07_dm_console/
Stage E:    验收部 (logic-auditor → blind-playtester)
            ↓ consistency_report.md + playtest_report.md (🚦 质量门)
Stage F:    交付部 (delivery-packager)
            ↓ 05_delivery/ 完整交付包
Stage 审计: 并行四路 (G-01 + G-02 + H-01 + ★I-01)
            ↓ 四份报告全 PASS
Stage E-03: 最终审计 (delivery-reviewer)
            ↓ ≥ 8.0 PASS
Stage 0':   发版交付给用户
```

## 2. 每个 Stage 的契约

### Stage A 入口契约
**必备文件**：无（这是入口，只需要用户对话）
**出口产物**：
- `00_brief/project_brief.json` (validated against schema)
- 可选：`_pre_research/reference_cards/*.md` (1-3 张)

**质量门**：brief.locked === true 才能进 Stage B

---

### Stage B 入口契约
**必备文件**：
- `00_brief/project_brief.json` (brief.locked === true)

**出口产物**：
- `01_planning/history.md`
- `01_planning/family_tree.json`
- `01_planning/paradox.json` + `paradox_visual.md`
- `01_planning/act_outline.json` + `info_flow.md`
- `01_planning/bible.json` (≤ 300 行)
- `01_planning/bible.md`
- `01_planning/bible_appendix.json`
- `01_planning/bible.lockfile`

**质量门**：bible.lockfile 存在 + user_approved=true，才能进 Stage C

---

### Stage B.5 入口契约（M-01 体验导演）
**必备文件**：
- B-03 `act_outline.json` 已完成
- B-04 `bible.json` 草稿（尚未锁版）

**出口产物**：
- `01_planning/experience_blueprint.json`（含 highlight_nodes、dm_console_events、atmosphere_layers、promo_assets）

**质量门**：experience_blueprint.json 存在 + 用户 approved，才能触发 Bible 锁版

---

### Stage C 入口契约
**必备文件**：
- `01_planning/bible.json` (锁版)
- `01_planning/bible.lockfile`
- `01_planning/experience_blueprint.json` (M-01 产物，用于 C-02 道具规格对齐)

**出口产物**：
- `02_engineering/mechanics.json`
- `02_engineering/clues.json`
- `02_engineering/details.json`
- `02_engineering/character_payloads/char_NN.json` × N
- `02_engineering/distribution_report.md`

**质量门**：distribution_report 中 mutex_check + completeness_check 都 pass，才能进 Stage C.5

---

### Stage C.5 入口契约（C-05 canonical 编译）
**必备文件**：
- `02_engineering/clues.json`（完整）
- `02_engineering/mechanics.json`
- `01_planning/bible.json`（锁版）

**出口产物**：
- `02_engineering/canonical_story_state.json`
- `02_engineering/canonical_story_state.sha256`
- `_trace/{timestamp}_C-05_canonical-compile.json`

**质量门**：C-05 输出状态为 COMPILED（非 COMPILE_ERROR），才能进 Stage D+M

---

### Stage D+M 入口契约（并行生产）
**必备文件（D 部门）**：
- `02_engineering/character_payloads/char_NN.json` × N (all)
- `01_planning/bible.json`（锁版）
- `02_engineering/canonical_story_state.json`（C-05 编译通过）

**必备文件（M 部门）**：
- `02_engineering/canonical_story_state.json`（唯一事实源）
- `01_planning/experience_blueprint.json`（M-01 蓝图）
- `05_delivery/prop_briefs/`（M-02 需要道具规格）

**D 部门出口产物**：
- `03_production/_cognitive/char_NN.json` × N
- `03_production/drafts/actK/char_NN.md` × (N × M)
- `03_production/finals/actK/char_NN.md` × (N × M)
- `03_production/production_report.md`

**M 部门出口产物**：
- `06_multimodal/media_manifest.json`（所有素材注册表）
- `06_multimodal/visual/character_portraits/*.prompt.md`（M-02）
- `06_multimodal/audio/ambience/*.prompt.md`（M-03）
- `06_multimodal/video/opening_60s_storyboard.md`（M-03）
- `07_dm_console/dm_console.html`（M-04 P0）
- `07_dm_console/player_qr/*.html`（M-04 P1）

**质量门**：所有 final 都存在 + must_reveal/hide 自检 pass + media_manifest.json 存在，才能进 Stage E

---

### Stage E 入口契约
**必备文件**：所有 `finals/actK/char_NN.md`

**出口产物**：
- `04_qa/consistency_report.md` (E-01 评分)
- `04_qa/playtest_report.md` (E-02 评分)

**质量门**：两份报告的 overall_score ≥ pass_threshold（或用户强制特许），才能进 Stage F

---

### Stage F 入口契约
**必备文件**：finals/ + bible.json + 两份 QA report (pass) + media_manifest.json

**出口产物**：`05_delivery/` + `06_multimodal/` + `07_dm_console/` 完整套件

---

### Stage 审计入口契约（四路并行，F-01 完成后）
**必备文件**：
- `05_delivery/` 完整
- `06_multimodal/media_manifest.json`（I-01 需要）
- `07_dm_console/dm_console.html`（I-01 需要）
- `02_engineering/canonical_story_state.json`（G-01/G-02/I-01 对比源）

**出口产物**：
- `_invariant_audit/G01_report_{timestamp}.json`（G-01）
- `_timeline/G02_report_{timestamp}.json`（G-02）
- `_spoiler_audit/H01_report_{timestamp}.json`（H-01）
- `_spoiler_audit/I01_multimodal_report_{timestamp}.json`（I-01）

**质量门**：四份报告全部 PASS（status = "PASS"，blockers 数组为空），才能进 E-03

## 3. 修订流程（Bible / payload / final 修订）

### 3.1 Bible 修订（B-04 → 重跑下游）
触发：E-01 / E-02 报告 blocker 指向 Bible

```
1. 主编剧创建 fix proposal:
   _工作区/{项目名}/_meta/bible_fix_proposals/{timestamp}_{blocker_id}.md
2. 主编剧用 AskUserQuestion 让用户审批
3. 用户同意后：
   a. 归档当前 bible 到 _archive/bible_v{X}.json
   b. 由 B-04 生成 bible_v{X+1}.json
   c. 写 lockfile（supersedes = v{X} 的 sha256）
   d. 同步删除所有受影响的下游产物 (character_payloads + finals)
4. 重跑 C-04 distributor
5. 重跑 D-02 + D-03 主笔流水线
6. 重跑 E-01 + E-02 验收
```

### 3.2 Payload 修订（C-04 → 重跑相关角色）
触发：盲测发现某角色信息不足，仅需修 visibility

```
1. 主编剧修改 02_engineering/details.json 或 clues.json 的 visibility
2. 重跑 C-04 distributor（自动重生成所有 payload）
3. 删除受影响角色的 finals（仅该角色 + 仅相关幕）
4. 重跑 D-02/D-03 该角色该幕
5. 重跑 E-01 + E-02
```

### 3.3 单角色单幕 final 修订（D-02/D-03 微调）
触发：审计指出某段文字小问题

```
1. 主编剧修改 03_production/finals/actK/char_NN.md
2. 在 _meta/changelog.md 记录手动修改
3. 重跑 E-01（增量）
```

## 4. 每次修订必写 changelog

文件：`_meta/changelog.md`

格式：
```markdown
## {ISO8601} · v{X} → v{X+1}

**触发**: {blocker_id 或 user_request}
**修订内容**: {diff 摘要}
**触发的 agent 重跑**: {agent 列表}
**预期评分变化**: {dimension}: {from} → {to}
**实际评分变化** (执行后回填): {from} → {to}
```

## 5. agent 跨阶段读权限

| Agent | 能读 | 不能读 |
|-------|------|--------|
| A-01 | 用户对话 | 工作区任意 |
| A-02 | brief + reference_index | finals / Bible |
| A-03 | 用户旧目录 | 工作区当前项目 |
| B-* | 上一 stage 产物 | finals / payload |
| M-01 | B-03 act_outline + B-04 bible 草稿 | finals / payload / canonical |
| C-01..C-03 | bible.json | character_payloads（必须等 C-04 产出） |
| C-04 | bible + mechanics + clues + details | finals |
| **C-05** | bible + clues + mechanics | finals / character_payloads |
| D-01 | bible 中该角色字段 | 其他角色字段 |
| D-02 | 自己 char 的 payload + cognitive + canonical（只读） | 其他角色任何文件 |
| D-03 | 自己 char 的 draft + voice_card | 其他角色任何文件 |
| **M-02** | canonical（只读）+ experience_blueprint + prop_briefs | finals / character_payloads |
| **M-03** | canonical（只读）+ experience_blueprint | finals / character_payloads |
| **M-04** | canonical（只读）+ experience_blueprint + DM手册 | finals / character_payloads |
| E-01 | finals + bible | playtest_report |
| E-02 主 agent | finals + payload + bible（对答案） | canonical（不应看到答案） |
| E-02 subagent | 仅自己 char 的 session.md（inline） | 工作区任何文件 |
| F-01 | finals + bible + QA reports + media_manifest | - |
| **I-01** | canonical（只读）+ 06_multimodal/ + 07_dm_console/ | finals / character_payloads |
| G-01/G-02 | canonical（只读）+ 05_delivery/ | - |
| H-01 | 05_delivery/packets/ + public_clues/ | canonical |

**E-02 subagent 的 prompt 必须强制声明禁止读工作区**，否则盲测无效。
**M-02/M-03/M-04 对 canonical 只读**，不得修改事实。

## 6. 反例（绝不能做）

- ❌ 跳过 Stage 直接做下一步（如不锁 Bible 就写主笔）
- ❌ 在内存里传产物，不落盘（断电就丢）
- ❌ 修了文件不写 changelog
- ❌ 让 D-02 直接读 details.json（应该读自己的 payload）
- ❌ 让 E-02 subagent 看到 Bible（盲测不盲了）

---
**版本**：v10.0 / 2026-05-31
