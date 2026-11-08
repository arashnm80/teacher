#!/usr/bin/env python3
"""
Simple offline launcher for teacher-playground (Windows lab PCs).

Uses only the Python standard library (tkinter + http.server).
No pip packages required.
"""

from __future__ import annotations

import atexit
import os
import socket
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from tk_bidi import ltr, rtl

ROOT = Path(__file__).resolve().parent
VENDOR_REQUIRED = (
    ROOT / "vendor" / "pyodide" / "pyodide.js",
    ROOT / "vendor" / "pyodide" / "pyodide.asm.js",
    ROOT / "vendor" / "pyodide" / "pyodide.asm.wasm",
    ROOT / "vendor" / "pyodide" / "python_stdlib.zip",
    # Legacy engine for lab PCs whose browser predates Chrome/Edge 96.
    ROOT / "vendor" / "pyodide-legacy" / "pyodide.js",
    ROOT / "vendor" / "pyodide-legacy" / "pyodide.asm.js",
    ROOT / "vendor" / "pyodide-legacy" / "pyodide.asm.wasm",
    ROOT / "vendor" / "pyodide-legacy" / "python_stdlib.zip",
    ROOT / "vendor" / "pyodide-legacy" / "repodata.json",
)
PORT_RANGE = range(8765, 8786)
# Dedicated lock port so a second double-click does not open another launcher.
INSTANCE_LOCK_PORT = 8764
FONT_FA = ("Tahoma", 10)
FONT_FA_TITLE = ("Tahoma", 14, "bold")
FONT_FA_SMALL = ("Tahoma", 8)
FONT_LTR = ("Consolas", 10)


