#!/usr/bin/env python3

import json
import shutil
import subprocess  # nosec B404
import sys


def main() -> int:
    openspec = shutil.which("openspec")

    if openspec is None:
        sys.stderr.write(
            "openspec is not installed, "
            "run `npm install -g @fission-ai/openspec` to set it up\n"
        )
        return 1

    result = subprocess.run(  # nosec B603
        [openspec, "list", "--json"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        sys.stderr.write(f"openspec list failed:\n{result.stderr}")
        return 1

    changes = json.loads(result.stdout)["changes"]

    if not changes:
        return 0

    sys.stderr.write("Active OpenSpec changes must be archived first:\n")

    for change in changes:
        done = change["completedTasks"]
        total = change["totalTasks"]
        sys.stderr.write(f"  {change['name']} ({done}/{total} tasks)\n")

    sys.stderr.write("\nRun `openspec archive <change>` for each of them.\n")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
