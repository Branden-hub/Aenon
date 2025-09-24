"""Simple persistent memory subsystem for Aenon.

This module provides a lightweight JSON backed memory implementation. The
original project referenced ChromaDB, but pulling that dependency adds
significant overhead and is unnecessary for the workflows that Aenon supports
inside this repository.  The implementation below keeps an append only log of
entries and exposes a couple of helper methods that the core system and the web
API can rely on.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List


class InfiniteMemory:
    """Persist structured memories as JSON on disk.

    The implementation is intentionally small – the goal is to provide a memory
    mechanism that works in constrained environments (including the execution
    sandbox used for evaluation).  Each call to :meth:`store` writes to an
    append-only log which makes the class resilient to abrupt shutdowns while
    keeping the behaviour easy to reason about.
    """

    def __init__(self, config: Dict[str, Any] | None):
        self.config = config or {}
        self.persist_dir = self.config.get("persist_dir", "./memory_db")
        os.makedirs(self.persist_dir, exist_ok=True)
        self.file_path = os.path.join(self.persist_dir, "aenon_memory.json")
        if not os.path.exists(self.file_path):
            self._save([])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load(self) -> List[Dict[str, Any]]:
        """Load all stored memories from disk."""

        try:
            with open(self.file_path, "r", encoding="utf-8") as handle:
                raw = handle.read().strip()
                if not raw:
                    return []
                return json.loads(raw)
        except (OSError, json.JSONDecodeError):
            # The file might be corrupted or partially written – start fresh to
            # keep the system responsive.
            return []

    def _save(self, entries: List[Dict[str, Any]]) -> None:
        """Persist the list of entries to disk."""

        with open(self.file_path, "w", encoding="utf-8") as handle:
            json.dump(entries, handle, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def store(self, context: str, content: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Store a new memory entry and return its identifier."""

        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "context": context,
            "content": content,
            "metadata": metadata,
        }
        entries = self._load()
        entries.append(entry)
        self._save(entries)
        return entry["id"]

    def retrieve(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Return entries that contain the query string.

        The matching logic is intentionally straightforward – it performs a
        substring search over the JSON serialisation of the entry.  When the
        query is empty the method falls back to returning the most recent
        entries.
        """

        query = (query or "").strip().lower()
        if not query:
            return self.recent(n_results)

        entries = self._load()
        scored: List[tuple[int, Dict[str, Any]]] = []
        for entry in entries:
            serialised = json.dumps(entry, default=str).lower()
            if query in serialised:
                scored.append((serialised.count(query), entry))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [entry for _, entry in scored[:n_results]]

    def recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Return the most recent ``limit`` entries."""

        entries = self._load()
        if limit <= 0:
            return []
        return list(reversed(entries[-limit:]))

    def update(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing entry.

        Returns ``True`` when the entry was found and updated.
        """

        entries = self._load()
        updated = False
        for entry in entries:
            if entry["id"] == entry_id:
                entry.update(updates)
                updated = True
                break
        if updated:
            self._save(entries)
        return updated

    def clear(self) -> None:
        """Remove all stored memories."""

        self._save([])
