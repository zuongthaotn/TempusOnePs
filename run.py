import asyncio
from core.event_bus import event_bus
from core.service_loader import load_config, load_services
from core.scheduler import Scheduler


async def main():
    config = load_config()
    services = load_services(config, event_bus)

    # Setup phase
    for group in services.values():
        for s in group:
            await s.setup()

    # Pipeline flow
    async def run_pipeline():
        for s in services.get("data", []):
            await s.run()

        for s in services.get("signals", []):
            await s.run()

        for s in services.get("execution", []):
            await s.run()

        for s in services.get("log", []):
            await s.run()

    cron_expr = config.get("cron")
    interval = config.get("interval", None)
    scheduler = Scheduler(interval=interval, cron_expr=cron_expr, callback=run_pipeline)
    await scheduler.start()

if __name__ == "__main__":
    asyncio.run(main())
