THE SCRATCH — Linux Setup Guide

Read This First

THE SCRATCH runs entirely on your computer.

It does NOT use cloud AI.

It does NOT send your notes anywhere.

It does NOT require an account.

To work correctly, THE SCRATCH needs:

1. Python
2. Tkinter
3. Ollama
4. At least one AI Model

If any of these are missing, THE SCRATCH cannot generate output.

---

WHAT IS PYTHON?

Python is the programming language used to run THE SCRATCH.

Think of Python as the fuel that allows the application to start.

If Python is missing, THE SCRATCH cannot launch.

---

WHAT IS TKINTER?

Tkinter is the graphical user interface system used by THE SCRATCH.

Without Tkinter, the application cannot display its window.

Many Linux distributions include Tkinter automatically.

Some do not.

---

STEP 1 — INSTALL PYTHON

Open Terminal.

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
```

Fedora:

```bash
sudo dnf install python3 python3-tkinter
```

Arch Linux:

```bash
sudo pacman -S python tk
```

Verify installation:

```bash
python3 --version
```

Success looks similar to:

```text
Python 3.14.0
```

Your version number may be different.

Any modern version should work.

---

STEP 2 — INSTALL OLLAMA

Visit:

https://ollama.com

Follow the Linux installation instructions for your distribution.

After installation completes, verify Ollama is available:

```bash
ollama --version
```

If a version number appears, Ollama is installed correctly.

---

STEP 3 — INSTALL AN AI MODEL

Installing Ollama does NOT install a model.

Think of it like this:

Ollama = Engine

Model = Brain

You need both.

---

HOW MUCH RAM DO I HAVE?

Open Terminal:

```bash
free -h
```

Look for the total memory amount.

Examples:

8 GB

16 GB

32 GB

---

RECOMMENDED MODELS

8 GB RAM

```bash
ollama pull llama3.2:1b
```

---

16 GB RAM

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

Navigate to the folder you downloaded.

Example:

```bash
cd ~/Downloads/THE_SCRATCH_linux
```

Your location may be different.

---

STEP 5 — MAKE THE LAUNCHER EXECUTABLE

IMPORTANT

The launcher included with THE SCRATCH is:

```text
launch.sh
```

Run:

```bash
chmod +x launch.sh
```

Press Enter.

You will usually see NO OUTPUT.

That is normal.

No message means success.

---

STEP 6 — LAUNCH THE SCRATCH

Run:

```bash
./launch.sh
```

The launcher will:

* Check for Python
* Create a virtual environment
* Install requirements if needed
* Launch THE SCRATCH

The first launch may take longer than future launches.

This is normal.

---

WHAT SUCCESS LOOKS LIKE

THE SCRATCH window opens.

You should see:

Connected

near the model controls.

You should also see a model available in the model selector.

Examples:

```text
llama3.2:1b
```

or

```text
qwen3:8b
```

Type a short note.

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

Permission denied

Run:

```bash
chmod +x launch.sh
```

again.

Then launch:

```bash
./launch.sh
```

---

python3: command not found

Python is not installed.

Install Python using your distribution's package manager.

Then try again.

---

Tkinter errors

Ubuntu / Debian:

```bash
sudo apt install python3-tk
```

Fedora:

```bash
sudo dnf install python3-tkinter
```

Arch Linux:

```bash
sudo pacman -S tk
```

Then launch THE SCRATCH again.

---

THE SCRATCH opens but generates no output

Usually:

* No model installed
* Ollama not running

Check:

```bash
ollama list
```

If no models appear, install one.

---

THE SCRATCH feels slow

Try using:

```bash
ollama pull llama3.2:1b
```

Smaller models generally run faster and require less memory.

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
