"""Updates the offline copy from the teacher's website. Python standard library only.

The copy keeps `offline-manifest.json` at its top folder: every file with its SHA-256. The website
publishes the same kind of file for its latest build. An update downloads only the files that
differ, checks each one against the hash in the manifest, and replaces files only after everything
has arrived intact, so a broken connection never leaves a half-updated copy.

The student's progress is kept by the browser, not in these files, so an update never touches it.

The launcher calls `handle_request` for the three addresses under /__update/. They answer only
the page that this launcher serves (same host and port).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath

SITE_URL = "https://teacher.arashnm80.ir/"
MANIFEST_NAME = "offline-manifest.json"
STAGING = ".update-staging"
TIMEOUT = 20
USER_AGENT = "offline-copy-updater"


class UpdateError(Exception):
    """A problem the student can be told about in a sentence."""


def _get(url: str, timeout: int = TIMEOUT) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except (urllib.error.URLError, OSError, ValueError) as err:
        raise UpdateError("offline") from err


def safe_path(root: Path, rel: str) -> Path:
    """A manifest path inside `root`, or an error: nothing outside the copy may be written."""
    pure = PurePosixPath(rel)
    if not rel or pure.is_absolute() or "\\" in rel or ":" in rel or "//" in rel or any(part in ("", ".", "..") for part in pure.parts):
        raise UpdateError(f"unsafe path in the manifest: {rel[:60]}")
    return root.joinpath(*pure.parts)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_manifest(raw: bytes) -> dict:
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as err:
        raise UpdateError("the manifest is not readable") from err
    if not isinstance(manifest, dict) or manifest.get("format") != 1 or not isinstance(manifest.get("files"), dict):
        raise UpdateError("the manifest is not in a known format")
    return manifest


def load_local(root: Path) -> dict | None:
    path = root / MANIFEST_NAME
    if not path.is_file():
        return None
    try:
        return read_manifest(path.read_bytes())
    except UpdateError:
        return None


def fetch_remote(site_url: str = SITE_URL) -> tuple[dict, bytes]:
    raw = _get(site_url + MANIFEST_NAME)
    return read_manifest(raw), raw


def plan(root: Path, local: dict | None, remote: dict) -> dict:
    """What has to be downloaded and what has to be removed."""
    old = (local or {}).get("files", {})
    download = []
    for rel, info in remote["files"].items():
        dest = safe_path(root, rel)
        same_as_before = rel in old and old[rel].get("sha256") == info["sha256"]
        if dest.is_file() and dest.stat().st_size == info["size"] and (same_as_before or sha256_file(dest) == info["sha256"]):
            continue
        download.append((rel, info))
    remove = [rel for rel in old if rel not in remote["files"] and safe_path(root, rel).is_file()]
    return {"download": download, "remove": remove, "bytes": sum(info["size"] for _, info in download)}


def check(root: Path, site_url: str = SITE_URL) -> dict:
    remote, _ = fetch_remote(site_url)
    local = load_local(root)
    current = (local or {}).get("version", "")
    result = {"ok": True, "current": current, "latest": remote.get("version", ""), "built": remote.get("built", "")}
    if current == result["latest"]:
        return {**result, "update": False, "files": 0, "bytes": 0}
    todo = plan(root, local, remote)
    return {**result, "update": bool(todo["download"] or todo["remove"] or not local),
            "files": len(todo["download"]), "bytes": todo["bytes"]}


def apply(root: Path, site_url: str = SITE_URL, progress=None) -> dict:
    remote, raw = fetch_remote(site_url)
    todo = plan(root, load_local(root), remote)
    staging = root / STAGING
    shutil.rmtree(staging, ignore_errors=True)
    total = len(todo["download"])
    try:
        for done, (rel, info) in enumerate(todo["download"], 1):
            data = _get(site_url + urllib.parse.quote(info.get("url", rel)), timeout=60)
            if len(data) != info["size"] or hashlib.sha256(data).hexdigest() != info["sha256"]:
                raise UpdateError(f"{rel} did not download correctly")
            out = safe_path(staging, rel)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            if progress:
                progress(done, total, rel)
        # Everything arrived and matches its hash: now replace the files.
        for rel, _ in todo["download"]:
            dest = safe_path(root, rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            os.replace(safe_path(staging, rel), dest)
        for rel in todo["remove"]:
            safe_path(root, rel).unlink(missing_ok=True)
        (root / MANIFEST_NAME).write_bytes(raw)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return {"updated": total, "removed": len(todo["remove"]), "version": remote.get("version", "")}


class Updater:
    """Runs an update in the background and reports how far it is."""

    def __init__(self, root: Path, site_url: str = SITE_URL):
        self.root = root
        self.site_url = site_url
        self.lock = threading.Lock()
        self.status = {"state": "idle", "done": 0, "total": 0, "message": "", "version": ""}

    def snapshot(self) -> dict:
        with self.lock:
            return dict(self.status)

    def _set(self, **values) -> None:
        with self.lock:
            self.status.update(values)

    def start(self) -> dict:
        with self.lock:
            if self.status["state"] == "running":
                return dict(self.status)
            self.status = {"state": "running", "done": 0, "total": 0, "message": "", "version": ""}
        threading.Thread(target=self._run, daemon=True).start()
        return self.snapshot()

    def _run(self) -> None:
        try:
            result = apply(self.root, self.site_url, lambda done, total, rel: self._set(done=done, total=total, message=rel))
            self._set(state="done", version=result["version"], message="")
        except UpdateError as err:
            self._set(state="error", message=str(err))
        except Exception as err:  # noqa: BLE001 - the page shows a sentence, never a traceback
            self._set(state="error", message=f"unexpected: {err.__class__.__name__}")


def handle_request(updater: Updater, method: str, path: str, headers, port: int) -> tuple[int, dict] | None:
    """Answers /__update/check, /__update/apply and /__update/status; None for any other path.

    Only the page this launcher serves may ask: the Host must be this server's own address, and
    starting an update needs a custom header that another website cannot send across sites.
    """
    route = urllib.parse.urlsplit(path).path
    if not route.startswith("/__update/"):
        return None
    if headers.get("Host", "") not in (f"127.0.0.1:{port}", f"localhost:{port}"):
        return 403, {"ok": False, "error": "forbidden"}
    if route == "/__update/status" and method == "GET":
        return 200, {"ok": True, **updater.snapshot()}
    if route == "/__update/check" and method == "GET":
        try:
            return 200, check(updater.root, updater.site_url)
        except UpdateError as err:
            return 200, {"ok": False, "error": str(err)}
    if route == "/__update/apply" and method == "POST":
        if headers.get("X-Teacher-Update") != "1":
            return 403, {"ok": False, "error": "forbidden"}
        return 200, {"ok": True, **updater.start()}
    return 404, {"ok": False, "error": "not_found"}
