# Lumira Stage1 source import

Destination: https://github.com/Lumira077/Lumira-Stage1

Imported Epic01–17 reviewed programs, reports, Stage1 board wiring images, Epic17 prototype and Pi/UNO identity bring-up. Existing Epic18–20 reference packages from the source repository are preserved, outside this development review scope.

Provenance: retri/KER-Robot baseline 96c628563544f10c4d53a6b41e36785ff59e462d; local R1 1788ac0; R2 ff6548f. Local Python tests: 595 passed. Remote CI is reported by GitHub Actions, separately from local tests.

These are offline prototypes and bring-up preparation, not a completed production robot. UNO target compilation and physical Pi/Hailo/actuator/user validation remain pending. No autonomous navigation or actuated fingers are enabled for Stage1. The rendering-only NotoSansKR.ttf build asset is omitted; finished wiring images are included.

Previous reports mentioning blocked GitHub access are historical; destination access was confirmed on 2026-10-06. See Development/review_20261006_R2/README.md and Development/Stage1/bringup/README.md.
