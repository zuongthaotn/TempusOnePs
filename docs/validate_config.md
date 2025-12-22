# Validate examples module
python tools/validate_config.py --mod examples

# Validate magnus module with verbose output
python tools/validate_config.py --mod magnus -v

# Validate root config (if exists)
python tools/validate_config.py

# Show help
python tools/validate_config.py --help