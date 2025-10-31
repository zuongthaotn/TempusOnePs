import importlib


def load_services(config, event_bus):
    services = {}
    for group_name, group_list in config["pipeline"].items():
        loaded = []
        for service in group_list:
            if not service.get("enabled", True):
                continue
            module = importlib.import_module(service['path'])
            service_class = getattr(module, service["class"])
            service_instance = service_class(service["name"], event_bus, config=service)
            loaded.append(service_instance)
        services[group_name] = loaded
    return services
