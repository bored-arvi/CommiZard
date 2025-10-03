# How to Contribute to CommiZard

Thank you for your interest in helping shape CommiZard! I’m building this in my
free time, so your help means the world.

Here are some ways you can help improve this project:

## 🛠️ Setting Up for Development

Want to contribute code? Here's how to get your development environment ready:

### Prerequisites

- Python 3.9 or higher
- Git
- pip

### Installation Steps

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/CommiZard.git
   cd CommiZard

2. Install in development mode with dev dependencies:
pip install -e ".[dev]"
2. This installs CommiZard in editable mode plus all development tools (pytest, black, ruff, mypy).
3. Verify installation:
commizard --help
pytest

Development Workflow

Before committing your changes:

1. Format your code with Black:
black src/ tests/
2. Lint with Ruff:
ruff check src/ tests/
3. Type check with mypy (optional but recommended):
mypy src/
4. Run tests:
pytest

4. Or with coverage:
pytest --cov=commizard tests/

Making Changes

1. Create a new branch: git checkout -b my-feature-or-fix
2. Make your changes
3. Run formatters and linters (see above)
4. Run tests to ensure nothing broke
5. Commit with a clear message
6. Push to your fork and open a PR

[!TIP]
Run black . and ruff check . before every commit to keep code style consistent!

## 🐞 Reporting Bugs / Requesting Features

1. First, Check if it’s already reported.
   search [open issues](https://github.com/Chungzter/CommiZard/issues).
2. If it’s new, [open an issue](https://github.com/Chungzter/CommiZard/issues)!
    - Be as detailed as you can: OS, Python version, steps to reproduce,
      expected vs actual behavior.
    - For feature requests, please describe your use case: why do you need it?

> [!TIP]
> The clearer your report, the faster we can fix or build it!

## ️ Pull Requests (Code Contributions)

1. Fork the repo, then clone your fork.
2. Create a new branch: `git checkout -b my-feature-or-fix`
3. Code your fix/feature. try to match existing style.
4. Write a clear commit message (ironic, right? 😄).
5. Push to your fork and when you're done, open a PR against `master`.

✅ I’ll review it as soon as I can!  
✅ Even small fixes — typos, docs, or tests — are welcome!

## 🧪 Testing & Quality

Since most of this software is dependent on user input and other software, every
kind of test contribution is appreciated: from adding test cases and increasing
the code coverage with tests, to manually using CommiZard on your system and
giving feedback, every contribution is appreciated.

## Starter Tasks

Not ready to write core features? No problem! These “behind-the-scenes” tasks
are **incredibly valuable**:

- ✍️ **Improve documentation**: Fix typos, clarify confusing sections, add
  examples to README or docstrings.
- **Test on different versions**: Does it work on Python 3.8? 3.10? What
  about different versions of key dependencies (like `ollama`, `requests`,
  `git`)? Report your setup + results!
- 🧩 **Tidy up code style**: Run `black` or `isort` and send a cleanup PR. (
  Check with me first if you’re making bulk changes.)
- 🔗 **Fix broken links or badges**: In README, docs, etc.
- **Improve this CONTRIBUTING.md file**: Make it clearer? More welcoming? Go
  for it!
- 🖼️ **Add example screenshots or asciinema recordings** — Show CommiZard in
  action!
- 🧹 **Run linters & report issues**: Try running `ruff`, `flake8`, `mypy`, or
  `pylint` on the codebase. Found warnings or style inconsistencies? Open an
  issue (or better yet, fix them and push a PR!).

> 💬 Even just asking questions — like "How does this part work?" or "Why is it
> built this way?" can be super helpful. Sometimes explaining it reveals better
> ways to do it!

Need guidance? Just comment on an issue (or open one) saying *"I’d like to help
with this!"*. I’ll happily walk you through it.

---

Whether you’re reporting a typo or sending a PR — you’re helping more than you
know! Thanks in advance.
