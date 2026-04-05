#!/usr/bin/env python3
"""
GTA V Solo Public Lobby Tool
Professional GUI for Windows 11
Suspends GTA5.exe to kick other players, leaving you in a solo public session.
"""

import sys
import ctypes
import threading
import time
from datetime import datetime

import psutil
import customtkinter as ctk

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PROCESS_NAME    = "GTA5.exe"
DEFAULT_WAIT    = 8          # seconds
COLOR_BG_HEADER = "#0f0f1a"
COLOR_GREEN     = "#00e676"
COLOR_RED       = "#ff1744"
COLOR_BLUE      = "#1565C0"
COLOR_BLUE_HOV  = "#0D47A1"
COLOR_ORANGE    = "#FF6D00"
COLOR_ORANGE_HOV= "#E65100"
COLOR_DIM       = "#555566"
COLOR_TEXT      = "#e0e0e0"
COLOR_SUBTEXT   = "#888899"
COLOR_LOG_BG    = "#080810"


# ── Main Window ────────────────────────────────────────────────────────────────
class SoloLobbyApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("GTA V — Solo Public Lobby Tool")
        self.geometry("540x700")
        self.resizable(False, False)
        self._center()

        self.is_running   = False
        self.wait_var     = ctk.IntVar(value=DEFAULT_WAIT)
        self._poll_job    = None

        self._build_ui()
        self._start_status_poll()

    # ── Layout ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header bar ──
        header = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_HEADER, height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="GTA V  ·  Solo Public Lobby",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=COLOR_TEXT,
        ).place(relx=0.5, rely=0.38, anchor="center")

        ctk.CTkLabel(
            header,
            text="Isolate your session — keep businesses & CEO work running",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_SUBTEXT,
        ).place(relx=0.5, rely=0.72, anchor="center")

        # ── Process status card ──
        self._status_card()

        # ── Settings card ──
        self._settings_card()

        # ── Progress card ──
        self._progress_card()

        # ── Action button ──
        self.action_btn = ctk.CTkButton(
            self,
            text="  Launch Solo Session",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            height=54,
            corner_radius=10,
            command=self._on_action,
            fg_color=COLOR_BLUE,
            hover_color=COLOR_BLUE_HOV,
            state="disabled",
        )
        self.action_btn.pack(fill="x", padx=20, pady=(10, 4))

        # ── Log card ──
        self._log_card()

        # ── Footer ──
        ctk.CTkLabel(
            self,
            text="Run as Administrator for best results  ·  Works in any public session",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_DIM,
        ).pack(pady=(0, 10))

    def _status_card(self):
        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(fill="x", padx=20, pady=(14, 5))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            inner,
            text="PROCESS STATUS",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=COLOR_DIM,
        ).pack(anchor="w")

        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x", pady=(6, 0))

        self.dot_lbl = ctk.CTkLabel(
            row, text="●",
            font=ctk.CTkFont(size=20),
            text_color=COLOR_RED,
            width=28,
        )
        self.dot_lbl.pack(side="left")

        self.proc_lbl = ctk.CTkLabel(
            row,
            text="GTA5.exe — not detected",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLOR_TEXT,
        )
        self.proc_lbl.pack(side="left", padx=(4, 0))

        self.pid_lbl = ctk.CTkLabel(
            row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_DIM,
        )
        self.pid_lbl.pack(side="right")

    def _settings_card(self):
        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(fill="x", padx=20, pady=5)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=14)

        header_row = ctk.CTkFrame(inner, fg_color="transparent")
        header_row.pack(fill="x")

        ctk.CTkLabel(
            header_row,
            text="SUSPEND DURATION",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=COLOR_DIM,
        ).pack(side="left")

        ctk.CTkLabel(
            header_row,
            text="Recommended: 7–10 s",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_DIM,
        ).pack(side="right")

        slider_row = ctk.CTkFrame(inner, fg_color="transparent")
        slider_row.pack(fill="x", pady=(8, 0))

        self.slider = ctk.CTkSlider(
            slider_row,
            from_=5, to=15,
            number_of_steps=10,
            variable=self.wait_var,
            command=self._on_slider,
        )
        self.slider.pack(side="left", fill="x", expand=True, padx=(0, 12))

        self.slider_val_lbl = ctk.CTkLabel(
            slider_row,
            text=f"{DEFAULT_WAIT} s",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=COLOR_TEXT,
            width=40,
        )
        self.slider_val_lbl.pack(side="right")

    def _progress_card(self):
        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(fill="x", padx=20, pady=5)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            inner,
            text="PROGRESS",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=COLOR_DIM,
        ).pack(anchor="w")

        self.progress_bar = ctk.CTkProgressBar(inner, height=10, corner_radius=5)
        self.progress_bar.pack(fill="x", pady=(8, 5))
        self.progress_bar.set(0)

        self.progress_lbl = ctk.CTkLabel(
            inner,
            text="Waiting for GTA V…",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COLOR_SUBTEXT,
        )
        self.progress_lbl.pack(anchor="w")

    def _log_card(self):
        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(fill="both", expand=True, padx=20, pady=(5, 8))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=14)

        log_header = ctk.CTkFrame(inner, fg_color="transparent")
        log_header.pack(fill="x")

        ctk.CTkLabel(
            log_header,
            text="EVENT LOG",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=COLOR_DIM,
        ).pack(side="left")

        clear_btn = ctk.CTkButton(
            log_header,
            text="Clear",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            width=50, height=22,
            corner_radius=6,
            fg_color="transparent",
            border_width=1,
            border_color=COLOR_DIM,
            text_color=COLOR_DIM,
            hover_color="#1a1a2e",
            command=self._clear_log,
        )
        clear_btn.pack(side="right")

        self.log_box = ctk.CTkTextbox(
            inner,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=COLOR_LOG_BG,
            corner_radius=6,
            state="disabled",
            wrap="word",
        )
        self.log_box.pack(fill="both", expand=True, pady=(8, 0))

    # ── Logic ──────────────────────────────────────────────────────────────────

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw - 540) // 2
        y = (sh - 700) // 2
        self.geometry(f"540x700+{x}+{y}")

    def _log(self, msg: str, color: str = COLOR_TEXT):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def _on_slider(self, value):
        self.slider_val_lbl.configure(text=f"{int(value)} s")

    def _find_gta(self):
        for p in psutil.process_iter(["pid", "name"]):
            if p.info["name"] and p.info["name"].lower() == PROCESS_NAME.lower():
                return p
        return None

    def _start_status_poll(self):
        self._poll_status()

    def _poll_status(self):
        proc = self._find_gta()
        if proc:
            self.dot_lbl.configure(text_color=COLOR_GREEN)
            self.proc_lbl.configure(text="GTA5.exe — Running")
            self.pid_lbl.configure(text=f"PID {proc.pid}")
            if not self.is_running:
                self.action_btn.configure(state="normal")
                self.progress_lbl.configure(text="Ready — click the button to isolate your session")
        else:
            self.dot_lbl.configure(text_color=COLOR_RED)
            self.proc_lbl.configure(text="GTA5.exe — Not Detected")
            self.pid_lbl.configure(text="")
            if not self.is_running:
                self.action_btn.configure(state="disabled")
                self.progress_lbl.configure(text="Launch GTA V to continue…")

        self._poll_job = self.after(2000, self._poll_status)

    def _on_action(self):
        if self.is_running:
            return
        threading.Thread(target=self._run_sequence, daemon=True).start()

    def _run_sequence(self):
        self.is_running = True
        wait = self.wait_var.get()

        self.after(0, lambda: self.action_btn.configure(state="disabled", text="  Working…"))
        self.after(0, lambda: self.progress_bar.set(0.05))

        proc = self._find_gta()
        if not proc:
            self.after(0, lambda: self._log("ERROR: GTA5.exe not found — launch GTA V first."))
            self._reset_ui()
            return

        self.after(0, lambda: self._log(f"Found GTA5.exe  (PID {proc.pid})"))
        self.after(0, lambda: self._log(f"Suspending process for {wait} seconds…"))
        self.after(0, lambda: self.progress_lbl.configure(text="Suspending GTA5.exe…"))

        try:
            proc.suspend()
        except psutil.AccessDenied:
            self.after(0, lambda: self._log("ERROR: Access Denied — restart the tool as Administrator."))
            self.after(0, lambda: self.progress_lbl.configure(text="Failed — run as Administrator"))
            self._reset_ui()
            return
        except psutil.NoSuchProcess:
            self.after(0, lambda: self._log("ERROR: GTA5.exe closed before suspend."))
            self._reset_ui()
            return
        except Exception as exc:
            self.after(0, lambda: self._log(f"ERROR: {exc}"))
            self._reset_ui()
            return

        self.after(0, lambda: self._log(f"Process suspended — counting down {wait} s…"))

        for i in range(wait):
            remaining = wait - i
            pct = 0.05 + (i / wait) * 0.82
            self.after(0, lambda p=pct: self.progress_bar.set(p))
            self.after(0, lambda r=remaining: self.progress_lbl.configure(
                text=f"Suspended — resuming in {r} second{'s' if r != 1 else ''}…"
            ))
            self.after(0, lambda r=remaining: self.action_btn.configure(
                text=f"  Resuming in {r}s…"
            ))
            time.sleep(1)

        self.after(0, lambda: self.progress_bar.set(0.90))
        self.after(0, lambda: self.progress_lbl.configure(text="Resuming GTA5.exe…"))
        self.after(0, lambda: self._log("Resuming process…"))

        try:
            proc.resume()
            self.after(0, lambda: self._log("Done! You should now be in a solo public session."))
            self.after(0, lambda: self._log("Tip: invite friends manually if you want a private crew session."))
            self.after(0, lambda: self.progress_bar.set(1.0))
            self.after(0, lambda: self.progress_lbl.configure(
                text="Success — solo public session active"
            ))
            self.after(0, lambda: self.action_btn.configure(
                fg_color=COLOR_ORANGE,
                hover_color=COLOR_ORANGE_HOV,
                text="  Run Again",
            ))
        except psutil.NoSuchProcess:
            self.after(0, lambda: self._log("WARNING: GTA5.exe closed during wait."))
            self.after(0, lambda: self.progress_lbl.configure(text="GTA V closed."))
        except Exception as exc:
            self.after(0, lambda: self._log(f"ERROR resuming: {exc}"))

        time.sleep(3)
        self.after(0, lambda: self.progress_bar.set(0))
        self.after(0, lambda: self.progress_lbl.configure(text="Ready — click to run again"))
        self.after(0, lambda: self.action_btn.configure(
            fg_color=COLOR_BLUE,
            hover_color=COLOR_BLUE_HOV,
            text="  Launch Solo Session",
            state="normal",
        ))
        self.is_running = False

    def _reset_ui(self):
        time.sleep(1.5)
        self.after(0, lambda: self.progress_bar.set(0))
        self.after(0, lambda: self.action_btn.configure(
            text="  Launch Solo Session", state="normal"
        ))
        self.is_running = False


# ── Entry point ────────────────────────────────────────────────────────────────

def _is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _relaunch_as_admin():
    """Re-launch this script elevated via ShellExecute runas."""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        " ".join(f'"{a}"' for a in sys.argv),
        None, 1,
    )


if __name__ == "__main__":
    if not _is_admin():
        _relaunch_as_admin()
        sys.exit(0)

    app = SoloLobbyApp()
    app.mainloop()
