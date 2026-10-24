# Ellipse Perimeter: Ramanujan Approximation and N-Series Geometric Acceleration

**Author:** C. Wayne Baker  
**Date:** June 1, 2026  
**Status:** Comparative numerical note / source and reproducibility archive

This repository contains the paper:

> **Ellipse Perimeter: Ramanujan Approximation and N-Series Geometric Acceleration**

## Read the paper

- [`paper/ramanujan_ellipse_nseries_comparison.pdf`](paper/ramanujan_ellipse_nseries_comparison.pdf)
- [`paper/ramanujan_ellipse_nseries_comparison.tex`](paper/ramanujan_ellipse_nseries_comparison.tex)

## Comparison

The paper compares:

1. Ramanujan's second ellipse-perimeter approximation, a one-shot closed
   algebraic formula in the eccentricity parameter;
2. polygonal N-Series acceleration, which combines chordal perimeter
   approximations at several resolutions to cancel successive even-power
   errors.

The three-scale operator is

\[
\widehat P_N^{(3)}
=
\frac{1}{45}P_N-\frac{4}{9}P_{2N}+\frac{64}{45}P_{4N},
\]

with predicted error \(O(N^{-6})\) when the required even-power asymptotic
expansion holds.

## Main numerical observation

At \(a=1,\ b=0.90\), Ramanujan's formula remains slightly more accurate than
the three-scale result at base \(N=256\). At the tested moderate and high
eccentricities \(b=0.75,\ 0.50,\ 0.25\), the three-scale refinement overtakes
Ramanujan's approximation and continues to improve with scale.

The conclusion is complementary rather than competitive.

## Reproduce the audit

```bash
python -m pip install mpmath
python scripts/verify_ellipse_ramanujan_nseries.py --precision 80 --output-dir output
```

Expected status:

```text
verification_passed: True
```

## Claim boundary

This is a finite numerical and structural comparison. It does not establish a
global crossover theorem, identify N-Series cancellation with Ramanujan's
modular derivation, or claim universal numerical dominance.

## Rights

Copyright © 2026 C. Wayne Baker. All rights reserved unless otherwise stated.

## Manuscript review status (October 24, 2026)

The PDF and LaTeX files currently in `paper/` are the repository's existing published/preprint versions. A subsequent editorial and mathematical review has identified proposed clarifications for a future revision. Those revisions have **not** been merged into this repository, and the current PDF must not be described as incorporating them. Existing numerical verification scripts and results are unchanged. A revised source/PDF pair will be considered separately after a source-to-PDF consistency check and further mathematical review. This status notice makes no new scientific or priority claim.
