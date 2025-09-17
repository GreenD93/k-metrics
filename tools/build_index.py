import json, yaml, argparse, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256_file(p: Path):
    if not p or not p.exists(): return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_items(base_dir: str, kind: str):
    out = []
    for y in (ROOT / base_dir).rglob("*.yaml"):
        with open(y, encoding="utf-8") as f:
            obj = yaml.safe_load(f) or {}
        # 공통 정규화
        sql_rel = obj.get("sql")
        sql_path = (y.parent / sql_rel) if sql_rel else None
        title = obj.get("title") or obj.get("name") or y.stem
        tags = obj.get("tags") or obj.get("keywords") or []

        item_full = {
            "id": obj.get("id"),
            "kind": kind,
            "title": title,
            "description": obj.get("description", ""),
            "contacts": obj.get("contacts"),
            "time_grains": obj.get("time_grains"),
            "entity_grain": obj.get("entity_grain"),
            "rollup_dimensions": obj.get("rollup_dimensions"),
            "depends_on_models": obj.get("depends_on_models"),
            "tags": tags,
            "parameters": obj.get("parameters"),
            "sql": sql_rel,
            "versions": obj.get("versions"),
            "_source": str(y.relative_to(ROOT)),
            "_sql_path": str(sql_path.relative_to(ROOT)) if sql_path else None,
            "_sql_sha256": sha256_file(sql_path) if sql_path else None,
        }

        # lite 뷰
        text = " ".join(filter(None, [
            item_full["id"] or "",
            str(title),
            item_full["description"] or "",
            " ".join(tags) if tags else "",
            kind
        ]))
        item_lite = {
            "id": item_full["id"],
            "kind": kind,
            "title": str(title),
            "description": item_full["description"] or "",
            "tags": tags,
            "text": " ".join(text.split()),            # 공백 정리
            "path_yaml": item_full["_source"],
            "path_sql": item_full["_sql_path"],
        }

        out.append((item_full, item_lite))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=str(ROOT / "build"))
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(exist_ok=True)

    all_full, all_lite = [], []

    for base_dir, kind in [("metrics", "metric"), ("queries", "query")]:
        for full, lite in load_items(base_dir, kind):
            # id 없는 항목은 스킵(최소 보정)
            if not full["id"]:
                continue
            all_full.append(full)
            all_lite.append(lite)

    (outdir / "registry_full.json").write_text(
        json.dumps(all_full, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (outdir / "search_lite.json").write_text(
        json.dumps(all_lite, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"FULL: {len(all_full)}  LITE: {len(all_lite)} → {outdir}/")

if __name__ == "__main__":
    main()
