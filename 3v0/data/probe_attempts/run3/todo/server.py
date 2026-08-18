#!/usr/bin/env python3
"""probe020: minimal Todo REST service with file persistence, restart-survival,
concurrency safety, and Idempotency-Key dedup. stdlib only."""
import json, os, re, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

DB = os.environ.get("TODO_DB", os.path.join(os.path.dirname(__file__), "todos.json"))
HOST, PORT = "127.0.0.1", int(os.environ.get("TODO_PORT", "8080"))

_lock = threading.Lock()
_todos = {}          # id -> {id, title, done}
_next = 1
_keys = {}           # idempotency key -> id
_dirty = False


def _load():
    global _todos, _next
    try:
        with open(DB) as f:
            _todos = {int(k): v for k, v in json.load(f).items()}
        _next = (max(_todos) + 1) if _todos else 1
    except FileNotFoundError:
        _todos, _next = {}, 1


def _save():
    with open(DB, "w") as f:
        json.dump(_todos, f)


def _read_body(self):
    n = int(self.headers.get("Content-Length", 0) or 0)
    return self.rfile.read(n).decode("utf-8", "replace") if n else ""


class H(BaseHTTPRequestHandler):
    server_version = "Todo/1.0"

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _todo(self, tid, mutate):
        with _lock:
            t = _todos.get(tid)
            if t is None:
                return None, None
            return t, (t.copy() if not mutate else t)

    def do_POST(self):
        global _next, _dirty
        if urlparse(self.path).path != "/todos":
            return self._send(404, {"error": "not found"})
        ik = self.headers.get("Idempotency-Key")
        with _lock:
            if ik and ik in _keys:
                existing = _todos[_keys[ik]]
                return self._send(200, {"id": existing["id"], "dup": True, "todo": existing})
            try:
                title = json.loads(_read_body(self)).get("title", "")
            except Exception:
                title = ""
            if not isinstance(title, str) or title.strip() == "":
                return self._send(400, {"error": "empty title"})
            t = {"id": _next, "title": title, "done": False}
            _todos[_next] = t
            if ik:
                _keys[ik] = _next
            _next += 1
            _dirty = True
            _save()
            return self._send(201, t)

    def do_GET(self):
        m = re.fullmatch(r"/todos(?:/(\d+))?", urlparse(self.path).path)
        if not m:
            return self._send(404, {"error": "not found"})
        if m.group(1) is None:
            with _lock:
                return self._send(200, list(_todos.values()))
        tid = int(m.group(1))
        with _lock:
            t = _todos.get(tid)
        if t is None:
            return self._send(404, {"error": "todo not found"})
        return self._send(200, t)

    def do_PUT(self):
        global _dirty
        m = re.fullmatch(r"/todos/(\d+)", urlparse(self.path).path)
        if not m:
            return self._send(404, {"error": "not found"})
        with _lock:
            t = _todos.get(int(m.group(1)))
            if t is None:
                return self._send(404, {"error": "todo not found"})
            try:
                patch = json.loads(_read_body(self))
            except Exception:
                patch = {}
            if "title" in patch and isinstance(patch["title"], str) and patch["title"].strip():
                t["title"] = patch["title"]
            if "done" in patch and isinstance(patch["done"], bool):
                t["done"] = patch["done"]
            _dirty = True
            _save()
            return self._send(200, t)

    def do_DELETE(self):
        global _dirty
        m = re.fullmatch(r"/todos/(\d+)", urlparse(self.path).path)
        if not m:
            return self._send(404, {"error": "not found"})
        with _lock:
            if int(m.group(1)) not in _todos:
                return self._send(404, {"error": "todo not found"})
            del _todos[int(m.group(1))]
            _dirty = True
            _save()
        return self._send(200, {"ok": True})

    def log_message(self, format, *args):
        pass


def main():
    if os.environ.get("TODO_FRESH") == "1" and os.path.exists(DB):
        os.remove(DB)
    _load()
    srv = ThreadingHTTPServer((HOST, PORT), H)
    print(f"todo-server on {HOST}:{PORT} (db={DB})", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
