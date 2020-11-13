#!/usr/bin/env python3
from pathlib import Path


def playbook_path():
    cwd = Path(__file__).resolve().parent
    path = str(cwd) + '/playbooks'

    return path
