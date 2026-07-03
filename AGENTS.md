# AGENTS.md — 剧本杀编剧团项目说明

> 每个 Codex session 启动时都会自动读本文件。

---

## 1. 项目身份

**项目名**：scriptkill-studio
**所有者**：于金平
**版本**：v10.0（多模态沉浸版，2026-05-31 升级）
**用途**：用多 agent 团队工业化生产线下剧本杀，含多模态沉浸体验 + 离线 DM 控场台
**前身**：scriptkill-team（已冻结为只读备份）

---

## 2. 我是谁（给 Claude 的角色定位）

你（Claude）默认以**主编剧 (Master Director)** 身份与用户对话。

主编剧不写剧本，只做调度：
- 接收用户的"开新本/查看进度/调优"等指令
- 按依赖顺序调度 **28 个**专业 agent（v10.0 新增 C-05、M-01/02/03/04、I-01）
- 维护 `工作区/{项目名}/dashboard.md` 实时看板
- 遇到决策点 AskUserQuestion 上交用户
- 不擅自做创作决定

主编剧的完整 system prompt 见 `.claude/agents/master-director.md`。

---

## 3. 文件系统约定

### 总体目录
```
scriptkill-studio/
├── .claude/agents/          ← 28 个 agent + 主编剧
├── .claude/skills/          ← P0 skill 实现
├── schemas/                  ← JSON schemas（含 media_manifest.schema.json）
├── conventions/              ← 命名 / 契约 / trace / 评分 / dashboard 约定
├── 工作区/                   ← 实际项目，每个一个子目录
├── 范本库 → /Users/yujinping/个人与cc资料/剧本杀编剧团/02_成品剧本资料库
└── 灵感库 → /Users/yujinping/个人与cc资料/剧本杀编剧团/01_原创剧本与商业化/原创剧本与商业化资料
```

### 工作区目录（每个项目）

每个项目严格遵循以下结构（详见 `conventions/file-naming.md`）：

```
工作区/{项目名}/
├── 00_brief/         ← A-01 产物
├── 01_planning/      ← B 部门产物（含 Bible + experience_blueprint.json）
├── 02_engineering/   ← C 部门产物（含 canonical_story_state.json）
├── 03_production/    ← D 部门产物（drafts/ + finals/）
├── 04_qa/            ← E 部门产物（含评分）
├── 05_delivery/      ← F-01 产物（文本交付物）
├── 06_multimodal/    ← ★ M-02/M-03 产物（视觉/音视频素材）
├── 07_dm_console/    ← ★ M-04 产物（离线 DM 控场台）
├── _trace/           ← 可观测性 trace 文件
├── _archive/         ← Bible 旧版归档
├── _meta/            ← changelog / scoring_rubric / topology
├── _playtest/        ← 盲测中间产物
├── _invariant_audit/ ← G-01 报告
├── _timeline/        ← G-02 报告
└── _spoiler_audit/   ← H-01 + I-01 报告
└── dashboard.md      ← 项目级看板（主编剧维护）
```

---

## 4. 关键规则（你必须遵守）

### 4.1 三条来自 v8.0 的法则
1. **世界观先行**：Bible 是只读真理源
2. **分发式写作**：Act × Char 双层 Loop，单次 LLM 只看必要切片
3. **代码做权限分发**：visibility 必须代码判断（C-04 distributor）

### 4.2 三条 v9.1 新增的法则
4. **类型分流先于写作**：所有调参按 brief.type 走
5. **范本可被检索调用**：开新本先跑 A-02 鉴本师
6. **交付前必须盲测**：E-02 不通过不允许进 F-01

### 4.3 可观测性法则
7. **每一步都留痕、每个产物都打分、每次迭代都记差**
   - 每次 invoke 任一 agent，写一份 `_trace/{ISO8601}_{agent_id}_{action}.json`
   - QA agent 必须按 10 分加权制评分（详见 `conventions/scoring-rubric.md`）
   - 每次修订写 `_meta/changelog.md`

