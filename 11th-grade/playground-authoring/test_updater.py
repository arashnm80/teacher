"""Tests for the offline copy's updater (playground/app/updater.py) against a fake website."""
import hashlib
import http.server
import json
import shutil
import sys
import tempfile
import threading
import unittest
from functools import partial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "playground" / "app"))
import updater  # noqa: E402


def entry(data: bytes, url=None):
    info = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
    if url:
        info["url"] = url
    return info


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class UpdaterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="updater-"))
        self.web = self.tmp / "web"
        self.copy = self.tmp / "copy"
        self.web.mkdir()
        self.copy.mkdir()
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(self.web)))
        self.url = f"http://127.0.0.1:{server.server_address[1]}/"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.server = server

    def tearDown(self):
        self.server.shutdown()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def publish(self, files: dict, version: str, variants=None):
        """Puts `files` (path -> bytes) on the fake website and writes its manifest."""
        manifest = {"format": 1, "version": version, "built": "2026-11-16T00:00:00Z", "files": {}}
        for rel, data in files.items():
            url = (variants or {}).get(rel)
            target = self.web / (url or rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            manifest["files"][rel] = entry(data, url)
        (self.web / updater.MANIFEST_NAME).write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        return manifest

    def install(self, files: dict, version: str):
        manifest = {"format": 1, "version": version, "files": {}}
        for rel, data in files.items():
            (self.copy / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.copy / rel).write_bytes(data)
            manifest["files"][rel] = entry(data)
        (self.copy / updater.MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")

    def test_check_says_there_is_nothing_new_when_versions_match(self):
        files = {"index.html": b"<html>1</html>"}
        self.publish(files, "v1")
        self.install(files, "v1")
        result = updater.check(self.copy, self.url)
        self.assertFalse(result["update"])
        self.assertEqual(result["current"], "v1")

    def test_check_counts_only_the_files_that_changed(self):
        old = {"index.html": b"old", "book/a.html": b"a", "gone.txt": b"x"}
        self.install(old, "v1")
        self.publish({"index.html": b"new page", "book/a.html": b"a", "book/b.html": b"brand new"}, "v2")
        result = updater.check(self.copy, self.url)
        self.assertTrue(result["update"])
        self.assertEqual((result["current"], result["latest"]), ("v1", "v2"))
        self.assertEqual(result["files"], 2)  # index.html changed, book/b.html is new
        self.assertEqual(result["bytes"], len(b"new page") + len(b"brand new"))

    def test_apply_downloads_changes_removes_old_files_and_keeps_the_rest(self):
        self.install({"index.html": b"old", "book/a.html": b"a", "gone.txt": b"x"}, "v1")
        (self.copy / "my-notes.txt").write_text("not in any manifest", encoding="utf-8")
        self.publish({"index.html": b"new page", "book/a.html": b"a", "book/b.html": b"brand new",
                      "\u0634\u0631\u0648\u0639.bat": b"@echo off"}, "v2")
        steps = []
        result = updater.apply(self.copy, self.url, lambda done, total, rel: steps.append((done, total)))
        self.assertEqual(result, {"updated": 3, "removed": 1, "version": "v2"})
        self.assertEqual((self.copy / "index.html").read_bytes(), b"new page")
        self.assertEqual((self.copy / "book/b.html").read_bytes(), b"brand new")
        self.assertEqual((self.copy / "\u0634\u0631\u0648\u0639.bat").read_bytes(), b"@echo off")
        self.assertFalse((self.copy / "gone.txt").exists(), "a file the website no longer has is removed")
        self.assertTrue((self.copy / "my-notes.txt").exists(), "files that were never in a manifest are left alone")
        self.assertEqual(updater.load_local(self.copy)["version"], "v2")
        self.assertEqual(steps[-1], (3, 3))
        self.assertFalse((self.copy / updater.STAGING).exists())
        self.assertFalse(updater.check(self.copy, self.url)["update"])

    def test_files_that_differ_in_the_offline_copy_come_from_their_own_address(self):
        self.install({"playground/index.html": b"online page"}, "v1")
        self.publish({"playground/index.html": b"offline page"}, "v2",
                     variants={"playground/index.html": "offline-files/playground/index.html"})
        updater.apply(self.copy, self.url)
        self.assertEqual((self.copy / "playground/index.html").read_bytes(), b"offline page")

    def test_a_file_that_does_not_match_its_hash_stops_the_update_and_changes_nothing(self):
        self.install({"index.html": b"old", "b.html": b"b"}, "v1")
        manifest = self.publish({"index.html": b"new", "b.html": b"b2"}, "v2")
        (self.web / "b.html").write_bytes(b"tampered!")  # the website's file no longer matches the manifest
        with self.assertRaises(updater.UpdateError):
            updater.apply(self.copy, self.url)
        self.assertEqual((self.copy / "index.html").read_bytes(), b"old", "nothing is replaced unless all files arrive")
        self.assertEqual(updater.load_local(self.copy)["version"], "v1")
        self.assertFalse((self.copy / updater.STAGING).exists())

    def test_paths_outside_the_copy_are_refused(self):
        for bad in ("../evil.txt", "/etc/passwd", "a/../../b", "C:/x", "a\\b", "", "a//b"):
            with self.assertRaises(updater.UpdateError, msg=bad):
                updater.safe_path(self.copy, bad)
        self.assertEqual(updater.safe_path(self.copy, "book/p1.html"), self.copy / "book" / "p1.html")

    def test_no_connection_is_reported_as_offline(self):
        self.server.shutdown()
        with self.assertRaises(updater.UpdateError) as caught:
            updater.check(self.copy, "http://127.0.0.1:9/")
        self.assertEqual(str(caught.exception), "offline")

    def test_the_handler_answers_only_its_own_page(self):
        self.install({"a": b"1"}, "v1")
        self.publish({"a": b"2"}, "v2")
        up = updater.Updater(self.copy, self.url)
        good = {"Host": "127.0.0.1:8765"}
        self.assertIsNone(updater.handle_request(up, "GET", "/index.html", good, 8765))
        status, body = updater.handle_request(up, "GET", "/__update/check", good, 8765)
        self.assertEqual((status, body["update"], body["latest"]), (200, True, "v2"))
        self.assertEqual(updater.handle_request(up, "GET", "/__update/check", {"Host": "evil.example:8765"}, 8765)[0], 403)
        self.assertEqual(updater.handle_request(up, "POST", "/__update/apply", good, 8765)[0], 403, "needs the custom header")
        self.assertEqual(updater.handle_request(up, "GET", "/__update/nothing", good, 8765)[0], 404)

    def test_applying_through_the_handler_runs_in_the_background(self):
        self.install({"a": b"1"}, "v1")
        self.publish({"a": b"2"}, "v2")
        up = updater.Updater(self.copy, self.url)
        headers = {"Host": "127.0.0.1:8765", "X-Teacher-Update": "1"}
        status, _ = updater.handle_request(up, "POST", "/__update/apply", headers, 8765)
        self.assertEqual(status, 200)
        for _ in range(200):
            snap = up.snapshot()
            if snap["state"] != "running":
                break
            threading.Event().wait(0.05)
        self.assertEqual(up.snapshot()["state"], "done")
        self.assertEqual((self.copy / "a").read_bytes(), b"2")


if __name__ == "__main__":
    unittest.main(verbosity=2)
