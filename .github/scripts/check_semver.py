#!/usr/bin/env python3
"""PR semver gate for the datamaxi public API.

Python analog of the Rust sibling's ``cargo-semver-checks`` job. It diffs the
public API of the ``datamaxi`` package between the PR base commit and the PR
head (working tree) with ``griffe check``, then fails when the version bump in
``datamaxi/__version__.py`` is smaller than the detected change requires.

Policy (0.x-aware, and future-proof for >=1.0):
  * pre-1.0 (base major == 0): breaking changes must land a **minor** bump
    (e.g. 0.29.0 -> 0.30.0), per the pre-1.0 SemVer convention.
  * >=1.0: breaking changes must land a **major** bump.
  * a version that goes backwards always fails.
  * no breaking changes + non-decreasing version always passes (we do not force
    a bump for additive-only changes, which griffe check does not surface).

griffe is static (AST-based), so it needs neither the optional deps
(``httpx``/``websockets``) nor prod credentials/network. griffe checks out the
base ref through an internal git worktree, so the workflow must use
``fetch-depth: 0``.

Usage:
    python .github/scripts/check_semver.py <base-ref>
"""

from __future__ import annotations

import re
import subprocess
import sys

PACKAGE = "datamaxi"
VERSION_FILE = "datamaxi/__version__.py"

_VERSION_RE = re.compile(r"""__version__\s*=\s*["']([^"']+)["']""")
# Markers that mean griffe itself blew up (bad ref, load failure, ...) rather
# than reporting genuine API breakages.
_ERROR_MARKERS = ("Traceback (most recent call last)", "GitError", "fatal:")

LEVELS = {"none": 0, "patch": 1, "minor": 2, "major": 3}


def fail(msg: str) -> None:
    print(f"::error::{msg}" if _in_gha() else f"ERROR: {msg}")
    sys.exit(1)


def tool_error(msg: str) -> None:
    print(f"::error::{msg}" if _in_gha() else f"TOOL ERROR: {msg}")
    sys.exit(2)


def _in_gha() -> bool:
    import os

    return os.environ.get("GITHUB_ACTIONS") == "true"


def read_version_at(ref: str | None) -> str | None:
    """Return the ``__version__`` string at ``ref`` (None == working tree)."""
    if ref is None:
        with open(VERSION_FILE, encoding="utf-8") as fh:
            text = fh.read()
    else:
        proc = subprocess.run(
            ["git", "show", f"{ref}:{VERSION_FILE}"],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return None
        text = proc.stdout
    match = _VERSION_RE.search(text)
    return match.group(1) if match else None


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse ``major.minor.patch`` leniently (ignores any pre-release suffix)."""
    nums = []
    for part in version.split(".")[:3]:
        match = re.match(r"\d+", part)
        nums.append(int(match.group(0)) if match else 0)
    while len(nums) < 3:
        nums.append(0)
    return nums[0], nums[1], nums[2]


def actual_bump_level(base: tuple, head: tuple) -> str:
    if head < base:
        return "decrease"
    if head == base:
        return "none"
    if head[0] != base[0]:
        return "major"
    if head[1] != base[1]:
        return "minor"
    return "patch"


def required_bump_level(base: tuple) -> str:
    """Minimum bump a breaking change requires, given the base version."""
    return "major" if base[0] >= 1 else "minor"


def run_griffe(base_ref: str) -> tuple[bool, str]:
    """Return (breaking?, report). griffe writes its report to stderr."""
    cmd = [
        sys.executable,
        "-m",
        "griffe",
        "check",
        PACKAGE,
        "-a",
        base_ref,
        "-f",
        "oneline",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    report = (proc.stdout + proc.stderr).strip()

    if proc.returncode == 0:
        return False, report
    if any(marker in report for marker in _ERROR_MARKERS):
        tool_error(f"griffe failed to run:\n{report}")
    # Non-zero + no error marker == breaking changes were reported.
    return True, report


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if sys.argv[1:] in (["-h"], ["--help"]) else 2)
    base_ref = sys.argv[1]

    # Validate the base ref up front so griffe git-worktree errors can't be
    # mistaken for breaking changes.
    if (
        subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{base_ref}^{{commit}}"],
            capture_output=True,
        ).returncode
        != 0
    ):
        tool_error(
            f"base ref '{base_ref}' is not a valid commit "
            "(the workflow needs actions/checkout with fetch-depth: 0)."
        )

    base_str = read_version_at(base_ref)
    head_str = read_version_at(None)

    if head_str is None:
        fail(f"could not read __version__ from {VERSION_FILE} in the working tree.")
    if base_str is None:
        # No version file at base (very old history / brand-new package). We
        # cannot enforce a policy without a baseline, so pass with a note.
        print(
            f"NOTE: no readable {VERSION_FILE} at base '{base_ref}'; "
            "skipping semver enforcement."
        )
        sys.exit(0)

    base = parse_version(base_str)
    head = parse_version(head_str)

    breaking, report = run_griffe(base_ref)
    level = actual_bump_level(base, head)

    print(f"base version : {base_str}  (from {base_ref[:12]})")
    print(f"head version : {head_str}  (working tree)")
    print(f"version bump : {level}")
    print(f"breaking API changes detected: {'yes' if breaking else 'no'}")

    if level == "decrease":
        if report:
            print("\ngriffe report:\n" + report)
        fail(
            f"version went backwards: {base_str} -> {head_str}. "
            "The version must never decrease."
        )

    if not breaking:
        print(
            "\nOK: no breaking public-API changes; version is non-decreasing. "
            "Nothing to enforce."
        )
        return

    required = required_bump_level(base)
    if LEVELS[level] < LEVELS[required]:
        era = "pre-1.0" if base[0] < 1 else ">=1.0"
        print("\ngriffe-detected breaking changes:\n" + report)
        fail(
            f"breaking public-API changes require at least a '{required}' version "
            f"bump ({era} policy), but {base_str} -> {head_str} is a '{level}' bump. "
            f"Bump {VERSION_FILE} accordingly (e.g. "
            f"{_suggest(base, required)})."
        )

    print(
        f"\nOK: breaking changes are covered by a '{level}' bump "
        f"({base_str} -> {head_str}), which meets the required '{required}' bump."
    )


def _suggest(base: tuple, required: str) -> str:
    major, minor, patch = base
    if required == "major":
        return f"{major + 1}.0.0"
    return f"{major}.{minor + 1}.0"


if __name__ == "__main__":
    main()
