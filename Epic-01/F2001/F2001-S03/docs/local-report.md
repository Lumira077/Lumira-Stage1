# F2001-S03 software integration results
Software gate: passed
Tests: 42; failures: 0; errors: 0
Mode: simulated; hardware tests NOT RUN; release ready: false

| Latency path | n | p50 ms | p95 ms | max ms | Proposed software target |
|---|---:|---:|---:|---:|---|
| step_save | 100 | 0.076 | 0.118 | 0.230 | passed |
| registration_to_simulated_ACK | 100 | 1.335 | 1.653 | 1.883 | passed |
| greeting_text_and_simulated_dispatch | 100 | 0.221 | 0.350 | 0.451 | not_defined |

Measurement excludes real voice onset/network/motion. Targets are initial proposals, not hardware acceptance.
Q1/R1 approval and physical measurements remain pending.
