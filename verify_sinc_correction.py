import mpmath as mp
from pathlib import Path

def audit(dps):
    with mp.workdps(dps):
        rows = {}
        for ratio in ('0.50', '0.25'):
            b = mp.mpf(ratio)
            P = 4*mp.ellipe(1-b*b)
            h = ((1-b)/(1+b))**2
            R = mp.pi*(1+b)*(1+3*h/(10+mp.sqrt(4-3*h)))
            def polygon(N):
                pts = [(mp.cos(2*mp.pi*j/N), b*mp.sin(2*mp.pi*j/N)) for j in range(N)]
                return mp.fsum(mp.sqrt((pts[(j+1)%N][0]-pts[j][0])**2+(pts[(j+1)%N][1]-pts[j][1])**2) for j in range(N))
            T = (polygon(64)-20*polygon(128)+64*polygon(256))/45
            errors = {'Ramanujan': abs(P-R), 'T64': abs(P-T)}
            for N in (64,128,448):
                S = polygon(N)/mp.sinc(mp.pi/N)
                M = (2*mp.pi/N)*mp.fsum(mp.sqrt(mp.sin(t)**2+b*b*mp.cos(t)**2) for t in (mp.pi*(2*j+1)/N for j in range(N)))
                assert abs(S-M) < mp.power(10,-dps+10), 'Sinc identity failed'
                errors[f'S{N}'] = abs(P-S)
            rows[ratio] = errors
        return rows

low, high = audit(170), audit(220)
mp.mp.dps = 220
expected = {'0.50': {'T64':'2.1e-13','S128':'1.4e-33','S448':'9.99e-111'}, '0.25': {'T64':'1.8e-11','S128':'2.2e-17','S448':'1.07e-53'}}
lines = ['SINC CORRECTION INDEPENDENT NUMERICAL AUDIT', 'Working precisions: 170 and 220 decimal digits']
passed = True
for ratio, errors in high.items():
    lines.append(f'\nb/a = {ratio}')
    for name, value in errors.items():
        stable = value != 0 and abs(low[ratio][name]-value)/abs(value) < mp.mpf('1e-40')
        passed = passed and stable
        lines.append(f'{name:12s}: {mp.nstr(value,25)} | precision stability: {stable}')
    for name, reference in expected[ratio].items():
        target = mp.mpf(reference)
        match = abs(errors[name]-target)/target < mp.mpf('0.05')
        passed = passed and match
        lines.append(f'Manuscript {name}: {match}')
lines.append(f'\nverification_passed: {passed}')
report = '\n'.join(lines)
print(report)
destination = Path(__file__).resolve().parent / 'evidence'
destination.mkdir(exist_ok=True)
(destination / 'sinc_correction_high_precision_audit.txt').write_text(report, encoding='utf-8')
raise SystemExit(0 if passed else 1)
