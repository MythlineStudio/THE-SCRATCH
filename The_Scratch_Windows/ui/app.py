import os
import platform
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import ttk

from engine.engine_bridge import OUTPUT_DIR, get_ollama_status, run_prompt


BG = "#151618"
PANEL = "#1f2125"
PANEL_2 = "#24272c"
TEXT_BG = "#101113"
TEXT_FG = "#f2f2f2"
MUTED = "#a7adb7"
BORDER = "#343842"
ACCENT = "#d7d7d7"
GOOD = "#7CFFB2"
WARN = "#FFD479"
BAD = "#FF7676"
BUTTON = "#30343b"
BUTTON_HOVER = "#3b4049"
BUTTON_ACTIVE = "#4a505b"
BUTTON_DISABLED = "#25282d"


class LabelButton(tk.Label):
    def __init__(self, master, text, command, width=None):
        tk.Label.__init__(
            self,
            master,
            text=text,
            bg=BUTTON,
            fg=TEXT_FG,
            activebackground=BUTTON_ACTIVE,
            activeforeground=TEXT_FG,
            padx=14,
            pady=9,
            width=width,
            cursor="hand2",
            takefocus=1,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            font=("Helvetica", 11, "bold"),
        )
        self.command = command
        self.disabled = False
        self.bind("<Button-1>", self._click)
        self.bind("<Return>", self._key_click)
        self.bind("<space>", self._key_click)
        self.bind("<Enter>", self._hover)
        self.bind("<Leave>", self._leave)
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)

    def set_disabled(self, disabled):
        self.disabled = bool(disabled)
        if self.disabled:
            self.configure(bg=BUTTON_DISABLED, fg="#777d87", cursor="arrow")
        else:
            self.configure(bg=BUTTON, fg=TEXT_FG, cursor="hand2")

    def _click(self, event=None):
        if not self.disabled and self.command:
            self.command()

    def _key_click(self, event=None):
        self._click()
        return "break"

    def _hover(self, event=None):
        if not self.disabled:
            self.configure(bg=BUTTON_HOVER)

    def _leave(self, event=None):
        if not self.disabled:
            self.configure(bg=BUTTON)

    def _press(self, event=None):
        if not self.disabled:
            self.configure(bg=BUTTON_ACTIVE)

    def _release(self, event=None):
        if not self.disabled:
            self.configure(bg=BUTTON_HOVER)