class QuietHandler(SimpleHTTPRequestHandler):
    # Lab Pythons vary; force MIME types Pyodide needs or loadPyodide hangs.
    extensions_map = {
        **getattr(SimpleHTTPRequestHandler, "extensions_map", {}),
        ".html": "text/html",
        ".js": "application/javascript",
        ".mjs": "application/javascript",
        ".css": "text/css",
        ".json": "application/json",
        ".wasm": "application/wasm",
        ".zip": "application/zip",
        ".map": "application/json",
        ".txt": "text/plain",
        ".md": "text/plain",
        "": "application/octet-stream",
    }

    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def acquire_single_instance() -> socket.socket | None:
    """Bind a loopback port as a mutex. None means another launcher is already up."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Exclusive bind — second process fails immediately.
        sock.bind(("127.0.0.1", INSTANCE_LOCK_PORT))
        sock.listen(1)
    except OSError:
        sock.close()
        return None
    return sock


class LauncherApp:
    def __init__(self, lock_sock: socket.socket) -> None:
        self.lock_sock = lock_sock
        self.root = tk.Tk()
        self.root.title(rtl("تمرین پایتون — راه‌انداز"))
        self.root.geometry("480x340")
        self.root.minsize(440, 320)
        self.root.resizable(False, False)

        self.server: ThreadingHTTPServer | None = None
        self.server_thread: threading.Thread | None = None
        self.url = ""
        self.port = 0
        self._closing = False

        self._build_ui()
        self._check_bundle()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        atexit.register(self._release_lock)

    def _release_lock(self) -> None:
        sock = getattr(self, "lock_sock", None)
        if sock is not None:
            try:
                sock.close()
            except OSError:
                pass
            self.lock_sock = None  # type: ignore[assignment]

    def _set_fa(self, widget: ttk.Label, text: str, **kwargs) -> None:
        widget.configure(text=rtl(text), **kwargs)

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, font=FONT_FA_TITLE)
        self._set_fa(title, "تمرین پایتون · پودمان ۱")
        title.pack(anchor="e", padx=8, pady=(0, 4))

        subtitle = ttk.Label(frame, font=FONT_FA_SMALL, wraplength=440, justify="right")
        self._set_fa(subtitle, "همین پنجره را باز بگذارید؛ تمرین در مرورگر اجرا می‌شود.")
        subtitle.pack(anchor="e", padx=8, pady=(0, 10))

        self.status = ttk.Label(frame, font=FONT_FA, foreground="#1f6f4a")
        self._set_fa(self.status, "آمادهٔ شروع")
        self.status.pack(anchor="e", padx=8, pady=(8, 2))

        self.url_label = ttk.Label(
            frame,
            font=FONT_FA,
            foreground="#333333",
            wraplength=440,
            justify="right",
        )
        self._set_fa(self.url_label, "آدرس هنوز ساخته نشده است")
        self.url_label.pack(anchor="e", padx=8, pady=(0, 8))

        self.open_browser = tk.BooleanVar(value=True)
        chk = ttk.Checkbutton(
            frame,
            text=rtl("بعد از شروع، مرورگر را باز کن"),
            variable=self.open_browser,
        )
        chk.pack(anchor="e", padx=8, pady=(10, 8))

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=(4, 8), padx=4)

        self.btn_start = ttk.Button(
            buttons, text=rtl("شروع تمرین"), command=self.start_server
        )
        self.btn_start.pack(side="right", padx=6, ipadx=10, ipady=4)

        self.btn_stop = ttk.Button(
            buttons, text=rtl("توقف"), command=self.stop_server, state="disabled"
        )
        self.btn_stop.pack(side="right", padx=6, ipadx=10, ipady=4)

        self.btn_open = ttk.Button(
            buttons,
            text=rtl("باز کردن مرورگر"),
            command=self.open_page,
            state="disabled",
        )
        self.btn_open.pack(side="left", padx=6, ipadx=6, ipady=4)

        # Tk cannot reliably mix Latin filenames inside Persian sentences —
        # keep them on separate LTR lines.
        tip1 = ttk.Label(frame, font=FONT_FA_SMALL, foreground="#666666", justify="right")
        self._set_fa(tip1, "نکته: فقط همین یک فایل را از پوشه اصلی باز کنید:")
        tip1.pack(anchor="e", padx=8, pady=(14, 0))

        tip_file = ttk.Label(frame, text=ltr("شروع.bat"), font=FONT_LTR, foreground="#444444")
        tip_file.pack(anchor="w", padx=8, pady=(2, 0))

        tip2 = ttk.Label(frame, font=FONT_FA_SMALL, foreground="#666666", justify="right")
        self._set_fa(tip2, "این فایل را مستقیم با دوبارکلیک باز نکنید:")
        tip2.pack(anchor="e", padx=8, pady=(6, 0))

        tip_html = ttk.Label(
            frame, text=ltr("app\\index.html"), font=FONT_LTR, foreground="#444444"
        )
        tip_html.pack(anchor="w", padx=8, pady=(2, 0))

    def _check_bundle(self) -> None:
        missing = [p.name for p in VENDOR_REQUIRED if not p.is_file()]
        if missing:
            self._set_fa(
                self.status,
                "بستهٔ آفلاین ناقص است — پوشهٔ موتور را کامل کپی کنید.",
                foreground="#a33",
            )
            self.btn_start.configure(state="disabled")
            messagebox.showerror(
                rtl("بسته ناقص"),
                rtl(
                    "فایل‌های موتور پایتون آفلاین پیدا نشد.\n"
                    "کل پوشهٔ برنامه را دوباره کپی کنید."
                )
                + "\n\n"
                + ltr("Missing:\n- " + "\n- ".join(missing)),
                parent=self.root,
            )

    def _find_port(self) -> int:
        for port in PORT_RANGE:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    sock.bind(("127.0.0.1", port))
                except OSError:
                    continue
                return port
        raise RuntimeError("no free port")

    def start_server(self) -> None:
        if self.server is not None:
            return
        try:
            port = self._find_port()
            handler = partial(QuietHandler, directory=str(ROOT))
            server = ThreadingHTTPServer(("127.0.0.1", port), handler)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror(
                rtl("خطا"),
                rtl("نتوانستم سرور را روشن کنم.") + "\n" + ltr(str(exc)),
                parent=self.root,
            )
            return

        self.server = server
        self.port = port
        self.url = f"http://127.0.0.1:{port}/"
        self.server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        self.server_thread.start()

        self.url_label.configure(
            text=ltr(self.url),
            font=FONT_LTR,
            justify="left",
            foreground="#111111",
        )
        self.url_label.pack_configure(anchor="w")
        self._set_fa(self.status, "در حال اجرا — این پنجره را نبندید", foreground="#1f6f4a")
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.btn_open.configure(state="normal")

        if self.open_browser.get():
            self.open_page()

    def stop_server(self) -> None:
        server = self.server
        if server is None:
            return
        self.server = None
        self.url = ""
        self.port = 0

        def _shutdown() -> None:
            try:
                server.shutdown()
            except Exception:  # noqa: BLE001
                pass
            try:
                server.server_close()
            except Exception:  # noqa: BLE001
                pass

        threading.Thread(target=_shutdown, daemon=True).start()

        self._set_fa(self.url_label, "آدرس هنوز ساخته نشده است")
        self.url_label.configure(font=FONT_FA, justify="right", foreground="#333333")
        self.url_label.pack_configure(anchor="e")
        self._set_fa(self.status, "متوقف شد", foreground="#666666")
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.btn_open.configure(state="disabled")

    def open_page(self) -> None:
        if not self.url:
            return
        try:
            webbrowser.open(self.url)
        except Exception as exc:  # noqa: BLE001
            messagebox.showwarning(
                rtl("مرورگر"),
                rtl("نتوانستم مرورگر را باز کنم. این آدرس را خودتان باز کنید:")
                + "\n"
                + ltr(self.url)
                + "\n"
                + ltr(str(exc)),
                parent=self.root,
            )

    def _on_close(self) -> None:
        if self._closing:
            return
        if self.server is not None:
            ok = messagebox.askokcancel(
                rtl("خروج"),
                rtl("سرور تمرین خاموش شود و برنامه بسته شود؟"),
                parent=self.root,
            )
            if not ok:
                return
            self.stop_server()
        self._closing = True
        self._release_lock()
        try:
            self.root.quit()
        except tk.TclError:
            pass
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def run(self) -> None:
        self.root.mainloop()


def _notify_already_running() -> None:
    root = tk.Tk()
    root.withdraw()
    try:
        messagebox.showinfo(
            rtl("در حال اجرا"),
            rtl("راه‌انداز از قبل باز است. همان پنجره را استفاده کنید."),
            parent=root,
        )
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass


def main() -> None:
    try:
        os.chdir(ROOT)
    except OSError:
        pass

    lock = acquire_single_instance()
    if lock is None:
        _notify_already_running()
        return

    app = LauncherApp(lock)
    try:
        app.run()
    finally:
        app._release_lock()


if __name__ == "__main__":
    main()
