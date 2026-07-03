"""
C-04 数据分发器 · Distributor
把全量 details/clues 按 visibility 规则分发到每个角色的 payload。
纯代码实现，零 LLM 调用——visibility 是布尔逻辑题，不需要语义理解。
"""
import json
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_json(path: Path) -> dict | list:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def distribute(project_path: Path) -> None:
    project_path = Path(project_path)

    # ── Step 1: 读全量 ──────────────────────────────────────────────────────
    bible_path = project_path / "01_planning/bible.json"
    bible = _read_json(bible_path)
    mechanics_raw = _read_json(project_path / "02_engineering/mechanics.json")
    clues_raw = _read_json(project_path / "02_engineering/clues.json")
    details_raw = _read_json(project_path / "02_engineering/details.json")

    # 兼容顶层是 dict（含 "mechanics"/"clues"/"details" 键）或直接是列表两种格式
    mechanics = mechanics_raw.get("mechanics", mechanics_raw) if isinstance(mechanics_raw, dict) else mechanics_raw
    clues = clues_raw.get("clues", clues_raw) if isinstance(clues_raw, dict) else clues_raw
    details = details_raw.get("details", details_raw) if isinstance(details_raw, dict) else details_raw

    characters = bible["characters"]
    bible_sha = _sha256(bible_path)

    # ── Step 2: 分发（每角色一份 payload）──────────────────────────────────
    output_dir = project_path / "02_engineering/character_payloads"
    output_dir.mkdir(parents=True, exist_ok=True)

    for char in characters:
        cid = char["id"]
        payload = {
            "schema_version": "1.0",
            "char_id": cid,
            "char_name": char.get("display_name", cid),
            "generated_at": _now(),
            "source_bible_sha256": bible_sha,
            "visible_details": [
                d for d in details
                if d.get("visibility") in ("ALL", cid)
            ],
            "owned_clues": [
                c for c in clues
                if c.get("visibility") == cid
            ],
            "public_clues": [
                c for c in clues
                if c.get("visibility") == "ALL"
            ],
            "applied_mechanics": [
                m for m in mechanics
                if cid in m.get("affects", []) or "ALL" in m.get("affects", [])
            ],
            "personal_props": char.get("personal_props", []),
        }
        _write_json(output_dir / f"{cid}.json", payload)

    # ── Step 3: 强制断言检查 ────────────────────────────────────────────────
    errors = _run_assertions(characters, details, output_dir)

    # ── Step 4: 输出分发报告 ────────────────────────────────────────────────
    _write_report(project_path, bible, characters, details, clues, mechanics, errors)

    if errors:
        print(f"❌ 分发完成，但有 {len(errors)} 条断言错误，请检查 distribution_report.md")
        for e in errors:
            print(f"  · {e}")
        sys.exit(1)
    else:
        print(f"✅ 分发完成，共 {len(characters)} 个角色 payload，断言全部通过")
        print(f"   报告：{project_path / '02_engineering/distribution_report.md'}")


def _run_assertions(characters: list, details: list, output_dir: Path) -> list[str]:
    """
    返回错误信息列表。列表为空表示全通过。

    断言 1：互斥检查——A 的私密细节不能出现在 B 的 payload 里。
    断言 2：完整性检查——每条 visibility != "ALL" 的细节必须分到对应角色。
    """
    errors = []

    # 读所有已生成的 payload
    payloads = {}
    for char in characters:
        cid = char["id"]
        p_path = output_dir / f"{cid}.json"
        if p_path.exists():
            payloads[cid] = _read_json(p_path)

    # 断言 1：互斥检查
    for c_a in characters:
        pa = payloads.get(c_a["id"], {})
        private_ids_a = {
            d["id"] for d in pa.get("visible_details", [])
            if d.get("visibility") == c_a["id"]
        }
        for c_b in characters:
            if c_a["id"] == c_b["id"]:
                continue
            pb = payloads.get(c_b["id"], {})
            detail_ids_b = {d["id"] for d in pb.get("visible_details", [])}
            leaked = private_ids_a & detail_ids_b
            for did in leaked:
                errors.append(
                    f"[互斥越权] 细节 {did} 属于 {c_a['id']} 但出现在 {c_b['id']} 的 payload"
                )

    # 断言 2：完整性检查
    for d in details:
        vis = d.get("visibility")
        if vis and vis != "ALL":
            owner_payload = payloads.get(vis, {})
            owner_ids = {x["id"] for x in owner_payload.get("visible_details", [])}
            if d["id"] not in owner_ids:
                errors.append(
                    f"[完整性丢失] 细节 {d['id']} 应属于 {vis} 但未出现在其 payload"
                )

    return errors


