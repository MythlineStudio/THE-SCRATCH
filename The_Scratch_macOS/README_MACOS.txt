THE SCRATCH — macOS Setup Guide

Read This First

THE SCRATCH runs entirely on your Mac.

It does NOT use cloud AI.

It does NOT send your notes anywhere.

It does NOT require an account.

To work correctly, THE SCRATCH needs:

1. Python
2. Ollama
3. At least one AI Model

If any of these are missing, THE SCRATCH cannot generate output.

---

WHAT IS PYTHON?

Python is the programming language used to run THE SCRATCH.

Think of Python as the fuel that allows the application to start.

If Python is missing, THE SCRATCH cannot launch.

---

STEP 1 — INSTALL PYTHON

Open Safari or your preferred browser.

Go to:

https://www.python.org/downloads/

Download the newest version of Python for macOS.

Run the installer.

Follow the default installation steps.

When installation finishes, open Terminal.

You can find Terminal by:

Applications → Utilities → Terminal

or

Press Command + Space and type:

Terminal

Open Terminal.

Type:

```bash
python3 --version
```

Press Enter.

Success looks like:

```text
Python 3.14.0
```

Your version number may be different.

Any recent version is fine.

---

STEP 2 — INSTALL OLLAMA

Open:

https://ollama.com

Download Ollama for macOS.

Install it like any normal Mac application.

Launch Ollama once after installation.

You should see the Ollama icon in the menu bar near the clock.

---

STEP 3 — INSTALL AN AI MODEL

Installing Ollama does NOT install a model.

Think of it like this:

Ollama = Engine

Model = Brain

You need both.

---

HOW MUCH MEMORY (RAM) DO I HAVE?

Click:

Apple Menu → About This Mac

Look for:

Memory

Examples:

8 GB

16 GB

24 GB

32 GB

---

RECOMMENDED MODELS

8 GB Memory

Open Terminal and run:

```bash
ollama pull llama3.2:1b
```

Wait for the download to finish.

---

16 GB Memory

Recommended:

```bash
ollama pull qwen3:8b
```

or

```bash
ollama pull llama3.1:8b
```

These larger models generally provide better results.

---

VERIFY THE MODEL IS INSTALLED

Open Terminal.

Run:

```bash
ollama list
```

Success looks similar to:

```text
NAME
llama3.2:1b
```

or

```text
qwen3:8b
```

If you see a model listed, you are ready.

---

STEP 4 — OPEN THE SCRATCH FOLDER

Locate the folder you downloaded.

Open:

THE_SCRATCH_macOS

You should see:

run_the_scratch.command

along with folders such as:

engine
ui
resources

---

IMPORTANT: APPLE SECURITY WARNING

Because THE SCRATCH is distributed outside the Mac App Store, macOS may prevent it from launching the first time.

This is normal.

Nothing is wrong.

---

METHOD 1 — TRY THE EASY WAY FIRST

Right-click:

run_the_scratch.command

Choose:

Open

A warning may appear.

Click:

Open

again.

If THE SCRATCH launches successfully, you are done.

---

METHOD 2 — REMOVE QUARANTINE (RECOMMENDED)

If Method 1 does not work, use Terminal.

Open Terminal.

Drag the THE_SCRATCH_macOS folder into the Terminal window.

Press Backspace once to remove the folder name.

Type:

```bash
cd
```

followed by a space.

Then drag the THE_SCRATCH_macOS folder into Terminal.

Example:

```bash
cd /Users/YourName/Downloads/THE_SCRATCH_macOS
```

Press Enter.

Now run:

```bash
xattr -dr com.apple.quarantine .
```

Press Enter.

IMPORTANT

You will usually see NO OUTPUT.

That is normal.

No message means the command worked.

Next run:

```bash
chmod +x run_the_scratch.command
```

Press Enter.

Again:

You will usually see NO OUTPUT.

That is normal.

No message means success.

---

STEP 5 — LAUNCH THE SCRATCH

Double-click:

run_the_scratch.command

A Terminal window may briefly appear.

THE SCRATCH should then open.

---

WHAT SUCCESS LOOKS LIKE

THE SCRATCH window opens.

You should see:

Connected

near the model controls.

You should also see an available model in the model selector.

Example:

llama3.2:1b

or

qwen3:8b

Type a short test note.

Click RUN.

If output is generated, everything is working correctly.

---

TROUBLESHOOTING

THE SCRATCH says:

Not Connected

Check:

1. Is Ollama installed?
2. Is Ollama running?
3. Does:

```bash
ollama list
```

show a model?

If not, install a model.

---

Double-clicking the launcher does nothing

Try:

Right-click → Open

If that fails:

Run the quarantine removal steps above.

---

Terminal says:

command not found: python3

Python is not installed correctly.

Reinstall Python from:

https://www.python.org/downloads/

---

THE SCRATCH opens but generates no output

Usually:

* No model installed
* Ollama not running

Run:

```bash
ollama list
```

If nothing appears, install a model.

---

THE SCRATCH feels slow

Try using:

```bash
ollama pull llama3.2:1b
```

Smaller models generally run faster.

---

PRIVACY

THE SCRATCH runs locally.

Your notes stay on your Mac.

No accounts.

No subscriptions.

No cloud processing.

No tracking.

---

Enjoy using THE SCRATCH.
