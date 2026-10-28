# Lap-Time Simulator — Final Decisions & Plan

## Context
- TU Delft aerospace student; personal lap-time sim. No open FS data.

## Model
- Stanford Pacejka (tires.pdf / Pacejka 87). Pure-slip Fy, Fx with a1-a13.
## Slip
- Normalized percent slip sigma (0<=|sigma|<=1). Not Guiggiani v_r.

## Combining
- Primary: MNC (SAE 2011-01-0094). Backup: friction ellipse. Not PAC2002 weights.

## Fitting
- Fabricated/digitized curves. Fit a1-a8 (load, gamma=0), then a9-a13 (camber).
## Camber
- Via gamma terms a9-a13 in B/E coefficients. Static only.
