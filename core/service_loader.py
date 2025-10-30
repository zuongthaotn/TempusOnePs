import importlib
import json


def load_config(path="config/config.json"):
    with open(path, "r") as f:
        return json.load(f)


def load_services(config, event_bus):
    services = {}
    for group_name, group_list in config["pipeline"].items():
        loaded = []
        for s in group_list:
            if not s.get("enabled", True):
                continue
            module_path = f"services.{group_name}.{s['name']}"
            module = importlib.import_module(module_path)
            service_class = getattr(module, s["class"])
            service_instance = service_class(s["name"], event_bus, config=s)
            loaded.append(service_instance)
        services[group_name] = loaded
    return services
