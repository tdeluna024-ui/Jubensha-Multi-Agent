---
name: distributor
description: 数据分发器。把全量 details / clues 按 visibility 规则切分到每个角色的 payload。当用户/主编剧说"分发线索 / 切 payload / 进入工程部最后一步"时触发。⚠️ 这是纯代码 skill，逻辑不能交给 LLM 推断——LLM 判断权限失败率极高，是 v8.0/v9.0 系统稳定性的核心。
tools: Read, Write, Bash
---

# Skill: distributor (数据分发器) 🔒 纯代码

## 设计哲学

**这是整个团队唯一一个明文规定"必须用代码"的 skill。**

不是不信任 LLM，是因为「visibility 判断」是布尔逻辑题，不需要语义理解。让 LLM 判断 50+ 条细节的 visibility 会出 5-10% 的错——而错一条就可能让玩家拿到本来不该看到的信息，从而让整本崩盘。

代码判断错误率 = 0。

## 何时触发

- C-01 / C-02 / C-03 都已产出
- 必备文件齐全：
  - `02_engineering/mechanics.json`
  - `02_engineering/clues.json`
  - `02_engineering/details.json`
  - `01_planning/bible.json` （需要角色列表）

## 核心目标

为每个角色生成一份 `character_payloads/{char_id}.json`，包含且仅包含该角色应该看到的：
- 私密细节（visibility = 自己）
- 公共细节（visibility = "ALL"）
- 该角色掌握的线索
- 该角色受到的机制约束（ability + constraint）

## 操作流程（纯算法）

### Step 1: 读全量

```python
bible = read_json("01_planning/bible.json")
mechanics = read_json("02_engineering/mechanics.json")
clues = read_json("02_engineering/clues.json")
details = read_json("02_engineering/details.json")

characters = bible["characters"]  # list of {"id": "char_01", ...}
```

### Step 2: 分发（每角色一遍）

```python
for char in characters:
    payload = {
        "schema_version": "1.0",
        "char_id": char["id"],
        "char_name": char["display_name"],
        "generated_at": now(),
        "source_bible_sha256": bible_sha,

        # 细节：visibility 是 "ALL" 或 char.id
        "visible_details": [
            d for d in details
            if d["visibility"] == "ALL" or d["visibility"] == char["id"]
        ],

        # 线索：visibility = char.id 表示私密归属
        "owned_clues": [
            c for c in clues
            if c.get("visibility") == char["id"]
        ],

        # 公共线索单独列（玩家都能看）
        "public_clues": [
            c for c in clues
            if c.get("visibility") == "ALL"
        ],

        # 机制：affects 该角色 或 affects "ALL"
        "applied_mechanics": [
            m for m in mechanics
            if char["id"] in m.get("affects", []) or "ALL" in m.get("affects", [])
        ],

        # 角色专属道具的引用（这些道具会在 F-01 打包阶段生成实物图文）
        "personal_props": char.get("personal_props", []),
    }

    write_json(f"02_engineering/character_payloads/{char['id']}.json", payload)
```

### Step 3: 强制断言检查

```python
# 1. 互斥检查：A 的私密细节不能出现在 B 的 payload 里
for c_a in characters:
    pa = read_payload(c_a)
    for c_b in characters:
        if c_a == c_b: continue
        pb = read_payload(c_b)
        for d in pa["visible_details"]:
            if d["visibility"] == c_a["id"] and d in pb["visible_details"]:
                raise Error(f"私密细节越权：{d['id']} 既属于 {c_a} 又出现在 {c_b}")

# 2. 完整性检查：每条 visibility != "ALL" 的细节必须分到对应角色
for d in details:
    if d["visibility"] != "ALL":
        owner_payload = read_payload(d["visibility"])
        assert d in owner_payload["visible_details"], f"细节 {d['id']} 丢失"
```

### Step 4: 输出分发报告

```
02_engineering/distribution_report.md
```

报告内容：
- 每个角色拿到了多少条细节 / 多少条线索 / 多少条机制
- 公共/私密比例
- 角色间分配均衡度（如果有角色拿到 80% 信息、其他角色只有 10%，需要警告）
- 自检通过/失败明细

## 输入 / 输出

### Input
- `01_planning/bible.json`
- `02_engineering/mechanics.json`
- `02_engineering/clues.json`
- `02_engineering/details.json`

### Output
- `02_engineering/character_payloads/{char_id}.json` × N
- `02_engineering/distribution_report.md`

## 与其他 skill 的协作

| 上游 | 调用方 | 下游 |
|------|--------|------|
| C-01/C-02/C-03 产物 + Bible | 主编剧 agent | D 部门所有 agent（按角色读取自己的 payload） |

## 重分发触发条件

`distributor` 会被多次调用，触发条件：

1. **首次分发**：工程部首次完工
2. **盲测后重分发**：E-02 报告"角色 X 拿不到关键线索" → 改 details/clues 的 visibility → 重跑 distributor
3. **Bible 修订后重分发**：Bible 从 v0.1 → v0.2 改了角色定义 → 必须全部重跑

## 实现技术栈

- 语言：Python 3.10+
- 依赖：`json`, `hashlib`, `pathlib`（全部标准库，零外部依赖）
- 运行：通过 Bash 工具 `python3 distributor.py {project_path}`

## 反例（绝不能做）

- ❌ 用 LLM 判断 "这条细节 char_03 该不该看到"
- ❌ 把 visibility 字段省略，让 LLM 自己读上下文判断
- ❌ 分发完不跑断言检查就交付下游
- ❌ 在 payload 里夹带 "供 LLM 参考的额外背景" —— payload 必须严格等于"该角色应得材料"

## 测试用例

参见 `02_agents/C-04-distributor.md` 的"示例 I/O"段落（批 2 交付）。

---

**优先级**：P0（系统稳定性核心）
**预估实现工时**：1 天（核心算法 1 小时 + 边界 case + 报告生成）
**对应 Agent 规格书**：`02_agents/C-04-distributor.md`
