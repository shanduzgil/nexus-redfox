from pathlib import Path
import sqlite3, json, os
from .config import Config
from .utils import sha256_file, rel, file_language, stable_id

SCHEMA="""CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, sha256 TEXT NOT NULL, size INTEGER NOT NULL, mtime_ns INTEGER NOT NULL, language TEXT NOT NULL);CREATE TABLE IF NOT EXISTS symbols(id TEXT PRIMARY KEY, kind TEXT NOT NULL, name TEXT NOT NULL, path TEXT NOT NULL, line INTEGER NOT NULL);CREATE TABLE IF NOT EXISTS edges(source TEXT NOT NULL,target TEXT NOT NULL,kind TEXT NOT NULL,PRIMARY KEY(source,target,kind));CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);"""

class ProjectIndex:
    def __init__(self,root:Path):
        self.root=root.resolve(); p=self.root/".nexus"/"index.db"; p.parent.mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(p); self.db.executescript(SCHEMA); self.db.commit()
    def close(self): self.db.close()
    def changed_files(self,cfg):
        rows={r[0]:r[1:] for r in self.db.execute("SELECT path,sha256,size,mtime_ns FROM files")}; changed=[]; seen=set()
        from .utils import iter_files
        for p,st in iter_files(self.root,cfg):
            rp=rel(p,self.root); seen.add(rp); old=rows.get(rp)
            if old and old[1]==st.st_size and old[2]==st.st_mtime_ns:
                continue
            digest=sha256_file(p)
            if old and old[0]==digest: continue
            changed.append((p,rp,digest,st));
        removed=set(rows)-seen
        return changed,removed
    def update_files(self,cfg,scan_symbols):
        changed,removed=self.changed_files(cfg)
        cur=self.db.cursor()
        for rp in removed:
            cur.execute("DELETE FROM files WHERE path=?",(rp,)); cur.execute("DELETE FROM symbols WHERE path=?",(rp,))
        for p,rp,digest,st in changed:
            cur.execute("INSERT OR REPLACE INTO files(path,sha256,size,mtime_ns,language) VALUES(?,?,?,?,?)",(rp,digest,st.st_size,st.st_mtime_ns,file_language(p)))
            cur.execute("DELETE FROM symbols WHERE path=?",(rp,))
            for s in scan_symbols(p,rp): cur.execute("INSERT OR REPLACE INTO symbols(id,kind,name,path,line) VALUES(?,?,?,?,?)",s)
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('last_update_ns',?)",(str(os.times().elapsed),))
        self.db.commit(); return changed,removed
    def file_rows(self): return self.db.execute("SELECT path,sha256,size,mtime_ns,language FROM files ORDER BY path").fetchall()
    def symbol_rows(self): return self.db.execute("SELECT id,kind,name,path,line FROM symbols ORDER BY path,line,name").fetchall()
    def set_graph(self,nodes,edges):
        cur=self.db.cursor(); cur.execute("DELETE FROM edges")
        for e in edges: cur.execute("INSERT OR IGNORE INTO edges(source,target,kind) VALUES(?,?,?)",e)
        self.db.commit()
    def reverse_edges(self,node_id): return self.db.execute("SELECT source,kind FROM edges WHERE target=?",(node_id,)).fetchall()
    def search(self,q):
        like=f"%{q}%"; return self.db.execute("SELECT id,kind,name,path,line FROM symbols WHERE name LIKE ? OR path LIKE ? ORDER BY path,line LIMIT 100",(like,like)).fetchall()
