"""Git-backed document store — the memory is the documents, not runtime state.

Evidence records are written one JSON file per content-hash id, so the store is
append-only by construction: the same content lands on the same path, and a
different-content write to an existing id is refused. If git is present the store
commits each change, giving free append-only history and time-travel; if git is
absent it degrades to plain files. No database, no index — read and grep, the
gstack way.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .models import Assertion, EvidenceRecord


class ImmutabilityError(Exception):
    pass


class Store:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.evidence_dir = self.root / "evidence"
        self.decisions_log = self.root / "decisions" / "log.jsonl"

    # -- lifecycle -------------------------------------------------------
    def init(self, git: bool = True) -> "Store":
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.decisions_log.parent.mkdir(parents=True, exist_ok=True)
        if git and self._git_available() and not (self.root / ".git").exists():
            self._git("init", "-q")
        return self

    # -- evidence --------------------------------------------------------
    def add_evidence(self, record: EvidenceRecord) -> Path:
        path = self.evidence_dir / f"{record.id}.json"
        payload = json.dumps(record.to_dict(), sort_keys=True, ensure_ascii=False, indent=2)
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            if json.loads(existing) != json.loads(payload):
                raise ImmutabilityError(
                    f"evidence id {record.id} already exists with different content"
                )
            return path  # idempotent
        path.write_text(payload, encoding="utf-8")
        self._commit(f"evidence: {record.id}", path)
        return path

    def evidence(self) -> list:
        out = []
        if not self.evidence_dir.exists():
            return out
        for p in sorted(self.evidence_dir.glob("*.json")):
            out.append(EvidenceRecord.from_dict(json.loads(p.read_text(encoding="utf-8"))))
        return out

    def evidence_by_id(self) -> dict:
        return {r.id: r for r in self.evidence()}

    # -- decision log ----------------------------------------------------
    def append_decision(self, entry: dict) -> None:
        with self.decisions_log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
        self._commit("decision-log append", self.decisions_log)

    # -- git glue --------------------------------------------------------
    def _git_available(self) -> bool:
        try:
            subprocess.run(
                ["git", "--version"], capture_output=True, check=True
            )
            return True
        except Exception:
            return False

    def _git(self, *args: str) -> None:
        subprocess.run(
            ["git", "-C", str(self.root), *args], capture_output=True, check=False
        )

    def _commit(self, message: str, path: Path) -> None:
        if not (self.root / ".git").exists():
            return
        rel = path.relative_to(self.root)
        self._git("add", str(rel))
        self._git(
            "-c", "user.email=soothsayer@local",
            "-c", "user.name=soothsayer",
            "commit", "-q", "-m", message,
        )
