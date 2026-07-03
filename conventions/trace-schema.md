# Trace Schema

> 每个 agent 一次调用必须写一份 trace。trace 是可观测性的第一层（详见 `01_architecture/v9.1-observability-addendum.md`）。

## 1. 文件路径

```
_工作区/{项目名}/_trace/{ISO8601}_{agent_id}_{action}.json
```

实际写盘时把 `:` 替换为 `-` 防 Windows 兼容问题：
```
_trace/2026-05-28T10-30-15Z_E-02_blind-playtest.json
```

## 2. JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Trace",
  "type": "object",
  "required": [
    "schema_version", "trace_id", "agent_id", "agent_name",
    "action", "project_name", "started_at", "ended_at",
    "duration_seconds", "status", "tokens_used"
  ],
  "properties": {
    "schema_version": { "const": "1.0" },
    "trace_id":       { "type": "string", "description": "uuid v4" },
    "agent_id":       { "type": "string", "pattern": "^[A-F]-\\d{2}$" },
    "agent_name":     { "type": "string" },
    "action":         { "type": "string", "description": "具体动作，如 build_bible / draft_act2_char01" },
    "params":         { "type": "object", "description": "调用参数，便于复现" },

    "project_name":   { "type": "string" },
    "started_at":     { "type": "string", "format": "date-time" },
    "ended_at":       { "type": "string", "format": "date-time" },
    "duration_seconds": { "type": "number" },

    "status": {
      "type": "string",
      "enum": ["success", "fail", "warn", "pending_revision"]
    },
    "error": {
      "type": ["object", "null"],
      "properties": {
        "code":    { "type": "string" },
        "message": { "type": "string" }
      }
    },
    "warnings": {
      "type": "array",
      "items": { "type": "string" }
    },

    "tokens_used": {
      "type": "object",
      "properties": {
        "input":  { "type": "integer" },
        "output": { "type": "integer" },
        "total":  { "type": "integer" }
      }
    },

    "input_refs":  { "type": "array", "items": { "type": "string" }, "description": "本次调用读取的文件相对路径" },
    "output_refs": { "type": "array", "items": { "type": "string" }, "description": "本次调用写入的文件相对路径" },

    "scores": {
      "type": ["object", "null"],
      "description": "仅 QA agent 填",
      "properties": {
        "overall_score": { "type": "number", "minimum": 0, "maximum": 10 },
        "passed":        { "type": "boolean" },
        "see":           { "type": "string", "description": "完整报告路径" }
      }
    },

    "agent_specific_metrics": {
      "type": "object",
      "description": "各 agent 自定义的关键指标，如 D-02 的 word_count / D-03 的 voice_compliance_score / C-04 的 mutex_check 等"
    },

    "subagents_invoked": {
      "type": "array",
      "items": { "type": "string" },
      "description": "如果本次调用启动了 subagent，列出来"
    },

    "parent_trace_id": {
      "type": ["string", "null"],
      "description": "如果本次是 subagent 调用，指向父 trace"
    },

    "bible_sha256_at_run": {
      "type": ["string", "null"],
      "description": "运行时 Bible 的 sha256，便于检测 Bible 改版后哪些 trace 已过期"
    }
  }
}
```

## 3. 必填 vs 选填字段

**必填**：schema_version / trace_id / agent_id / agent_name / action / project_name / started_at / ended_at / duration_seconds / status / tokens_used

**强烈推荐**：input_refs / output_refs

**按情况选填**：error（status=fail 时必填）/ warnings / scores（QA agent 必填）/ agent_specific_metrics / subagents_invoked / parent_trace_id / bible_sha256_at_run

## 4. 各 agent 的 agent_specific_metrics 推荐字段

| Agent | 推荐字段 |
|-------|---------|
| A-01 | questions_asked, dimensions_locked |
| A-02 | references_scanned, references_matched, match_method |
| A-03 | directories_scanned, cards_generated, by_completeness |
| B-01 | generations, characters_in_tree, hidden_blood_relations |
| B-02 | topology, truth_layers, physical_constraints_count |
| B-03 | total_acts, reveal_hide_conflicts |
| B-04 | bible_lines, appendix_lines, self_check_passed, user_approved, bible_version |
| C-01 | mechanics_count, all_have_constraints, unbalanced_mechanics |
| C-02 | total_clues, public_clues, private_clues, misleading_clues, coverage_per_truth_layer |
| C-03 | total_details, by_type, by_visibility, orphan_details |
| C-04 | characters_processed, mutex_check, completeness_check, balance_warnings |
| D-01 | characters_processed, double_identity_count, all_have_breaking_point |
| D-02 | word_count, must_reveal_met, must_hide_violated, details_planted, clues_planted |
| D-03 | draft_words, final_words, voice_card_compliance_score, details_preserved |
| E-01 | scores.overall_score, blockers_count, blockers_high/medium/low |
| E-02 | scores.overall_score, subagents_launched, blockers_count, estimated_overall_after_all_fixes |
| F-01 | deliverables (object: 角色本/DM手册/... 数量), total_word_count, qa_gate_status |

## 5. 主编剧 agent 的责任

每次 invoke 任一 agent 时：
1. 生成 `trace_id` (uuid v4)
2. 记录 `started_at`
3. 调用 agent
4. 接收 agent 返回
5. 记录 `ended_at`
6. 整合所有字段写盘到 `_trace/`
7. 同步更新 `dashboard.md`

## 6. trace 文件不可修改

写完即只读。如果要修订只能写新 trace。这样能保证历史完整性。

## 7. 跨项目分析

每个项目的 `_trace/` 永久保留（用户拍板）。未来可以批量分析：
- 同一 agent 在不同项目的失败模式分布
- 某 prompt 调优前后的评分差异
- 平均 token 消耗趋势

详见 `06_handoff/` 中的"跨项目学习库"实现建议。

---
**版本**：v9.1 / 2026-05-28
