# TempusOnePs
Hệ thống algo trading cho CK phái sinh
## Design hệ thống
📦 trading_system/
│
├── config/
│   └── config.json               # định nghĩa pipeline và tham số
│
├── core/
│   ├── event_bus.py              # publish/subscribe events
│   ├── base_service.py           # Base class cho tất cả service
│   ├── scheduler.py              # Job loop / 5-min timer
│   └── loader.py                 # đọc config, load service dynamically
│
├── services/
│   ├── data_service.py           # fetch & update data
│   ├── signal_service.py         # generate trading signals
│   ├── execution_service.py      # simulate hoặc send order
│   ├── log_service.py            # store logs or push to DB
│   └── monitoring_service.py     # optional: collect metrics
│
└── run.py                        # entrypoint
├── requirements.txt
├── pyproject.toml or setup.py
└── README.md