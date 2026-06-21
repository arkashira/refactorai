# RefactorAI – Simulated AI‑Powered Refactoring Recommendations

A tiny, self‑contained Python library that mimics the workflow of an
AI‑driven refactoring service:

1. **Upload** a codebase (a mapping of filenames → source strings).
2. **Train** a model – here we simply parse the source with the standard
   `ast` module and collect function metadata.
3. **Generate recommendations** – functions longer than a configurable
   threshold are flagged with a human‑readable suggestion.

## Installation
