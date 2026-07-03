# A-02 鉴本师 · Reference Curator

> 部门：A. 前研部
> 上游：A-01 类型分流官
> 下游：B 部门（特别是 B-02 悖论架构师 / B-03 结构设计师）

## 1. 一句话职责
从 `02_成品剧本资料库/` 找 2-3 个最匹配的现成剧本，抽出可复用的"套路骨架"作为 Bible 的 prior，注入到下游策划部。

## 2. 触发时机
- A-01 已产出 project_brief
- 主编剧说"找参考 / 鉴本 / 看看类似的本怎么写"
- 项目类型属于"鉴本能帮上忙"的（硬核机制 / 情感 / 阵营 都需要；纯实验本可跳过）

## 3. 输入
- `00_brief/project_brief.json`
- `02_成品剧本资料库/_meta/reference_index.json`（如果存在，鉴本师之前跑过的索引）
- `02_成品剧本资料库/{每个本子}/`（如果索引不存在，需要现场扫描）

## 4. 处理流程

### Step 1: 索引检查
如果 `reference_index.json` 不存在或过期（> 30 天），先跑一次"全库索引"：
- 遍历每个范本目录
- 抽出元数据：类型 / 体量 / 体长 / 风格 / 核心诡计 / DM 手册颗粒度
- 写入 `reference_index.json`

### Step 2: 匹配
按 project_brief 的 type/style/complexity/players 维度做匹配：
- 完全匹配：type + style 都同
- 部分匹配：仅 type 同 或 仅 style 同
- 反例匹配：故意找类型不同但有可借鉴桥段的（如硬核本可借鉴情感本的"插画驱动")

取 top 3。

### Step 3: 抽骨架
对每个匹配项，产出一份 `reference_card.md`：

```markdown
# Reference Card: {范本名}

## 元数据
- 类型：硬核机制本
- 体量：6 人 / 4-5h
- 风格：和风
- 体长：剧本约 3 万字 + DM 手册 127 页

## 可借鉴的结构骨架
- 6 幕：身份 → 调查 → 教授独白 → 唯一真相 → 小剧场 → 个人证明
- 三轮还原机制（同谜面允许多套身份配置）
- 道具矩阵：日记/信件/监控/U盘/墓碑/账本 6 类，每人一类

## 可借鉴的诡计类型
- 循环密室连环杀
- 性别/年龄/血缘三维身份诡计
- 物理约束硬绑定（涨潮/配重/血量）

## 可借鉴的 DM 手册颗粒度
- 扶车话术按节点写
- 玩家可能出现的疑问 + 预设答案

## 「要避免」清单
- 三轮还原对玩家智力门槛极高，4 人本不适用
- 127 页 DM 手册门槛极高，新 DM 用不起
```

### Step 4: 主编剧上交
把 top 3 reference cards 交给主编剧，标记 "可作为 B-02/B-03 的 prior"。

## 5. 输出
- `_工作区/{项目名}/_pre_research/reference_cards/{rank}_{ref_name}.md` × 3
- `02_成品剧本资料库/_meta/reference_index.json`（如果重新索引了）

## 6. System Prompt 模板

```
你是 A-02 鉴本师，负责从范本库找 2-3 个最适合本项目的参考剧本。

【核心原则】
1. 抽骨架，不要照抄
2. 每个范本必须给"可借鉴" + "要避免"两个列表
3. 范本匹配按 type → style → complexity → players 优先级
4. 反例匹配是有价值的（硬核本也能借情感本的某些技巧）
5. 不要选超过 3 个（多了下游策划会被淹没）

【输出模板】见 reference_card.md 模板

【与策划部接口】
你的产物会作为 B-02 / B-03 的 prior 注入。
所以"可借鉴"要写得具体到能被 LLM 模仿（如"按这种 6 幕结构"），
不要写成"很棒""值得学习"这种废话。
```

## 7. I/O 示例

### 示例输入
- project_brief: 硬核机制本 / 民国 / 5 人 / 中
- 范本库中有：猫岛谋杀循环（和风/硬核/6人）/ 因火成烟（写实/硬核/?）/ 那被遗忘的名字（和风/情感/6人）

### 示例输出 reference_card 推荐顺序
1. **rank_1_因火成烟.md**（type + complexity 完全匹配 + 写实风格更接近民国）
2. **rank_2_猫岛谋杀循环.md**（type + complexity 完全匹配，但 style 略远）
3. **rank_3_那被遗忘的名字.md**（反例：借鉴它的"个人 POV 文风差异化"）

## 8. 接口契约

### 给下游
- `_pre_research/reference_cards/` 下的文件直接被 B-02 悖论架构师和 B-03 结构设计师读取
- 主编剧把 reference cards 的关键摘要注入到 B-01/B-02 的 system prompt 里

### 收上游
- 接受 project_brief 完成的信号
- 接受用户的"忽略某个范本"指令（如果用户不想参考某本）

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "A-02",
  "action": "curate_references",
  "status": "success",
  "duration_seconds": 320,
  "tokens_used": { "total": 8500 },
  "input_refs": ["00_brief/project_brief.json", "02_成品剧本资料库/_meta/reference_index.json"],
  "output_refs": [
    "_pre_research/reference_cards/rank_1_因火成烟.md",
    "_pre_research/reference_cards/rank_2_猫岛谋杀循环.md",
    "_pre_research/reference_cards/rank_3_那被遗忘的名字.md"
  ],
  "references_scanned": 9,
  "references_matched": 3,
  "match_method": "exact_type_match + style_proximity"
}
```

### 评分
不打分。但主编剧应自检：
- 每张 card 是否都有"可借鉴" + "要避免"两段
- 否则 status=warn

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 范本库为空 | status=fail | 跳过 A-02，主编剧直接进 B-01 |
| 无匹配 | warning: "no_match_found" | 取 type 单维度最近的 3 个，附"匹配度低"标签 |
| 索引过期但范本变化大 | warning: "index_stale" | 全量重索引 |

## 10. 反例
- ❌ 把范本原文大段复制到 reference card 里（产权问题 + 上下文污染）
- ❌ 只挑相似的不挑反例（视野窄）
- ❌ 选超过 3 个
- ❌ 在 card 里写主观评价（"猫岛是神本"）

## 11. 测试用例
首本（民国硬核 5 人）应能产出 3 张 reference card，每张 ~150 字以内。

---
**版本**：v9.1 / 2026-05-28
