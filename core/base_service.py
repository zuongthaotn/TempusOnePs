class BasePluginService:
    def __init__(self, name, event_bus, config=None):
        self.name = name
        self.bus = event_bus
        self.config = config or {}

    async def setup(self):
        """Gọi khi service được khởi tạo"""
        pass

    async def run(self):
        """Gọi khi service được trigger"""
        pass

    async def handle_event(self, event_name, data):
        """Đăng ký xử lý event"""
        pass