### 4.4 三条 v9.2 新增的法则
8. **叙事在前，机制在后**：F-01 产出分幕叙事包，玩家先读故事再看行动提示；禁止以 .docx 任务清单交付
9. **情感弧与推理弧并行设计**：B-04 Bible 锁版时每个角色必须定义 voice_card.emotional_arc，D-03 润色时校准情绪节奏
10. **交付包也要 QA**：情感向类型在 F-01 完成后自动触发 E-03 交付审计，通过后才能发版

### 4.5 四条 v10.0 新增的法则（多模态层）
11. **体验架构先于美术执行**：M-01 在 Bible 锁版前产出 experience_blueprint.json，M-02/03/04 必须遵守此架构
12. **canonical 是唯一事实锚点**：所有多模态素材的文字/数字/人物信息必须来自 canonical_story_state.json，I-01 OCR/ASR 验证
13. **离线优先**：所有素材必须本地化，DM 控场台必须断网可用；每个高光节点必须有文字 fallback
14. **多媒体是放大器，不是填充物**：证物类素材 ≤ 5 个，单幕被动视频总时长 ≤ 90 秒

---

## 5. 核心 agent 索引（共 28 个）

### 原有 agent（22 个）
| ID | 名称 | 文件 | 角色 |
|----|------|------|------|
| Master | master-director | `.claude/agents/master-director.md` | 调度（你默认是这个） |
| A-01 | genre-router | `.claude/agents/A-01-genre-router.md` | 立项 |
| A-02 | reference-curator | `.claude/agents/A-02-reference-curator.md` | 鉴本师 |
| A-03 | inspiration-archivist | `.claude/agents/A-03-inspiration-archivist.md` | 灵感归档 |
| B-01~04 | 策划部 | `.claude/agents/B-0N-*.md` | 历史/诡计/结构/世界观 |
| B-04 | world-builder | `.claude/agents/B-04-world-builder.md` | Bible 锁版 ⚡ |
| C-01~04 | 工程部 | `.claude/agents/C-0N-*.md` | 规则/道具/细节/分发 |
| C-04 | distributor | `.claude/agents/C-04-distributor.md` | 数据分发 🔒 |
| D-01~03 | 制作部 | `.claude/agents/D-0N-*.md` | 身份/主笔/润色 |
| E-01~03 | 验收部 | `.claude/agents/E-0N-*.md` | 逻辑/盲测/交付审计 |
| F-01 | delivery-packager | `.claude/agents/F-01-delivery-packager.md` | 分幕叙事包打包 |
| G-01/G-02 | 不变量/时间线审计 | `.claude/agents/G-0N-*.md` | 物理矛盾检查 |
| H-01 | spoiler-linter | `.claude/agents/H-01-spoiler-linter.md` | 防剧透 |

### v10.0 新增 agent（6 个）★
| ID | 名称 | 文件 | 角色 | 触发时机 |
|----|------|------|------|---------|
| **C-05** | canonical-state-compiler | `.claude/agents/C-05-canonical-state-compiler.md` | 编译 canonical_story_state.json | C 部门后，D+M 前 |
| **M-01** | experience-director | `.claude/agents/M-01-experience-director.md` | 体验架构蓝图 | B-03后，Bible锁版前 |
| **M-02** | visual-director | `.claude/agents/M-02-visual-director.md` | 视觉素材 AI 提示词 | C-05 后，并行 |
| **M-03** | audio-video-director | `.claude/agents/M-03-audio-video-director.md` | 音景/视频分镜 | C-05 后，并行 |
| **M-04** | interactive-builder | `.claude/agents/M-04-interactive-builder.md` | **离线 DM 控场台 P0** | C-05 后，并行 |
| **I-01** | multimodal-auditor | `.claude/agents/I-01-multimodal-auditor.md` | 多模态一致性审计 | F-01 后，并行 |

---

## 6. 常用对话模式

### 6.1 开新本
> 我想做一个 {主题}，{类型}，{人数}

主编剧动作：
1. 调用 A-01 genre-router
2. 用 AskUserQuestion 拆 6 维度
3. 写 brief
4. 提示下一步

### 6.2 查看进度
> 现在到哪了？ / 怎么样了？

主编剧动作：
1. Read `工作区/{当前项目}/dashboard.md`
2. 给用户摘要 + 关键评分 + 下一步

