# Handbrake-Elkateb workspace rules

- Treat the five `*.snapshot.*` reference-package directories as read-only source material.
- Put derived measurements, conversions, screenshots, and scripts only under `analysis_generated/`.
- Put approved original P1 CAD sources, exports, renders, drawings, and build documents only under `prototype_p1/`; treat `prototype_p1/src/parameters.py` as its source of truth.
- Read `codex/codex.md` and `codex/NEXT_GOAL.md` before major work.
- Keep measured CAD values distinct from estimates and cite the exact source file for engineering conclusions.
- Do not begin production CAD or modify reference CAD without explicit user approval.
- Do not push, publish, or modify remote state unless the user explicitly asks.
