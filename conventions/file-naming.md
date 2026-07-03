# 文件命名约定

> 所有 agent 必须遵守。命名约定是"机器读"的接口，乱命名 = 跨 agent 找不到文件 = 团队崩溃。

## 1. 工作区目录结构（每个项目）

```
工作区/{项目名}/
├── 00_brief/
│   └── project_brief.json
├── 01_planning/
│   ├── history.md
│   ├── family_tree.json
│   ├── key_historical_events.json
│   ├── paradox.json
│   ├── paradox_visual.md
│   ├── act_outline.json
│   ├── info_flow.md
│   ├── bible.json                    ← 锁版后只读
│   ├── bible.md
│   ├── bible_appendix.json
│   ├── bible.lockfile
│   └── experience_blueprint.json     ← ★ M-01 产物（Bible锁版前生成）
├── 02_engineering/
│   ├── mechanics.json
│   ├── clues.json
│   ├── details.json
│   ├── distribution_report.md
│   ├── canonical_story_state.json    ← ★ C-05 产物（D+M 部门的事实锚点）
│   ├── canonical_story_state.sha256  ← ★ canonical 校验文件
│   └── character_payloads/
│       ├── char_01.json
│       ├── char_02.json
│       └── ...
├── 03_production/
│   ├── _cognitive/
│   │   ├── char_01.json
│   │   └── ...
│   ├── drafts/
│   │   ├── act1/
│   │   │   ├── char_01.md
│   │   │   └── ...
│   │   └── act2/...
│   ├── finals/
│   │   └── (同 drafts 结构)
│   └── production_report.md
├── 04_qa/
│   ├── consistency_report.md
│   └── playtest_report.md
├── 05_delivery/           ← F-01 文本交付物
│   ├── README.md
│   ├── release_notes.md
│   ├── packets/
│   │   └── char_{NN}_{name}/
│   │       ├── 幕1_亮相.md
│   │       └── ...
│   ├── public_clues/
│   │   └── 幕N_公共线索.md
│   ├── prop_briefs/
│   │   └── {cNNN}_{name}.md
│   ├── DM手册.md
│   └── 道具清单.md
├── 06_multimodal/         ← ★ M-02/M-03 产物（视觉/音视频素材）
│   ├── media_manifest.json            ← 所有素材注册表（绑定 canonical）
│   ├── visual/
│   │   ├── character_portraits/
│   │   │   └── char_{NN}_{name}.prompt.md
│   │   ├── props_photorealistic/
│   │   │   └── {cNNN}_{name}.prompt.md
│   │   ├── scene_maps/
│   │   └── promo/
│   ├── audio/
│   │   ├── ambience/
│   │   │   └── 幕N_音景.prompt.md
│   │   ├── character_themes/
│   │   │   └── char_{NN}_{name}.prompt.md
│   │   └── sfx/
│   │       └── {event_id}.prompt.md
│   └── video/
│       ├── opening_60s_storyboard.md
│       └── flashbacks/
│           └── {cNNN}_{trigger}.storyboard.md
├── 07_dm_console/         ← ★ M-04 产物（离线 DM 控场台）
│   ├── dm_console.html               ← 主控场台（单文件，离线可用）
│   ├── dm_console_assets/
│   │   ├── audio/
│   │   └── video/
│   ├── dm_console_build.json         ← 控场台数据配置
│   ├── player_qr/
│   │   └── char_{NN}_{name}_private.html
│   └── README_控场台使用说明.md
├── _playtest/            ← 盲测中间产物
│   ├── {char_id}_session.md
│   └── {char_id}_reasoning.md
├── _trace/               ← 可观测性：每个 agent 调用一份 trace
│   └── {ISO8601}_{agent_id}_{action}.json
├── _archive/             ← Bible 旧版归档
│   └── bible_v0.1.json
├── _meta/
│   ├── changelog.md
│   ├── scoring_rubric.json
│   └── topology.mmd
├── _invariant_audit/     ← G-01 物理不变量报告
├── _timeline/            ← G-02 时间线状态机报告
└── _spoiler_audit/       ← H-01 防剧透报告 + I-01 多模态审计报告
└── dashboard.md          ← 项目级看板，主编剧维护
```

## 2. ID 命名规则

