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

Run/Type:

python3 --version

Press Enter.

Success looks similar to:

Python 3.14.0

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

Open Terminal Type and run:

ollama pull llama3.2:1b

Wait for the download to finish.

---

16 GB Memory

Recommended/Type in Terminal:


ollama pull qwen3:8b


or


ollama pull llama3.1:8b


---

24 GB+ Memory

Recommended:

ollama pull qwen3:8b

or

ollama pull llama3.1:8b

or another model of your choice.

These larger models generally provide better results.

---

VERIFY THE MODEL IS INSTALLED

Open Terminal.

Run/Type:

ollama list

Press Enter

Success looks similar to:

NAME
llama3.2:1b

or

qwen3:8b

If you see a model listed, you are ready.

---

STEP 4 — OPEN THE SCRATCH FOLDER

Locate the folder you downloaded and extracted.

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

THE SCRATCH is distributed outside the Mac App Store.

Because of this, macOS may prevent it from launching the first time.

This is normal.

Nothing is wrong with THE SCRATCH.

You only need to complete the following steps once.

---

STEP 5 — PREPARE THE SCRATCH FOR FIRST LAUNCH

Open Terminal.

Type:

cd

followed by a space.

Now drag the entire:

THE_SCRATCH_macOS

folder into the Terminal window.

Example:

cd /Users/YourName/Downloads/THE_SCRATCH_macOS

Press Enter.

Now run:

xattr -dr com.apple.quarantine .

Press Enter.

IMPORTANT

You will usually see NO OUTPUT.

That is normal.

No message usually means the command completed successfully.

Next run:

chmod +x run_the_scratch.command

Press Enter.

Again:

You will usually see NO OUTPUT.

That is normal.

No message usually means success.

These commands only need to be run once.

---

STEP 6 — LAUNCH THE SCRATCH

While still in Terminal, run:

./run_the_scratch.command

Press Enter.

THE SCRATCH should launch.

---

WHAT SUCCESS LOOKS LIKE

THE SCRATCH window opens.

You should see:

Connected

near the model controls.

You should also see an available model in the model selector.

Examples:

llama3.2:1b

or

qwen3:8b

Type a short test note.

Click:

RUN

If output is generated, everything is working correctly.

---

TROUBLESHOOTING

THE SCRATCH says:

Not Connected

Check:

1. Is Ollama installed?
2. Is Ollama running?
3. Does:

ollama list

show a model?

If not, install a model.

---

THE SCRATCH does not launch

Return to the THE_SCRATCH_macOS folder in Terminal and run:

xattr -dr com.apple.quarantine .
chmod +x run_the_scratch.command

Then launch again using:

./run_the_scratch.command

If a Terminal window remains open, leave it open while using THE SCRATCH.

Closing the Terminal window may close THE SCRATCH.

---

Terminal says:

command not found: python3

Python is not installed correctly.

Reinstall Python from:

https://www.python.org/downloads/

---

THE SCRATCH opens but generates no output

Usually:

• No model installed

• Ollama not running

Run:

ollama list

If nothing appears, install a model.

---

THE SCRATCH feels slow

Try using:

ollama pull llama3.2:1b

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