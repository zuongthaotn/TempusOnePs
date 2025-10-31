#!/bin/bash
#
DIR=$(cd "$(dirname "$0")"; pwd)
__python_version="3.12"
#
rm -rf venv/lib/python"$__python_version"/site-packages/brokers
ln -s ""$DIR/lib/brokers"" venv/lib/python"$__python_version"/site-packages/brokers
#
rm -rf venv/lib/python"$__python_version"/site-packages/stock_price_patterns
ln -s ""$DIR/lib/stock_price_patterns"" venv/lib/python"$__python_version"/site-packages/stock_price_patterns
