from dataclasses import dataclass, field, asdict
from pathlib import Path
import json

DEFAULT_IGNORES = [".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "target", ".nexus", ".idea", ".pytest_cache", ".mypy_cache"]

@dataclass
class Config:
    root: Path
    max_file_bytes: int = 4_000_000
    include_hidden: bool = False
    workers: int = 0
    ignore: list[str] = field(default_factory=lambda: list(DEFAULT_IGNORES))
    agent_url: str = "http://127.0.0.1:11434"
    agent_model: str = "qwen2.5-coder:7b"
    agent_timeout: int = 180
    allow_remote_agent: bool = False
    scan_mode: str = "fast"
    def file(self): return self.root / ".nexus" / "config.json"
    def save(self):
        p=self.file(); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps({"max_file_bytes":self.max_file_bytes,"include_hidden":self.include_hidden,"workers":self.workers,"ignore":self.ignore,"agent_url":self.agent_url,"agent_model":self.agent_model,"agent_timeout":self.agent_timeout,"allow_remote_agent":self.allow_remote_agent,"scan_mode":self.scan_mode}, indent=2, ensure_ascii=False), encoding="utf-8")
    @classmethod
    def load(cls, root: Path):
        root=root.resolve(); cfg=cls(root)
        p=cfg.file()
        if p.exists():
            try:
                data=json.loads(p.read_text(encoding="utf-8"))
                for k,v in data.items():
                    if hasattr(cfg,k): setattr(cfg,k,v)
            except (OSError, ValueError):
                pass
        return cfg
