# k-metrics

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
├─ build/                   # 인덱스 산출물 저장 위치
├─ requirements.txt
└─ README.md
