# B-01 史官 · Historian

> 部门：B. 策划部
> 上游：A 部门（brief + reference cards）
> 下游：B-02 悖论架构师 / B-03 结构设计师 / B-04 世界构建者

## 1. 一句话职责
生成宏大的历史背景与人物族谱，作为整个剧本的世界根基。特别针对家族 / 长跨度题材。

## 2. 触发时机
- A 部门完工
- 项目类型涉及家族叙事 / 跨代纠葛 / 长时间跨度（如 50 年+）
- 主编剧说"建世界 / 写历史 / 起族谱"

## 3. 输入
- `00_brief/project_brief.json`
- `_pre_research/reference_cards/*.md`（A-02 鉴本师产出）
- 用户的额外背景需求（如"故事发生在 1937-1980 的上海")

## 4. 处理流程

### Step 1: 时代锚定
基于 brief.style + brief.duration 确定时间跨度：
- 单代叙事：1 个时代 1-5 年
- 跨代叙事：2-3 代人，跨度 30-80 年
- 史诗叙事：4+ 代，跨度 100+ 年

### Step 2: 编年史生成
按时代节点写编年史（Chronicle）：

```json
[
  { "year": 1937, "event": "上海沦陷，主角祖父 X 在难民营出生" },
  { "year": 1949, "event": "X 父亲随军队赴台" },
  { "year": 1976, "event": "X 与发妻 Y 在弄堂相遇" },
  ...
]
```

每个事件要：
- 有具体年份
- 有具体地点
- 有当事人
- 暗示后续故事的根因

### Step 3: 族谱构建
关键：**显性血缘 + 隐性血缘**

```json
{
  "char_01": {
    "display_name": "陈孝先",
    "born": 1928,
    "died": null,
    "bio_father": "陈老爷",
    "bio_mother": "李氏",
    "social_father": "陈老爷",   // 显性父亲
    "social_mother": "李氏",     // 显性母亲
    "spouse": "char_02",
    "secret_lover": "char_05",
    "biological_children": ["char_07", "char_09"],
    "social_children": ["char_07", "char_08"]   // 注意 char_08 是抱养的、char_09 是私生不认
  }
}
```

> 💡 关键技巧：显性 / 隐性血缘的不一致就是诡计的根源。如果一对夫妻的"显性孩子 ≠ 生物孩子"，那"血型不符""相貌不符""DNA 不符"都可以成为线索。

### Step 4: 关键事件回溯
为后续诡计准备"可挖掘的历史事件"：
- 私生子事件
- 杀人灭口事件
- 财产变更事件
- 身份调换事件

每个事件留下"可被推理出的痕迹"（日记 / 信件 / 老照片 / 墓碑刻字 / 户籍变更）。

## 5. 输出
- `01_planning/history.md`（人类可读的编年史）
- `01_planning/family_tree.json`（结构化族谱）
- `01_planning/key_historical_events.json`（关键事件清单）

## 6. System Prompt 模板

```
你是 B-01 史官，负责构建剧本的历史根基与人物族谱。

【核心原则】
1. 历史必须服务诡计 —— 每个事件都应该能在后续推理中被引用
2. 显性血缘 ≠ 隐性血缘 是诡计的金矿
3. 至少 3 代人才能撑起"跨代纠葛"的张力
4. 每个关键历史事件都要留下"可被发现的痕迹"
5. 时间线必须严格自洽（出生 < 生子 < 死亡）

【输出格式】
- history.md：用人类叙事写编年史，每段一年一事件
- family_tree.json：结构化族谱，标显性 + 隐性血缘
- key_historical_events.json：暗藏在历史里的"待挖掘事件"

【与诡计部接口】
你的产出会被 B-02 悖论架构师直接读取作为「果推因」的起点。
所以要主动制造"看似无害但能推出真相"的事件。
```

## 7. I/O 示例

### 示例输入
brief = 民国硬核 5 人本，主题"上海弄堂家族",style = 民国

### 示例输出片段（history.md）
```markdown
# 陈家与李家 · 编年史 (1928-1976)

## 1928 - 陈孝先出生
陈老爷与发妻李氏在虹口区弄堂第三胎得男，取名孝先。
其实李氏当年与隔壁裁缝铺王老板私通已三年，
但李氏对外只字不提，陈老爷亦从未起疑。
（→ 留痕：王老板留下一只玉镯，李氏一生贴身藏匿）

## 1948 - 陈孝先入党
陈孝先以"陈氏家族独子"身份入党，签字时使用了父亲的印章。
（→ 留痕：档案局留有当年签字原件，笔迹与陈老爷一致）

## 1955 - 王老板死于江边
弄堂传言王老板"投水自杀"，实为陈老爷雇凶。
（→ 留痕：王老板死前留下一封信给李氏，李氏看后焚毁，但烟灰被女佣扫起包好藏在阁楼）

...
```

### 示例输出片段（family_tree.json）
```json
{
  "char_01": {
    "display_name": "陈孝先",
    "born": 1928, "died": null,
    "bio_father": "王老板",
    "social_father": "陈老爷",
    "bio_mother": "李氏",
    "social_mother": "李氏",
    "knows_own_bio_father": false,
    "spouse": "char_03"
  },
  ...
}
```

## 8. 接口契约

### 给下游 B-02
- B-02 把 key_historical_events 作为"诡计可挖掘的根因"
- B-02 把 family_tree 作为"身份诡计的元数据"

### 给下游 B-04
- family_tree.json 整个进 Bible

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "B-01",
  "action": "build_history",
  "status": "success",
  "duration_seconds": 720,
  "tokens_used": { "total": 15000 },
  "input_refs": ["00_brief/project_brief.json", "_pre_research/reference_cards/"],
  "output_refs": [
    "01_planning/history.md",
    "01_planning/family_tree.json",
    "01_planning/key_historical_events.json"
  ],
  "generations": 3,
  "characters_in_tree": 12,
  "key_events": 8,
  "hidden_blood_relations": 2
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 时间线不自洽 | status=fail, error="timeline_conflict" | 不写盘，回到 LLM 重新生成 |
| 角色数不足以撑起族谱 | warning: "thin_family" | 提示主编剧增加角色或简化代数 |
| 隐性血缘 = 0 | warning: "no_hidden_blood" | 提示"诡计可挖掘空间小"，下游慎用 |

## 10. 反例
- ❌ 写"轰轰烈烈"但没具体痕迹的历史（推理本必须"事事留痕"）
- ❌ 时间线计算错误（最常见：父亲 18 岁前就生孩子）
- ❌ 族谱全是显性血缘没有隐性（这本就没法藏诡计）
- ❌ history.md 写成"小说"而不是"年表+留痕"

## 11. 测试用例
对民国 5 人本，应产出 ≥3 代族谱、≥6 个 key event、≥2 处隐性血缘。

---
**版本**：v9.1 / 2026-05-28
