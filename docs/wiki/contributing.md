
# Contributing

Contributions are welcome! Whether you're fixing a bug, improving documentation, or proposing a new feature, here's how to get started.

---

## Setting up the development environment

```bash
git clone https://github.com/victorbenezoli/geodata.git
cd geodata
poetry install
```

---

## Workflow

1. **Fork** the repository and create a branch from `main`:

   ```bash
   git checkout -b feat/my-feature
   ```

2. **Make your changes** and ensure all tests pass:

   ```bash
   pytest tests/
   ```

3. **Commit** following [Conventional Commits](https://www.conventionalcommits.org/):

   ```
   feat: add support for mesoregions
   fix: correct sindex predicate for border points
   docs: improve GeoLocator example
   ```

4. **Open a pull request** against the `main` branch with a clear description of the change.

---

## Code style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. Before committing, run:

```bash
ruff check .
ruff format .
```

---

## Running the tests

```bash
pytest tests/ -v
```

---

## Building the documentation locally

```bash
poetry install --with docs
mkdocs serve
```

The site will be available at `http://127.0.0.1:8000`.

---

## Reporting issues

Open an issue on [GitHub](https://github.com/victorbenezoli/geodata/issues) with:

- A clear description of the problem
- Steps to reproduce
- Expected vs actual behaviour
- Python and package versions (`pip show ibge-geodata`)
