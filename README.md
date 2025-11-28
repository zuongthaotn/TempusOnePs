# TempusOnePs
Modular, Connectable, and Scalable Quant & Algo Trading Platform for VN Stocks, Crypto, Forex, and Gold Markets.

## System Design
![System Design](TempusOnePs.png)

## System Architecture

TempusOnePs operates as a pipeline-based system where data flows through a series of stages:

1.  **Data**: Fetches market data from various sources.
2.  **Signals**: Processes data to generate trading signals (Buy, Sell, Close, etc.). This stage runs in parallel using multiprocessing for performance.
3.  **Execution**: Executes trades based on the generated signals.
4.  **Log**: Logs the results of the pipeline execution.

The system is built around a `ServiceLoader` that dynamically loads services defined in `config/config.json`.

## Configuration

The system behavior is controlled by `config/config.json`. This file defines the pipeline stages and the services to run in each stage.

Example structure:

```json
{
  "cron": "*/5 * * * *", // Cron expression for scheduling
  "interval": 5,         // Interval in seconds (optional override)
  "pipeline": {
    "data": [ ... ],
    "signals": [ ... ],
    "execution": [ ... ],
    "log": [ ... ]
  }
}
```

Each service entry in the pipeline looks like this:

```json
{
  "name": "ServiceName",
  "class": "ClassName",
  "path": "module.path",
  "enabled": true,
  "other_params": "value"
}
```

## Running the System

### Manual Run
To run the pipeline once immediately:

```bash
python run.py --mod <module_name>
```

### Scheduled Run
To run the pipeline continuously based on the cron schedule defined in the config:

```bash
python run-cron.py --mod <module_name>
```

If `--mod` is not provided, the system will look for `config/config.json` in the root directory.
If `--mod <module_name>` is provided, it will look for `modules/<module_name>/config/config.json`.

## Extending the System

To add a new service (e.g., a new signal strategy):

1.  Create a new Python file in `modules/` (or appropriate subdirectory).
2.  Define a class that inherits from the appropriate base class:
    *   `BaseServicePlugin` for general services.
    *   `BaseSignalPlugin` for signal services.
3.  Implement the `run` method.
4.  Add the new service to `config/config.json` under the appropriate pipeline stage.

### Example Signal Service

```python
from core.service.base_signal import BaseSignalPlugin

class MyStrategy(BaseSignalPlugin):
    def run(self, df):
        # Implement logic here
        # df['signal'] = ...
        return df
```