class ScratchCompiler(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("The Scratch — Note Compiler")
        self.geometry("1080x760")
        self.minsize(940, 700)
        self.configure(bg=BG)

        self.processing = False
        self.logo_img = None
        self.startup_notice_shown = False
        self.status_poll_job = None
        self.available_models = []

        self.model_name = tk.StringVar(value="Checking Ollama...")
        self.selected_model = tk.StringVar(value="")
        self.status_text = tk.StringVar(value="Ollama not available")

        self.mode = tk.StringVar(value="SUMMARIZE")
        self.anti_ai = tk.BooleanVar(value=True)

        self.summary_paragraphs = tk.IntVar(value=2)
        self.essay_words = tk.IntVar(value=500)
        self.outline_detail = tk.StringVar(value="MEDIUM")

        self.kp_all = tk.BooleanVar(value=True)
        self.kp_names = tk.BooleanVar(value=True)
        self.kp_dates = tk.BooleanVar(value=True)
        self.kp_numbers = tk.BooleanVar(value=True)
        self.kp_expand = tk.BooleanVar(value=False)

        self.system_info = self._get_system_info()

        self._configure_ttk()
        self._build_ui()
        self.refresh_params()
        self.after(100, lambda: self.refresh_ollama_status(show_startup=True))
        self.after(250, lambda: self.input_box.focus_set())

    def _configure_ttk(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            style.theme_use("default")

        style.configure("Scratch.TLabel", background=PANEL, foreground=TEXT_FG, font=("Helvetica", 11))
        style.configure("Muted.TLabel", background=PANEL, foreground=MUTED, font=("Helvetica", 10))
        style.configure("Header.TLabel", background=BG, foreground=TEXT_FG, font=("Helvetica", 20, "bold"))
        style.configure("SubHeader.TLabel", background=BG, foreground=MUTED, font=("Helvetica", 11))
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("Scratch.TRadiobutton", background=PANEL, foreground=TEXT_FG, font=("Helvetica", 10))
        style.map(
            "Scratch.TRadiobutton",
            background=[("active", PANEL), ("selected", PANEL)],
            foreground=[("active", TEXT_FG), ("selected", TEXT_FG)],
        )
        style.configure("Scratch.TCheckbutton", background=PANEL, foreground=TEXT_FG, font=("Helvetica", 10))
        style.map(
            "Scratch.TCheckbutton",
            background=[("active", PANEL), ("selected", PANEL)],
            foreground=[("active", TEXT_FG), ("selected", TEXT_FG)],
        )
        style.configure("Scratch.TSpinbox", fieldbackground=TEXT_BG, foreground=TEXT_FG, background=PANEL_2)
        style.configure("Scratch.TCombobox", fieldbackground=TEXT_BG, foreground=TEXT_FG, background=PANEL_2)
        style.configure("Scratch.Horizontal.TSeparator", background=BORDER)

    def _build_ui(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=16, pady=14)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        header = tk.Frame(root, bg=BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        logo_holder = tk.Frame(header, bg=BG, width=72, height=72)
        logo_holder.pack(side="left", padx=(0, 12))
        logo_holder.pack_propagate(False)

        try:
            logo_path = Path(__file__).resolve().parents[1] / "resources" / "images" / "the_scratch_logo.png"
            raw_logo = tk.PhotoImage(file=str(logo_path))
            scale = max(1, int(max(raw_logo.width(), raw_logo.height()) / 64))
            self.logo_img = raw_logo.subsample(scale, scale)
            tk.Label(logo_holder, image=self.logo_img, bg=BG).pack(expand=True)
        except Exception as exc:
            tk.Label(
                logo_holder,
                text="SCR",
                bg=PANEL_2,
                fg=TEXT_FG,
                font=("Helvetica", 16, "bold"),
                width=5,
                height=3,
            ).pack(expand=True, fill="both")
            print("Logo failed to load:", exc, file=sys.stderr)

        title_block = tk.Frame(header, bg=BG)
        title_block.pack(side="left", fill="x", expand=True)
        ttk.Label(title_block, text="THE SCRATCH", style="Header.TLabel").pack(anchor="w")
        ttk.Label(title_block, text="Local note compiler for durable text outputs", style="SubHeader.TLabel").pack(anchor="w")

        status_card = tk.Frame(header, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=8)
        status_card.pack(side="right", fill="y")
        tk.Label(status_card, text="OLLAMA", bg=PANEL, fg=MUTED, font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.status_label = tk.Label(status_card, textvariable=self.status_text, bg=PANEL, fg=BAD, font=("Helvetica", 11, "bold"))
        self.status_label.pack(anchor="w")
        tk.Label(status_card, textvariable=self.model_name, bg=PANEL, fg=MUTED, font=("Helvetica", 9), wraplength=260, justify="left").pack(anchor="w", pady=(2, 5))

        self.model_picker = ttk.Combobox(
            status_card,
            textvariable=self.selected_model,
            state="disabled",
            width=28,
            style="Scratch.TCombobox",
            takefocus=True,
        )
        self.model_picker.pack(anchor="w", fill="x")
        self.model_picker.bind("<<ComboboxSelected>>", self._model_selected)

        body = tk.Frame(root, bg=BG)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)

        output_panel = tk.Frame(body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        output_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        output_header = tk.Frame(output_panel, bg=PANEL)
        output_header.pack(fill="x", padx=12, pady=(10, 6))
        tk.Label(output_header, text="OUTPUT", bg=PANEL, fg=TEXT_FG, font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Label(output_header, text="Saved locally after each successful run", bg=PANEL, fg=MUTED, font=("Helvetica", 9)).pack(side="right")

        output_wrap = tk.Frame(output_panel, bg=PANEL)
        output_wrap.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.output_box = tk.Text(
            output_wrap,
            bg=TEXT_BG,
            fg=TEXT_FG,
            state="disabled",
            wrap="word",
            insertbackground=TEXT_FG,
            selectbackground="#4d5666",
            selectforeground=TEXT_FG,
            relief="flat",
            padx=12,
            pady=12,
            font=("Menlo", 12),
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self.output_box.pack(side="left", fill="both", expand=True)
        output_scroll = tk.Scrollbar(output_wrap, command=self.output_box.yview)
        output_scroll.pack(side="right", fill="y")
        self.output_box.configure(yscrollcommand=output_scroll.set)

        control_panel = tk.Frame(body, bg=PANEL, width=280, highlightbackground=BORDER, highlightthickness=1)
        control_panel.grid(row=0, column=1, sticky="ns")
        control_panel.grid_propagate(False)

        controls_inner = tk.Frame(control_panel, bg=PANEL)
        controls_inner.pack(fill="both", expand=True, padx=14, pady=14)

        tk.Label(controls_inner, text="MODE", bg=PANEL, fg=TEXT_FG, font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(0, 6))
        for mode_name in ["SUMMARIZE", "ESSAY", "OUTLINE", "KEY POINTS"]:
            ttk.Radiobutton(
                controls_inner,
                text=mode_name,
                value=mode_name,
                variable=self.mode,
                command=self.refresh_params,
                style="Scratch.TRadiobutton",
                takefocus=True,
            ).pack(anchor="w", pady=2)

        ttk.Separator(controls_inner, style="Scratch.Horizontal.TSeparator").pack(fill="x", pady=12)
        tk.Label(controls_inner, text="PARAMETERS", bg=PANEL, fg=TEXT_FG, font=("Helvetica", 11, "bold")).pack(anchor="w")

        self.param_frame = tk.Frame(controls_inner, bg=PANEL)
        self.param_frame.pack(fill="x", pady=8)

        ttk.Separator(controls_inner, style="Scratch.Horizontal.TSeparator").pack(fill="x", pady=12)
        ttk.Checkbutton(
            controls_inner,
            text="Plain language (Anti-AI)",
            variable=self.anti_ai,
            style="Scratch.TCheckbutton",
            takefocus=True,
        ).pack(anchor="w")

        spacer = tk.Frame(controls_inner, bg=PANEL)
        spacer.pack(fill="both", expand=True)

        self.refresh_button = LabelButton(controls_inner, "REFRESH OLLAMA", self.refresh_ollama_status)
        self.refresh_button.pack(fill="x", pady=(0, 8))

        self.open_button = LabelButton(controls_inner, "OPEN OUTPUT", self.open_output)
        self.open_button.pack(fill="x")

        input_panel = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        input_panel.grid(row=2, column=0, sticky="ew", pady=(12, 0))

        input_header = tk.Frame(input_panel, bg=PANEL)
        input_header.pack(fill="x", padx=12, pady=(10, 6))
        tk.Label(input_header, text="INPUT NOTES", bg=PANEL, fg=TEXT_FG, font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Label(input_header, text="Enter = run   Shift+Enter = new line   Tab = next control", bg=PANEL, fg=MUTED, font=("Helvetica", 9)).pack(side="right")

        input_row = tk.Frame(input_panel, bg=PANEL)
        input_row.pack(fill="x", padx=12, pady=(0, 12))

        self.input_box = tk.Text(
            input_row,
            height=5,
            wrap="word",
            bg=TEXT_BG,
            fg=TEXT_FG,
            insertbackground=TEXT_FG,
            selectbackground="#4d5666",
            selectforeground=TEXT_FG,
            relief="flat",
            padx=12,
            pady=10,
            font=("Menlo", 12),
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            undo=True,
            takefocus=1,
        )
        self.input_box.pack(side="left", fill="both", expand=True)
        self.input_box.bind("<Return>", self._input_return)
        self.input_box.bind("<Shift-Return>", self._input_shift_return)
        self.input_box.bind("<Tab>", self._focus_next)
        self.input_box.bind("<ISO_Left_Tab>", self._focus_prev)
        self.input_box.bind("<Shift-Tab>", self._focus_prev)

        run_holder = tk.Frame(input_row, bg=PANEL)
        run_holder.pack(side="right", fill="y", padx=(10, 0))
        self.run_button = LabelButton(run_holder, "RUN", self.run, width=12)
        self.run_button.pack(fill="x", expand=True)

    def refresh_params(self):
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        mode = self.mode.get()

        if mode == "SUMMARIZE":
            tk.Label(self.param_frame, text="Paragraphs", bg=PANEL, fg=MUTED, font=("Helvetica", 10)).pack(anchor="w")
            ttk.Spinbox(
                self.param_frame,
                from_=1,
                to=8,
                textvariable=self.summary_paragraphs,
                width=6,
                style="Scratch.TSpinbox",
                takefocus=True,
            ).pack(anchor="w", pady=(3, 0))

        elif mode == "ESSAY":
            tk.Label(self.param_frame, text="Target words", bg=PANEL, fg=MUTED, font=("Helvetica", 10)).pack(anchor="w")
            ttk.Spinbox(
                self.param_frame,
                from_=200,
                to=3000,
                increment=100,
                textvariable=self.essay_words,
                width=8,
                style="Scratch.TSpinbox",
                takefocus=True,
            ).pack(anchor="w", pady=(3, 0))

        elif mode == "OUTLINE":
            tk.Label(self.param_frame, text="Detail level", bg=PANEL, fg=MUTED, font=("Helvetica", 10)).pack(anchor="w")
            for level in ["LOW", "MEDIUM", "HIGH"]:
                ttk.Radiobutton(
                    self.param_frame,
                    text=level,
                    value=level,
                    variable=self.outline_detail,
                    style="Scratch.TRadiobutton",
                    takefocus=True,
                ).pack(anchor="w", pady=2)

        elif mode == "KEY POINTS":
            ttk.Checkbutton(
                self.param_frame,
                text="All (Names + Dates + Numbers)",
                variable=self.kp_all,
                command=self._kp_apply_all,
                style="Scratch.TCheckbutton",
                takefocus=True,
            ).pack(anchor="w", pady=(0, 6))

            self.kp_names_cb = ttk.Checkbutton(
                self.param_frame,
                text="Names",
                variable=self.kp_names,
                command=self._kp_maybe_update_all,
                style="Scratch.TCheckbutton",
                takefocus=True,
            )
            self.kp_dates_cb = ttk.Checkbutton(
                self.param_frame,
                text="Dates",
                variable=self.kp_dates,
                command=self._kp_maybe_update_all,
                style="Scratch.TCheckbutton",
                takefocus=True,
            )
            self.kp_numbers_cb = ttk.Checkbutton(
                self.param_frame,
                text="Numbers",
                variable=self.kp_numbers,
                command=self._kp_maybe_update_all,
                style="Scratch.TCheckbutton",
                takefocus=True,
            )

            self.kp_names_cb.pack(anchor="w")
            self.kp_dates_cb.pack(anchor="w")
            self.kp_numbers_cb.pack(anchor="w")

            ttk.Separator(self.param_frame, style="Scratch.Horizontal.TSeparator").pack(fill="x", pady=8)
            ttk.Checkbutton(
                self.param_frame,
                text="Expand after extract",
                variable=self.kp_expand,
                style="Scratch.TCheckbutton",
                takefocus=True,
            ).pack(anchor="w")

            self._kp_apply_all()

    def _kp_apply_all(self):
        if not hasattr(self, "kp_names_cb"):
            return
        all_on = self.kp_all.get()
        for checkbox in [self.kp_names_cb, self.kp_dates_cb, self.kp_numbers_cb]:
            checkbox.state(["disabled"] if all_on else ["!disabled"])
        if all_on:
            self.kp_names.set(True)
            self.kp_dates.set(True)
            self.kp_numbers.set(True)

    def _kp_maybe_update_all(self):
        self.kp_all.set(self.kp_names.get() and self.kp_dates.get() and self.kp_numbers.get())
        self._kp_apply_all()

    def refresh_ollama_status(self, show_startup=False):
        def worker():
            status = get_ollama_status()
            self.after(0, lambda: self._apply_status(status, show_startup=show_startup))

        threading.Thread(target=worker, daemon=True).start()

    def _apply_status(self, status, show_startup=False):
        state = status.get("state", "Ollama not available")
        model = status.get("model")
        models = status.get("models", [])
        detail = status.get("detail", "")

        self.available_models = [str(item) for item in models]
        self.status_text.set(str(state))

        if self.available_models:
            self.model_picker.configure(values=self.available_models, state="readonly")
            current = self.selected_model.get()
            if current not in self.available_models:
                self.selected_model.set(str(model or self.available_models[0]))
        else:
            self.model_picker.configure(values=[], state="disabled")
            self.selected_model.set("")

        if state == "Connected":
            self.status_label.configure(fg=GOOD)
            self.model_name.set("Active Model: " + str(self.selected_model.get() or model))
        elif state == "No models installed":
            self.status_label.configure(fg=WARN)
            self.model_name.set("Install a model, then refresh.")
        elif state == "Disconnected":
            self.status_label.configure(fg=WARN)
            self.model_name.set(detail or "Disconnected")
        else:
            self.status_label.configure(fg=BAD)
            self.model_name.set(detail or "Start Ollama locally.")

        if show_startup and not self.startup_notice_shown and self._should_show_startup_notice(state):
            self.startup_notice_shown = True
            self.after(150, lambda: self._show_startup_notice(status))

        self._schedule_status_poll()

    def _model_selected(self, event=None):
        picked = self.selected_model.get().strip()
        if picked:
            self.model_name.set("Active Model: " + picked)

    def _schedule_status_poll(self):
        if self.status_poll_job is not None:
            try:
                self.after_cancel(self.status_poll_job)
            except Exception:
                pass
        self.status_poll_job = self.after(8000, self.refresh_ollama_status)

    def _should_show_startup_notice(self, state):
        # Only interrupt the user when setup is incomplete.
        # If Ollama is connected and at least one model exists, stay out of the way.
        if state in {"Ollama not available", "No models installed", "Disconnected"}:
            return True
        if not self._python_is_recommended():
            return True
        return False

    def _show_startup_notice(self, status):
        state = status.get("state", "Ollama not available")
        model = self.selected_model.get() or status.get("model") or "None"
        detail = status.get("detail", "")

        win = tk.Toplevel(self)
        win.title("The Scratch — Startup Check")
        win.configure(bg=BG)
        win.transient(self)
        win.grab_set()
        win.resizable(False, False)

        card = tk.Frame(win, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=16)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        tk.Label(card, text="THE SCRATCH SETUP CHECK", bg=PANEL, fg=TEXT_FG, font=("Helvetica", 13, "bold")).pack(anchor="w")
        tk.Label(
            card,
            text="Local status only. No telemetry. No account. No cloud check.",
            bg=PANEL,
            fg=MUTED,
            font=("Helvetica", 10),
        ).pack(anchor="w", pady=(2, 12))

        status_color = GOOD if state == "Connected" else WARN if state == "No models installed" else BAD
        lines = [
            ("Ollama Status", str(state), status_color),
            ("Active Model", str(model), TEXT_FG if model != "None" else MUTED),
            ("Platform", self.system_info["platform"], TEXT_FG),
            ("CPU", self.system_info["cpu"], TEXT_FG),
            ("Memory", self.system_info["memory"], TEXT_FG),
            ("Python", self.system_info["python"], TEXT_FG),
        ]

        for label, value, color in lines:
            row = tk.Frame(card, bg=PANEL)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label + ":", bg=PANEL, fg=MUTED, font=("Helvetica", 10, "bold"), width=16, anchor="w").pack(side="left")
            tk.Label(row, text=value, bg=PANEL, fg=color, font=("Helvetica", 10), anchor="w").pack(side="left")

        message = self._startup_message_for_status(state, detail)
        tk.Label(card, text=message, bg=PANEL, fg=TEXT_FG, font=("Helvetica", 10), justify="left", wraplength=520).pack(anchor="w", pady=(14, 10))

        button_row = tk.Frame(card, bg=PANEL)
        button_row.pack(fill="x", pady=(4, 0))

        self._popup_button(button_row, "OPEN OLLAMA DOWNLOAD", lambda: self._open_url("https://ollama.com/download")).pack(side="left", padx=(0, 8))
        self._popup_button(button_row, "OPEN OLLAMA LIBRARY", lambda: self._open_url("https://ollama.com/library")).pack(side="left", padx=(0, 8))
        self._popup_button(button_row, "OPEN PYTHON", lambda: self._open_url("https://www.python.org/downloads/")).pack(side="left", padx=(0, 8))
        self._popup_button(button_row, "OK", win.destroy, width=7).pack(side="right")

        self.update_idletasks()
        x = self.winfo_x() + max(40, int((self.winfo_width() - 640) / 2))
        y = self.winfo_y() + max(40, int((self.winfo_height() - 340) / 2))
        win.geometry(f"+{x}+{y}")

    def _popup_button(self, master, text, command, width=None):
        return tk.Button(
            master,
            text=text,
            command=command,
            bg=BUTTON,
            fg=TEXT_FG,
            activebackground=BUTTON_ACTIVE,
            activeforeground=TEXT_FG,
            cursor="hand2",
            takefocus=True,
            relief="flat",
            padx=10,
            pady=7,
            width=width,
            highlightthickness=1,
            highlightbackground=BORDER,
            font=("Helvetica", 10, "bold"),
        )

    def _open_url(self, url):
        try:
            webbrowser.open_new_tab(url)
        except Exception as exc:
            self._set_output("Could not open this page:\n\n" + url + "\n\n" + str(exc))

    def _startup_message_for_status(self, state, detail):
        if state == "Connected":
            return "Ready. THE SCRATCH will send prompts only to your local Ollama server and save outputs in the local output folder."

        if state == "No models installed":
            return (
                "Ollama is running, but no model is installed yet.\n\n"
                "Beginner recommendations:\n"
                "8 GB RAM: gemma3:4b\n"
                "16 GB RAM: qwen3.5:9b\n"
                "24+ GB RAM: gemma3:12b\n\n"
                "These are suggestions only. Install any Ollama model you prefer."
            )

        python_warning = ""
        if not self._python_is_recommended():
            python_warning = "\n\nPython 3.10 or newer is recommended."

        return (
            (detail or "Ollama is not available at http://localhost:11434.")
            + "\n\nInstall Ollama, start Ollama, or download a model, then refresh connection."
            + python_warning
        )

    def _python_is_recommended(self):
        return sys.version_info >= (3, 10)

    def _get_system_info(self):
        return {
            "platform": self._platform_name(),
            "cpu": self._cpu_name(),
            "memory": self._memory_label(),
            "python": self._python_label(),
        }

    def _platform_name(self):
        system = platform.system()
        if system == "Darwin":
            return "macOS"
        if system == "Windows":
            return "Windows"
        if system == "Linux":
            return "Linux"
        return system or "Unknown"

    def _cpu_name(self):
        machine = platform.machine().lower()
        if self._platform_name() == "macOS":
            if machine in ("arm64", "aarch64"):
                return "Apple Silicon"
            if machine in ("x86_64", "amd64", "i386", "i686"):
                return "Intel"
        return platform.machine() or "Unknown"

    def _memory_label(self):
        try:
            if sys.platform == "darwin":
                raw = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()
                gb = round(int(raw) / (1024 ** 3))
                return f"{gb} GB RAM"
            if hasattr(os, "sysconf"):
                pages = os.sysconf("SC_PHYS_PAGES")
                page_size = os.sysconf("SC_PAGE_SIZE")
                gb = round((pages * page_size) / (1024 ** 3))
                return f"{gb} GB RAM"
        except Exception:
            pass
        return "Unknown"

    def _python_label(self):
        try:
            return platform.python_version()
        except Exception:
            return "Not Detected"

    def _input_return(self, event=None):
        if self.processing:
            return "break"
        if self.input_box.get("1.0", "end").strip():
            self.run()
            return "break"
        return "break"

    def _input_shift_return(self, event=None):
        self.input_box.insert("insert", "\n")
        return "break"

    def _focus_next(self, event=None):
        event.widget.tk_focusNext().focus_set()
        return "break"

    def _focus_prev(self, event=None):
        event.widget.tk_focusPrev().focus_set()
        return "break"

    def run(self):
        if self.processing:
            return

        notes = self.input_box.get("1.0", "end").strip()
        if not notes:
            self._set_output("Paste notes first. Empty prompts do not run.")
            return

        params = {
            "summary_paragraphs": self.summary_paragraphs.get(),
            "essay_words": self.essay_words.get(),
            "outline_detail": self.outline_detail.get(),
            "kp_all": self.kp_all.get(),
            "kp_names": self.kp_names.get(),
            "kp_dates": self.kp_dates.get(),
            "kp_numbers": self.kp_numbers.get(),
            "kp_expand": self.kp_expand.get(),
        }

        self.processing = True
        self.run_button.set_disabled(True)
        self.refresh_button.set_disabled(True)
        self._set_output("Checking local Ollama connection...\n")

        def worker():
            try:
                status = get_ollama_status()
                selected = self.selected_model.get().strip() or None
                self.after(0, lambda: self._apply_status(status))
                result = run_prompt(
                    notes,
                    self.mode.get(),
                    params=params,
                    anti_ai=self.anti_ai.get(),
                    model_name=selected,
                )
            except Exception as exc:
                result = "The Scratch hit an application error:\n\n" + str(exc)
            self.after(0, lambda: self._finish_run(result))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_run(self, result):
        self._set_output(result)
        self.input_box.delete("1.0", "end")
        self.processing = False
        self.run_button.set_disabled(False)
        self.refresh_button.set_disabled(False)
        self.refresh_ollama_status()
        self.input_box.focus_set()

    def _set_output(self, text):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", text)
        self.output_box.config(state="disabled")

    def open_output(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = str(OUTPUT_DIR.resolve())
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", output_path], check=False)
            elif os.name == "nt":
                os.startfile(output_path)  # type: ignore[attr-defined]
            else:
                subprocess.run(["xdg-open", output_path], check=False)
        except Exception as exc:
            self._set_output("Could not open output folder:\n\n" + output_path + "\n\n" + str(exc))


if __name__ == "__main__":
    app = ScratchCompiler()
    app.mainloop()