def _write_report(
    project_path: Path,
    bible: dict,
    characters: list,
    details: list,
    clues: list,
    mechanics: list,
    errors: list[str],
) -> None:
    output_dir = project_path / "02_engineering/character_payloads"
    lines = [
        "# C-04 分发报告",
        f"\n生成时间：{_now()}",
        f"\nBible 版本：{bible.get('version', 'unknown')} · 项目：{bible.get('project_name', '未命名')}",
        "\n---\n",
        "## 每角色分配概览\n",
        "| 角色 ID | 角色名 | 私密细节 | 公共细节 | 私密线索 | 公共线索 | 受影响机制 |",
        "|---------|--------|---------|---------|---------|---------|---------|",
    ]

    total_private = 0
    total_public_d = 0

    for char in characters:
        cid = char["id"]
        p_path = output_dir / f"{cid}.json"
        if not p_path.exists():
            lines.append(f"| {cid} | {char.get('display_name','')} | ❌ payload 缺失 | | | | |")
            continue
        p = _read_json(p_path)
        priv_d = sum(1 for d in p["visible_details"] if d.get("visibility") == cid)
        pub_d = sum(1 for d in p["visible_details"] if d.get("visibility") == "ALL")
        owned_c = len(p["owned_clues"])
        pub_c = len(p["public_clues"])
        mech_n = len(p["applied_mechanics"])
        total_private += priv_d
        total_public_d = pub_d  # 公共细节每人相同，取最后一次即可
        lines.append(
            f"| {cid} | {char.get('display_name','')} | {priv_d} | {pub_d} | {owned_c} | {pub_c} | {mech_n} |"
        )

    # 均衡性检查（私密细节偏差警告）
    if characters:
        private_counts = []
        for char in characters:
            p_path = output_dir / f"{char['id']}.json"
            if p_path.exists():
                p = _read_json(p_path)
                cnt = sum(1 for d in p["visible_details"] if d.get("visibility") == char["id"])
                private_counts.append(cnt)
        if private_counts and max(private_counts) > 0:
            ratio = max(private_counts) / max(sum(private_counts) / len(private_counts), 1)
            if ratio > 2.5:
                lines.append(
                    f"\n⚠️ **均衡警告**：最多私密细节角色是平均值的 {ratio:.1f} 倍，建议检查信息量分布。"
                )

    lines.append(f"\n---\n\n## 全局统计\n")
    lines.append(f"- 角色总数：{len(characters)}")
    lines.append(f"- 细节总数：{len(details)}（公共 {total_public_d} + 私密 {total_private}）")
    lines.append(f"- 线索总数：{len(clues)}")
    lines.append(f"- 机制总数：{len(mechanics)}")

    lines.append(f"\n---\n\n## 断言检查结果\n")
    if errors:
        lines.append(f"❌ 共 {len(errors)} 条错误：\n")
        for e in errors:
            lines.append(f"- {e}")
    else:
        lines.append("✅ 互斥检查：通过")
        lines.append("✅ 完整性检查：通过")

    report_path = project_path / "02_engineering/distribution_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 distributor.py <project_path>")
        sys.exit(1)
    distribute(Path(sys.argv[1]))
