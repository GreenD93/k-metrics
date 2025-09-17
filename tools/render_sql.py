from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pathlib import Path

def _sql_str(value):
    # 아주 단순한 escape: ' → '' 로
    if value is None:
        return "NULL"
    s = str(value).replace("'", "''")
    return f"'{s}'"

def make_env(base_dir: Path):
    env = Environment(
        loader=FileSystemLoader(str(base_dir)),
        autoescape=False,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["sql_str"] = _sql_str
    return env

def render_sql(sql_path: str, params: dict) -> str:
    p = Path(sql_path)
    env = make_env(p.parent)
    tpl = env.get_template(p.name)
    return tpl.render(**params)
