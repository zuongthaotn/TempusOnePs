# How to Create a New Module in TempusOnePs

This guide will walk you through the process of creating a new module in the TempusOnePs trading platform.

## Table of Contents
- [Module Structure Overview](#module-structure-overview)
- [Step-by-Step Guide](#step-by-step-guide)
- [Service Types](#service-types)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Examples](#examples)

## Module Structure Overview

A module in TempusOnePs is a self-contained directory that includes:

```
modules/
└── your_module_name/
    ├── config/
    │   └── config.json          # Module configuration
    ├── data/                     # Data fetching services
    │   └── your_data_service.py
    ├── signals/                  # Signal generation services
    │   └── your_signal.py
    ├── execution/                # Trade execution services
    │   └── your_executor.py
    ├── log/                      # Logging services
    │   └── your_logger.py
    └── backtest/                 # (Optional) Backtesting utilities
        └── your_backtest.py
```

## Step-by-Step Guide

### Step 1: Create Module Directory Structure

Create a new directory under `modules/` with your module name:

```bash
cd TempusOnePs/modules
mkdir -p your_module_name/{config,data,signals,execution,log,backtest}
```

### Step 2: Create Configuration File

Create `config/config.json` in your module directory. This file defines the pipeline and scheduling:

```json
{
  "cron": "*/5 9,10,11,13,14 * * 1-5",  // Cron expression (for run-cron.py)
  "interval": 5,                         // Interval in seconds (for run.py)
  "pipeline": {
    "data": [
      {
        "name": "your_data_service",
        "path": "modules.your_module_name.data.your_data_service",
        "class": "YourDataServiceClass",
        "enabled": true
      }
    ],
    "signals": [
      {
        "name": "your_signal",
        "path": "modules.your_module_name.signals.your_signal",
        "class": "YourSignalClass",
        "enabled": true
      }
    ],
    "execution": [
      {
        "name": "your_executor",
        "path": "modules.your_module_name.execution.your_executor",
        "class": "YourExecutorClass",
        "enabled": true
      }
    ],
    "log": [
      {
        "name": "your_logger",
        "path": "modules.your_module_name.log.your_logger",
        "class": "YourLoggerClass",
        "enabled": true
      }
    ]
  }
}
```

**Configuration Fields:**
- `name`: Unique identifier for the service
- `path`: Python import path to the service module
- `class`: Class name of the service
- `enabled`: Boolean to enable/disable the service

### Step 3: Create Data Service

Create a data service in `data/your_data_service.py`:

```python
from core.service.base_service import BaseServicePlugin
import pandas as pd

class YourDataServiceClass(BaseServicePlugin):
    def setup(self):
        """
        Initialize resources, connections, etc.
        Called once at startup.
        """
        pass
    
    def run(self):
        """
        Fetch and return market data as a pandas DataFrame.
        This is called on each pipeline iteration.
        
        Returns:
            pd.DataFrame: OHLC data with DatetimeIndex
        """
        # Fetch your data here
        df = self.fetch_data()
        
        # Log the data (optional)
        self.trigger_after(df, "data_fetched")
        
        return df
    
    def fetch_data(self):
        """
        Your custom data fetching logic.
        """
        # Example: Create sample data
        data = {
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [99, 100, 101],
            'Close': [103, 104, 105],
            'Volume': [1000, 1100, 1200]
        }
        df = pd.DataFrame(data)
        df.index = pd.date_range('2024-01-01', periods=3, freq='5min')
        return df
    
    def teardown(self):
        """
        Clean up resources.
        Called once at shutdown.
        """
        pass
```

### Step 4: Create Signal Service

Create a signal service in `signals/your_signal.py`:

```python
from core.service.base_service import BaseServicePlugin
from core.service.base_signal import SignalConfig

class YourSignalClass(BaseServicePlugin):
    def run(self, data=None):
        """
        Generate trading signals from the data.
        
        Args:
            data (pd.DataFrame): OHLC data from the data service
            
        Returns:
            dict: Contains 'data' (DataFrame with signals) and 'meta_data'
        """
        if data is None or len(data) == 0:
            return {
                "data": None,
                "meta_data": {
                    "service_name": self.name
                }
            }
        
        # Create a copy to avoid modifying original
        df = data.copy()
        
        # Calculate your indicators
        df = self.calculate_indicators(df)
        
        # Generate signals
        df['your_signal'] = df.apply(self.generate_signal, axis=1)
        
        # Return only the columns you need
        return {
            "data": df[['your_signal']],  # Add your indicator columns
            "meta_data": {
                "service_name": self.name
            }
        }
    
    def calculate_indicators(self, df):
        """
        Calculate technical indicators.
        """
        # Example: Simple Moving Average
        df['sma_20'] = df['Close'].rolling(window=20).mean()
        df['sma_50'] = df['Close'].rolling(window=50).mean()
        return df
    
    def generate_signal(self, row):
        """
        Generate signal for a single row.
        
        Returns:
            str: Signal type (buy, sell, or empty string)
        """
        if pd.isna(row['sma_20']) or pd.isna(row['sma_50']):
            return SignalConfig.NO_SIGNAL
        
        # Example: Golden cross / Death cross
        if row['sma_20'] > row['sma_50']:
            return SignalConfig.BUY_SIGNAL
        elif row['sma_20'] < row['sma_50']:
            return SignalConfig.SELL_SIGNAL
        
        return SignalConfig.NO_SIGNAL
```

**Available Signal Types:**
- `SignalConfig.NO_SIGNAL` - "" (empty string)
- `SignalConfig.BUY_SIGNAL` - "buy"
- `SignalConfig.SELL_SIGNAL` - "sell"
- `SignalConfig.CLOSE_SIGNAL` - "close"
- `SignalConfig.CLOSE_BUY_SIGNAL` - "close.buy"
- `SignalConfig.CLOSE_SELL_SIGNAL` - "close.sell"
- `SignalConfig.SWITCH_TO_BUY_SIGNAL` - "switch.to.buy"
- `SignalConfig.SWITCH_TO_SELL_SIGNAL` - "switch.to.sell"

### Step 5: Create Execution Service

Create an execution service in `execution/your_executor.py`:

```python
from core.service.base_service import BaseServicePlugin
from core.service.base_signal import SignalConfig

class YourExecutorClass(BaseServicePlugin):
    def setup(self):
        """
        Initialize broker connection, load state, etc.
        """
        pass
    
    def run(self, data=None):
        """
        Execute trades based on signals.
        
        Args:
            data (pd.DataFrame): Merged data with all signals
        """
        if data is None or len(data) == 0:
            return
        
        self.trigger_before(data, "execution")
        
        try:
            # Get the latest data point
            last_row = data.iloc[-1]
            
            # Check signals and execute trades
            if last_row['your_signal'] == SignalConfig.BUY_SIGNAL:
                self.execute_buy(last_row)
            elif last_row['your_signal'] == SignalConfig.SELL_SIGNAL:
                self.execute_sell(last_row)
            
            # Log execution result
            result = {
                "signal": last_row['your_signal'],
                "price": last_row['Close']
            }
            self.trigger_after(result, "execution")
            
        except Exception as e:
            self.trigger_after({"error": str(e)}, "execution")
    
    def execute_buy(self, row):
        """
        Execute buy order.
        """
        print(f"Executing BUY at {row['Close']}")
        # Add your broker API call here
    
    def execute_sell(self, row):
        """
        Execute sell order.
        """
        print(f"Executing SELL at {row['Close']}")
        # Add your broker API call here
    
    def teardown(self):
        """
        Close connections, save state, etc.
        """
        pass
```

### Step 6: Create Log Service

Create a logging service in `log/your_logger.py`:

```python
from core.service.base_service import BaseServicePlugin
import json
import os

class YourLoggerClass(BaseServicePlugin):
    def __init__(self, name, config=None, log_queue=None, mode='live'):
        self.log_file = None
        super().__init__(name, config=config, log_queue=log_queue, mode=mode)
    
    def setup(self):
        """
        Open log file for writing.
        """
        current_folder = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(current_folder, "trading.log")
        
        file_exists = os.path.isfile(log_path)
        if not file_exists:
            self.log_file = open(log_path, "w", encoding="utf-8")
            self.log_file.write("=== TempusOnePs Trading Log ===\n")
        else:
            self.log_file = open(log_path, "a", encoding="utf-8")
    
    def run(self, data=None):
        """
        Write all queued logs to file.
        """
        logs = self.log_queue.get_all()
        
        for log in logs:
            self.log_file.write(json.dumps(log, ensure_ascii=False) + "\n")
            self.log_file.flush()
    
    def teardown(self):
        """
        Close log file.
        """
        if self.log_file:
            self.log_file.close()
```

### Step 7: Run Your Module

Run your module using one of these commands:

```bash
# Run once with interval-based scheduling
python run.py --mod your_module_name

# Run with cron-based scheduling
python run-cron.py --mod your_module_name
```

## Service Types

### BaseServicePlugin

The base class for all services. Provides:

**Attributes:**
- `self.name` - Service name from config
- `self.mode` - Execution mode ('live' or other)
- `self.config` - Service configuration dict
- `self.log_queue` - Queue for logging

**Methods:**
- `setup()` - Called once at startup
- `run(data=None)` - Main execution method
- `teardown()` - Called once at shutdown
- `trigger_before(data, strategy_name)` - Log before processing
- `trigger_after(data, strategy_name)` - Log after processing

### Signal Services

Signal services run in **parallel using multiprocessing** for better performance. Each signal service:

1. Receives a copy of the data DataFrame
2. Processes independently
3. Returns a dict with `data` and `meta_data`
4. Results are merged back into the main DataFrame

**Important:** Signal services must return this structure:

```python
{
    "data": pd.DataFrame,  # Your signal columns
    "meta_data": {
        "service_name": self.name
    }
}
```

## Configuration

### Cron Expression

For scheduled execution with `run-cron.py`:

```json
"cron": "*/5 9,10,11,13,14 * * 1-5"
```

Format: `minute hour day month day_of_week`
- `*/5` - Every 5 minutes
- `9,10,11,13,14` - Hours 9, 10, 11, 13, 14
- `*` - Every day
- `*` - Every month
- `1-5` - Monday to Friday

### Interval

For simple interval-based execution with `run.py`:

```json
"interval": 5  // Run every 5 seconds
```

## Best Practices

### 1. Error Handling

Always wrap your logic in try-except blocks:

```python
def run(self, data=None):
    try:
        # Your logic here
        result = self.process_data(data)
        self.trigger_after(result, "success")
    except Exception as e:
        self.trigger_after({"error": str(e)}, "error")
```

### 2. Data Validation

Validate data before processing:

```python
def run(self, data=None):
    if data is None or len(data) == 0:
        return None
    
    # Check for required columns
    required_cols = ['Open', 'High', 'Low', 'Close']
    if not all(col in data.columns for col in required_cols):
        return None
```

### 3. Mode-Aware Logic

Use `self.mode` to differentiate between live and backtest:

```python
def run(self, data=None):
    if self.mode == 'live':
        # Execute real trades
        self.broker.place_order(...)
    else:
        # Simulate for backtest
        print(f"Simulated order: {price}")
```

### 4. Logging

Use the logging methods for debugging:

```python
# Log before processing
self.trigger_before(data, "my_strategy")

# Your processing logic
result = self.process(data)

# Log after processing
self.trigger_after(result, "my_strategy")
```

### 5. State Management

For services that need to persist state between runs:

```python
import pickle
from pathlib import Path

class StatefulService(BaseServicePlugin):
    def setup(self):
        self.state_file = Path(__file__).parent / "state.pkl"
        self.state = self.load_state()
    
    def load_state(self):
        if self.state_file.exists():
            with open(self.state_file, 'rb') as f:
                return pickle.load(f)
        return {"position": None, "entry_price": 0}
    
    def save_state(self):
        with open(self.state_file, 'wb') as f:
            pickle.dump(self.state, f)
    
    def teardown(self):
        self.save_state()
```

## Examples

### Example 1: Simple CSV Data Module

See `modules/examples/` for a complete working example that:
- Reads OHLC data from CSV files
- Generates EMA crossover signals
- Simulates trade execution
- Logs results to file

### Example 2: Live Trading Module

See `modules/magnus/` for a production example that:
- Fetches live VN30F1M data from DNSE
- Uses multiple signal strategies (EMA, Momentum, MACD)
- Executes real trades via broker API
- Manages positions with stop-loss and take-profit
- Logs to file and sends Telegram notifications

### Running Examples

```bash
# Run the CSV example
python run.py --mod examples

# Run the live trading module
python run-cron.py --mod magnus
```

## Pipeline Flow

Understanding the execution flow:

```
1. SETUP PHASE
   ├── Load config
   ├── Initialize services
   └── Call setup() on all services

2. PIPELINE EXECUTION (repeated)
   ├── DATA: Fetch market data
   │   └── Returns DataFrame
   ├── SIGNALS: Generate signals (parallel)
   │   ├── Signal 1 processes data copy
   │   ├── Signal 2 processes data copy
   │   └── Results merged into DataFrame
   ├── EXECUTION: Execute trades
   │   └── Receives merged DataFrame with all signals
   ├── LOG: Write logs
   │   └── Flush log queue to storage
   └── Clear log queue

3. TEARDOWN PHASE
   └── Call teardown() on all services
```

## Troubleshooting

### Module Not Found

If you get `ModuleNotFoundError`, check:
1. The `path` in config.json matches your file structure
2. The `class` name matches your class definition
3. Your module directory is under `modules/`

### Signals Not Merging

If signals aren't appearing in execution:
1. Ensure signal services return the correct dict structure
2. Check that `data` is a DataFrame with matching index
3. Verify `enabled: true` in config.json

### No Data in Pipeline

If data service returns None:
1. Check data fetching logic
2. Verify DataFrame has DatetimeIndex
3. Ensure data is not empty

## Additional Resources

- [README.md](file://TempusOnePs/README.md) - System overview
- [TempusOnePs.txt](file://TempusOnePs/TempusOnePs.txt) - Detailed documentation
- [core/service/base_service.py](file://TempusOnePs/core/service/base_service.py) - Base service implementation
- [core/service/base_signal.py](file://TempusOnePs/core/service/base_signal.py) - Signal service implementation

---

**Happy Trading! 🚀**
