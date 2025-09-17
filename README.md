# k-metrics

## 프로젝트 구조
```markdown
├─ metrics/
│  └─ active_users/
│     ├─ active_users.yaml
│     └─ active_users.sql
├─ queries/
│  └─ sample/
│     ├─ query.yaml
│     └─ query.sql
├─ models/
│  └─ app_events.yaml
├─ dimensions.yaml
├─ tools/
│  ├─ build_index.py        # yaml → index.json
│  ├─ render_sql.py         # Jinja 렌더(초경량)
│  ├─ run_query.py          # Athena 실행(boto3)
├─ build/                   # 인덱스 산출물 저장 위치
├─ requirements.txt
└─ README.md
```

### 인덱싱
```bash
python tools/build_index.py
```
- 결과 ex) build/search_lite.json
```json
[
  {
    "id": "metric.active_users",
    "kind": "metric",
    "title": "active_users",
    "description": "활성 사용자(기간 기준 distinct)",
    "tags": [
      "active_users",
      "dau",
      "wau",
      "mau"
    ],
    "text": "metric.active_users active_users 활성 사용자(기간 기준 distinct) active_users dau wau mau metric",
    "path_yaml": "metrics/active_users/active_users.yaml",
    "path_sql": "metrics/active_users/active_users.sql"
  },
  {
    "id": "query.top_channels",
    "kind": "query",
    "title": "sample",
    "description": "지정된 기간 동안 이벤트 수 기준 상위 채널 조회",
    "tags": [
      "channel",
      "events",
      "topN"
    ],
    "text": "query.top_channels sample 지정된 기간 동안 이벤트 수 기준 상위 채널 조회 channel events topN query",
    "path_yaml": "queries/sample/sample.yaml",
    "path_sql": "queries/sample/query.sql"
  }
]
```
