"""Configuration — model selection, confidentiality, and key sourcing.

Keys come from the environment, never the repo. Author and reviewer models must
differ by default (model diversity). `validate()` returns a list of problems so
the CLI and setup can refuse an unsafe configuration loudly.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass


def _as_bool(v) -> bool:
    """Coerce a config value to bool. A hand-edited JSON string like "false"
    must not read as truthy, or a typo could silently disable a safety gate."""
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("1", "true", "yes", "on")
    return bool(v)


@dataclass
class Config:
    # The reviewer runs on a DIFFERENT model from the author, for error-independence.
    author_model: str = "claude-opus-4-8"
    reviewer_model: str = "claude-sonnet-5"
    allow_same_model: bool = False

    # Confidentiality: redact client identifiers before any content leaves the machine.
    redact_before_send: bool = True

    # Key is read from this environment variable, never stored in the repo.
    provider_key_env: str = "ANTHROPIC_API_KEY"

    def validate(self) -> list:
        problems = []
        if not _as_bool(self.allow_same_model) and self.author_model == self.reviewer_model:
            problems.append(
                "author_model and reviewer_model are identical; the review gate "
                "would be phrasing-independent but not error-independent. Choose "
                "two models, or set allow_same_model=true to override."
            )
        return problems

    def key_present(self, environ=None) -> bool:
        environ = environ if environ is not None else os.environ
        return bool(environ.get(self.provider_key_env))

    @classmethod
    def load(cls, path: str | None = None, environ=None) -> "Config":
        environ = environ if environ is not None else os.environ
        data = {}
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        cfg = cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        # normalise bool-typed fields so a JSON string can't read as truthy
        cfg.allow_same_model = _as_bool(cfg.allow_same_model)
        cfg.redact_before_send = _as_bool(cfg.redact_before_send)
        # env overrides
        if environ.get("SOOTHSAYER_AUTHOR_MODEL"):
            cfg.author_model = environ["SOOTHSAYER_AUTHOR_MODEL"]
        if environ.get("SOOTHSAYER_REVIEWER_MODEL"):
            cfg.reviewer_model = environ["SOOTHSAYER_REVIEWER_MODEL"]
        return cfg

    def to_dict(self) -> dict:
        return asdict(self)
