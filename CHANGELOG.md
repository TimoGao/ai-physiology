# Changelog

## MAO Experiment v0.4 — 2026-09-29

Fair-comparison and ablation upgrade:
- deterministic shared stress traces across all variants
- 30-seed evaluation path
- engineering baseline with retry, circuit breaker, cleanup, filtering, monitoring and load shedding
- ablations for AI Blood, Homeostasis, Vital Signs and Organ Health
- paired mean differences, approximate 95% confidence intervals and paired effect size
- task, memory, security, regulation and overhead metrics
- first 1080-run synthetic analysis
- experimental conclusion narrowed: physiology currently looks more like a long-term health-management layer than a replacement for reliability engineering

## MAO Experiment v0.3 — 2026-09-29

Experiment system upgrade:
- stronger engineering baseline with retry, cleanup, risk filtering and monitoring
- naive vs strong baseline comparison
- multi-seed repeated experiments
- summary statistics (n / mean / stdev / min / max)
- JSON and CSV result export
- experiment matrix runner
- expanded automated tests
- GitHub Actions CI across Python 3.10 / 3.11 / 3.12
- execution roadmap updated to v0.2

## v0.1-draft — 2026-09-29

Initial public-structure draft:
- AI Physiology definition
- cell/tissue/organ/organism hierarchy
- nine organ systems
- four internal communication networks
- six physiological loops
- homeostasis and vital signs
- organ internalization
- initial AIP specifications
- Minimal Artificial Organism experiment
