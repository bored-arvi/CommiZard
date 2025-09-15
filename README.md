# CommiZard

BANNER_IMAGE_TO_BE_ADDED
BADGES_TO_BE_ADDED

CommiZard — An interactive commit assistant, powered by AI!
Generate, tweak, and copy commit messages with full control, right from a REPL.

## Features

- REPL style. Stay in an interactive session, try multiple commits, don’t
  restart a process each time.
- Generates commit messages from `git diff`.
- Simple CLI interface with familiar commands.
- Flexible model integration and plans to implement online models
- Clipboard integration. Instantly copy to your system clipboard, ready to
  paste anywhere.
- No background daemons. Runs only when you want it; no hooks, no processes
  hanging around. You can do whatever you want with the generated output.
- You always decide whether to commit, copy, or discard.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
CommiZard:

```bash
pip install git+URL_TO_BE_DETERMINED
```

You can also install CommiZard from source:

```bash
git clone URL_TO_BE_DETERMINED
cd CommiZard
pip install .
```

Or build it with PEP 517 build tools:

```bash
git clone URL_TO_BE_DETERMINED
cd CommiZard
python -m build # or use hatchling if installed: hatchling build
pip install dist/commizard-version-py3-none-any.whl 
```

## Usage

The following screenshot is an example workflow from commizard running on
itself.
IMAGE_TO_BE_ADDED
This is one of the very first times the program has been used to help a user
(in this case, me) write a commit message.

## Contributing
