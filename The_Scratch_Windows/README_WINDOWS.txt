THE SCRATCH — Windows Setup Guide

Read This First

THE SCRATCH runs entirely on your computer.

It does NOT use cloud AI.

It does NOT send your notes to us.

It does NOT require an account.

To work correctly, THE SCRATCH needs three things:

1. Python
2. Ollama
3. At least one AI Model

If any of these are missing, THE SCRATCH cannot generate output.

---

WHAT IS PYTHON?

Python is the programming language used to run THE SCRATCH.

Think of Python as the fuel that allows the application to start.

If Python is not installed, THE SCRATCH cannot launch.

---

STEP 1 — INSTALL PYTHON

Open your web browser.

Go to:

https://www.python.org/downloads/

Download the newest version of Python for Windows.

Run the installer.

IMPORTANT:

If you see:

Add Python to PATH

Make sure that box is checked before clicking Install.

Wait for installation to finish.

Success looks like:

Open Command Prompt and type:

```cmd
python --version
```

You should see something similar to:

```text
Python 3.14.0
```

The version number may be different.

Any recent version is fine.

---

STEP 2 — INSTALL OLLAMA

Ollama allows AI models to run on your computer.

Think of Ollama as the engine.

Go to:

https://ollama.com

Download Ollama for Windows.

Install it normally.

When installation finishes, Ollama should automatically start.

You may see an Ollama icon in your system tray.

---

STEP 3 — INSTALL AN AI MODEL

This step is REQUIRED.

Installing Ollama does NOT install a model.

Ollama = Engine

Model = Brain

You need both.

---

HOW MUCH RAM DO I HAVE?

Press:

Windows Key

Type:

About your PC

Open it.

Look for:

Installed RAM

Examples:

8 GB RAM

16 GB RAM

32 GB RAM

---

RECOMMENDED MODELS

8 GB RAM

Open Command Prompt and run:

```cmd
ollama pull llama3.2:1b
```

If Windows says:

"ollama is not recognized"

Use the tested command below:

```cmd
"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" pull llama3.2:1b
```

Wait for the download to finish.

---

16 GB RAM

Recommended:

```cmd
ollama pull qwen3:8b
```

or

```cmd
ollama pull llama3.1:8b
```

These models are larger and generally produce better results.

---

VERIFY YOUR MODEL IS INSTALLED

Open Command Prompt.

Run:

```cmd
ollama list
```

You should see something similar to:

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

STEP 4 — LAUNCH THE SCRATCH

Open the THE_SCRATCH_windows folder.

Double-click:

launch.bat

The launcher will:

* Check for Python
* Create a virtual environment if needed
* Install required components
* Start THE SCRATCH

The first launch may take a little longer than future launches.

This is normal.

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

If output is generated, everything is working.

---

TROUBLESHOOTING

THE SCRATCH says:

Not Connected

Check:

1. Is Ollama installed?
2. Is Ollama running?
3. Does:

```cmd
ollama list
```

show a model?

If not, install a model.

---

Double-clicking launch.bat closes immediately

Usually Python is missing.

Install Python and try again.

---

THE SCRATCH opens but generates nothing

Usually:

* No model installed
* Ollama not running

Run:

```cmd
ollama list
```

If no models appear, install one.

---

Ollama command not found

Try:

```cmd
"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" list
```

If that works, use the full path version of Ollama commands.

---

THE SCRATCH is slow

This usually means:

* Model is too large for your computer
* Not enough RAM available

Try:

```cmd
ollama pull llama3.2:1b
```

and use that model instead.

---

PRIVACY

THE SCRATCH runs locally.

Your notes stay on your computer.

No accounts.

No subscriptions.

No cloud processing.

No tracking.

---

Enjoy using THE SCRATCH.
