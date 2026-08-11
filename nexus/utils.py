from pathlib import Path
import hashlib, json, os, re, subprocess, time
from typing import Iterable

TEXT_EXTS={".py",".pyi",".js",".jsx",".mjs",".cjs",".ts",".tsx",".java",".kt",".kts",".go",".rs",".rb",".php",".c",".h",".cc",".cpp",".hpp",".cs",".swift",".scala",".sh",".bash",".zsh",".yaml",".yml",".json",".toml",".ini",".cfg",".conf",".env",".md",".txt",".html",".css",".sql",".xml",".gradle",".properties"}
SPECIAL_NAMES={"Dockerfile","Containerfile","Makefile","CMakeLists.txt","Gemfile","Rakefile","Jenkinsfile"}
BINARY_EXTS={".png",".jpg",".jpeg",".gif",".webp",".ico",".pdf",".zip",".gz",".tar",".7z",".exe",".dll",".so",".dylib",".bin",".woff",".woff2",".ttf",".mp3",".mp4",".mov"}

def now_ms(): return time.time_ns() // 1_000_000
def sha256_bytes(data: bytes): return hashlib.sha256(data).hexdigest()
def sha256_file(path: Path, chunk=1024*1024):
    h=hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b=f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()
def stable_id(*parts): return hashlib.sha256("\0".join(str(x) for x in parts).encode()).hexdigest()[:24]
def rel(path: Path, root: Path): return path.resolve().relative_to(root.resolve()).as_posix()
def read_text(path: Path, limit=4_000_000):
    try:
        data=path.read_bytes()
        if b"\x00" in data[:8192]: return ""
        return data[:limit].decode("utf-8", "ignore")
    except OSError: return ""
def file_language(path: Path):
    s=path.suffix.lower()
    m={".py":"python",".pyi":"python",".js":"javascript",".jsx":"javascript",".mjs":"javascript",".cjs":"javascript",".ts":"typescript",".tsx":"typescript",".java":"java",".kt":"kotlin",".kts":"kotlin",".go":"go",".rs":"rust",".rb":"ruby",".php":"php",".c":"c",".h":"c",".cc":"cpp",".cpp":"cpp",".hpp":"cpp",".cs":"csharp",".swift":"swift",".scala":"scala",".sh":"shell",".bash":"shell",".zsh":"shell",".yaml":"yaml",".yml":"yaml",".json":"json",".toml":"toml",".xml":"xml",".sql":"sql",".html":"html",".css":"css",".gradle":"gradle",".properties":"properties"}
    if path.name in SPECIAL_NAMES: return "special"
    return m.get(s,"text")
def iter_files(root: Path, cfg, include_large=False):
    root=root.resolve(); ignores=set(cfg.ignore)
    for base,dirs,names in os.walk(root, topdown=True, followlinks=False):
        basep=Path(base)
        dirs[:] = sorted(d for d in dirs if d not in ignores and (cfg.include_hidden or not d.startswith(".")))
        for name in sorted(names):
            if name in ignores: continue
            p=basep/name
            try:
                st=p.stat()
                if not include_large and st.st_size > cfg.max_file_bytes: continue
                if p.suffix.lower() in BINARY_EXTS: continue
                if p.suffix.lower() not in TEXT_EXTS and p.name not in SPECIAL_NAMES: continue
                yield p,st
            except OSError:
                continue
def safe_json_write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding="utf-8")
    os.replace(tmp,path)
def run_cmd(args, cwd=None, timeout=30):
    try:
        cp=subprocess.run(args,cwd=cwd,capture_output=True,text=True,timeout=timeout,shell=False,encoding="utf-8",errors="replace")
        return cp.returncode,cp.stdout,cp.stderr
    except subprocess.TimeoutExpired as e:
        return 124,"",str(e)
    except OSError as e:
        return 127,"",str(e)
def is_loopback_url(url):
    return bool(re.match(r"^https?://(?:127\.0\.0\.1|localhost|\[::1\])(?::\d+)?(?:/|$)",url,re.I))
def line_col(text, pos):
    line=text.count("\n",0,pos)+1
    last=text.rfind("\n",0,pos)
    return line,pos-last
