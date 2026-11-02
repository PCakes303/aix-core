#!/usr/bin/env python3
"""Run AIX Core starter checks."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "tools/validate_message.py"], cwd=ROOT, check=True)
print("AIX Core starter build passed.")
