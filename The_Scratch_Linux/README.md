# THE SCRATCH

Local-Only Note Compiler

---

## What Is THE SCRATCH?

THE SCRATCH is a local-first AI note compiler.

It takes rough notes, thoughts, bullet points, meeting notes, research, or brainstorming and transforms them into structured output.

Depending on the mode you select, THE SCRATCH can generate:

* Summaries
* Essays
* Outlines
* Key Points

THE SCRATCH runs entirely on your computer.

Your notes stay on your machine.

No accounts.

No subscriptions.

No cloud processing.

No tracking.

No data collection.

---

# Privacy First

THE SCRATCH is designed to run locally.

Your information is processed by an AI model running on your own computer through Ollama.

Nothing is sent to us.

Nothing is uploaded to our servers.

Nothing is stored online.

If your computer is offline, THE SCRATCH still works.

---

# Important: Ollama vs AI Models

Many new users assume installing Ollama installs an AI model.

It does not.

Think of it like this:

Ollama = Engine

AI Model = Brain

You need BOTH.

Installing Ollama gives you the engine.

Installing a model gives the engine something to run.

THE SCRATCH cannot generate output unless at least one model is installed.

---

# Before You Start

You will need:

1. Python
2. Ollama
3. At least one AI model

Once all three are installed:

4. Launch THE SCRATCH

---

# Step 1: Install Python

Python is the programming language used to run THE SCRATCH.

If you already have Python installed, you can skip this step.

Download Python from:

https://www.python.org/downloads/

Install the newest version available.

During installation:

Windows:

* Check "Add Python to PATH" if shown.

macOS:

* Use the standard installer.

Linux:

* Install using your package manager.

---

# Step 2: Install Ollama

Download Ollama from:

https://ollama.com

Install it like any other application.

After installation, Ollama should be running in the background.

---

# Step 3: Install an AI Model

Open:

Windows:

* Command Prompt

macOS:

* Terminal

Linux:

* Terminal

For most users:

8 GB RAM:

```bash
ollama pull llama3.2:1b
```

16 GB RAM:

```bash
ollama pull qwen3:8b
```

or

```bash
ollama pull llama3.1:8b
```

Wait for the download to finish.

This may take several minutes depending on your internet connection.

---

# How Much RAM Do I Have?

Windows:

1. Press Windows Key
2. Type:

```text
About your PC
```

3. Open it

Look for:

Installed RAM

---

macOS:

1. Click Apple Menu
2. About This Mac

Look for:

Memory

---

Linux:

Open Terminal:

```bash
free -h
```

---

# Verify Ollama Can See Your Model

Open Terminal or Command Prompt and run:

```bash
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

If you see a model listed, you're ready.

---

# Launching THE SCRATCH

Each operating system includes its own launcher.

Please read the operating-system-specific guide included with your download:

Windows:
README_WINDOWS.txt

macOS:
README_MACOS.txt

Linux:
README_LINUX.txt

These guides include step-by-step instructions for first-time users.

---

# What Happens When THE SCRATCH Starts?

THE SCRATCH automatically checks for:

* Ollama
* Installed AI models

If Ollama is running and a model is installed:

Status will show:

Connected

If Ollama is not running:

Status will show:

Not Connected

If no models are installed:

THE SCRATCH will explain what is missing.

---

# Troubleshooting

THE SCRATCH says "Not Connected"

Check:

1. Is Ollama installed?
2. Is Ollama running?
3. Does:

```bash
ollama list
```

show a model?

---

THE SCRATCH opens but does not generate output

Usually this means:

* No model is installed
* Ollama is not running

---

Nothing happens when I launch

Make sure:

* Python is installed
* Ollama is installed
* A model is installed

Then follow your operating-system-specific guide.

---

# Open Source

THE SCRATCH is provided as open-source software.

You are free to inspect the code, learn from it, modify it, and build upon it according to the project's license.

---

THE SCRATCH

Local-Only Note Compilation

Your notes stay yours.
