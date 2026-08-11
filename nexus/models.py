from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(slots=True)
class Finding:
    rule_id: str
    severity: str
    title: str
    message: str
    path: str
    line: int = 0
    column: int = 0
    fingerprint: str = ""
    confidence: str = "medium"
    cwe: str = ""
    remediation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self): return asdict(self)

@dataclass(slots=True)
class Node:
    node_id: str
    kind: str
    name: str
    path: str
    line: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self): return asdict(self)

@dataclass(slots=True)
class Edge:
    source: str
    target: str
    kind: str
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self): return asdict(self)

@dataclass(slots=True)
class ScanResult:
    root: str
    findings: list[Finding] = field(default_factory=list)
    files: int = 0
    scanned_files: int = 0
    skipped_files: int = 0
    duration_ms: int = 0
    mode: str = "fast"
    def to_dict(self):
        counts = {k: 0 for k in ("critical", "high", "medium", "low", "info")}
        for f in self.findings: counts[f.severity] = counts.get(f.severity, 0) + 1
        return {"root": self.root, "files": self.files, "scanned_files": self.scanned_files, "skipped_files": self.skipped_files, "duration_ms": self.duration_ms, "mode": self.mode, "counts": counts, "findings": [f.to_dict() for f in self.findings]}
