import aiocron
import asyncio

class Scheduler:
    def __init__(self, interval=None, cron_expr=None, callback=None):
        self.interval = interval
        self.cron_expr = cron_expr
        self.callback = callback
        self.cron_job = None

    async def start(self):
        if self.cron_expr:
            print(f"⏰ Using cron schedule: {self.cron_expr}")
            self.cron_job = aiocron.crontab(self.cron_expr, func=self.callback)
            while True:
                await asyncio.sleep(3600)
        else:
            print(f"⏳ Running every {self.interval}s")
            while True:
                await self.callback()
                await asyncio.sleep(self.interval)
