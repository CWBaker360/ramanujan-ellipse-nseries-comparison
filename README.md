# Ellipse Perimeter: Ramanujan Approximation and N-Series Geometric Acceleration

**Subtitle:** A Chord-Cost and Sinc-Correction Comparison  
**Author:** C. Wayne Baker  
**Original:** June 1, 2026  
**Review revision:** October 24, 2026 (v1.2)  
**Reproducibility audit:** November 24, 2026  
**Status:** Comparative numerical note / source and reproducibility archive

## Read the paper

- [PDF manuscript](paper/ramanujan_ellipse_nseries_comparison.pdf)
- [LaTeX source](paper/ramanujan_ellipse_nseries_comparison.tex)

The October 24 review revision is incorporated in both manuscript files. The November 24 audit confirmed that the archived PDF and repository PDF have identical SHA-256 hashes, and that the archived v1.2 LaTeX and repository source agree after line-ending normalization. A local PDF rebuild with font expansion disabled was compared against the original by extracted-content review; no substantive differences were identified. This is not a claim of byte-identical or visually identical PDF rebuilds.

## Three approximation mechanisms

1. Ramanujan's second ellipse-perimeter approximation: a fixed closed-form approximation in the eccentricity parameter $h=((a-b)/(a+b))^2$.
2. Three-scale geometric N-Series acceleration: Richardson cancellation of the second- and fourth-order polygonal errors.
3. Exact sinc correction: removal of the complete algebraic chord factor, leaving periodic midpoint-quadrature error.

For equal-parameter inscribed polygon perimeters $P_N$, the three-scale estimator is

$$T_N=\frac{P_N-20P_{2N}+64P_{4N}}{45}=P+O(N^{-6}).$$

For each fixed nondegenerate ellipse, the exact factorization is

$$P_N=\operatorname{sinc}(\pi/N)M_N,\qquad S_N=\frac{P_N}{\operatorname{sinc}(\pi/N)}=M_N,$$

where $M_N$ is the periodic midpoint approximation to the perimeter integral and $\operatorname{sinc}(x)=\sin(x)/x$. For fixed $0<b<a$, the corrected error is $O(e^{-\rho N})$ for every fixed $0<\rho<\operatorname{artanh}(b/a)$. The bound is not uniform as $b/a\to0$.

## Numerical comparison

At $a=1$, $b=0.90$, Ramanujan remains slightly more accurate than the three-scale estimator at base $N=256$. At the tested ratios $b=0.75,0.50,0.25$, the three-scale estimator is more accurate at that resolution.

The following rounded absolute errors were reproduced in the November 24 audit:

| Method | b/a = 0.50 | b/a = 0.25 |
|---|---:|---:|
| Ramanujan | 2.21e-9 | 1.07e-6 |
| Three-scale T64 (448 chords) | 2.10e-13 | 1.76e-11 |
| Sinc S128 (128 chords) | 1.44e-33 | 2.22e-17 |
| Sinc S448 (448 chords) | 9.99e-111 | 1.07e-53 |

The direct three-scale cost is $7N$ chords, not $N$. The equal-chord-count comparison applies to T64 and S448; Ramanujan's closed form requires no polygonal chord evaluations. Chord counts are not runtime benchmarks.

## Reproduce the audits

From the repository root:

```bash
python -m pip install mpmath
python scripts/verify_ellipse_ramanujan_nseries.py --precision 80 --output-dir output
python verify_sinc_correction.py
```

Both scripts are expected to report `verification_passed: True` and exit successfully. The second script writes its report to `evidence/sinc_correction_high_precision_audit.txt`.

The 80-decimal-digit audit covers four ellipse cases and base resolutions 32, 64, 128 and 256. The observed sixth-order error-reduction factors for b/a = 0.50 are 63.997840350887599893 and 63.99947290864573311, approaching 64.

The additional audit computes actual polygon chords and the midpoint sum separately at 170 and 220 decimal digits. All ten error values satisfy the cross-precision relative agreement threshold of 1e-40; all six targeted rounded manuscript values agree within the script's 5% tolerance. These are computational checks, not rigorous interval enclosures or independent human peer review.

## Claim boundaries

The methods are complementary rather than universally competitive. The results do not establish a global crossover theorem, a modular equivalence, superiority to established elliptic-integral or AGM algorithms, or runtime dominance. Sinc correction uses an analytic factor involving pi; it is not an exact straightedge-and-compass correction claim. Exponential convergence is for fixed nondegenerate ellipses. The manuscript contains the AI-assistance and numerical provenance disclosure.

## Rights

Copyright (c) 2026 C. Wayne Baker. All rights reserved unless otherwise stated.
