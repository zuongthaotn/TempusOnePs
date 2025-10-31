import asyncio
from core.utils import load_config
from core.event_bus import event_bus
from core.service_loader import load_services
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
        for se in services.get("data", []):
            await se.run()

        for se in services.get("signals", []):
            await se.run()

        for se in services.get("execution", []):
            await se.run()

        for se in services.get("log", []):
            await se.run()

    cron_expr = config.get("cron")
    interval = config.get("interval", None)
    scheduler = Scheduler(interval=interval, cron_expr=cron_expr, callback=run_pipeline)
    await scheduler.start()

    # Final phase
    for group in services.values():
        for st in group:
            await st.teardown()

if __name__ == "__main__":
    asyncio.run(main())
