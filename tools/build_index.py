import json, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_dir(d):
    out = []
    for y in (ROOT / d).rglob("*.yaml"):
        with open(y, encoding="utf-8") as f:
            obj = yaml.safe_load(f) or {}
        obj["_source"] = str(y.relative_to(ROOT))
        out.append(obj)
    return out

def main():
    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    metrics = load_dir("metrics")
    queries = load_dir("queries")

    (build / "metric_index.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (build / "query_index.json").write_text(
        json.dumps(queries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Indexed {len(metrics)} metrics, {len(queries)} queries → build/*.json")

if __name__ == "__main__":
    main()
