#!/bin/bash
cd ..
#
git pull --recurse-submodules
#
git submodule update --init --recursive
#
git submodule update --recursive --remote