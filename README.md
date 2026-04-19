# Verification Automation Harness

> A lightweight verification pipeline that maps requirement IDs to executable test cases and produces traceable results.

## What it does
This project reads a manifest of requirements and verification cases, builds a small C target, executes the cases, and generates a Markdown verification report. It demonstrates the core workflow of linking requirements to unit-level verification with automation.

## Why I built it
I wanted a concrete way to show how requirements become executable verification. The focus is on traceability, repeatability, and fast feedback.

## Core capabilities
- Requirement-linked test cases
- Automated execution of a C verification target
- Pass/fail summary with stdout and exit code capture
- Requirement coverage mapping
- Markdown report generation

## Architecture
```mermaid
flowchart LR
    A[manifest.json] --> B[Python runner]
    B --> C[Compile C target]
    C --> D[Execute verification cases]
    D --> E[Coverage map + report]
    E --> F[Markdown output]
```

## Tech stack
- Python
- Standard library
- C
- gcc/clang

## Quick start
```bash
make build
make run
```

Run tests:

```bash
python -m unittest
```

## Limitations
- The sample target is intentionally small so the verification flow stays readable.
- This is not a full requirements management system.
- It is designed to show verification discipline, not to replace an industrial toolchain.

## Testing
The repo includes unit tests for the runner and an end-to-end executable verification flow.

## Docker
```bash
docker build -t verification-harness .
docker run --rm verification-harness
```
