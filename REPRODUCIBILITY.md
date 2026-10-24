# Reproducibility

## Requirements

- Python 3.10 or newer
- `mpmath`
- `pdflatex`

Install:

```bash
python -m pip install mpmath
```

Run:

```bash
python scripts/verify_ellipse_ramanujan_nseries.py --precision 80 --output-dir output
```

The audit covers:

```text
b = 0.90, 0.75, 0.50, 0.25
N = 32, 64, 128, 256
```

It records exact elliptic-integral values, Ramanujan errors, raw polygon
errors, two-scale errors, and three-scale errors.

Rebuild:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory paper paper/ramanujan_ellipse_nseries_comparison.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory paper paper/ramanujan_ellipse_nseries_comparison.tex
```

## Checksum manifest status (2026-10-24)

`SHA256SUMS.txt` predates subsequent README and citation-metadata edits, and must not be treated as a verified manifest of the current repository checkout. The verification commands above refer to the currently checked-in scripts, not to the pending revised manuscripts. The existing manifest is preserved as an earlier snapshot; regenerate and validate a complete manifest against the exact release commit before declaring repository-wide SHA-256 verification successful. Do not replace manuscript PDFs, source files, or scientific output merely to make a checksum match.
