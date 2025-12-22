#!/usr/bin/env python3
"""
Validate TempusOnePs configuration files.

This script validates that all services defined in config.json:
- Have valid module paths
- Have valid class names
- Can be imported successfully
"""

import json
import importlib
import os
import sys
import argparse
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    # This script is in tools/, so parent is project root
    return Path(__file__).parent.parent


def get_config_path(module_name=None):
    """
    Get the config path based on module name.
    
    Args:
        module_name: Optional module name. If None, uses root config.
        
    Returns:
        Path to config.json
    """
    project_root = get_project_root()
    
    if module_name:
        config_path = project_root / "modules" / module_name / "config" / "config.json"
    else:
        config_path = project_root / "config" / "config.json"
    
    return config_path


def validate_service(module_path: str, class_name: str, service_name: str) -> bool:
    """
    Check if module and class exist and can be imported.
    
    Args:
        module_path: Python import path (e.g., "modules.examples.data.replay_ohcl_csv")
        class_name: Class name to validate
        service_name: Service name for logging
        
    Returns:
        True if valid, False otherwise
    """
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        print(f"❌ [{service_name}] Module not found: {module_path}")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"❌ [{service_name}] Error importing module: {module_path}")
        print(f"   Error: {e}")
        return False

    if hasattr(module, class_name):
        print(f"✅ [{service_name}] {module_path}.{class_name}")
        return True
    else:
        print(f"❌ [{service_name}] Class '{class_name}' not found in module '{module_path}'")
        available_classes = [name for name in dir(module) if not name.startswith('_') and name[0].isupper()]
        if available_classes:
            print(f"   Available classes: {', '.join(available_classes)}")
        return False


def validate_config(config_path, verbose=False):
    """
    Validate configuration file.
    
    Args:
        config_path: Path to config.json
        verbose: Print additional information
        
    Returns:
        True if all services are valid, False otherwise
    """
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return False

    # Read JSON file
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {config_path}")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading config file: {config_path}")
        print(f"   Error: {e}")
        return False

    if verbose:
        print(f"📄 Config file: {config_path}")
        if "cron" in config:
            print(f"⏰ Cron schedule: {config['cron']}")
        if "interval" in config:
            print(f"⏱️  Interval: {config['interval']} seconds")
        print()

    print("🔍 Validating services...\n")

    # Get pipeline configuration
    pipeline = config.get("pipeline", {})
    if not pipeline:
        print("⚠️  No 'pipeline' found in config")
        return False

    all_ok = True
    service_types = ["data", "signals", "execution", "log"]

    for service_type in service_types:
        services = pipeline.get(service_type, [])
        
        if not services:
            if verbose:
                print(f"ℹ️  No {service_type} services configured")
            continue
        
        print(f"📦 {service_type.upper()} Services:")
        
        for service in services:
            # Check if service is enabled
            if not service.get("enabled", True):
                if verbose:
                    print(f"⏭️  [{service.get('name', 'unknown')}] Disabled, skipping")
                continue
            
            # Validate required fields
            if "path" not in service:
                print(f"❌ [{service.get('name', 'unknown')}] Missing 'path' field")
                all_ok = False
                continue
            
            if "class" not in service:
                print(f"❌ [{service.get('name', 'unknown')}] Missing 'class' field")
                all_ok = False
                continue
            
            # Validate the service
            ok = validate_service(
                service["path"],
                service["class"],
                service.get("name", "unknown")
            )
            all_ok = all_ok and ok
        
        print()  # Empty line between service types

    return all_ok


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate TempusOnePs configuration files"
    )
    parser.add_argument(
        "--mod",
        type=str,
        help="Module name to validate (e.g., 'examples', 'magnus'). If not provided, validates root config."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print verbose output"
    )
    
    args = parser.parse_args()
    
    # Get config path
    config_path = get_config_path(args.mod)
    
    # Add project root to Python path so imports work
    project_root = get_project_root()
    sys.path.insert(0, str(project_root))
    
    # Print header
    print("=" * 60)
    if args.mod:
        print(f"🔧 Validating Module: {args.mod}")
    else:
        print("🔧 Validating Root Configuration")
    print("=" * 60)
    print()
    
    # Validate
    success = validate_config(config_path, verbose=args.verbose)
    
    # Print result
    print("=" * 60)
    if success:
        print("✅ All services validated successfully!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ Some services failed validation.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
