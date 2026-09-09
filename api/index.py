"""
Vercel Serverless Function entry point for BIS Saathi FastAPI backend.
"""

import sys
import os
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
cwd = os.getcwd()
for p in [ROOT_DIR, cwd]:
    if p and p not in sys.path:
        sys.path.insert(0, p)

from backend.main import app
