#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

# Project root directory
BASE_PATH = Path(__file__).resolve().parent.parent

# Alembic migration files directory
ALEMBIC_VERSION_DIR = BASE_PATH / 'alembic' / 'versions'

# Log files directory
LOG_DIR = BASE_PATH / 'log'

# Static resources directory
STATIC_DIR = BASE_PATH / 'static'
