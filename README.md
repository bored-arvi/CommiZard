# CommiZard

<div style="text-align: center;">

![CommiZard's banner](https://github.com/user-attachments/assets/851536f3-49a0-42a9-961d-20d975595d04)
[![Python version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
![GitHub License](https://img.shields.io/github/license/Chungzter/Commizard)
</div>
CommiZard — An interactive commit assistant, powered by AI! 🧙‍♂️
Generate, tweak, and copy commit messages with full control — right from a REPL.

## Features

- **REPL-style Interface** — Stay in an interactive session. Generate multiple
  commit variations without restarting.
- **Smart Generation** — Creates commit messages directly from your `git diff`.
- **Simple CLI** — Familiar, intuitive commands. No learning curve.
- **Flexible AI** backends — Easily swap models. Online model support planned!
- **Clipboard Magic** — Instantly copy generated messages to your system
  clipboard, ready to paste into `git commit`.
- **Zero Daemons** — No background processes, No Git hooks, no surprises.
- **Absolute Control** — Run it when *you* want, and you decide to commit,
  copy, tweak, or discard.

> [!WARNING]
>
> ⚠️ **Heads up!** CommiZard is in **early alpha**. Not all features are
> complete or stable yet.
>
> CommiZard is under active development — expect bugs, crashes, and missing
> functionality.
> Please [open an issue](https://github.com/Chungzter/CommiZard/issues) if you
> encounter problems.
>
> Many features are still missing, since this project was released as a Minimum
> Viable Product (MVP). Stay tuned for new improvements!

## ⚙️ Installation

Install via [pip](https://pip.pypa.io/en/stable/) (from GitHub):

```bash
pip install git+URL_TO_BE_DETERMINED
```

Install from source:

```bash
git clone URL_TO_BE_DETERMINED
cd CommiZard
pip install .
```

Or build from source using PEP 517 (e.g., with `build` or `hatchling`):

```bash
git clone URL_TO_BE_DETERMINED
cd CommiZard
python -m build
# or: hatchling build
pip install dist/commizard-*-py3-none-any.whl
```

## Usage

After installing CommiZard (See [Installation](#-installation)), you can launch
the interactive REPL in your Git repository:

```bash
commizard
```

Once launched, you’ll enter the interactive CommiZard terminal, where you can
use the following commands:

### Commands

|     Command      |                         Description                          |
|:----------------:|:------------------------------------------------------------:|
|      `list`      |  List all available Ollama models installed on your system.  |
|      `gen`       | Generate a new commit message based on the current Git diff. |
|       `cp`       |         Copy the generated output to your clipboard          |
|     `commit`     |             Directly commit the generated output             |
| `exit` or `quit` |                    Exit the REPL session.                    |

### Example Usage

![CommiZard on 7323da1a1847908 during alpha dev](https://github.com/user-attachments/assets/d8696e0a-ba6e-496d-b1f8-8d0247339cd4)

This is one of the very first times the program helped a user (me 😄) write a
meaningful commit message.

## 🧭 Alternatives & Similar Tools

When I started building CommiZard, I made sure to look around — and guess what?

> CommiZard isn’t the only wizard in town! 😊

If you’re exploring AI-powered commit tools, here are some other great projects
worth checking out:

- **[easycommit](https://github.com/blackironj/easycommit)** — written in Go,
  supports Ollama models out of the box.
- **[aicommit](https://github.com/suenot/aicommit)** — Packed with features —
  including a handy VS Code extension.
- **[AICommit2](https://github.com/tak-bro/aicommit2)** — The most complete FOSS
  option I've found

> *Why did I still follow through and build this?*
>
> Because I couldn’t find a tool that gave me both full user control and the
> little UX comforts I wanted.
>
> So yeah — I built CommiZard for me… and maybe for you too 😉

## Contributing

Contributions of all kinds are welcome.

If you’d like to get involved:

- Read the [CONTRIBUTING.md](CONTRIBUTING.md) guide for details on how to report
  bugs, suggest features, or open pull requests.
- Found a bug 🐞 or have an idea
  💡? [Open an issue](https://github.com/Chungzter/CommiZard/issues) and let’s
  discuss it!
- Starter-friendly tasks are listed in the
  [Starter Tasks section](./CONTRIBUTING.md#starter-tasks). Check it out if
  you’re not ready to dive into core features yet.

Not sure where to start? Open an issue or comment “I’d like to help with this,”
and we’ll figure it out together!

## License

`CommiZard` is released under the [MIT license](LICENSE).

Copyright (c) 2025 Chungzter
