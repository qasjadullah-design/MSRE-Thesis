"""Surface the tail of the newest Snakemake and rule logs as GitHub error annotations.

Usage: python ci_annotate_logs.py <path to pypsa-usa/workflow>

Job logs on GitHub need a signed-in account with repository access; check-run
annotations do not. Emitting the log tails as annotations lets a failed run be
diagnosed from the public API.
"""

from __future__ import annotations

import sys
from pathlib import Path

MAX_CHARS = 3500
RULE_LOGS = 4


def escape(text: str, is_property: bool = False) -> str:
    text = text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    if is_property:
        text = text.replace(":", "%3A").replace(",", "%2C")
    return text


def tail(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace").rstrip()
    return text[-MAX_CHARS:] if text else "(empty)"


def newest(folder: Path, pattern: str, count: int) -> list[Path]:
    if not folder.exists():
        return []
    files = [p for p in folder.rglob(pattern) if p.is_file()]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:count]


def last_traceback(path: Path) -> str | None:
    """Return the text from the last Python traceback in a console capture, if any."""
    text = path.read_text(encoding="utf-8", errors="replace")
    start = text.rfind("Traceback (most recent call last)")
    if start < 0:
        return None
    block = text[start:]
    end = block.find("\n[", 1)  # snakemake's next "[timestamp]" line ends the script's stderr
    block = block[:end] if end > 0 else block
    return block[-MAX_CHARS:].rstrip()


def publish_notices(title: str, paths: list[Path], max_notices: int = 9) -> int:
    """Publish whole files (in chunks) as notice annotations, e.g. the run summary."""
    text = "\n\n".join(p.read_text(encoding="utf-8", errors="replace").rstrip() for p in paths if p.is_file())
    if not text:
        print(f"::notice title={escape(title, is_property=True)}::(nothing to report)")
        return 0
    lines, chunks, current = text.splitlines(), [], ""
    for line in lines:
        if current and len(current) + len(line) + 1 > MAX_CHARS:
            chunks.append(current)
            current = ""
        current += line[:MAX_CHARS] + "\n"
    chunks.append(current)
    for number, chunk in enumerate(chunks[:max_notices], start=1):
        label = escape(f"{title} ({number}/{min(len(chunks), max_notices)})", is_property=True)
        print(f"::notice title={label}::{escape(chunk.rstrip())}")
    return 0


def main() -> int:
    if sys.argv[1] == "--notice":
        return publish_notices(sys.argv[2], [Path(arg) for arg in sys.argv[3:]])
    workflow = Path(sys.argv[1])
    consoles = [Path(arg) for arg in sys.argv[2:] if Path(arg).is_file()]
    for path in consoles:
        trace = last_traceback(path)
        if trace:
            print(f"::error title={escape('traceback in ' + path.name, is_property=True)}::{escape(trace)}")
    targets = newest(workflow / ".snakemake" / "log", "*.log", 1) + newest(workflow / "logs", "*.log", RULE_LOGS)
    if not targets and not consoles:
        print("::error title=ci_annotate_logs::no log files found")
        return 0
    for path in targets:
        title = escape(str(path.relative_to(workflow)), is_property=True)
        print(f"::error title={title}::{escape(tail(path))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