### 6.3 调优某个 agent
> {agent_id} 的评分总上不去，帮我看看

主编剧动作：
1. Read 该 agent 最近若干份 trace
2. 对比评分走势
3. 提议 prompt 改动
4. 让用户审批后改 `.Codex/agents/{agent_id}.md`
5. 同步回写 `_设计包/02_agents/{agent_id}.md`

### 6.4 修订当前项目
> 第 3 幕的 char_07 描述不准，我想改

主编剧动作：
1. 询问改什么、改成什么
2. 判断是改 final（D-02/D-03 重跑）还是改 Bible（B-04 重跑链条）
3. 走 `conventions/data-contracts.md` 的修订流程
4. 在 changelog 记修订原因 + 评分 delta

---

## 7. Token 预算

| 项目大小 | 预估 tokens |
|---------|------------|
| 小本 4-5 人 demo | 200-400k |
| 标准 5-6 人本 | 400-700k |
| 大本 7-8 人本 | 700k-1.2M |

主编剧应在 dashboard 实时显示累计 token 消耗。

---

## 8. 不能做的事

- ❌ 跳过 Bible 锁版直接进 D 部门
- ❌ 让 subagent 读工作区任意文件（盲测必须 prompt inline）
- ❌ 用 LLM 判断 visibility（必须代码）
- ❌ 跳过 E-01/E-02 直接打包
- ❌ 情感向类型跳过 E-03 直接发版
- ❌ F-01 交付叙事正文里插入任务说明（"你要做/你需要"）
- ❌ 叙事正文里出现打破第四堵墙的元叙事语言
- ❌ 不写 trace
- ❌ 修了文件不写 changelog
- ❌ 把范本原文大段塞进 prompt（产权 + 上下文污染）

---

## 9. 出问题时怎么办

| 症状 | 怎么办 |
|------|--------|
| Bible 锁版后发现错 | 走 v0.x → v0.(x+1) 修订流程（见 `conventions/data-contracts.md` §3.1） |
| 盲测分数低 | 看 playtest_report 的 blockers，按 root_cause_agent 回炉 |
| 主笔一直卡（不出文本） | 检查 Bible 是否过大（>500 行需要拆 appendix）/ payload 是否完整 |
| subagent 串味（互相知道私密） | E-02 主 agent 的 session 切分逻辑出错，检查 SKILL.md |
| token 超预算 | 查 trace 找消耗最大的 agent，减少其上下文投喂 |

---

## 10. 用户偏好

- 偏好**硬核情感混合本**（v9.2 新增类型），同时要求叙事细腻和推理严密
- 盲测 pass_threshold 提高到 **8.0**（默认 7.0）；情感弧完成度不得低于 6.5
- 对民国/历史题材有研究，可在 history.md 阶段多次请求审阅
- token 预算：超出 1M tokens 单本时先停下来问用户
- Sprint 1 阶段质量门适度宽松，Sprint 2 之后收紧

---

## 11. 关键链接

- 设计包源头：`/Users/yujinping/个人与cc资料/剧本杀编剧团/04_系统架构与工具/_设计包/`
- 设计包架构总览：`_设计包/01_architecture/v9.0-architecture.md`
- 落地手册：`_设计包/06_handoff/Codex-setup.md`

---

## 12. scriptkill-team vs scriptkill-studio

| | scriptkill-team | scriptkill-studio |
|--|--|--|
| 状态 | 🔒 冻结备份 | ✅ 活跃开发 |
| 版本 | v9.6 | v10.0 |
| Agent 数 | 22 | 28 |
| 多模态 | 无 | M-01/02/03/04 + I-01 |
| DM 控场台 | 无 | ✅ 离线单 HTML |
| canonical 编译 | 手动维护 | C-05 自动编译 |

scriptkill-team 不再主动修改。新功能全部在 scriptkill-studio 开发。

---

**版本**：v10.0 / 2026-05-31
**首次配置**：2026-05-29（scriptkill-team v9.2）
**v10.0 核心变更**：多模态沉浸版架构；6 个新 agent（C-05/M-01/02/03/04/I-01）；共 28 agent；离线 DM 控场台 P0 优先级；canonical_story_state.json 自动编译；I-01 多模态一致性审计
