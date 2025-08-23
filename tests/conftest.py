import json
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """Set up test data files"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Create test knowledge base if file doesn't exist
    kb_file = data_dir / "kb.json"
    if not kb_file.exists():
        kb_data = {
            "entries": [
                {
                    "name": "Ada Lovelace",
                    "summary": "Ada Lovelace was a 19th-century mathematician regarded as an early computing pioneer for her work on Charles Babbage's Analytical Engine.",
                },
                {
                    "name": "Alan Turing",
                    "summary": "Alan Turing was a mathematician and logician, widely considered to be the father of theoretical computer science and artificial intelligence.",
                },
            ]
        }

        with open(kb_file, "w") as f:
            json.dump(kb_data, f, indent=2)
