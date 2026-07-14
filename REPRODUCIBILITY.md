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
