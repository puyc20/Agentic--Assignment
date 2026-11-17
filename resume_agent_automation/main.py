from __future__ import annotations

import argparse
from pathlib import Path


def run_pytest(test_path: str | None = None) -> None:
    import subprocess

    command = ["pytest"]
    if test_path:
        command.append(test_path)
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Resume Agent Automation Framework")
    parser.add_argument("--pytest", nargs="?", const="resume_agent_automation/tests", default=None)
    args = parser.parse_args()
    run_pytest(args.pytest)


if __name__ == "__main__":
    main()