| 实体 | 模式 | 示例 |
|------|------|------|
| 角色 | `char_NN` (2 位数字) | char_01, char_07 |
| 真相层 | `tl_NN` | tl_01, tl_02 |
| 机制 | `m_NN` | m_01, m_04 |
| 线索 | `c_NNN` (3 位数字) | c_001, c_058 |
| 细节 | `d_NNN` | d_001, d_065 |
| Blocker | `B-N` (1 起跳，按发现顺序) | B-1, B-2 |
| Trace | `{ISO8601}_{agent_id}_{action}` | `2026-05-28T10:30:15Z_E-02_blind-playtest` |

**禁止**：
- ❌ `char_1`（必须 2 位 → `char_01`）
- ❌ `c_1`（必须 3 位 → `c_001`）
- ❌ 用中文 ID（display_name 可中文，但 ID 必须英文 + 数字）

## 3. 项目名约定

- 中文，长度 2-12 字
- 无空格、无 `/\:*?"<>|` 等文件系统特殊字符
- 一旦立项不可改（要改 = 新建项目）

**示例**：废院循证录 / 民国弄堂案 / 龙脊村末日

## 4. Trace 文件名

格式：`{ISO8601_UTC}_{agent_id}_{action}.json`

示例：
```
2026-05-28T10:30:15Z_A-01_genre-routing.json
2026-05-28T10:35:00Z_B-04_build-bible.json
2026-05-28T11:00:42Z_D-02_draft-act2-char_01.json
2026-05-28T11:45:18Z_E-02_blind-playtest-v0.1.json
```

约定：
- 时间戳必须 UTC（带 Z 后缀）
- 文件名使用 ISO8601 但用 `T` 隔开日期时间，**不用** `:` 直接拼（macOS 文件系统可，但跨平台 Windows 不行）

> ⚠️ 实际写盘时，把 `:` 替换为 `-`：
> `2026-05-28T10-30-15Z_A-01_genre-routing.json`

## 5. 角色本文件名

`05_delivery/角色本/{char_display_name}.docx`

- 用 display_name（中文姓名），不用 char_id
- 不加幕号（一个角色一本，含所有幕）

## 6. Bible 修订归档

每次锁新版前归档旧版到 `_archive/`：

```
_archive/bible_v0.1.json
_archive/bible_v0.1.md
_archive/bible_v0.1.lockfile
_archive/bible_v0.1.diff.md       ← 与 v0.2 的差异
```

## 7. Agent ID 命名

固定不变（用于 trace 和报告引用）：

| ID | 名称 | 部门 |
|----|------|------|
| A-01 | genre-router | 前研部 |
| A-02 | reference-curator | 前研部 |
| A-03 | inspiration-archivist | 前研部 |
| B-01 | historian | 策划部 |
| B-02 | paradox-architect | 策划部 |
| B-03 | structure-designer | 策划部 |
| B-04 | world-builder | 策划部 |
| C-01 | rule-maker | 工程部 |
| C-02 | prop-master | 工程部 |
| C-03 | detail-injector | 工程部 |
| C-04 | distributor | 工程部 |
| **C-05** | **canonical-state-compiler** | **工程部 ★v10.0** |
| D-01 | identity-architect | 制作部 |
| D-02 | lead-writer | 制作部 |
| D-03 | voice-differentiator | 制作部 |
| E-01 | logic-auditor | 验收部 |
| E-02 | blind-playtester | 验收部 |
| E-03 | delivery-reviewer | 验收部 |
| F-01 | delivery-packager | 交付部 |
| G-01 | invariant-auditor | 审计部 |
| G-02 | timeline-statemachine | 审计部 |
| H-01 | spoiler-linter | 审计部 |
| **I-01** | **multimodal-auditor** | **审计部 ★v10.0** |
| **M-01** | **experience-director** | **多模态部 ★v10.0** |
| **M-02** | **visual-director** | **多模态部 ★v10.0** |
| **M-03** | **audio-video-director** | **多模态部 ★v10.0** |
| **M-04** | **interactive-builder** | **多模态部 ★v10.0** |

## 8. 反例（绝不能做）

- ❌ 在 `_工作区/` 根目录创建任意命名的文件（必须落到对应 stage 目录）
- ❌ 用 `tmp_` / `test_` / `bak_` 前缀（应该用 _trace / _archive）
- ❌ 把中间产物提交到 `05_delivery/`（用户看到会误以为是成品）
- ❌ 写 `bible_final.json` / `bible_FINAL_v2.json` 这种命名（用 lockfile + 版本号）

---
**版本**：v10.0 / 2026-05-31
