# C-04 数据分发器 · Distributor 🔒 纯代码

> 部门：C. 工程部
> 上游：C-01 mechanics + C-02 clues + C-03 details + Bible
> 下游：D 部门所有 agent
> 对应 skill：`03_skills/distributor/SKILL.md`

## 1. 一句话职责
按 visibility 规则把 mechanics / clues / details 切分到每个角色的 payload。**必须用代码实现，不能交给 LLM**。

## 2. 触发时机
- C-01 / C-02 / C-03 都已产出
- Bible 锁版
- 主编剧说"分发 / 切 payload / 进入工程部最后一步"
- 任何修订需要重分发时

## 3. 输入
- `01_planning/bible.json`
- `02_engineering/mechanics.json`
- `02_engineering/clues.json`
- `02_engineering/details.json`

## 4. 处理流程（纯算法，见 SKILL.md 详解）

简化版：
```python
for char in bible["characters"]:
    payload = {
        "char_id": char["id"],
        "visible_details": [d for d in details if d["visibility"] in ("ALL", char["id"])],
        "owned_clues": [c for c in clues if c.get("visibility") == char["id"]],
        "public_clues": [c for c in clues if c.get("visibility") == "ALL"],
        "applied_mechanics": [m for m in mechanics if char["id"] in m["affects"] or "ALL" in m["affects"]],
    }
    write_json(f"02_engineering/character_payloads/{char['id']}.json", payload)
```

> ⚠️ **约定**：clues 与 details 一样，都用 `visibility` 字段（值为 `"ALL"` 或 `char_XX`）。**不要**用 `assigned_to`——v9.1 已统一收敛到 `visibility`。

### 强制断言（不允许跳过）
1. **互斥**：A 的私密 ∉ B 的 payload
2. **完整**：每条 non-ALL detail/clue 一定在对应角色的 payload 里
3. **数量校验**：每个角色的 payload ≥ M 条（M 是项目最小阈值）

## 5. 输出
- `02_engineering/character_payloads/{char_id}.json` × N
- `02_engineering/distribution_report.md`

## 6. 实现要求（不是 prompt，是代码规范）

- 语言：Python 3.10+
- 依赖：仅标准库 (json, hashlib, pathlib)
- 入口：`python3 distributor.py {project_path}`
- 异常：分发失败必须 raise，不能 silent fail
- 日志：每个角色的分发结果写到 distribution_report.md

## 7. I/O 示例

### 示例输出 char_01 payload（节选）
```json
{
  "schema_version": "1.0",
  "char_id": "char_01",
  "char_name": "陈孝先",
  "generated_at": "2026-05-28T10:00:00Z",
  "source_bible_sha256": "f3e2a8b9...",

  "visible_details": [
    {"id": "d_001", "content": "弄堂下雪傍晚总有钟声", "visibility": "ALL"},
    {"id": "d_023", "content": "陈孝先口袋里有半块怀表", "visibility": "char_01"}
  ],

  "owned_clues": [
    {"id": "c_001", "content": "陈孝先的工作证", "visibility": "ALL", "act_introduced": 2}
  ],

  "public_clues": [
    {"id": "c_010", "content": "案件报告：死亡时间 21:00-22:00", "visibility": "ALL"}
  ],

  "applied_mechanics": [
    {"id": "m_02", "name": "真言纸", "ability": "...", "constraint": "..."}
  ],

  "personal_props": ["怀表（已破损半块）", "工作证"]
}
```

### 示例输出 distribution_report.md
```markdown
# Distribution Report · v0.1

## 整体
- 角色数：5
- 总 details：65 (公共 15 / 私密 50)
- 总 clues：58 (公共 22 / 私密 36)
- 总 mechanics：4

## 按角色
| 角色 | 私密 details | 私密 clues | applied mechanics | payload 行数 |
|------|------------|----------|------------------|------------|
| char_01 | 10 | 7 | 2 | 142 |
| char_02 | 9 | 8 | 1 | 138 |
| char_03 | 11 | 6 | 2 | 145 |
| char_04 | 8 | 8 | 1 | 130 |
| char_05 | 12 | 7 | 2 | 150 |

## 自检
✅ 互斥检查通过 (0 越权)
✅ 完整性检查通过 (0 丢失)
✅ 最小阈值通过 (最少 8 / 阈值 5)

## 均衡度警告
⚠️ char_04 私密 details = 8（最少），均值 10。建议补 2 条。
```

## 8. 接口契约

### 给下游 D 部门
- D-01/D-02/D-03 只读自己的 payload，不读其他角色的
- payload 是单一信息源，不再读 mechanics/clues/details 原始文件

### 重分发触发
- E-02 盲测发现某角色信息不足
- Bible 修订（v0.x → v0.y）
- 用户手动修改 visibility

## 9. Observability

### Trace 模板
```json
{
  "agent_id": "C-04",
  "action": "distribute",
  "status": "success",
  "duration_seconds": 3,
  "tokens_used": { "total": 0 },
  "input_refs": ["bible.json", "mechanics.json", "clues.json", "details.json"],
  "output_refs": ["character_payloads/", "distribution_report.md"],
  "characters_processed": 5,
  "total_distributions": 127,
  "mutex_check": "pass",
  "completeness_check": "pass",
  "min_threshold_check": "pass",
  "balance_warnings": ["char_04_below_avg"]
}
```

### 失败模式
| 模式 | trace 标注 | 处理 |
|------|-----------|------|
| 互斥违反（A 的私密进了 B） | status=fail, error="mutex_violation" | 必须修上游 visibility |
| 完整性违反（某 detail 谁都没拿到） | status=fail, error="orphan_detail" | 必须修上游 |
| 某角色信息严重不足 | warning: "thin_payload" | 提示补 details |

## 10. 反例（绝不能做）
- ❌ 用 LLM 判断 visibility（必须代码）
- ❌ 在 payload 里"夹带"非该角色的信息（哪怕是为了"上下文")
- ❌ 自检失败但写盘
- ❌ 分发完不写 distribution_report

## 11. 测试用例
对 5 人本，应在 < 5 秒内完成分发，5 个 payload 文件齐全，distribution_report 包含完整自检。

---
**版本**：v9.1 / 2026-05-28
**实现优先级**：P0
